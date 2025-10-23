import streamlit as st
from tasks import TaskManager
from utils.date_utils import today_str, tomorrow_str, date_to_str
import datetime

st.set_page_config(page_title="Study Partner", layout="wide", page_icon="📚")

tm = TaskManager("database/tasks.db")

st.sidebar.title("📅 Today")
st.sidebar.write(f"**{today_str()}**")
st.sidebar.markdown("---")

today=today_str()
tasks=tm.get_tasks_by_date(today)

if not tasks:
    st.sidebar.info("No task for today.Add some from the main page")
else:
    st.sidebar.write(f"**{len(tasks)} tasks**")
    for t in tasks:
       key = f"task_{t['id']}"
       checked=True if t["status"]=="done" else False
       st.sidebar.checkbox(t['title'], value=checked, key=key)
       
if st.sidebar.button("Save Statuses"):
    moved = 0
    updated = 0
    for t in tasks:
        key = f"task_{t['id']}"
        new_status = "done" if st.session_state.get(key, False) else "pending"
        if new_status != t['status']:
            tm.update_task_status(t['id'], new_status)
            updated += 1
            if new_status == "pending":
                tm.move_task_to_date(t['id'], tomorrow_str())
                moved += 1
    st.sidebar.success(f"Saved. {updated} updated, {moved} moved to tomorrow.")

st.sidebar.markdown("---")
if st.sidebar.button("Process all pending (Move to tomorrow)"):
  count = tm.move_all_pending_on_date(today, tomorrow_str())
  st.sidebar.success(f"Moved {count} pending tasks to tomorrow.")

st.sidebar.markdown("---")
st.sidebar.write("App Commands")
st.sidebar.write("• Add tasks on main page")
st.sidebar.write("• Tasks auto-move when left pending")



#  Main page
st.title("📚 Study Partner — Dashboard")
st.markdown("Hello! 👋 This is your Study Partner. Use the sidebar for today's quick checklist.")

all_today=tm.get_tasks_by_date(today)
completed=sum(1 for t in all_today if(t['status']=="done"))
pending=sum(1 for t in all_today if(t['status']=="pending"))

col1, col2, col3 = st.columns(3)
col1.metric("📋 Total today", len(all_today))
col2.metric("✅ Completed", completed)
col3.metric("⏳ Pending", pending)

# Progress bar
if all_today:
    progress = completed / len(all_today)
    st.progress(progress)
    st.write(f"**Daily Progress: {int(progress * 100)}%**")

st.markdown("---")

st.header("Add new task")
with st.form("add_task_form"):
    title=st.text_input("Task title")
    date_obj = st.date_input("Assign date", value=datetime.date.today())#default today
    period=st.selectbox("Period:",["day","week","month","year"])
    submit = st.form_submit_button("Add Task")
    if submit:
        if not title.strip():
            st.error("Please enter a task title.")
        else:
            date_str = date_to_str(date_obj)
            tm.add_task(title.strip(), date_str, period)
            st.success(f"Task added for {date_str}")
            
# Show Upcoming tasks (next 7 days)
st.header("📅 Upcoming (7 days)")
upcoming = tm.get_tasks_between_dates(today_str(), (datetime.date.today()+datetime.timedelta(days=7)))
# Filter out done tasks
upcoming = [t for t in upcoming if t['status'] != 'done']
if not upcoming:
  st.info("No upcoming tasks")
else:
  # Sort by date
  upcoming.sort(key=lambda x: x['date'])
  for t in upcoming:
    with st.container():
      col1, col2, col3 = st.columns([3, 1, 1])
      with col1:
        if t['date'] == today_str():
          st.markdown(f"**📍 Today — {t['title']}**")
        else:
          st.markdown(f"**📅 {t['date']} — {t['title']}**")
      with col2:
        if t['status'] == 'pending':
          st.markdown("⏳ Pending")
        else:
          st.markdown("✅ Done")
      with col3:
        if st.button("🗑️", key=f"delete_{t['id']}", help="Delete task"):
          tm.delete_task(t['id'])
          st.success(f"Deleted task: {t['title']}")
          st.rerun()
    st.markdown("---")
    

