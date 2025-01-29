import json #imports json
import os # imports os for seamless intercation with the operating system
from datetime import datetime, timedelta, date #imports datetime for setting up dates and timedelta for the reminders
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

    def reassign_ids(self):
        #method that reassigns sequential IDs to tasks
        for index, task in enumerate(self.tasks, start=1):
         task["id"] = index


    @log_operation
    def load_tasks(self):
        # loads tasks from the JSON file or returns an empty list if the file doesn't exist
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                tasks = json.load(file) # loads tasks from the JSON file as a Python list
                self.tasks = tasks
                self.reassign_ids()
                return self.tasks
        return []

    @log_operation
    def save_tasks(self):
        # writes tasks to the JSON file
        with open(self.data_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    @log_operation
    def add_task(self, title, due_date=None, priority=None, category=None):
        # method to add a new task with optional due date, priority, and category
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
        self.reassign_ids() 
        self.save_tasks() #calls save_tasks 
        print("Task added successfully!")

    @log_operation
    def view_tasks_due_today(self):
        #method to display tasks due on the day
        print("---Tasks Due Today---")
        today = date.today()
        today_tasks = [
            task for task in self.tasks 
            if task.get("due_date") and datetime.strptime(task["due_date"], "%Y-%m-%d").date() == today
         ]
        if today_tasks:
            for task in today_tasks:
                print(f"ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
        else:
            print("No tasks due today.")

    @log_operation
    def view_tasks(self, filter_by=None, search_term=None):
        # method to view tasks by optional filters (completed/pending/all)
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
    def mark_task_completed(self):
        # method to mark a task as completed by using its ID
        print("\n---All Tasks---")
        for task in self.tasks:
            print(f"ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}" )
        try:
            task_id = int(input("Enter task ID to mark as completed: "))
            for task in self.tasks:
                if task["id"] == task_id:
                    task["completed"] = True
                    self.save_tasks()
                    print("Task marked as completed.")
                    return
            print("Task not found.")
        except ValueError:
            print ("Invalid ID. Please enter a numeric value.")

    @log_operation
    def delete_task(self):
        # method to delete a task by its ID
        print ("\n--- All Tasks ---")
        if not self.tasks:
            print("No tasks available.")
            return
        
        for task in self.tasks:
            print(f"ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}, Due Date: {task['due_date']}")
        
        while True: 
            user_input = input ("\n Enter the ID of the task you want to delete (or type 'b' to go back): ")

            if user_input.lower() == 'b':
                #option to go back to the menu
                print("Returning to the menu...")
                return
            
            try:
                task_id = int(user_input)
                task_to_delete = next((task for task in self.tasks if task["id"] == task_id), None)

                if task_to_delete:
                    self.tasks.remove(task_to_delete)
                    self.reassign_ids()  # Reassigns IDs to maintain consistency
                    self.save_tasks()
                    print(f"Task with ID {task_id} deleted successfully!")
                    return
                else:
                    print(f"No task found with ID {task_id}.")
            except ValueError:
                print("Invalid input. Please enter a valid ID or 'b' to go back.")    

        

    @log_operation
    def reminder(self):
        # Method to see a reminder for a task. Notifies the user of tasks due this week
        print("Checking for reminders...")
        today = datetime.now().date()
        end_of_week = today + timedelta(days=7)
        upcoming_tasks = []
            
        for task in self.tasks:
            due_date = task.get ("due_date")
            if due_date: 
                try: 
                    task_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                    if today <= task_due_date <= end_of_week:
                        upcoming_tasks.append(task)
                except ValueError:
                    print(f"[WARNING] Skipping task with invalid due date: {due_date}")
    
        if upcoming_tasks:
            for task in upcoming_tasks:
                print(f"ID: {task['id']}, Title: {task['title']}, Due Date: {task['due_date']}, Priority: {task.get('priority', 'N/A')}")
        else:
            print("No tasks due in the next 7 days.")    

    @log_operation
    def startup_reminder(self):
        # function that automatically checks for reminders when the program starts
        print("\n--- Upcoming Tasks (Next 7 Days) ---")
        self.reminder()

    def run(self):
        # Main loop for task manager
        self.startup_reminder()
        while True:
            print("\n--- Welcome to Task Manager! ---")
            print("1. Add a Task")
            print("2. View Tasks due today")
            print("3. View all Tasks")
            print("4. Mark Task as Completed")
            print("5. Delete a Task")
            print("6. See Reminders")
            print("7. Exit")

            choice = input("What would you like to do? Please enter your choice: ")
            if choice == "1":
                title = input("Enter task title: ")
                due_date = input("Enter due date (YYYY-MM-DD, optional): ") or None
                priority = input("Enter priority (High/Medium/Low, optional): ") or None
                category = input("Enter category (optional): ") or None
                self.add_task(title, due_date, priority, category)
            elif choice == "2":
                self.view_tasks_due_today()
            elif choice == "3":
                filter_by = input("Filter by status (completed/pending/all): ").lower()
                if filter_by not in ["completed", "pending", "all"]:
                    filter_by = None
                self.view_tasks(filter_by)
            elif choice == "4":
                self.mark_task_completed()
            elif choice =="5":
                self.delete_task()
            elif choice == "6":
                self.reminder()
            elif choice == "7":
                print("Exiting Task Manager. Have a productive day!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    manager = TaskManager()
    manager.run()
