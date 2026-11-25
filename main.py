"""The Absurd Clause Contest — one-sentence absurd ToS clause entry."""

import os
import sys

CLAUSE = (
    "By using this service, you irrevocably assign to us all rights in any "
    "song you hum in the shower, including royalties, remixes, and future "
    "shower performances."
)


def validate_clause(text):
    """Ensure the clause is exactly one sentence within the 200-char cap."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("clause is empty")
    if len(stripped) > 200:
        raise ValueError("clause exceeds 200 characters")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("clause must be exactly one sentence")
    return stripped


def resolve_output_path():
    """Return the file path where the entry text should be written."""
    target = os.environ.get("ENTRY_OUT")
    if not target:
        return "entry.txt"
    if os.path.isdir(target):
        return os.path.join(target, "entry.txt")
    return target


def main():
    checked_clause = validate_clause(CLAUSE)
    path = resolve_output_path()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(checked_clause + "\n")
    print(checked_clause)
    return 0


if __name__ == "__main__":
    sys.exit(main())
