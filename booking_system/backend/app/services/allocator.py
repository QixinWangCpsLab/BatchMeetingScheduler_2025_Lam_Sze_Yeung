from __future__ import annotations

from typing import Dict

from sqlalchemy import Select, asc, select
from sqlalchemy.orm import Session

from ..models import GroupPreference, GroupResult, Meeting, MeetingGroup, MeetingSlot


def allocate_fcfs(db: Session, meeting: Meeting) -> Dict[str, int]:
    groups_stmt: Select = (
        select(MeetingGroup)
        .where(MeetingGroup.meeting_id == meeting.id, MeetingGroup.scheduled.is_(False))
        .order_by(asc(MeetingGroup.last_submitted_at), asc(MeetingGroup.id))
    )
    groups = db.scalars(groups_stmt).all()

    used_slot_ids = set(
        db.scalars(select(GroupResult.slot_id).where(GroupResult.meeting_id == meeting.id)).all()
    )

    allocated_count = 0
    allocated_group_ids: list[int] = []
    for group in groups:
        prefs = db.scalars(
            select(GroupPreference)
            .where(
                GroupPreference.meeting_id == meeting.id,
                GroupPreference.meeting_group_id == group.id,
                GroupPreference.round_index == meeting.round_index,
            )
            .order_by(asc(GroupPreference.priority))
        ).all()

        picked_slot = None
        for pref in prefs:
            if pref.slot_id in used_slot_ids:
                continue

            slot = db.scalar(
                select(MeetingSlot).where(
                    MeetingSlot.id == pref.slot_id,
                    MeetingSlot.meeting_id == meeting.id,
                    MeetingSlot.scheduled.is_(False),
                )
            )
            if slot:
                picked_slot = slot
                break

        if not picked_slot:
            continue

        picked_slot.scheduled = True
        group.scheduled = True
        used_slot_ids.add(picked_slot.id)

        db.add(
            GroupResult(
                meeting_id=meeting.id,
                meeting_group_id=group.id,
                slot_id=picked_slot.id,
                round_index=meeting.round_index,
                notes="Allocated by FCFS",
            )
        )
        allocated_count += 1
        allocated_group_ids.append(group.id)

    db.commit()

    unscheduled_count = db.query(MeetingGroup).filter(
        MeetingGroup.meeting_id == meeting.id,
        MeetingGroup.scheduled.is_(False),
    ).count()

    return {
        "allocated_count": allocated_count,
        "allocated_group_ids": allocated_group_ids,
        "unscheduled_count": unscheduled_count,
        "round_index": meeting.round_index,
    }
