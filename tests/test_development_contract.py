"""Pure schema checks. Structural execution experiments run inside accepted W0."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from programmo_evolvens.development import validate
from programmo_evolvens.runtime import GenomeError
from world.wsl2.build_development import build

ROOT = Path(__file__).resolve().parent.parent


class DevelopmentContractTests(unittest.TestCase):
    def setUp(self):
        self.genome = json.loads((ROOT / 'examples/development/text-retention.json').read_text())

    def test_contract_has_mechanism_and_structural_genes(self):
        genes, rules = validate(self.genome)
        self.assertEqual(set(genes), {'clean', 'retain', 'body'})
        self.assertEqual(len(rules), 4)

    def test_external_actions_and_unknown_rules_are_rejected_before_execution(self):
        for change in ('action', 'operation', 'source', 'budget', 'duplicate'):
            value = deepcopy(self.genome)
            if change == 'action':
                value['genes'][2]['rules'][0]['action']['op'] = 'exec'
            elif change == 'operation':
                value['genes'][0]['program']['steps'][0]['pp'] = 'ACT'
            elif change == 'source':
                value['genes'][0]['program']['steps'][0]['params']['source'] = '/mnt/c'
            elif change == 'budget':
                value['initial']['budget'] = 1000000
            else:
                value['genes'].append(deepcopy(value['genes'][0]))
            with self.subTest(change=change), self.assertRaises(GenomeError):
                validate(value)

    def test_bundle_is_deterministic_and_contains_only_fixed_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory)/'a.pyz', Path(directory)/'b.pyz'
            build(ROOT, a)
            build(ROOT, b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(a) as bundle:
                self.assertEqual(len(bundle.namelist()), 5)
                self.assertTrue(all(item.create_system == 3 for item in bundle.infolist()))
                self.assertIn('programmo_evolvens/development_genome.json', bundle.namelist())
