"""Absurd Clause Contest entry.

Writes one absurd terms-of-service clause to the entry file the grader
reads. The output location is resolved defensively because the grader runs
``python3 -P -s /bot/main.py`` with no ENTRY_OUT set, from a read-only
repository directory, while /output is writable.
"""

import os
import sys

SHOWER_HUM_CLAUSE = (
    "By using this service, you irrevocably assign to us all rights in any "
    "song you hum in the shower, including royalties, remixes, and future "
    "shower performances."
)

_MAX_CLAUSE_CHARS = 200


def _sanitise_clause(raw_clause):
    """Return the clause, checked: one sentence, within the 200-char cap."""
    clause = raw_clause.strip()
    if not clause:
        raise ValueError("clause is empty")
    if len(clause) > _MAX_CLAUSE_CHARS:
        raise ValueError("clause exceeds 200 characters")
    if clause.count(".") != 1 or not clause.endswith("."):
        raise ValueError("clause must be exactly one sentence")
    return clause


def _as_entry_file(raw_value):
    """Turn one env value into a concrete file path, or None if blank."""
    if not raw_value:
        return None
    value = raw_value.strip()
    if not value:
        return None
    if os.path.isdir(value):
        return os.path.join(value, "entry.txt")
    return value


def _candidate_paths():
    """Yield candidate entry locations, best first.

    1. ENTRY_OUT (file, or a directory holding entry.txt).
    2. MAKEFUN_OUTPUT_DIR (file, or a directory holding entry.txt).
    3. /output/entry.txt — the grader's writable output directory.
    4. entry.txt in the current working directory, as a last resort.
    """
    for env_name in ("ENTRY_OUT", "MAKEFUN_OUTPUT_DIR"):
        candidate = _as_entry_file(os.environ.get(env_name))
        if candidate is not None:
            yield candidate
    yield os.path.join(os.sep, "output", "entry.txt")
    yield os.path.join(os.getcwd(), "entry.txt")


def _pick_entry_path():
    """Return the first candidate entry location."""
    return next(_candidate_paths())


def _persist_entry(destination, clause):
    """Write the clause to destination, creating its parent directory."""
    parent = os.path.dirname(os.path.abspath(destination))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(destination, "w", encoding="utf-8") as stream:
        stream.write(clause + "\n")


def main_entry():
    clause = _sanitise_clause(SHOWER_HUM_CLAUSE)
    written_to = None
    last_error = None
    for destination in _candidate_paths():
        try:
            _persist_entry(destination, clause)
        except OSError as exc:
            # That spot is not writable (e.g. a read-only cwd); keep trying
            # the next candidate instead of failing outright.
            last_error = exc
            continue
        written_to = destination
        break
    if written_to is None:
        raise last_error
    print(clause)
    return 0


if __name__ == "__main__":
    sys.exit(main_entry())
