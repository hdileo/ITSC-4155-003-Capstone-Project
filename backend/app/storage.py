import uuid

# In-memory storage for Sprint 1

#Storgae FIle( Storing our Tasks: Operations like Getting, Adding a New Task, Deleting,etc..)


#Step #1: Need a Location to Store All our Tasks -- List 
#Lesson #1 --> When Dealing with Priority We Can Assign a Value to It Based off a Dictionary 

#Method #1: Creating a Task(We Need the Title, DueDate, Priority)
# Displaying -- ID, Title, Status, Due Date, Priority

#Second Aspect to THis --> Getting all The Tasks 
#Storing Tasks --.
TASKS = []

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

def create_task(title: str, due_date: str, priority: str):
    task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "status": "Pending",
        "due_date": due_date.strip(),   # frontend sends "YYYY-MM-DD HH:MM"
        "priority": priority.strip()     # "Low"|"Medium"|"High"
    }
    TASKS.append(task)
    return task

def get_all_tasks(sort_by: str | None = None):
    tasks = list(TASKS)

    if sort_by == "date":
        # Works correctly if due_date format is consistent: "YYYY-MM-DD HH:MM"
        tasks.sort(key=lambda t: t["due_date"])
    elif sort_by == "priority":
        tasks.sort(key=lambda t: PRIORITY_ORDER.get(t["priority"], 99))

    return tasks