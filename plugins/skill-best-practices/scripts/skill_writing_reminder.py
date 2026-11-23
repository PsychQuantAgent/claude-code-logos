#!/usr/bin/env python3
"""PreToolUse hook on Write|Edit: deliver rules/skill-writing.md for SKILL.md.

Plugins have no rules/ component, so the rule file is never auto-loaded.
This hook is what delivers it: when the target path is a SKILL.md, the file's
text is added as context, once per session.

The session marker lives in a directory private to the user under the system
temp directory. The hook keeps markers only where it can verify that directory
through an open descriptor (a user id, descriptor-relative file calls,
O_DIRECTORY, O_NOFOLLOW and fcntl), and only when the temp directory itself is
owned by the user or root and is either closed to writes by others or sticky,
so nobody else can rename the private directory. Everywhere else, and whenever
a check fails, it sends the reminder and writes no marker. The marker check,
the print and the marker write run under a lock; no lock attempt starts after
the wait has run out, a lock found taken after it is let go, and the marker is
written only after the context has been printed. Owners and permission bits are checked; ACLs are not. Never
decides the call.
"""
import json
import os
import pathlib
import re
import stat
import sys
import tempfile
import time

RULE_FILE = pathlib.Path(__file__).resolve().parents[1] / "rules" / "skill-writing.md"
LOCK_NAME = ".lock"
LOCK_WAIT_SECONDS = 5
LOCK_RETRY_SECONDS = 0.05

try:
    import fcntl
except ImportError:  # not POSIX
    fcntl = None


def is_skill_file(path):
    return isinstance(path, str) and re.split(r"[\\/]", path)[-1] == "SKILL.md"


def _can_verify():
    """Whether this platform has what the hook needs to verify the marker directory."""
    return (fcntl is not None and hasattr(os, "getuid")
            and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
            and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
            and os.mkdir in os.supports_dir_fd and os.stat in os.supports_follow_symlinks)


def _temp_dir_trusted(info):
    """Whether nobody but the user or root can rename entries in the temp directory."""
    return (stat.S_ISDIR(info.st_mode) and info.st_uid in (os.getuid(), 0)
            and (not info.st_mode & 0o022 or bool(info.st_mode & stat.S_ISVTX)))


def _open_marker_dir():
    """An open descriptor of the user's private marker directory, or None when it cannot be trusted.

    Trusted means: the open temp directory passes _temp_dir_trusted, and the
    marker directory, opened relative to it without following a symlink, shows
    in fstat a directory owned by the current user with no permission bits for
    group or others.
    """
    if not _can_verify():
        return None
    try:
        parent = tempfile.gettempdir()
        parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
    except Exception:  # no usable temp directory
        return None
    name = f"skill-best-practices-{os.getuid()}"
    try:
        if not _temp_dir_trusted(os.fstat(parent_fd)):
            return None
        try:
            os.mkdir(name, 0o700, dir_fd=parent_fd)
        except FileExistsError:
            pass
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
    except OSError:  # a symlink (ELOOP), a regular file (ENOTDIR), or no permission
        return None
    finally:
        os.close(parent_fd)
    try:
        info = os.fstat(fd)
        trusted = (stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid()
                   and not info.st_mode & 0o077)
    except OSError:
        trusted = False
    if not trusted:
        os.close(fd)
        return None
    return fd


def _lock(dir_fd):
    """An exclusive lock on the lock file in the marker directory, or None after LOCK_WAIT_SECONDS."""
    try:
        lock_fd = os.open(LOCK_NAME, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
    except OSError:
        return None
    deadline = time.monotonic() + LOCK_WAIT_SECONDS
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if time.monotonic() < deadline:
                return lock_fd
            break  # taken too late: let it go (closing the descriptor releases it)
        except BlockingIOError:
            pass
        except OSError:
            break  # an error other than busy ends the wait at once
        left = deadline - time.monotonic()
        if left <= 0:
            break
        time.sleep(min(LOCK_RETRY_SECONDS, left))
        if time.monotonic() >= deadline:
            break  # no attempt starts after the deadline
    os.close(lock_fd)
    return None


def _print_context(rule):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": rule,
    }}, ensure_ascii=False))
    sys.stdout.flush()


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path")
    if not is_skill_file(path):
        return 0
    try:
        rule = RULE_FILE.read_text(encoding="utf-8")
    except OSError:
        return 0
    session_id = payload.get("session_id")
    dir_fd = _open_marker_dir() if session_id else None
    if dir_fd is None:
        _print_context(rule)
        return 0
    try:
        lock_fd = _lock(dir_fd)
        if lock_fd is None:
            _print_context(rule)
            return 0
        try:
            marker = re.sub(r"[^A-Za-z0-9_.-]", "_", str(session_id)) + ".skill-writing"
            try:
                os.stat(marker, dir_fd=dir_fd, follow_symlinks=False)
                return 0  # this session already had the reminder
            except FileNotFoundError:
                pass
            except OSError:
                _print_context(rule)
                return 0
            _print_context(rule)
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW
            try:
                os.close(os.open(marker, flags, 0o600, dir_fd=dir_fd))
            except OSError:
                pass
            return 0
        finally:
            os.close(lock_fd)  # closing releases the lock
    finally:
        os.close(dir_fd)


if __name__ == "__main__":
    sys.exit(main())
