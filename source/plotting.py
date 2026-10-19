import matplotlib.pyplot as plt
from source.data import Activity, START_DATE
from typing import List, Optional
import datetime

ACTIVITY_TYPE_COLOR_MAP = {
    "swim": "tab:blue",
    "ride": "tab:green",
    "run": "tab:red",
    "gym": "tab:orange"
}

def filter_activities_based_on_dates(activities: List[Activity], start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None) -> List[Activity]:
    """Remove activities outside of the date range from the activities list and return the resulting list."""
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError("start_date must be on or before end_date")

    if start_date:
        activities = [activity for activity in activities if start_date <= activity.start_time.date()]
    if end_date:
        activities = [activity for activity in activities if activity.start_time.date() <= end_date]

    return activities
        
def workout_indicator_plot(activities: List[Activity], start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None):
    """Plots the workout indicator above separate swim, ride, and run charts."""
    plt.style.use("seaborn-v0_8-ticks")

    activities = filter_activities_based_on_dates(activities, start_date=start_date, end_date=end_date)
    if activities:
        start_date = min(a.start_time.date() for a in activities)
        end_date = max(a.start_time.date() for a in activities)
    else:
        raise ValueError(f"No activities registered in between {start_date} and {end_date}!")

    fig = plt.figure(figsize=(12, 8))
    grid = fig.add_gridspec(2, 3, height_ratios=[1, 2])
    indicator_ax = fig.add_subplot(grid[0, :])
    type_axes = {
        "swim": fig.add_subplot(grid[1, 0]),
        "ride": fig.add_subplot(grid[1, 1]),
        "run": fig.add_subplot(grid[1, 2]),
    }

    activity_type_to_y_map = {"swim": 4, "ride": 3, "run": 2, "gym": 1}
    day_numbers = range((start_date - START_DATE).days, (end_date - START_DATE).days + 1)
    indicator_ax.vlines([day for day in day_numbers if (day + 5) % 7 != 0], ymin=0, ymax=5, colors="black", linewidth=0.3)
    indicator_ax.vlines([day for day in day_numbers if (day + 5) % 7 == 0], ymin=0, ymax=5, colors="black", linewidth=0.7)

    for activity in activities:
        indicator_ax.scatter(activity.day_number, y=activity_type_to_y_map[activity.typ], c=ACTIVITY_TYPE_COLOR_MAP[activity.typ], zorder=2, s=120)

    indicator_ax.set_yticks(ticks=list(activity_type_to_y_map.values()), labels=list(activity_type_to_y_map.keys()))
    indicator_ax.set_xticks(day_numbers)
    indicator_ax.set_ylim(0.8, 4.2)
    indicator_ax.set_xlabel("Day")
    indicator_ax.set_title("Workout Indicator Plot")

    for activity_type, ax in type_axes.items():
        type_activities = [a for a in activities if a.typ == activity_type]
        ax.scatter([a.day_number for a in type_activities], [a.duration / 60 for a in type_activities], color=ACTIVITY_TYPE_COLOR_MAP[activity_type])
        ax.set_title(activity_type.title())
        ax.set_xlabel("Day")
        ax.set_ylabel("Duration (minutes)")

    fig.tight_layout()
    plt.show()