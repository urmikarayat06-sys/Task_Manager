import json
import os

TASK_FILE = 'tasks.json'


def load_tasks():
    """
    Loads tasks from the JSON file. If the file doesn't exist, returns an empty list.
    """
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, 'r') as f:
              
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
           
            return []
    return []

def save_tasks(tasks):
    """
    Saves the current list of tasks to the JSON file.
    """
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def generate_new_id(tasks):
    """
    Generates a unique ID for a new task by finding the maximum existing ID + 1.
    """
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def display_tasks(tasks):
    """
    Displays all tasks, sorted by priority (1=High to 3=Low).
    """
    if not tasks:
        print("\n--- Your To-Do List is empty! ---")
        return

    sorted_tasks = sorted(tasks, key=lambda x: (x['completed'], x['priority'], x['id']))

    print("\n=============================================")
    print("           Task Manager To-Do List           ")
    print("=============================================")

    PRIORITY_COLORS = {
        1: "\033[91m",  
        2: "\033[93m",  
        3: "\033[94m",  
    }
    RESET_COLOR = "\033[0m"

    for task in sorted_tasks:
        status = "[X]" if task['completed'] else "[ ]"
        prio_color = PRIORITY_COLORS.get(task['priority'], RESET_COLOR)

        if task['completed']:
          
            line_style_start = "\033[9m"
            line_style_end = RESET_COLOR + RESET_COLOR
        else:
            line_style_start = ""
            line_style_end = ""

        task_line = (
            f"{line_style_start}{prio_color}"
            f"ID {task['id']:<3} | {status} "
            f"{task['description']}"
            f" (Prio: {task['priority']})"
            f"{line_style_end}"
        )
        print(task_line)

    print("=============================================\n")


def add_task(tasks):
    """
    Prompts the user for a task description and priority, then adds the new task.
    """
    print("\n--- ADD NEW TASK ---")
    description = input("Enter task description: ").strip()

    if not description:
        print("\nError: Task description cannot be empty.")
        return

    while True:
        try:
            priority = int(input("Enter priority (1=High, 2=Medium, 3=Low): ").strip())
            if priority in [1, 2, 3]:
                break
            else:
                print("Error: Priority must be 1, 2, or 3.")
        except ValueError:
            print("Error: Invalid input. Please enter a number (1, 2, or 3).")

    new_id = generate_new_id(tasks)
    new_task = {
        'id': new_id,
        'description': description,
        'priority': priority,
        'completed': False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"\n Task ID {new_id} added successfully: '{description}' (Priority: {priority}).")


def delete_task(tasks):
    """
    Prompts for a Task ID and removes the corresponding task.
    """
    display_tasks(tasks)
    if not tasks:
        return

    while True:
        try:
            task_id = int(input("Enter ID of the task to DELETE: ").strip())
            break
        except ValueError:
            print("Error: Invalid input. Please enter a numerical ID.")

    initial_length = len(tasks)
  
    tasks[:] = [task for task in tasks if task['id'] != task_id]

    if len(tasks) < initial_length:
        save_tasks(tasks)
        print(f"\n️ Task ID {task_id} successfully DELETED.")
    else:
        print(f"\n Error: Task with ID {task_id} not found.")


def complete_task(tasks):
    """
    Prompts for a Task ID and marks the corresponding task as complete.
    """
    display_tasks(tasks)
    if not tasks:
        return

    while True:
        try:
            task_id = int(input("Enter ID of the task to MARK AS COMPLETE: ").strip())
            break
        except ValueError:
            print("Error: Invalid input. Please enter a numerical ID.")

    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            found = True
            break

    if found:
        save_tasks(tasks)
        print(f"\n Task ID {task_id} marked as COMPLETE.")
    else:
        print(f"\n Error: Task with ID {task_id} not found.")


def prioritize_task(tasks):
    """
    Prompts for a Task ID and allows the user to change its priority.
    """
    display_tasks(tasks)
    if not tasks:
        return

    while True:
        try:
            task_id = int(input("Enter ID of the task to CHANGE PRIORITY: ").strip())
            break
        except ValueError:
            print("Error: Invalid input. Please enter a numerical ID.")

    target_task = next((task for task in tasks if task['id'] == task_id), None)

    if not target_task:
        print(f"\n Error: Task with ID {task_id} not found.")
        return

    while True:
        try:
            new_priority = int(input(f"Enter new priority for ID {task_id} (Current: {target_task['priority']}) (1=High, 2=Medium, 3=Low): ").strip())
            if new_priority in [1, 2, 3]:
                break
            else:
                print("Error: Priority must be 1, 2, or 3.")
        except ValueError:
            print("Error: Invalid input. Please enter a number (1, 2, or 3).")
    target_task['priority'] = new_priority
    save_tasks(tasks)
    print(f"\n Task ID {task_id} priority updated to {new_priority}.")


def show_menu():
    """
    Displays the main menu options.
    """
    print("\n--- Task Manager Menu ---")
    print("1: View Tasks (Sorted by Priority)")
    print("2: Add New Task")
    print("3: Mark Task as Complete")
    print("4: Change Task Priority")
    print("5: Delete Task")
    print("0: Exit & Save")
    print("-------------------------")


def main_cli():
    """
    The main loop for the Command-Line Interface.
    """
    tasks = load_tasks()
    print("\n Welcome to the Python CLI Task Manager! ")

    while True:
        display_tasks(tasks)
        show_menu()
        choice = input("Enter your choice (0-5): ").strip()

        if choice == '1':
            continue
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            prioritize_task(tasks)
        elif choice == '5':
            delete_task(tasks)
        elif choice == '0':
            print("\n Saving tasks and exiting. Goodbye!")
            save_tasks(tasks)
            break
        else:
            print("\n Invalid choice. Please enter a number between 0 and 5.")

if __name__ == "__main__":
    main_cli()

