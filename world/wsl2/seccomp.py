"""Build a Linux x86-64 seccomp BPF artifact. Does not load it in this process."""

import argparse
import ctypes
import errno
import json
from pathlib import Path
import platform

# Initial single-threaded Python probe profile, not a universal organism profile.
# No sockets, process creation, namespace manipulation, mounting, ptrace or BPF.
SYSCALLS = (
    "read", "write", "readv", "writev", "close", "close_range", "fstat", "newfstatat",
    "stat", "lstat", "statx", "lseek", "pread64", "openat", "access", "faccessat",
    "faccessat2", "getdents64", "readlink", "readlinkat", "getcwd", "chdir",
    "mmap", "mprotect", "munmap", "mremap", "madvise", "brk", "arch_prctl",
    "rt_sigaction", "rt_sigprocmask", "rt_sigreturn", "sigaltstack", "futex",
    "set_tid_address", "set_robust_list", "rseq", "getrandom", "clock_gettime",
    "clock_nanosleep", "nanosleep", "gettimeofday", "getpid", "getppid", "gettid",
    "getuid", "geteuid", "getgid", "getegid", "getgroups", "uname", "sysinfo",
    "getrlimit", "prlimit64", "fcntl", "ioctl", "poll", "ppoll", "select", "pselect6",
    "dup", "dup2", "dup3", "pipe2", "mkdir", "mkdirat", "unlink", "unlinkat",
    "rename", "renameat", "renameat2", "ftruncate", "fsync", "fdatasync",
    "execve", "exit", "exit_group"
)


def build(output):
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        raise RuntimeError("initial profile requires Linux x86_64")
    lib = ctypes.CDLL("libseccomp.so.2", use_errno=True)
    lib.seccomp_init.argtypes = [ctypes.c_uint32]
    lib.seccomp_init.restype = ctypes.c_void_p
    lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    lib.seccomp_syscall_resolve_name.restype = ctypes.c_int
    lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    lib.seccomp_rule_add.restype = ctypes.c_int
    lib.seccomp_export_bpf.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.seccomp_export_bpf.restype = ctypes.c_int
    lib.seccomp_release.argtypes = [ctypes.c_void_p]
    context = lib.seccomp_init(0x00050000 | errno.EPERM)  # default SCMP_ACT_ERRNO
    if not context:
        raise RuntimeError("seccomp_init failed")
    try:
        for name in SYSCALLS:
            number = lib.seccomp_syscall_resolve_name(name.encode("ascii"))
            if number < 0 or lib.seccomp_rule_add(context, 0x7FFF0000, number, 0) != 0:
                raise RuntimeError(f"cannot allow syscall {name}")
        with Path(output).open("xb") as stream:
            if lib.seccomp_export_bpf(context, stream.fileno()) != 0:
                raise RuntimeError("BPF export failed")
    finally:
        lib.seccomp_release(context)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.output)
    args.output.with_suffix(".json").write_text(json.dumps({
        "architecture": "x86_64", "default": "EPERM", "syscalls": SYSCALLS,
        "status": "experimental; requires W0 acceptance"
    }, indent=2) + "\n", encoding="utf-8")
