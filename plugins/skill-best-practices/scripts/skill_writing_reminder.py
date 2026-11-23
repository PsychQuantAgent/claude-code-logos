#!/usr/bin/env python3
"""PreToolUse hook on Write|Edit: deliver rules/skill-writing.md for SKILL.md.

Plugins have no rules/ component, so the rule file is never auto-loaded.
This hook is what delivers it: when the target path is a SKILL.md, the file's
text is added as context, once per session. The session marker lives in a
directory private to the user under the system temp directory; a directory
that cannot be trusted gets no marker, so the reminder is sent every time.
The marker is written only after the context has been printed. Never decides
the call.
"""
import getpass
import json
import os
import pathlib
import re
import stat
import sys
import tempfile

RULE_FILE = pathlib.Path(__file__).resolve().parents[1] / "rules" / "skill-writing.md"


def is_skill_file(path):
    return isinstance(path, str) and re.split(r"[\\/]", path)[-1] == "SKILL.md"


def _owner_tag():
    """The user id, or the user name where the platform has no user id (Windows)."""
    getuid = getattr(os, "getuid", None)
    if getuid is not None:
        return str(getuid())
    try:
        name = getpass.getuser()
    except Exception:  # getuser raises when no name can be found
        name = "user"
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name) or "user"


def _trusted_marker_dir():
    """The user's private marker directory, or None when it cannot be trusted.

    Trusted means: lstat shows a directory that is not a symlink, and, where the
    platform has a user id, it is owned by the current user with no permission
    bits for group or others.
    """
    path = os.path.join(tempfile.gettempdir(), f"skill-best-practices-{_owner_tag()}")
    try:
        os.mkdir(path, 0o700)
    except FileExistsError:
        pass
    except OSError:
        return None
    try:
        info = os.lstat(path)
    except OSError:
        return None
    # On Windows lstat does not report an NTFS junction as a symlink; the temp directory there is per-user.
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        return None
    getuid = getattr(os, "getuid", None)
    if getuid is not None and (info.st_uid != getuid() or info.st_mode & 0o077):
        return None
    return path


def session_marker(session_id):
    """The marker path for this session, or None (no usable session id, or no trusted directory)."""
    if not session_id:
        return None
    directory = _trusted_marker_dir()
    if directory is None:
        return None
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(session_id))
    return os.path.join(directory, f"{safe}.skill-writing")


def write_marker(marker):
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        os.close(os.open(marker, flags, 0o600))
    except OSError:
        pass  # another hook of the session got there first, or the directory went away


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
    marker = session_marker(payload.get("session_id"))
    if marker is not None and os.path.lexists(marker):
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": rule,
    }}, ensure_ascii=False))
    sys.stdout.flush()
    if marker is not None:
        write_marker(marker)
    return 0


if __name__ == "__main__":
    sys.exit(main())
