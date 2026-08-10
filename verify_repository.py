#!/usr/bin/env python3
"""Validate the public AP Microeconomics repository structure and content."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULES = [
    Path("lecture/00-课程介绍.md"),
    Path("lecture/01-基本经济概念.md"),
    Path("lecture/02-供给与需求.md"),
    Path("lecture/03-生产成本与完全竞争.md"),
    Path("lecture/04-不完全竞争.md"),
    Path("lecture/05-要素市场.md"),
    Path("lecture/06-市场失灵与政府作用.md"),
    Path("lecture/07-练习题答案.md"),
]

EXPECTED_TITLES = [
    "# AP Micro考试概览",
    "# Basic Economic Concepts",
    "# Supply and Demand",
    "# Production, Cost & Perfect Competition",
    "# Imperfect Competition",
    "# Factor Markets",
    "# Market Failure & Role of Government",
    "# 答案与解析 {-}",
]

FORBIDDEN_PUBLIC_FILES = {
    "AGENTS.md",
    "AP微观经济学讲义.md",
    "AP微观经济学讲义.html",
    "AP微观经济学讲义.pdf",
    "补充练习题.md",
    "对话上下文总结.md",
    "test_output.html",
}
FORBIDDEN_PUBLIC_PREFIXES = ("docs/", "superpower/", "superpowers/")
FORBIDDEN_PUBLIC_PATTERNS = (
    re.compile(r"^micro_review.*\.md$"),
    re.compile(r"^overflow_results.*\.json$"),
    re.compile(r"^ap\d+-frq-set\d+\.pdf$", re.IGNORECASE),
)


def count_numbered_questions(block: str) -> int:
    return len(re.findall(r"(?m)^\s*\d+\.\s+", block))


def count_subparts(block: str) -> int:
    return len(re.findall(r"(?m)^(?:\*\*)?\([a-e]\)", block))


def sections(text: str, heading_pattern: str) -> list[str]:
    matches = list(re.finditer(heading_pattern, text, flags=re.MULTILINE))
    result: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append(text[match.start() : end])
    return result


def tracked_files() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [line.replace("\\", "/") for line in completed.stdout.splitlines()]


def main() -> int:
    errors: list[str] = []

    missing = [path.as_posix() for path in MODULES if not (ROOT / path).is_file()]
    if missing:
        errors.append("missing lecture modules: " + ", ".join(missing))

    obsolete = [
        name
        for name in ("AP微观经济学讲义.md", "补充练习题.md", "AGENTS.md")
        if (ROOT / name).exists()
    ]
    if obsolete:
        errors.append("obsolete public-source files still exist: " + ", ".join(obsolete))
    # Empty ignored directories are not part of a Git repository; tracked-file
    # checks below enforce that no internal docs are published.

    module_texts: list[str] = []
    if not missing:
        for path, title in zip(MODULES, EXPECTED_TITLES, strict=True):
            text = (ROOT / path).read_text(encoding="utf-8")
            module_texts.append(text)
            first_heading = next((line for line in text.splitlines() if line.startswith("# ")), "")
            if first_heading != title:
                errors.append(f"{path.as_posix()} starts with {first_heading!r}, expected {title!r}")

        unit_texts = module_texts[1:7]
        for unit, text in enumerate(unit_texts, start=1):
            mcq_blocks = sections(text, r"^### MCQ\s*$")
            if len(mcq_blocks) != 1:
                errors.append(f"Unit {unit} has {len(mcq_blocks)} MCQ sections, expected 1")
            elif count_numbered_questions(mcq_blocks[0]) != 10:
                errors.append(
                    f"Unit {unit} has {count_numbered_questions(mcq_blocks[0])} MCQs, expected 10"
                )

        expected_frq = [[5, 4], [], [5, 5], [5], [4], [5]]
        actual_frq: list[list[int]] = []
        for text in unit_texts:
            blocks = sections(text, r"^### FRQ(?: 2)?\s*$")
            actual_frq.append([count_subparts(block) for block in blocks])
        if actual_frq != expected_frq:
            errors.append(f"FRQ question subparts {actual_frq}, expected {expected_frq}")

        answer_text = module_texts[7]
        unit_answers = sections(answer_text, r"^## Unit [1-6]:.*\{-\}\s*$")
        if len(unit_answers) != 6:
            errors.append(f"answer module has {len(unit_answers)} unit sections, expected 6")
        else:
            answer_mcq_counts: list[int] = []
            answer_frq: list[list[int]] = []
            for block in unit_answers:
                mcq_match = re.search(
                    r"(?ms)^### MCQ \{-\}\s*$.*?(?=^### |^## |\Z)", block
                )
                answer_mcq_counts.append(
                    len(re.findall(r"(?m)^\s*\d+\.\s+\*\*[a-e]\*\*", mcq_match.group(0)))
                    if mcq_match
                    else 0
                )
                frq_blocks = sections(block, r"^### FRQ(?: 2)? \{-\}\s*$")
                answer_frq.append([count_subparts(item) for item in frq_blocks])
            if answer_mcq_counts != [10] * 6:
                errors.append(f"MCQ answer counts {answer_mcq_counts}, expected {[10] * 6}")
            if answer_frq != expected_frq:
                errors.append(f"FRQ answer subparts {answer_frq}, expected {expected_frq}")

        combined = "".join(module_texts)
        refs = re.findall(r"!\[[^\]]*\]\((charts/[^)]+\.png)\)", combined)
        assets = {path.relative_to(ROOT).as_posix() for path in (ROOT / "charts").glob("*.png")}
        if set(refs) != assets:
            missing_assets = sorted(set(refs) - assets)
            orphan_assets = sorted(assets - set(refs))
            errors.append(
                f"chart closure failed; missing={missing_assets}, unreferenced={orphan_assets}"
            )

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for path in MODULES:
            if path.as_posix() not in readme:
                errors.append(f"README does not link to {path.as_posix()}")

    try:
        tracked = tracked_files()
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"cannot inspect Git index: {exc}")
    else:
        forbidden_tracked: list[str] = []
        for path in tracked:
            if path in FORBIDDEN_PUBLIC_FILES or path.startswith(FORBIDDEN_PUBLIC_PREFIXES):
                forbidden_tracked.append(path)
                continue
            if any(pattern.search(path) for pattern in FORBIDDEN_PUBLIC_PATTERNS):
                forbidden_tracked.append(path)
        if forbidden_tracked:
            errors.append("forbidden tracked files: " + ", ".join(sorted(forbidden_tracked)))

    if errors:
        print("Repository verification FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository verification PASSED")
    print("- 8 ordered lecture modules")
    print("- 60 MCQs and matching answer keys")
    print("- FRQ question/answer subparts match by unit")
    print("- chart references and published PNG assets are closed")
    print("- no forbidden public files are tracked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
