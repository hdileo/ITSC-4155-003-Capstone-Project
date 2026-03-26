import os
import tempfile
import unittest
from datetime import datetime, timedelta

from backend.app import create_app


class ApiTests(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["DB_NAME"] = self.db_path

        with self.app.app_context():
            from backend.app.database import init_db
            init_db()

        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_create_and_list_tasks(self):
        res = self.client.post("/api/tasks", json={
            "title": "Math Homework",
            "due_date": "2026-03-01 23:59",
            "priority": "High"
        })

        self.assertEqual(res.status_code, 201)

        res = self.client.get("/api/tasks")
        self.assertEqual(res.status_code, 200)

        data = res.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Math Homework")
        self.assertEqual(data[0]["status"], "Pending")
        self.assertEqual(data[0]["due_date"], "2026-03-01 23:59")
        self.assertEqual(data[0]["priority"], "High")

    def test_edit_task(self):
        res = self.client.post("/api/tasks", json={
            "title": "Finish Sprint Report",
            "due_date": "2026-03-10 17:00",
            "priority": "High"
        })

        task = res.get_json()
        task_id = task["id"]

        res = self.client.put(f"/api/tasks/{task_id}", json={
            "title": "Finish Sprint Report (Updated)",
            "due_date": "2026-03-12 12:00",
            "priority": "Medium",
            "status": "Not Started",
            "duration_minutes": 60,
            "effort_level": "Medium",
            "start_after": "",
            "category": "General",
            "description": "",
            "notes": ""
        })

        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/tasks")
        data = res.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Finish Sprint Report (Updated)")
        self.assertEqual(data[0]["priority"], "Medium")
        self.assertEqual(data[0]["status"], "Not Started")

    def test_delete_task(self):
        res = self.client.post("/api/tasks", json={
            "title": "Task To Delete",
            "due_date": "2026-04-01 12:00",
            "priority": "Low"
        })

        task = res.get_json()
        task_id = task["id"]

        res = self.client.delete(f"/api/tasks/{task_id}")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/tasks")
        data = res.get_json()

        self.assertEqual(len(data), 0)



'''
    User Story #4: Generate Schedule From Task Log 
'''




    #User Story #4:Generate Scheduling 
    
    def test_generate_schedule_with_no_tasks(self):
    # If your routes are protected by login_required,
    # log in first before calling the API.
    self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })

    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })

    self.assertEqual(res.status_code, 200)

    data = res.get_json()

    self.assertEqual(data["message"], "No tasks available to schedule.")
    self.assertEqual(data["schedule"], {})


   

    def test_generate_schedule_sorts_by_due_date_and_priority(self):
    # If your routes are protected by login_required,
    # log in first before calling the API.
    self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })

    now = datetime.now()

    same_due = (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    later_due = (now + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")

    # Higher priority, earlier due date
    self.client.post("/api/tasks", json={
        "title": "Task A",
        "due_date": same_due,
        "priority": "High",
        "duration_minutes": 60,
        "effort_level": "Medium",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })

    # Lower priority, same due date
    self.client.post("/api/tasks", json={
        "title": "Task B",
        "due_date": same_due,
        "priority": "Low",
        "duration_minutes": 60,
        "effort_level": "Medium",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })

    # Later due date
    self.client.post("/api/tasks", json={
        "title": "Task C",
        "due_date": later_due,
        "priority": "High",
        "duration_minutes": 60,
        "effort_level": "Medium",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })

    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 5
    })

    self.assertEqual(res.status_code, 200)

    data = res.get_json()
    schedule = data["schedule"]

    self.assertTrue(len(schedule) > 0)

    first_day = list(schedule.keys())[0]
    tasks = schedule[first_day]

    self.assertEqual(tasks[0]["title"], "Task A")
    self.assertEqual(tasks[1]["title"], "Task B")
    self.assertEqual(tasks[2]["title"], "Task C")


''' 
Unit Test for Duration based Scheduling 
'''

    def test_duration_based_scheduling(self):
        now = datetime.now()
        due_a = (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
        due_b = (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")

        self.client.post("/api/tasks", json={
            "title": "Task A",
            "due_date": due_a,
            "priority": "High",
            "duration_minutes": 30,
            "effort_level": "Medium",
            "start_after": "",
            "category": "General",
            "description": "",
            "notes": ""
        })

        self.client.post("/api/tasks", json={
            "title": "Task B",
            "due_date": due_b,
            "priority": "Medium",
            "duration_minutes": 90,
            "effort_level": "Medium",
            "start_after": "",
            "category": "General",
            "description": "",
            "notes": ""
        })

        res = self.client.post("/api/schedule", json={
            "days": 1,
            "max_tasks_per_day": 5
        })

        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        schedule = data["schedule"]

        self.assertTrue(len(schedule) > 0)

        day = list(schedule.keys())[0]
        tasks = schedule[day]

        self.assertEqual(len(tasks), 2)

        task_a = tasks[0]
        task_b = tasks[1]

        self.assertEqual(task_a["scheduled_start"], "9:00 AM")
        self.assertEqual(task_a["scheduled_end"], "9:30 AM")

        self.assertEqual(task_b["scheduled_start"], "9:30 AM")
        self.assertEqual(task_b["scheduled_end"], "11:00 AM")

        self.assertEqual(task_a["scheduled_end"], task_b["scheduled_start"])


    def login(self):
    return self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })


def time_to_minutes(self, time_str):
    time_part, meridiem = time_str.split(" ")
    hours, minutes = map(int, time_part.split(":"))

    if meridiem == "PM" and hours != 12:
        hours += 12
    if meridiem == "AM" and hours == 12:
        hours = 0

    return hours * 60 + minutes
  

  '''
  User Story #5: Conflict Detection 

  '''

def find_conflicts_in_schedule(self, schedule):
    conflicts = []

    for day_key, tasks in schedule.items():
        for i in range(len(tasks)):
            first = tasks[i]
            first_start = self.time_to_minutes(first["scheduled_start"])
            first_end = self.time_to_minutes(first["scheduled_end"])

            for j in range(i + 1, len(tasks)):
                second = tasks[j]
                second_start = self.time_to_minutes(second["scheduled_start"])
                second_end = self.time_to_minutes(second["scheduled_end"])

                overlaps = first_start < second_end and second_start < first_end

                if overlaps:
                    conflicts.append({
                        "day": day_key,
                        "first": first,
                        "second": second,
                        "suggested_next_slot": first["scheduled_end"]
                    })

    return conflicts

    def test_conflict_detection_story(self):
    """
    USER STORY: Conflict Detection

    As a user, I want conflicts detected in my schedule
    so that tasks do not overlap.
    """

    self.login()

    conflict_schedule = {
        "2026-03-25": [
            {
                "id": 1,
                "title": "Task A",
                "scheduled_start": "2:00 PM",
                "scheduled_end": "3:00 PM"
            },
            {
                "id": 2,
                "title": "Task B",
                "scheduled_start": "2:30 PM",
                "scheduled_end": "3:30 PM"
            }
        ]
    }

    conflicts = self.find_conflicts_in_schedule(conflict_schedule)

    # AC 1 + AC 2:
    # overlapping scheduled task times are detected automatically
    self.assertEqual(len(conflicts), 1)

    # AC 3:
    # suggested next available slot is shown
    self.assertEqual(conflicts[0]["suggested_next_slot"], "3:00 PM")

    # AC 4:
    # verify the two overlapping tasks are the ones identified
    self.assertEqual(conflicts[0]["first"]["title"], "Task A")
    self.assertEqual(conflicts[0]["second"]["title"], "Task B")

    def test_no_conflict_detection_story(self):
    """
    USER STORY: No Conflict Case

    Given no overlapping task times exist,
    the system should detect no conflicts.
    """

    self.login()

    no_conflict_schedule = {
        "2026-03-25": [
            {
                "id": 1,
                "title": "Task A",
                "scheduled_start": "2:00 PM",
                "scheduled_end": "3:00 PM"
            },
            {
                "id": 2,
                "title": "Task B",
                "scheduled_start": "3:00 PM",
                "scheduled_end": "4:00 PM"
            }
        ]
    }

    conflicts = self.find_conflicts_in_schedule(no_conflict_schedule)

    # AC 5:
    # no overlap means no conflict detected
    self.assertEqual(len(conflicts), 0)



'''

User Story #58 -- Schedule Auto Refresh


'''




    def login(self):
    return self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })


def test_schedule_reflects_latest_task_changes(self):
    """
    USER STORY: Schedule Auto Refresh

    As a user, I want the schedule to refresh automatically
    after task changes so that it always displays current information.

    This test verifies the backend side of that story:
    - schedule includes newly created task
    - schedule reflects edited task data
    - schedule removes deleted task
    - schedule returns empty state when no tasks exist
    """

    # Login first if routes are protected
    self.login()

    now = datetime.now()
    due_date = (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")

    # -----------------------------------
    # 1. Empty state
    # -----------------------------------
    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })

    self.assertEqual(res.status_code, 200)
    data = res.get_json()
    self.assertEqual(data["message"], "No tasks available to schedule.")
    self.assertEqual(data["schedule"], {})

    # -----------------------------------
    # 2. Create task -> schedule should include it
    # -----------------------------------
    create_res = self.client.post("/api/tasks", json={
        "title": "Task A",
        "due_date": due_date,
        "priority": "High",
        "duration_minutes": 60,
        "effort_level": "Medium",
        "start_after": "",
        "category": "General",
        "description": "Original description",
        "notes": "Original notes"
    })

    self.assertEqual(create_res.status_code, 201)
    created_task = create_res.get_json()
    task_id = created_task["id"]

    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })

    self.assertEqual(res.status_code, 200)
    data = res.get_json()
    schedule = data["schedule"]

    self.assertTrue(len(schedule) > 0)

    all_titles = []
    for day_tasks in schedule.values():
        for task in day_tasks:
            all_titles.append(task["title"])

    self.assertIn("Task A", all_titles)

    # -----------------------------------
    # 3. Edit task -> schedule should show updated info
    # -----------------------------------
    edit_res = self.client.put(f"/api/tasks/{task_id}", json={
        "title": "Task A Updated",
        "due_date": due_date,
        "priority": "Medium",
        "status": "Not Started",
        "duration_minutes": 90,
        "effort_level": "High",
        "start_after": "",
        "category": "School",
        "description": "Updated description",
        "notes": "Updated notes"
    })

    self.assertEqual(edit_res.status_code, 200)

    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })

    self.assertEqual(res.status_code, 200)
    data = res.get_json()
    schedule = data["schedule"]

    found_updated_task = None
    for day_tasks in schedule.values():
        for task in day_tasks:
            if task["title"] == "Task A Updated":
                found_updated_task = task
                break
        if found_updated_task:
            break

    self.assertIsNotNone(found_updated_task)
    self.assertEqual(found_updated_task["priority"], "Medium")
    self.assertEqual(found_updated_task["duration_minutes"], 90)
    self.assertEqual(found_updated_task["effort_level"], "High")
    self.assertEqual(found_updated_task["category"], "School")
    self.assertEqual(found_updated_task["description"], "Updated description")
    self.assertEqual(found_updated_task["notes"], "Updated notes")

    # -----------------------------------
    # 4. Delete task -> schedule should no longer include it
    # -----------------------------------
    delete_res = self.client.delete(f"/api/tasks/{task_id}")
    self.assertEqual(delete_res.status_code, 200)

    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 4
    })

    self.assertEqual(res.status_code, 200)
    data = res.get_json()

    self.assertEqual(data["message"], "No tasks available to schedule.")
    self.assertEqual(data["schedule"], {})

    




    def test_task_duration_scheduling_story(self):
    """
    USER STORY: Task Duration Scheduling

    As a user, I want tasks to be scheduled based on their duration
    so that longer tasks reserve the correct amount of time in my schedule.
    """

    # Log in first if routes are protected
    self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })

    now = datetime.now()
    due_a = (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
    due_b = (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")

    # Task A = 30 minutes
    res_a = self.client.post("/api/tasks", json={
        "title": "Task A",
        "due_date": due_a,
        "priority": "High",
        "duration_minutes": 30,
        "effort_level": "Medium",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })
    self.assertEqual(res_a.status_code, 201)

    # Task B = 90 minutes
    res_b = self.client.post("/api/tasks", json={
        "title": "Task B",
        "due_date": due_b,
        "priority": "Medium",
        "duration_minutes": 90,
        "effort_level": "Medium",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })
    self.assertEqual(res_b.status_code, 201)

    # Generate schedule
    res = self.client.post("/api/schedule", json={
        "days": 1,
        "max_tasks_per_day": 5
    })
    self.assertEqual(res.status_code, 200)

    data = res.get_json()
    schedule = data["schedule"]

    # Make sure schedule exists
    self.assertTrue(len(schedule) > 0)

    # Get first scheduled day
    day = list(schedule.keys())[0]
    tasks = schedule[day]

    # Should have both tasks
    self.assertEqual(len(tasks), 2)

    task_a = tasks[0]
    task_b = tasks[1]

    # AC 1: duration field affects schedule
    self.assertEqual(task_a["duration_minutes"], 30)
    self.assertEqual(task_b["duration_minutes"], 90)

    # AC 2: 90-minute task gets full 90-minute range
    self.assertEqual(task_a["scheduled_start"], "9:00 AM")
    self.assertEqual(task_a["scheduled_end"], "9:30 AM")

    self.assertEqual(task_b["scheduled_start"], "9:30 AM")
    self.assertEqual(task_b["scheduled_end"], "11:00 AM")

    # AC 3 + AC 5: tasks are sequential and do not overlap
    self.assertEqual(task_a["scheduled_end"], task_b["scheduled_start"])

    # AC 4: longer task gets longer block than shorter task
    def to_minutes(time_str):
        time_part, meridiem = time_str.split(" ")
        hours, minutes = map(int, time_part.split(":"))
        if meridiem == "PM" and hours != 12:
            hours += 12
        if meridiem == "AM" and hours == 12:
            hours = 0
        return hours * 60 + minutes

    task_a_length = to_minutes(task_a["scheduled_end"]) - to_minutes(task_a["scheduled_start"])
    task_b_length = to_minutes(task_b["scheduled_end"]) - to_minutes(task_b["scheduled_start"])

    self.assertEqual(task_a_length, 30)
    self.assertEqual(task_b_length, 90)
    self.assertGreater(task_b_length, task_a_length)



    def test_effort_level_scheduling_story(self):
    """
    USER STORY: Effort Level Scheduling

    As a user, I want tasks with higher effort levels
    to be prioritized when generating a schedule so that
    more demanding tasks are handled earlier.
    """

    # Login first if routes are protected
    self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })

    now = datetime.now()
    same_due = (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")

    # Task A: High effort
    res_a = self.client.post("/api/tasks", json={
        "title": "Task A",
        "due_date": same_due,
        "priority": "Medium",
        "duration_minutes": 60,
        "effort_level": "High",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })
    self.assertEqual(res_a.status_code, 201)

    # Task B: Low effort
    res_b = self.client.post("/api/tasks", json={
        "title": "Task B",
        "due_date": same_due,
        "priority": "Medium",
        "duration_minutes": 60,
        "effort_level": "Low",
        "start_after": "",
        "category": "General",
        "description": "",
        "notes": ""
    })
    self.assertEqual(res_b.status_code, 201)

    # Generate schedule
    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 5
    })
    self.assertEqual(res.status_code, 200)

    data = res.get_json()
    schedule = data["schedule"]

    self.assertTrue(len(schedule) > 0)

    # Flatten all scheduled tasks in order
    scheduled_tasks = []
    for day_tasks in schedule.values():
        scheduled_tasks.extend(day_tasks)

    self.assertEqual(len(scheduled_tasks), 2)

    # AC 1 + AC 2:
    # Same due date + same priority -> higher effort first
    self.assertEqual(scheduled_tasks[0]["title"], "Task A")
    self.assertEqual(scheduled_tasks[0]["effort_level"], "High")
    self.assertEqual(scheduled_tasks[1]["title"], "Task B")
    self.assertEqual(scheduled_tasks[1]["effort_level"], "Low")

    def test_daily_task_limit_with_fewer_tasks_than_limit(self):
    self.client.post("/api/login", json={
        "username": "admin",
        "password": "momentum123"
    })

    now = datetime.now()

    for i in range(2):
        due_date = (now + timedelta(days=1, hours=i)).strftime("%Y-%m-%d %H:%M")

        res = self.client.post("/api/tasks", json={
            "title": f"Small Task {i + 1}",
            "due_date": due_date,
            "priority": "Medium",
            "duration_minutes": 60,
            "effort_level": "Medium",
            "start_after": "",
            "category": "General",
            "description": "",
            "notes": ""
        })

        self.assertEqual(res.status_code, 201)

    res = self.client.post("/api/schedule", json={
        "days": 7,
        "max_tasks_per_day": 3
    })

    self.assertEqual(res.status_code, 200)

    data = res.get_json()
    schedule = data["schedule"]

    day_keys = sorted(schedule.keys())
    self.assertEqual(len(schedule[day_keys[0]]), 2)

    for day_key, tasks in schedule.items():
        self.assertLessEqual(len(tasks), 3)
 


if __name__ == "__main__":
    unittest.main()