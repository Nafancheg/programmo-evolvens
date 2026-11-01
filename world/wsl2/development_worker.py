"""Fixed development experiment, executed ONLY as the W0 zipapp workload."""
from copy import deepcopy
from importlib.resources import files
import json
import sys
import time

from programmo_evolvens.development import Development, genome_hash, validate
from programmo_evolvens.runtime import GenomeError


def main():
    request = sys.stdin.buffer.readline(65537)
    if len(request) > 65536:
        raise ValueError('input exceeds world contract')
    request = json.loads(request)
    seed = request['seed']
    sequence = 0

    def emit(event):
        nonlocal sequence
        print(json.dumps({'type': 'heartbeat', 'seq': sequence, 'timestamp': time.time(),
                          'development': event, 'experiment': 'baseline'}), flush=True)
        sequence += 1

    genome = json.loads(files('programmo_evolvens').joinpath('development_genome.json').read_text())
    original = genome_hash(genome)
    baseline = Development(genome, emit=emit)
    result = baseline.run('  HeLLo  ')
    tests = []

    def check(case, condition, **data):
        tests.append({'case': case, 'passed': bool(condition), **data})
        if not condition:
            raise AssertionError(case)

    checks = [e for e in baseline.events if e['event'] == 'function_checked']
    check('development', result['delivered'] and result['value'] == 'hello'
          and len(result['cells']) == 2 and len(result['links']) == 1
          and all(not e['delivered'] for e in checks[:-1]) and checks[-1]['delivered']
          and baseline.events[0]['cells'][0]['mechanisms'] == [], value=result['value'], ticks=result['ticks'])
    check('cell-memory', result['cells'][1]['memory'] == {'last': 'hello'} and all(c['health'] == 'ok' for c in result['cells']))
    structural = [event for event in baseline.events if event['event'] in {'cell_created', 'mechanism_expressed', 'link_created'}]
    check('provenance', len(structural) == 4 and all(event['origin']['gene'] == 'body'
          and event['origin']['rule'] in result['fired_rules']
          and event['origin']['genome'] == original for event in structural))
    repeated = Development(genome)
    same = repeated.run('  HeLLo  ')
    check('determinism', same == result and repeated.events == baseline.events)
    new = Development(genome).run('  NeW DATA\t')
    check('additional-public-input', new['value'] == 'new data', value=new['value'])
    variant = deepcopy(genome)
    variant['id'] = 'text-retention-strip'
    variant['genes'][0]['program']['steps'].pop()
    variant['genes'][0]['program']['outputs']['out'] = {'ref': 'trim'}
    changed = Development(variant).run('  HeLLo  ')
    check('gene-variant', changed['delivered'] and changed['value'] == 'HeLLo' and changed['value'] != result['value'], value=changed['value'])
    broken = deepcopy(genome)
    broken['genes'][2]['rules'].pop()
    absent = Development(broken).run('  HeLLo  ')
    check('link-ablation', not absent['delivered'] and absent['feedback'] == 'disconnected' and absent['links'] == [], feedback=absent['feedback'])
    limited = deepcopy(genome)
    limited['initial']['budget'] = 3
    exhausted = Development(limited).run('  HeLLo  ')
    check('cell-budget', not exhausted['delivered'] and exhausted['feedback'] == 'budget_exhausted', feedback=exhausted['feedback'])
    invalid = deepcopy(genome)
    invalid['genes'][0]['program']['steps'][0]['pp'] = 'PYTHON_EVAL'
    rejected = False
    try:
        validate(invalid)
    except GenomeError:
        rejected = True
    check('unknown-operation-rejected', rejected)
    check('heritable-genome-unchanged', genome_hash(genome) == original)
    print(json.dumps({'type': 'result', 'seed': seed, 'passed': all(test['passed'] for test in tests),
                      'experiment': 'development-v0', 'cases': tests, 'development': result,
                      'scope': 'prescribed development; no learning or evolution claim'}), flush=True)


if __name__ == '__main__':
    main()
