"""Ordering helpers for TODO issues."""

from __future__ import annotations

from typing import Any


def apply_dependency_order(
    issues: list[dict[str, Any]],
    done_ids: set[str],
    order_index: dict[str, int],
) -> list[dict[str, Any]]:
    id_to_issue = {str(item.get("id")): item for item in issues}
    indegree = {issue_id: 0 for issue_id in id_to_issue}
    dependents: dict[str, list[str]] = {issue_id: [] for issue_id in id_to_issue}

    for issue_id, issue in id_to_issue.items():
        for dep in issue.get("depends_on", []):
            dep_id = str(dep)
            if dep_id in done_ids:
                continue
            if dep_id not in id_to_issue:
                continue
            indegree[issue_id] += 1
            dependents[dep_id].append(issue_id)

    zero = sorted(
        [issue_id for issue_id, count in indegree.items() if count == 0],
        key=lambda issue_id: order_index[issue_id],
    )
    ordered: list[str] = []
    while zero:
        current = zero.pop(0)
        ordered.append(current)
        for dep in dependents[current]:
            indegree[dep] -= 1
            if indegree[dep] == 0:
                zero.append(dep)
        zero.sort(key=lambda issue_id: order_index[issue_id])

    if len(ordered) != len(issues):
        return issues
    return [id_to_issue[issue_id] for issue_id in ordered]
