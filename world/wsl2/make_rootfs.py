"""Create a new curated Python-only image from trusted installed distro files."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import sysconfig


def build(target):
    if sys.platform != "linux" or os.geteuid() != 0:
        raise RuntimeError("run only as administrator of the dedicated WSL distro")
    target = Path(target)
    if target.exists() or target.is_symlink():
        raise RuntimeError("target must not exist; no existing image is overwritten")
    executable = Path(sys.executable).resolve(strict=True)
    stdlib = Path(sysconfig.get_path("stdlib")).resolve(strict=True)
    if not executable.is_relative_to("/usr") or not stdlib.is_relative_to("/usr/lib"):
        raise RuntimeError("expected trusted system Python, not a virtual environment")
    target.mkdir(parents=True, mode=0o755)
    for name in ("usr/bin", "app", "proc", "dev", "work", "tmp", "etc"):
        (target / name).mkdir(parents=True, exist_ok=True)
    shutil.copy2(executable, target / "usr/bin/python3")
    destination = target / stdlib.relative_to("/")
    shutil.copytree(stdlib, destination, symlinks=False,
                    ignore=shutil.ignore_patterns("site-packages", "dist-packages", "__pycache__", "test", "tests"))
    binaries = [executable, *stdlib.glob("lib-dynload/*.so")]
    for binary in binaries:
        response = subprocess.run(["/usr/bin/ldd", str(binary)], capture_output=True,
                                  env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, text=True, check=True)
        for match in re.finditer(r"(?:=>\s*)?(/[^\s()]+)", response.stdout):
            library = Path(match[1])
            if not library.is_file() or not str(library).startswith(("/usr/lib/", "/lib/", "/lib64/")):
                raise RuntimeError(f"unexpected library path: {library}")
            output = target / library.relative_to("/")
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(library, output)
    (target / "app/main.py").touch()
    (target / "etc/passwd").write_text("nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\n")
    (target / "etc/group").write_text("nogroup:x:65534:\n")
    manifest = {}
    for path in sorted(target.rglob("*")):
        if path.is_file():
            manifest[path.relative_to(target).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    target.with_name("rootfs.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    build(parser.parse_args().target)
