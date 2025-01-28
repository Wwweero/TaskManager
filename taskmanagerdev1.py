import json #imports json
import os # imports os for seamless intercation with the operating system
from datetime import datetime, timedelta #imports datetime for setting up dates and timedelta for the reminders
import time # imports time module to work with time

# decorator for logging operations; logs the start and end of any method in the app
def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} completed.")
        return result
    return wrapper

class TaskManager:
    # creates the TaskManager class
    def __init__(self, data_file="tasks.json"): #initializes json file
        # defines a file path to store tasks
        self.data_file = data_file
        # loads tasks from the JSON file
        self.tasks = self.load_tasks()

    @log_operation
    def load_tasks(self):
        # loads tasks from the JSON file or returns an empty list if the file doesn't exist
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return json.load(file) # loads tasks from the JSON file as a Python list
        return []

    @log_operation
    def save_tasks(self):
        # writes tasks to the JSON file
        with open(self.data_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    @log_operation
    def add_task(self, title, due_date=None, priority=None, category=None):
        # function to add a new task with optional due date, priority, and category
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "completed": False,
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks() #calls save_task 
        print("Task added successfully!")

    @log_operation
    def view_tasks(self, filter_by=None, search_term=None):
        # function to view tasks by optional filters (completed/pending/all)
        tasks_to_display = self.tasks

        if filter_by == "completed":
            tasks_to_display = [task for task in self.tasks if task["completed"]]
        elif filter_by == "pending":
            tasks_to_display = [task for task in self.tasks if not task["completed"]]

        if search_term:
            tasks_to_display = [task for task in tasks_to_display if search_term.lower() in task["title"].lower()]

        if not tasks_to_display:
            print("No tasks found.")
        else:
            for task in tasks_to_display:
                print(f"ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}, Priority: {task['priority']}, Due Date: {task['due_date']}, Category: {task['category']}")

    @log_operation
    def mark_task_completed(self, task_id):
        # function to mark a task as completed by using its ID
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                print("Task marked as completed.")
                return
        print("Task not found.")

    @log_operation
    def delete_task(self, task_id):
        # function to delete a task by its ID
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        print("Task deleted.")

    @log_operation
    def reminder(self):
        ''' Function to set a reminder for a task. Notifies the user of tasks due in the next 24 hours'''
        print("Checking for reminders...")
        for task in self.tasks:
            if task["due_date"]:
                due_date = datetime.fromisoformat(task["due_date"])
                if not task["completed"] and datetime.now() <= due_date <= datetime.now() + timedelta(days=1):
                    print(f"Reminder: Task '{task['title']}' is due soon (Due: {task['due_date']})!")

    @log_operation
    def startup_reminder(self):
        # function that automatically checks for reminders when the program starts
        print("\n--- Upcoming Reminders ---")
        self.reminder()

    def run(self):
        # Main loop for the task manager application
        self.startup_reminder()
        while True:
            print("\n--- Welcome to Task Manager! ---")
            print("1. Add a Task")
            print("2. View Tasks")
            print("3. Mark a Task as Completed")
            print("4. Delete a Task")
            print("5. Set a Reminder")
            print("6. Exit")

            choice = input("What would you like to do? Please enter your choice: ")
            if choice == "1":
                title = input("Enter task title: ")
                due_date = input("Enter due date (YYYY-MM-DD HH:MM, optional): ") or None
                priority = input("Enter priority (High/Medium/Low, optional): ") or None
                category = input("Enter category (optional): ") or None
                self.add_task(title, due_date, priority, category)
            elif choice == "2":
                filter_by = input("Filter by status (completed/pending/all): ").lower()
                if filter_by not in ["completed", "pending", "all"]:
                    filter_by = None
                self.view_tasks(filter_by)
            elif choice == "3":
                try:
                    task_id = int(input("Enter task ID to mark it as completed: "))
                    self.mark_task_completed(task_id)
                except ValueError:
                    print("Invalid ID.")
            elif choice == "4":
                try:
                    task_id = int(input("Enter task ID you want to delete: "))
                    self.delete_task(task_id)
                except ValueError:
                    print("Invalid ID.")
            elif choice == "5":
                self.reminder()
            elif choice == "6":
                print("Exiting Task Manager. Have a productive day!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    manager = TaskManager()
    manager.run()
