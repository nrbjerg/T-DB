from __future__ import annotations
import pandas as pd 
from dataclasses import dataclass
from typing import Dict, List, Optional, Literal, Tuple
from collections import defaultdict
import datetime
import os 
import re

PATH_TO_ACTIVITIES = os.path.join(os.getcwd(), "activities.csv")
START_DATE = datetime.date(year=2026, month=10, day=3)
START_TIME = datetime.datetime(year=2026, month=10, day=3)

@dataclass
class Activity:
    """Stores all of the information associated with a single activity."""
    name: str
    number: int
    typ: Literal["swim", "ride", "run", "gym"]
    start_time: datetime.datetime
    duration: float # Seconds
    distance: Optional[float] # Meters
    hr_information: Optional[Tuple[float, float]] # BPM
    elevation_gain: Optional[float] = None # Meters

    @property
    def day_number(self) -> int:
        """Returns the number of days between the start date and the start_time of the activity"""
        return (self.start_time.date() - START_DATE).days

def load_activity_data() -> List[Activity]:
    """Loads the activity data from the activities.csv file and sorts them into key session types, 
       extracts important information such as duration, distance, elevation gain, hr information etc."""
    df = pd.read_csv(PATH_TO_ACTIVITIES)
    activities = []
    for _, row in df.iterrows():
        start_time = datetime.datetime.strptime(row["Activity Date"], "%b %d, %Y, %I:%M:%S %p")
        match = re.search(r"^(.*?)\[(.*)\]", row["Activity Name"])
        if start_time.date() < START_DATE or match is None or row["Activity Type"].lower() not in ["swim", "ride", "virtual ride", "run"]: # NOTE: Skip unrelated activity types.
            continue

        # TODO: Import wattage and pace as well.
        name = match.group(1).strip().lower()
        number = int(match.group(2).split(" ")[-1].strip())
        typ = row["Activity Type"].lower().split(" ")[-1] # NOTE: A virtual ride is also just a ride.
        duration = row["Moving Time"] if typ != "swim" else row["Elapsed Time"]
        distance = float(row["Distance"]) * 1000 if typ != "swim" else float(row["Distance"].replace(",", ""))
        hr_information = (float(row["Average Heart Rate"]), float(row["Max Heart Rate"]))
        elevation_gain = float(row["Elevation Gain"]) if typ != "swim" else None

        activities.append(Activity(name, number, typ, start_time, duration, distance, hr_information, elevation_gain))

    return list(reversed(activities))

@dataclass
class GroupedActivities:
    """Models a group of activity, for instance they could be grouped by week."""
    swims: List[Activity]
    rides: List[Activity]
    runs: List[Activity]

    def __init__(self, activities: List[Activity]):
        """Sorts the activities into their respective disciplines"""
        self.swims, self.rides, self.runs = [], [], []

        for activity in activities:
            if activity.typ == "swim":
                self.swims.append(activity)
            elif activity.typ == "ride":
                self.rides.append(activity)
            else:
                self.runs.append(activity)

    def __repr__ (self):
        return f"({len(self.swims)}, {len(self.rides)}, {len(self.runs)})"

def group_activities_into_weeks(activities: List[Activity]) -> Dict[int, GroupedActivities]:
    """Groups the activities into the weeks from the starting date"""
    activities_grouped_by_weeks = defaultdict(list)

    for activity in activities:
        week_number = ((activity.start_time.date() - START_DATE).days + 5) // 7 # NOTE: The +5 is because the first session on the 3rd of october 2026 was a saturday.
        activities_grouped_by_weeks[week_number].append(activity)

    return {week_number: GroupedActivities(activities) for week_number, activities in activities_grouped_by_weeks.items()}
        
if __name__ == "__main__":
    activities = load_activity_data()
    print(activities[0])
    activities_grouped_by_weeks = group_activities_into_weeks(activities)