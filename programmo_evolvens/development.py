"""Bounded declarative development v0. Execute candidates only inside accepted W0."""
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import json
import re

from .runtime import GenomeError, Runtime, bounded_json, keys, require

SCHEMA = 'development-v0'
MAX_CELLS, MAX_RULES, MAX_TICKS, MAX_MECHANISMS = 4, 16, 16, 8
FEEDBACK = {'source_unexpressed', 'endpoint_missing', 'endpoint_unexpressed', 'disconnected'}


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[a-z][a-z0-9_-]{0,39}', value), 'invalid identifier')


def genome_hash(genome):
    return hashlib.sha256(json.dumps(genome, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def validate(genome):
    bounded_json(genome, 16384)
    keys(genome, {'schema', 'id', 'initial', 'genes', 'endpoint'})
    require(genome['schema'] == SCHEMA, 'unsupported developmental schema')
    identifier(genome['id'])
    keys(genome['initial'], {'cell', 'budget'})
    identifier(genome['initial']['cell'])
    require(type(genome['initial']['budget']) is int and 1 <= genome['initial']['budget'] <= 64, 'invalid cell budget')
    keys(genome['endpoint'], {'cell', 'port'})
    identifier(genome['endpoint']['cell'])
    require(genome['endpoint']['port'] == 'out', 'only text output port supported')
    require(isinstance(genome['genes'], list) and 1 <= len(genome['genes']) <= 12, 'invalid gene count')
    genes, rules = {}, []
    checker = Runtime(max_steps=8, max_payload_bytes=16384)
    for gene in genome['genes']:
        require(isinstance(gene, dict), 'gene must be an object')
        identifier(gene.get('id'))
        require(gene['id'] not in genes, 'duplicate gene')
        if gene.get('kind') == 'mechanism':
            keys(gene, {'id', 'kind', 'program'})
            types = checker.validate(gene['program'])
            require(set(gene['program']['outputs']) == {'out'}, 'mechanism requires one out port')
            require(checker._binding_type(gene['program']['outputs']['out'], types) == 'text', 'cell output must be text')
            for node in gene['program']['steps']:
                if node['pp'] == 'SENSE':
                    require(node['params'] == {'source': 'in', 'type': 'text'}, 'cell senses only its text inbox')
        elif gene.get('kind') == 'development':
            keys(gene, {'id', 'kind', 'rules'})
            require(isinstance(gene['rules'], list), 'rules must be a list')
            for rule in gene['rules']:
                keys(rule, {'id', 'when', 'action'})
                identifier(rule['id'])
                keys(rule['when'], {'feedback'})
                require(rule['when']['feedback'] in FEEDBACK, 'unknown feedback condition')
                action = rule['action']
                require(isinstance(action, dict), 'action must be an object')
                op = action.get('op')
                fields = {'express': {'op', 'cell', 'gene'}, 'bud': {'op', 'parent', 'cell', 'budget'},
                          'connect': {'op', 'from', 'to'}}
                require(isinstance(op, str) and op in fields, 'unknown developmental action')
                keys(action, fields[op])
                for key in fields[op] - {'op', 'budget'}:
                    identifier(action[key])
                if op == 'bud':
                    require(type(action['budget']) is int and 1 <= action['budget'] <= 64, 'invalid bud budget')
                rules.append((gene['id'], rule))
        else:
            raise GenomeError('unknown gene kind')
        genes[gene['id']] = gene
    require(0 < len(rules) <= MAX_RULES, 'invalid developmental rule count')
    require(len({rule['id'] for _, rule in rules}) == len(rules), 'duplicate developmental rule')
    for _, rule in rules:
        action = rule['action']
        if action['op'] == 'express':
            require(action['gene'] in genes and genes[action['gene']]['kind'] == 'mechanism', 'unknown mechanism gene')
    return genes, rules


@dataclass
class Cell:
    id: str
    parent: str | None
    budget: int
    mechanisms: list = field(default_factory=list)
    inbox: deque = field(default_factory=deque)
    runtime: Runtime = field(default_factory=lambda: Runtime(max_steps=8, max_payload_bytes=16384))
    used_steps: int = 0
    state: str = 'idle'
    health: str = 'ok'
    origin: dict = field(default_factory=dict)

    def snapshot(self):
        return {'id': self.id, 'parent': self.parent, 'ports': {'in': 'text', 'out': 'text'},
                'mechanisms': deepcopy(self.mechanisms), 'memory': deepcopy(self.runtime.store),
                'state': self.state, 'health': self.health, 'budget': self.budget,
                'used_steps': self.used_steps, 'mailbox_capacity': 4, 'origin': self.origin}


class Development:
    def __init__(self, genome, emit=None):
        self.genome = deepcopy(genome)
        self.genes, self.rules = validate(self.genome)
        self.hash = genome_hash(self.genome)
        initial = self.genome['initial']
        cell = Cell(initial['cell'], None, initial['budget'], origin={'initial': True, 'genome': self.hash})
        self.cells = {cell.id: cell}
        self.links, self.fired, self.events = [], set(), []
        self.sink = emit
        self.tick = 0
        self.record('initial', cells=[cell.snapshot()], links=[])

    def record(self, kind, **values):
        event = {'seq': len(self.events), 'tick': self.tick, 'event': kind, 'genome_sha256': self.hash, **values}
        self.events.append(event)
        if self.sink:
            self.sink(deepcopy(event))

    def apply(self, gene_id, rule):
        action = rule['action']
        origin = {'gene': gene_id, 'rule': rule['id'], 'genome': self.hash}
        if action['op'] == 'express':
            cell = self.cells.get(action['cell'])
            require(cell is not None and cell.health == 'ok', 'expression target unavailable')
            require(sum(len(c.mechanisms) for c in self.cells.values()) < MAX_MECHANISMS, 'mechanism budget exceeded')
            require(action['gene'] not in [m['gene'] for m in cell.mechanisms], 'mechanism already expressed')
            mechanism = {'id': f'{cell.id}:{action["gene"]}', 'gene': action['gene'], 'origin': origin}
            cell.mechanisms.append(mechanism)
            self.record('mechanism_expressed', cell=cell.id, mechanism=mechanism, origin=origin)
        elif action['op'] == 'bud':
            require(action['parent'] in self.cells, 'bud parent unavailable')
            require(action['cell'] not in self.cells and len(self.cells) < MAX_CELLS, 'cell budget or duplicate cell')
            child = Cell(action['cell'], action['parent'], action['budget'], origin=origin)
            self.cells[child.id] = child
            self.record('cell_created', cell=child.snapshot(), origin=origin)
        else:
            source, target = action['from'], action['to']
            require(source in self.cells and target in self.cells and source != target, 'invalid link endpoints')
            require(not any(link['from'] == source and link['to'] == target for link in self.links), 'duplicate link')
            # Reachability check: adding source -> target must not close a cycle.
            reached, pending = set(), [target]
            while pending:
                here = pending.pop()
                require(here != source, 'cell connection cycle')
                if here not in reached:
                    reached.add(here)
                    pending.extend(link['to'] for link in self.links if link['from'] == here)
            link = {'from': source, 'from_port': 'out', 'to': target, 'to_port': 'in', 'origin': origin}
            self.links.append(link)
            self.record('link_created', link=link, origin=origin)
        self.fired.add(rule['id'])

    def probe(self, text):
        require(isinstance(text, str), 'input requires text')
        bounded_json(text, 4096)
        source = self.cells[self.genome['initial']['cell']]
        endpoint = self.genome['endpoint']['cell']
        if not source.mechanisms:
            return {'feedback': 'source_unexpressed', 'delivered': False}
        for cell in self.cells.values():
            require(not cell.inbox, 'mailbox must be drained between probes')
        source.inbox.append({'value': text, 'from': 'world'})
        pending = deque([source.id])
        result = None
        while pending:
            cell = self.cells[pending.popleft()]
            packet = cell.inbox.popleft()
            self.record('cell_received', cell=cell.id, source=packet['from'])
            if not cell.mechanisms:
                self.record('cell_unexpressed', cell=cell.id)
                continue
            value = packet['value']
            cell.state = 'running'
            for mechanism in cell.mechanisms:
                program = self.genes[mechanism['gene']]['program']
                cost = len(program['steps'])
                if cell.used_steps + cost > cell.budget:
                    cell.state, cell.health = 'stopped', 'budget_exhausted'
                    self.record('cell_stopped', cell=cell.id, reason=cell.health)
                    return {'feedback': 'budget_exhausted', 'delivered': False}
                cell.used_steps += cost
                try:
                    executed = cell.runtime.run(program, {'in': value})
                except Exception:
                    cell.state, cell.health = 'stopped', 'execution_failed'
                    self.record('cell_stopped', cell=cell.id, reason=cell.health)
                    raise
                value = executed['outputs']['out']
                self.record('mechanism_executed', cell=cell.id, mechanism=mechanism['id'],
                            gene=mechanism['gene'], output=value, memory=deepcopy(cell.runtime.store),
                            nodes=[{'id': node['node'], 'pp': node['pp'], 'status': node['status'], 'value': node['value']} for node in executed['trace']])
            cell.state = 'idle'
            if cell.id == endpoint:
                result = value
            for link in self.links:
                if link['from'] == cell.id:
                    target = self.cells[link['to']]
                    require(len(target.inbox) < 4, 'mailbox overflow')
                    target.inbox.append({'value': value, 'from': cell.id})
                    pending.append(target.id)
        if result is not None:
            return {'feedback': 'delivered', 'delivered': True, 'value': result}
        feedback = ('endpoint_missing' if endpoint not in self.cells else
                    'endpoint_unexpressed' if not self.cells[endpoint].mechanisms else 'disconnected')
        return {'feedback': feedback, 'delivered': False}

    def run(self, text):
        result = None
        for self.tick in range(MAX_TICKS + 1):
            result = self.probe(text)
            self.record('function_checked', **result)
            if result['delivered']:
                break
            selected = next(((gene, rule) for gene, rule in self.rules
                             if rule['id'] not in self.fired and rule['when']['feedback'] == result['feedback']), None)
            if selected is None or self.tick == MAX_TICKS:
                self.record('development_stalled', reason=result['feedback'])
                break
            self.apply(*selected)
        require(genome_hash(self.genome) == self.hash, 'heritable genome changed')
        return {'genome_id': self.genome['id'], 'genome_sha256': self.hash, 'delivered': result['delivered'],
                'feedback': result['feedback'], 'value': result.get('value'), 'ticks': self.tick,
                'cells': [cell.snapshot() for cell in self.cells.values()], 'links': deepcopy(self.links),
                'fired_rules': sorted(self.fired), 'event_count': len(self.events)}
