from source.analytics import estimate_gym_sessions
from source.data import load_activity_data
from source.plotting import workout_indicator_plot

activities_with_gym_sessions = estimate_gym_sessions(activities = load_activity_data())
workout_indicator_plot(activities_with_gym_sessions)
