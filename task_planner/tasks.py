import sqlite3
from sqlite3 import Connection
from utils.date_utils import str_to_date, date_to_str
import os
from typing import List, Dict

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
date TEXT NOT NULL,
status TEXT NOT NULL DEFAULT 'pending',
period TEXT
);
'''


class TaskManager:
  def __init__(self, db_path: str = "database/tasks.db"):
   self.db_path = db_path
# ensure directory exists
   os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
   self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
   self._init_db()


  def _init_db(self):
   cur = self.conn.cursor()
   cur.execute(CREATE_TABLE_SQL)
   self.conn.commit()


  def add_task(self, title: str, date_str: str, period: str = "day") -> int:
   cur = self.conn.cursor()
   cur.execute("INSERT INTO tasks (title, date, status, period) VALUES (?, ?, 'pending', ?)", (title, date_str, period))
   self.conn.commit()
   return cur.lastrowid


  def get_tasks_by_date(self, date_str: str) -> List[Dict]:
   cur = self.conn.cursor()
   cur.execute("SELECT id, title, date, status, period FROM tasks WHERE date = ? ORDER BY id", (date_str,))
   rows = cur.fetchall()
   return [self._row_to_dict(r) for r in rows]


  def get_tasks_between_dates(self, start_date_str: str, end_date_obj) -> List[Dict]:
# end_date_obj is datetime.date
   start = str_to_date(start_date_str)
   end = end_date_obj
   cur = self.conn.cursor()
   cur.execute("SELECT id, title, date, status, period FROM tasks ORDER BY date, id")
   rows = cur.fetchall()
   result = []
   for r in rows:
    row_date = str_to_date(r[2])
    if start <= row_date <= end:
     result.append(self._row_to_dict(r))
   return result


  def update_task_status(self, task_id: int, status: str):
   cur = self.conn.cursor()
   cur.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
   self.conn.commit()


  def move_task_to_date(self, task_id: int, new_date_str: str):
# Move task by updating its date (used for carry-forward move + merge behavior)
   cur = self.conn.cursor()
   cur.execute("UPDATE tasks SET date = ? WHERE id = ?", (new_date_str, task_id))
   self.conn.commit()


  def move_all_pending_on_date(self, from_date_str: str, to_date_str: str) -> int:
   cur = self.conn.cursor()
   cur.execute("UPDATE tasks SET date = ? WHERE date = ? AND status = 'pending'", (to_date_str, from_date_str))
   self.conn.commit()
   return cur.rowcount


  def delete_task(self, task_id: int):
   cur = self.conn.cursor()
   cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
   self.conn.commit()


  def _row_to_dict(self, row):
   return {"id": row[0], "title": row[1], "date": row[2], "status": row[3], "period": row[4]}


  def close(self):
   try:
    self.conn.close()
   except Exception:
    pass




if __name__ == "__main__":
 tm = TaskManager()
 print("DB initialized at", tm.db_path)