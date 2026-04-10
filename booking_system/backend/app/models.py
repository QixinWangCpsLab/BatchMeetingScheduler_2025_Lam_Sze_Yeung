from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    teacher_email: Mapped[str] = mapped_column(String(200))
    teacher_password: Mapped[str] = mapped_column(String(200))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    round_index: Mapped[int] = mapped_column(Integer, default=1)
    date_choice_num: Mapped[int] = mapped_column(Integer, default=2)
    slot_choice_num: Mapped[int] = mapped_column(Integer, default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MeetingDate(Base):
    __tablename__ = "meeting_dates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    day: Mapped[Date] = mapped_column(Date)

    __table_args__ = (UniqueConstraint("meeting_id", "day", name="uq_meeting_day"),)


class MeetingSlot(Base):
    __tablename__ = "meeting_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    day: Mapped[Date] = mapped_column(Date, index=True)
    start_time: Mapped[str] = mapped_column(String(5))
    end_time: Mapped[str] = mapped_column(String(5))
    scheduled: Mapped[bool] = mapped_column(Boolean, default=False)
    round_index: Mapped[int] = mapped_column(Integer, default=1)


class MeetingGroup(Base):
    __tablename__ = "meeting_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    group_code: Mapped[str] = mapped_column(String(50), index=True)
    group_name: Mapped[str] = mapped_column(String(120))
    contact_email: Mapped[str] = mapped_column(String(200))
    group_password: Mapped[str] = mapped_column(String(80))
    scheduled: Mapped[bool] = mapped_column(Boolean, default=False)
    last_submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("meeting_id", "group_code", name="uq_meeting_group_code"),)


class GroupMember(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_group_id: Mapped[int] = mapped_column(ForeignKey("meeting_groups.id", ondelete="CASCADE"), index=True)
    member_id: Mapped[str] = mapped_column(String(80))
    member_name: Mapped[str] = mapped_column(String(120), default="")


class GroupPreference(Base):
    __tablename__ = "group_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    meeting_group_id: Mapped[int] = mapped_column(ForeignKey("meeting_groups.id", ondelete="CASCADE"), index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("meeting_slots.id", ondelete="CASCADE"), index=True)
    priority: Mapped[int] = mapped_column(Integer)
    round_index: Mapped[int] = mapped_column(Integer, default=1)

    __table_args__ = (
        UniqueConstraint("meeting_id", "meeting_group_id", "priority", "round_index", name="uq_group_preference_rank"),
    )


class GroupResult(Base):
    __tablename__ = "group_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    meeting_group_id: Mapped[int] = mapped_column(ForeignKey("meeting_groups.id", ondelete="CASCADE"), index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("meeting_slots.id", ondelete="CASCADE"), index=True)
    round_index: Mapped[int] = mapped_column(Integer)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes: Mapped[str] = mapped_column(Text, default="")

    __table_args__ = (UniqueConstraint("meeting_id", "meeting_group_id", name="uq_group_result"),)
