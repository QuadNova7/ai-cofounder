"""GTM Weekly Sprint Plan Generator.

Formats, validates, and serializes the 12 weekly sprints and Day 1-14 immediate actions.
"""

from typing import List, Dict, Any
from shared.contracts.marketing import Milestone
from app.agents.marketing.schemas import WeeklySprintItem


class GTMPlanGenerator:
    """Manages serialization and validation of 12-week execution sprints."""

    @staticmethod
    def build_milestones_from_sprints(sprints: List[Any]) -> List[Milestone]:
        """Converts raw sprint items or dicts into typed shared Milestone contracts."""
        milestones: List[Milestone] = []

        for i, item in enumerate(sprints):
            if isinstance(item, dict):
                week = item.get("week", i + 1)
                month = item.get("month", ((week - 1) // 4) + 1)
                focus = item.get("focus", f"Week {week} Execution Focus")
                target_kpi = item.get("target_kpi", "Active milestone deliverable validation")
                deliverables = item.get("deliverables", ["Implement planned sprint tasks"])
            elif hasattr(item, "week"):
                week = item.week
                month = item.month if hasattr(item, "month") else ((week - 1) // 4) + 1
                focus = item.focus
                target_kpi = item.target_kpi
                deliverables = item.deliverables
            else:
                week = i + 1
                month = ((week - 1) // 4) + 1
                focus = f"Week {week} Execution"
                target_kpi = "Sprint deliverables complete"
                deliverables = ["Execute planned tactics"]

            milestones.append(Milestone(
                month=month,
                week=week,
                focus=focus,
                target_kpi=target_kpi,
                deliverables=deliverables
            ))

        return milestones
