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


# Shared by the Intake runbook and issue creation help because these are the
# two operational points where an agent may otherwise turn priority into a
# batch ranking.
INTAKE_PRIORITY_GUIDANCE = (
    "Priority policy:\n"
    "- Keep priority 5 by default; omitting --priority is the normal path.\n"
    "- Do not rank issues in a batch or use priority to encode planned sequence.\n"
    "- Natural order resumes the current doing issue, defers unresolved dependencies, "
    "then uses stable issue ID order.\n"
    "- Use depends_on only for real precedence and create a batch in its desired natural order.\n"
    "- Change priority only to run before (>5) or after (<5) that order, and record the "
    "relative reason in the issue Markdown."
)


def add_global_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--dev",
        metavar="<developer-slug>",
        help=(
            "Developer namespace: lowercase ASCII letters, digits, and hyphens; "
            "must start with a letter (example: mynick)"
        ),
    )
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--json", action="store_true", help="Shorthand for --format json")
    parser.add_argument("--dry-run", action="store_true", help="Simulate changes")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")


def resolve_format(args: argparse.Namespace) -> str:
    if getattr(args, "json", False):
        return "json"
    return getattr(args, "format", "md")
