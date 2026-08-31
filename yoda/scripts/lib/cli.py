"""CLI helpers for YODA scripts."""

import argparse


# Appended to every YODA command epilog. Kept in one place so the twelve help
# texts cannot drift, and repeated across all of them so the rule survives an
# agent losing earlier context.
AGENT_OUTPUT_RULE = (
    "\n\nAgent output rule:\n"
    "- Follow the runbook this command returns; it is your instruction for this step.\n"
    "- Never discard, silence, or redirect this output. Present it to the human."
)


def add_global_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dev", help="Developer slug")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--json", action="store_true", help="Shorthand for --format json")
    parser.add_argument("--dry-run", action="store_true", help="Simulate changes")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")


def resolve_format(args: argparse.Namespace) -> str:
    if getattr(args, "json", False):
        return "json"
    return getattr(args, "format", "md")
