# analytics.py
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "database/tasks.db"

def get_task_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return df

def get_weekly_summary():
    df = get_task_data()

    if df.empty:
        return 0, 0, 0

    df["date"] = pd.to_datetime(df["date"])
    today = datetime.today().date()
    week_start = today - timedelta(days=7)

    # Filter last 7 days
    df_week = df[df["date"].dt.date >= week_start]

    tasks_added = len(df_week)
    tasks_done = len(df_week[df_week["status"] == "done"])
    completion_rate = round((tasks_done / tasks_added) * 100, 1) if tasks_added > 0 else 0

    return tasks_added, tasks_done, completion_rate

def get_daily_completion_trend():
    df = get_task_data()
    if df.empty:
        return pd.DataFrame(columns=["date", "completed_count"])

    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.date

    daily = df.groupby("date")["status"].apply(lambda x: (x == "done").sum()).reset_index(name="completed_count")
    return daily

def get_category_distribution():
    df = get_task_data()
    if "category" not in df.columns or df.empty:
        return pd.DataFrame(columns=["category", "count"])

    dist = df.groupby("category").size().reset_index(name="count")
    return dist
