
import streamlit as st
import pandas as pd
from datetime import date
from utils import load_data, save_task

st.set_page_config(page_title="To‑Do List", page_icon="✅")

st.title("✅ To‑Do List")

# Add task
st.header("Add Task")
task_date = st.date_input("Date", value=date.today())
task_text = st.text_input("Task description")
task_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])

if st.button("Add Task"):
    if task_text:
        save_task(task_date, task_text, task_status)
        st.success("Task added!")
    else:
        st.error("Please write a task description.")

# View / update tasks
_, _, todo_df = load_data()
st.subheader("Tasks")
if todo_df.empty:
    st.info("No tasks yet.")
else:
    todo_df = todo_df.sort_values(['date','status'])
    edited_df = st.data_editor(
        todo_df,
        num_rows="dynamic",
        use_container_width=True,
        key="todo_editor"
    )

    if st.button("Save Changes"):
        edited_df.to_csv("data/todo.csv", index=False)
        st.success("Changes saved!")
