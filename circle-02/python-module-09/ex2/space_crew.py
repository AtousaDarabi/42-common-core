from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        leadership_ranks = {Rank.COMMANDER, Rank.CAPTAIN}
        has_leader = any(
            member.rank in leadership_ranks for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced_members = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            required_count = len(self.crew) / 2.0
            if experienced_members < required_count:
                raise ValueError(
                    "Missions longer than 1 year require at least 50% "
                    "experienced crew members (5+ years experience)"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 9, 1, 8, 0, 0),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="M01",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=42,
                    specialization="Mission Command",
                    years_experience=15,
                ),
                CrewMember(
                    member_id="M02",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=34,
                    specialization="Navigation",
                    years_experience=8,
                ),
                CrewMember(
                    member_id="M03",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=28,
                    specialization="Engineering",
                    years_experience=5,
                ),
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )
        print()

    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("=" * 41)

    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_LUNAR",
            mission_name="Lunar Base Alpha",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=30,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="M04",
                    name="Bob Brown",
                    rank=Rank.LIEUTENANT,
                    age=30,
                    specialization="Pilot",
                    years_experience=3,
                )
            ],
        )
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].removeprefix("Value error, "))


if __name__ == "__main__":
    main()
