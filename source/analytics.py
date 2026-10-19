from source.data import Activity, START_DATE, START_TIME
from typing import List
import datetime

def estimate_gym_sessions(activities: List[Activity]) -> List[Activity]:
    """Estimates when gym sessions occurs based on the numbers from the sessions."""
    generate_gym_activity = lambda n, date: Activity("gym", n, "gym", date, 3600, None, None, None)
     
    for i in range(len(activities) - 1, 1, -1):
        print(activities[i].number, activities[i].start_time)
        if activities[i - 1].number + 1 < activities[i].number:
            # NOTE: If there is a discrepancy a gym activity did occur in between the activities.
            a = activities[i - 1].start_time + datetime.timedelta(seconds=activities[i - 1].duration)
            b = activities[i].start_time 
            date_estimate = a + (b - a) / 2
            activities.insert(i, generate_gym_activity(activities[i].number - 1, date_estimate))
           
    activities.insert(0, generate_gym_activity(1, START_TIME))
    return activities