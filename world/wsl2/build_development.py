"""Build a deterministic trusted zipapp; never executes a genome."""
import argparse
from pathlib import Path
import zipfile


def build(repository, target):
    root, target = Path(repository).resolve(strict=True), Path(target)
    entries = {'__main__.py': 'world/wsl2/development_worker.py',
               'programmo_evolvens/__init__.py': 'programmo_evolvens/__init__.py',
               'programmo_evolvens/runtime.py': 'programmo_evolvens/runtime.py',
               'programmo_evolvens/development.py': 'programmo_evolvens/development.py',
               'programmo_evolvens/development_genome.json': 'examples/development/text-retention.json'}
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_STORED) as archive:
        for destination, source in sorted(entries.items()):
            path = (root / source).resolve(strict=True)
            if not path.is_relative_to(root) or path.is_symlink():
                raise ValueError('bundle source outside repository')
            item = zipfile.ZipInfo(destination, date_time=(2026, 1, 1, 0, 0, 0))
            item.create_system = 3  # stable metadata across Windows and Linux builders
            item.external_attr = 0o100644 << 16
            archive.writestr(item, path.read_bytes())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path)
    parser.add_argument('target', type=Path)
    options = parser.parse_args()
    build(options.repository, options.target)
