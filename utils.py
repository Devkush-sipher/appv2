# utils.py

import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
SLEEP_FILE = os.path.join(DATA_DIR, "sleep.csv")
EXP_FILE = os.path.join(DATA_DIR, "expenses.csv")
TODO_FILE = os.path.join(DATA_DIR, "todo.csv")
MED_FILE = os.path.join(DATA_DIR, "medicine.csv")

# Make sure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# If any of these files do not exist, create them with the proper header row:
if not os.path.isfile(SLEEP_FILE):
    pd.DataFrame(columns=["date", "start", "end", "duration"]).to_csv(SLEEP_FILE, index=False)

if not os.path.isfile(EXP_FILE):
    pd.DataFrame(columns=["date", "amount", "category", "status"]).to_csv(EXP_FILE, index=False)

if not os.path.isfile(TODO_FILE):
    pd.DataFrame(columns=["date", "task", "status"]).to_csv(TODO_FILE, index=False)

if not os.path.isfile(MED_FILE):
    pd.DataFrame(columns=["category", "time_of_day", "sub_category"]).to_csv(MED_FILE, index=False)


def load_data():
    """
    Reads sleep.csv, expenses.csv, and todo.csv, ensuring that each
    DataFrame always has the expected columns. Returns (sleep_df, exp_df, todo_df).
    """
    # ---------------------------
    # 1) Load Sleep DataFrame
    # ---------------------------
    sleep_df = pd.read_csv(SLEEP_FILE, parse_dates=["date", "start", "end"])
    # If "duration" column is missing (e.g. an older file), compute it or set 0
    if "duration" not in sleep_df.columns:
        if "start" in sleep_df.columns and "end" in sleep_df.columns:
            sleep_df["duration"] = (
                pd.to_datetime(sleep_df["end"]) - pd.to_datetime(sleep_df["start"])
            ).dt.total_seconds() / 3600.0
        else:
            sleep_df["duration"] = 0.0

    # ---------------------------
    # 2) Load Expenses DataFrame
    # ---------------------------
    exp_df = pd.read_csv(EXP_FILE, parse_dates=["date"])
    # If any expected column is missing, add it with a sensible default
    for col in ["amount", "category", "status"]:
        if col not in exp_df.columns:
            if col == "amount":
                exp_df[col] = 0.0
            else:
                exp_df[col] = ""

    # ---------------------------
    # 3) Load To-Do DataFrame
    # ---------------------------
    todo_df = pd.read_csv(TODO_FILE, parse_dates=["date"])
    for col in ["task", "status"]:
        if col not in todo_df.columns:
            todo_df[col] = ""

    return sleep_df, exp_df, todo_df


def save_sleep(start_dt, end_dt):
    """
    Appends a new sleep row into sleep.csv
    """
    duration_hrs = round((end_dt - start_dt).total_seconds() / 3600.0, 2)
    log_date = start_dt.date()
    new_row = {
        "date": pd.Timestamp(log_date),
        "start": pd.Timestamp(start_dt),
        "end": pd.Timestamp(end_dt),
        "duration": duration_hrs,
    }

    sleep_df, exp_df, todo_df = load_data()
    sleep_df = pd.concat([sleep_df, pd.DataFrame([new_row])], ignore_index=True)
    sleep_df.to_csv(SLEEP_FILE, index=False)


def save_expense(exp_date, amount, category, status):
    """
    Appends a new expense row into expenses.csv
    """
    new_row = {
        "date": pd.Timestamp(exp_date),
        "amount": float(amount),
        "category": category,
        "status": status,
    }

    sleep_df, exp_df, todo_df = load_data()
    exp_df = pd.concat([exp_df, pd.DataFrame([new_row])], ignore_index=True)
    exp_df.to_csv(EXP_FILE, index=False)


def save_task(task_date, task_text, status):
    """
    Appends a new to-do task row into todo.csv
    """
    new_row = {
        "date": pd.Timestamp(task_date),
        "task": task_text,
        "status": status,
    }

    sleep_df, exp_df, todo_df = load_data()
    todo_df = pd.concat([todo_df, pd.DataFrame([new_row])], ignore_index=True)
    todo_df.to_csv(TODO_FILE, index=False)


def load_medicine():
    """
    Reads medicine.csv. If columns are missing, it adds them.
    Returns a DataFrame with columns = [category, time_of_day, sub_category].
    """
    med_df = pd.read_csv(MED_FILE)
    for col in ["category", "time_of_day", "sub_category"]:
        if col not in med_df.columns:
            med_df[col] = ""
    return med_df


def save_medicine(category, time_of_day, sub_category):
    """
    Appends a new medicine reminder into medicine.csv
    """
    new_row = {
        "category": category,
        "time_of_day": time_of_day,
        "sub_category": sub_category,
    }

    med_df = load_medicine()
    med_df = pd.concat([med_df, pd.DataFrame([new_row])], ignore_index=True)
    med_df.to_csv(MED_FILE, index=False)
