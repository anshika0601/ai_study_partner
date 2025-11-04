# dashboard.py
import streamlit as st
import plotly.express as px
from utils.analytics import (
    get_weekly_summary,
    get_daily_completion_trend,
    get_category_distribution
)

def show_dashboard():
    st.subheader("📊 Progress Dashboard")

    # --- Summary Metrics ---
    tasks_added, tasks_done, completion_rate = get_weekly_summary()
    st.markdown("### 📈 Weekly Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tasks Added (7 days)", tasks_added)
    col2.metric("Tasks Completed", tasks_done)
    col3.metric("Completion Rate", f"{completion_rate}%")

    # --- Daily Trend Chart ---
    trend_df = get_daily_completion_trend()
    if not trend_df.empty:
        st.markdown("### 📆 Daily Task Completion Trend")
        fig = px.bar(
            trend_df,
            x="date",
            y="completed_count",
            title="Tasks Completed per Day",
            labels={"date": "Date", "completed_count": "Completed Tasks"},
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No tasks yet. Start adding tasks to see your progress!")

    # --- Category Distribution ---
    dist_df = get_category_distribution()
    if not dist_df.empty:
        st.markdown("### 🧩 Category Distribution")
        pie_fig = px.pie(
            dist_df,
            names="category",
            values="count",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(pie_fig, use_container_width=True)
    else:
        st.info("No categories found. Try adding 'category' field to tasks.")
