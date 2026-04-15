#!/usr/bin/env python3
"""
bundle.py — Bundle C++/Java/C# source files into the MANIFEST format
            defined in requirements.md §4.3.

Usage:
    python bundle.py --root <src_dir> [--out bundle.txt]
                     [--include '*.cpp'] [--exclude '*/test/*']
                     [--max-chars 80000]

Outputs a single text file (or chunked bundle-001.txt, bundle-002.txt, ...
when --max-chars is set) in the format:

    === MANIFEST ===
    File: <relative/path>
    Classes: A, B
    ...

    === FILE: <relative/path> ===
    <file content>

    === FILE: <next path> ===
    ...
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_EXTENSIONS = {
    ".cpp", ".cxx", ".cc", ".c++",
    ".hpp", ".hxx", ".hh", ".h",
    ".java",
    ".cs",
}

# Loose regex — MANIFEST is a hint for the AI, not ground truth.
# Matches `class Name`, `interface Name`, `struct Name` at any indent,
# skipping `class;` forward-declarations (handled by requiring a body or base).
CLASS_PATTERN = re.compile(
    r"^\s*(?:public|internal|private|protected|static|sealed|abstract|final|partial|\s)*"
    r"\b(?:class|interface|struct)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)


def iter_source_files(
    root: Path,
    extensions: set[str],
    includes: list[str],
    excludes: list[str],
) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        rel = path.relative_to(root).as_posix()
        if includes and not any(fnmatch.fnmatch(rel, pat) for pat in includes):
            continue
        if excludes and any(fnmatch.fnmatch(rel, pat) for pat in excludes):
            continue
        yield path


def extract_classes(source: str) -> list[str]:
    seen: list[str] = []
    for name in CLASS_PATTERN.findall(source):
        if name not in seen:
            seen.append(name)
    return seen


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp932", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def build_manifest_section(entries: list[tuple[str, list[str]]]) -> str:
    lines = ["=== MANIFEST ==="]
    for rel, classes in entries:
        lines.append(f"File: {rel}")
        if classes:
            lines.append(f"Classes: {', '.join(classes)}")
        else:
            lines.append("Classes: (none detected)")
    return "\n".join(lines) + "\n"


def build_file_section(rel: str, content: str) -> str:
    if not content.endswith("\n"):
        content += "\n"
    return f"\n=== FILE: {rel} ===\n{content}"


def write_chunks(out_path: Path, chunks: list[str]) -> list[Path]:
    if len(chunks) == 1:
        out_path.write_text(chunks[0], encoding="utf-8")
        return [out_path]
    written: list[Path] = []
    stem = out_path.stem
    suffix = out_path.suffix or ".txt"
    parent = out_path.parent
    for i, chunk in enumerate(chunks, 1):
        p = parent / f"{stem}-{i:03d}{suffix}"
        p.write_text(chunk, encoding="utf-8")
        written.append(p)
    return written


def chunk_bundle(
    entries: list[tuple[str, list[str], str]],
    max_chars: int | None,
) -> list[str]:
    """Split entries into bundles, each under max_chars when set.

    Each bundle has its own MANIFEST reflecting only the files in that bundle.
    """
    if max_chars is None:
        manifest = build_manifest_section([(rel, cls) for rel, cls, _ in entries])
        body = "".join(build_file_section(rel, content) for rel, _, content in entries)
        return [manifest + body]

    chunks: list[str] = []
    current: list[tuple[str, list[str], str]] = []

    def flush():
        if not current:
            return
        manifest = build_manifest_section([(rel, cls) for rel, cls, _ in current])
        body = "".join(build_file_section(rel, content) for rel, _, content in current)
        chunks.append(manifest + body)

    for entry in entries:
        tentative = current + [entry]
        manifest = build_manifest_section([(rel, cls) for rel, cls, _ in tentative])
        body = "".join(build_file_section(rel, content) for rel, _, content in tentative)
        size = len(manifest) + len(body)
        if size > max_chars and current:
            flush()
            current = [entry]
        else:
            current = tentative

    flush()
    return chunks


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", required=True, type=Path, help="Source directory to scan")
    p.add_argument("--out", type=Path, default=Path("bundle.txt"), help="Output file (default: bundle.txt)")
    p.add_argument("--include", action="append", default=[], help="Glob pattern to include (relative path, repeatable)")
    p.add_argument("--exclude", action="append", default=[], help="Glob pattern to exclude (relative path, repeatable)")
    p.add_argument("--max-chars", type=int, default=None, help="Split output when a chunk exceeds this char count")
    p.add_argument("--ext", action="append", default=[], help="Override extension list (e.g., --ext .cpp --ext .h)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root: Path = args.root.resolve()
    if not root.is_dir():
        print(f"error: --root is not a directory: {root}", file=sys.stderr)
        return 2

    extensions = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.ext} or DEFAULT_EXTENSIONS

    entries: list[tuple[str, list[str], str]] = []
    for path in iter_source_files(root, extensions, args.include, args.exclude):
        rel = path.relative_to(root).as_posix()
        content = read_text(path)
        classes = extract_classes(content)
        entries.append((rel, classes, content))

    if not entries:
        print(f"warning: no source files matched under {root}", file=sys.stderr)

    chunks = chunk_bundle(entries, args.max_chars)
    written = write_chunks(args.out, chunks)
    for p in written:
        print(f"wrote {p} ({p.stat().st_size} bytes)")
    print(f"files: {len(entries)}  chunks: {len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
