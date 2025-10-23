from tasks import TaskManager
from utils.date_utils import today_str, tomorrow_str
import datetime




def move_pending_and_merge(db_path: str, from_date: str = None, to_date: str = None) -> int:
 """
Move all pending tasks from from_date to to_date using TaskManager.
Returns number of tasks moved.
If from_date / to_date are None, uses today -> tomorrow.
"""
 tm = TaskManager(db_path)
 if from_date is None:
    from_date = today_str()
 if to_date is None:
    to_date = tomorrow_str()
 count = tm.move_all_pending_on_date(from_date, to_date)
 tm.close()
 return count




if __name__ == "__main__":
 db = "database/tasks.db"
 moved = move_pending_and_merge(db)
 print(f"Moved {moved} pending tasks to tomorrow.")
