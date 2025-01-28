# TaskManager
A Python CLI application for task management.

## Features 📍

- **Add Tasks**: Create a task with a title, optional due date, priority (High/Medium/Low), and category.
- **View Tasks**: Display all stored tasks or filter by completed/pending status.
- **Mark Task as Completed**: Select and mark task as completed.
- **Delete Task**: Remove outdated or unnecessary tasks.
- **Reminders**: Get notified about tasks due in the next 24 hours whenever the program starts.
- **Persistent Storage**: Tasks are saved in a JSON file (`tasks.json`) for use across sessions.
- **Menu Navigation**: Return to the main menu at any point for seamless usage.

---

## Installation 🔧

### Clone the Repository:

```bash
git clone https://github.com/Wwweero/TaskManager.git
cd TaskManager
```

### Run the Script:

Ensure you have Python installed, then execute:

```bash
python taskmanagerdev1.py
```

---

## Usage Instructions 📖

### Start the Program:
Run the script to access the main menu.

### Choose an Option:
- Add a Task (Option 1).
- View Tasks (Option 2).
- Mark a Task as Completed (Option 3).
- Delete a Task (Option 4).
- Set a Reminder (Option 5).
- Exit (Option 6).

### Storage:
Tasks are automatically saved in a file named `tasks.json` in the same directory. You can also edit this file manually if needed.

---

## Example Usage (Adding a Task) 🎯

```text
Welcome to Task Manager!
1. Add a Task
2. View Tasks
3. Mark a Task as Completed
4. Delete a task
5. Set a Reminder
6. Exit

Enter your choice: 1

Enter task title: Update the README file
Enter due date (YYYY-MM-DD HH:MM, optional): 2025-01-28 16:00
Enter priority (High/Medium/Low, optional): High
Enter category (optional): Work

Task added successfully!
```

---

## Requirements 🖥️

- Python 3.8 or higher

---

