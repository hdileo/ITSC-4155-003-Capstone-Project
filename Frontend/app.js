const form = document.getElementById("taskForm");
const msg = document.getElementById("message");
const tbody = document.getElementById("taskTableBody");
const sortSelect = document.getElementById("sortSelect");

// Edit form elements
const editSection = document.getElementById("editTaskSection");
const editForm = document.getElementById("editTaskForm");
const editTaskId = document.getElementById("editTaskId");
const editTitle = document.getElementById("editTitle");
const editDueDate = document.getElementById("editDueDate");
const editPriority = document.getElementById("editPriority");
const editStatus = document.getElementById("editStatus");
const editMessage = document.getElementById("editMessage");
const editDueDateMsg = document.getElementById("editDueDateMsg");
const cancelEditBtn = document.getElementById("cancelEditBtn");
const editDurationMinutes = document.getElementById("editDurationMinutes");
const editEffortLevel = document.getElementById("editEffortLevel");
const editStartAfter = document.getElementById("editStartAfter");
const editCategory = document.getElementById("editCategory");

// Store original task values so we can compare after edit
let originalTaskData = null;

// ---------- Helpers ----------
function formatForBackend(datetimeLocalValue) {
  return datetimeLocalValue.includes("T")
    ? datetimeLocalValue.replace("T", " ")
    : datetimeLocalValue;
}

function parseDateInput(value) {
  if (!value) return null;

  if (value.includes("T")) {
    const [datePart, timePart] = value.split("T");
    const [y, m, d] = datePart.split("-").map(Number);
    const [h = 0, min = 0] = (timePart || "").split(":").map(Number);
    return new Date(y, m - 1, d, h, min);
  }

  return new Date(value);
}

function validateFutureDate(inputValue, inlineMsgEl) {
  inlineMsgEl.textContent = "";

  if (!inputValue) {
    inlineMsgEl.textContent = "Required";
    return false;
  }

  const dateObj = parseDateInput(inputValue);
  if (!dateObj || isNaN(dateObj.getTime())) {
    inlineMsgEl.textContent = "Invalid date";
    return false;
  }

  const now = new Date();
  if (dateObj <= now) {
    inlineMsgEl.textContent = "Due date must be in the future.";
    return false;
  }

  return true;
}

function clearCreateMessageAfterDelay() {
  setTimeout(() => {
    msg.textContent = "";
    msg.className = "message";
  }, 5000);
}

function clearEditMessageAfterDelay() {
  setTimeout(() => {
    editMessage.textContent = "";
    editMessage.className = "message";
  }, 5000);
}

// ---------- Fetch + Render ----------
async function fetchTasks() {
  if (!tbody || !sortSelect) return;
  try {
    const sort = sortSelect.value;
    const url = sort ? `/api/tasks?sort=${encodeURIComponent(sort)}` : "/api/tasks";

    const res = await fetch(url);
    const tasks = await res.json();

    if (!res.ok) {
      throw new Error(tasks.error || "Failed to load tasks.");
    }

    renderTasks(tasks);
  } catch (err) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5">Failed to load tasks.</td>
      </tr>
    `;
    console.error(err);
  }
}

function renderTasks(tasks) {
  tbody.innerHTML = "";

  if (!tasks.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5">No tasks found.</td>
      </tr>
    `;
    return;
  }

  tasks.forEach((task) => {
    const row = document.createElement("tr");
    row.dataset.taskId = task.id;

    let statusClass = "status-pending";
if (task.status === "In Progress") statusClass = "status-progress";
if (task.status === "Completed") statusClass = "status-completed";

let priorityClass = "priority-low";
if (task.priority === "High") priorityClass = "priority-high";
if (task.priority === "Medium") priorityClass = "priority-medium";

const formattedStartAfter = task.start_after
  ? task.start_after
  : "No restriction";

row.innerHTML = `
  <td>
    <div class="task-title-cell">
      <div class="task-main-title">${task.title}</div>
      <div class="task-meta">
        <span class="task-meta-pill">${task.category}</span>
        <span class="task-meta-pill">${task.duration_minutes} min</span>
        <span class="task-meta-pill">${task.effort_level} Effort</span>
        <span class="task-meta-pill">Start: ${formattedStartAfter}</span>
      </div>
    </div>
  </td>
  <td><span class="status-badge ${statusClass}">${task.status}</span></td>
  <td>${task.due_date}</td>
  <td><span class="priority-pill ${priorityClass}">${task.priority}</span></td>
  <td>
    <button type="button" class="edit-btn">Edit</button>
    <button type="button" class="delete-btn">Delete</button>
  </td>
`;

    row.querySelector(".edit-btn").addEventListener("click", () => {
      openEditForm(task);
    });

    row.querySelector(".delete-btn").addEventListener("click", () => {
      handleDeleteTask(task.id, task.title);
    });

    tbody.appendChild(row);
  });
}

// Highlight only the fields that changed after edit
function highlightUpdatedFields(id, updatedTask) {
  const row = document.querySelector(`tr[data-task-id="${id}"]`);
  if (!row || !originalTaskData) return;

  const cells = row.children;

  if (updatedTask.title !== originalTaskData.title) {
    cells[0].classList.add("updated-field");
  }

  if (updatedTask.status !== originalTaskData.status) {
    cells[1].classList.add("updated-field");
  }

  if (updatedTask.due_date !== originalTaskData.due_date) {
    cells[2].classList.add("updated-field");
  }

  if (updatedTask.priority !== originalTaskData.priority) {
    cells[3].classList.add("updated-field");
  }

  if (
    updatedTask.duration_minutes !== originalTaskData.duration_minutes ||
    updatedTask.effort_level !== originalTaskData.effort_level ||
    updatedTask.start_after !== originalTaskData.start_after ||
    updatedTask.category !== originalTaskData.category
  ) {
    cells[0].classList.add("updated-field");
  }

  row.classList.add("updated-row");

  setTimeout(() => {
    row.classList.remove("updated-row");
    Array.from(cells).forEach(cell => cell.classList.remove("updated-field"));
  }, 2500);
}

// ---------- Create Task ----------
if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    msg.textContent = "";
    msg.className = "message";

    const title = document.getElementById("title").value.trim();
    const dueInput = document.getElementById("dueDate").value.trim();
    const priority = document.getElementById("priority").value;
    const durationMinutes = document.getElementById("durationMinutes").value;
    const effortLevel = document.getElementById("effortLevel").value;
    const startAfterInput = document.getElementById("startAfter").value.trim();
    const category = document.getElementById("category").value;
    const dueDateMsg = document.getElementById("dueDateMsg");

    dueDateMsg.textContent = "";

    if (!validateFutureDate(dueInput, dueDateMsg)) {
      return;
    }

    const due_date = formatForBackend(dueInput);
    const start_after = startAfterInput ? formatForBackend(startAfterInput) : null;

    if (!title || !due_date) {
      msg.textContent = "Title and due date are required.";
      msg.className = "message error";
      return;
    }

    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          due_date,
          priority,
          duration_minutes: Number(durationMinutes),
          effort_level: effortLevel,
          start_after,
          category
        })
      });

      const data = await res.json();

      if (!res.ok) {
        msg.textContent = data.error || "Failed to create task.";
        msg.className = "message error";
        return;
      }

      form.reset();
      dueDateMsg.textContent = "";
      msg.textContent = "✓ Task created successfully!";
      msg.className = "message success";

      await fetchTasks();
      clearCreateMessageAfterDelay();
    } catch (err) {
      msg.textContent = "Failed to create task.";
      msg.className = "message error";
      console.error(err);
    }
  });
}

// ---------- Edit Task ----------
function openEditForm(task) {
  editSection.style.display = "block";

  editTaskId.value = task.id;
  editTitle.value = task.title;
  editDueDate.value = task.due_date.replace(" ", "T");
  editPriority.value = task.priority;
  editStatus.value = task.status;
  editDurationMinutes.value = task.duration_minutes ?? 60;
  editEffortLevel.value = task.effort_level ?? "Medium";
  editStartAfter.value = task.start_after ? task.start_after.replace(" ", "T") : "";
  editCategory.value = task.category ?? "General";

  originalTaskData = { ...task };

  editMessage.textContent = "";
  editMessage.className = "message";
  editDueDateMsg.textContent = "";

  editSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function closeEditForm() {
  editSection.style.display = "none";
  editForm.reset();
  editTaskId.value = "";
  editMessage.textContent = "";
  editMessage.className = "message";
  editDueDateMsg.textContent = "";
  originalTaskData = null;
}

async function handleDeleteTask(taskId, taskTitle) {
  const confirmed = window.confirm(`Are you sure you want to delete "${taskTitle}"?`);

  if (!confirmed) {
    return;
  }

  try {
    const res = await fetch(`/api/tasks/${taskId}`, {
      method: "DELETE"
    });

    const data = await res.json();

    if (!res.ok) {
      msg.textContent = data.error || "Task could not be deleted.";
      msg.className = "message error";
      clearCreateMessageAfterDelay();
      return;
    }

    msg.textContent = "Task deleted successfully.";
    msg.className = "message success";

    await fetchTasks();
    clearCreateMessageAfterDelay();
  } catch (err) {
    msg.textContent = "Task could not be deleted.";
    msg.className = "message error";
    console.error(err);
    clearCreateMessageAfterDelay();
  }
}

if (editForm) {
  editForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    editMessage.textContent = "";
    editMessage.className = "message";
    editDueDateMsg.textContent = "";

    const id = editTaskId.value;
    const title = editTitle.value.trim();
    const dueInput = editDueDate.value.trim();
    const priority = editPriority.value;
    const status = editStatus.value;
    const durationMinutes = editDurationMinutes.value;
    const effortLevel = editEffortLevel.value;
    const startAfterInput = editStartAfter.value.trim();
    const category = editCategory.value;

    if (!title) {
      editMessage.textContent = "Title is required.";
      editMessage.className = "message error";
      return;
    }

    if (!validateFutureDate(dueInput, editDueDateMsg)) {
      return;
    }

    const due_date = formatForBackend(dueInput);
    const start_after = startAfterInput ? formatForBackend(startAfterInput) : null;

    try {
      const res = await fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          due_date,
          priority,
          status,
          duration_minutes: Number(durationMinutes),
          effort_level: effortLevel,
          start_after,
          category
        })
      });

      const data = await res.json();

      if (!res.ok) {
        editMessage.textContent = data.error || "Task update failed.";
        editMessage.className = "message error";
        return;
      }

      editMessage.textContent = "✓ Task updated successfully!";
      editMessage.className = "message success";

      const updatedTask = {
        id: Number(id),
        title,
        due_date,
        priority,
        status,
        duration_minutes: Number(durationMinutes),
        effort_level: effortLevel,
        start_after,
        category
      };

      await fetchTasks();
      highlightUpdatedFields(id, updatedTask);
      clearEditMessageAfterDelay();

      setTimeout(() => {
        closeEditForm();
      }, 800);
    } catch (err) {
      editMessage.textContent = "Task update failed.";
      editMessage.className = "message error";
      console.error(err);
    }
  });
}

if (cancelEditBtn) {
  cancelEditBtn.addEventListener("click", closeEditForm);
}

// ---------- Sorting ----------
if (sortSelect) {
  sortSelect.addEventListener("change", fetchTasks);
}

// ---------- Schedule Generation ----------
const generateScheduleBtn = document.getElementById("generateScheduleBtn");
const scheduleMessage = document.getElementById("scheduleMessage");
const scheduleOutput = document.getElementById("scheduleOutput");
const scheduleRange = document.getElementById("scheduleRange");
const maxTasksPerDay = document.getElementById("maxTasksPerDay");

function renderSchedule(schedule) {
  if (!scheduleOutput) return;

  const selectedDays = scheduleRange ? Number(scheduleRange.value) : 7;
  const today = new Date();
  const todayString = today.toISOString().split("T")[0];

  scheduleOutput.innerHTML = '<div class="schedule-grid"></div>';
  const grid = scheduleOutput.querySelector(".schedule-grid");

  let hasAnyTasks = false;

  for (let i = 0; i < selectedDays; i++) {
    const currentDate = new Date();
    currentDate.setDate(today.getDate() + i);

    const dayKey = currentDate.toISOString().split("T")[0];
    const tasksForDay = schedule[dayKey] || [];

    const dayCard = document.createElement("div");
    dayCard.className = "schedule-day";

    if (dayKey === todayString) {
      dayCard.classList.add("today");
    }

    const heading = document.createElement("h3");
    heading.innerHTML = `
      ${currentDate.toLocaleDateString(undefined, {
        weekday: "long"
      })}
      <span class="schedule-day-date">
        ${currentDate.toLocaleDateString(undefined, {
          month: "short",
          day: "numeric",
          year: "numeric"
        })}
      </span>
    `;
    dayCard.appendChild(heading);

    if (!tasksForDay.length) {
      const emptyText = document.createElement("p");
      emptyText.className = "schedule-empty";
      emptyText.textContent = "No tasks scheduled.";
      dayCard.appendChild(emptyText);
      grid.appendChild(dayCard);
      continue;
    }

    hasAnyTasks = true;

    tasksForDay.forEach((task) => {
      let statusClass = "status-pending";
      if (task.status === "In Progress") statusClass = "status-progress";
      if (task.status === "Completed") statusClass = "status-completed";
    
      let priorityClass = "priority-low";
      if (task.priority === "High") priorityClass = "priority-high";
      if (task.priority === "Medium") priorityClass = "priority-medium";
    
      const taskCard = document.createElement("div");
      taskCard.className = "schedule-task";

      

   

      taskCard.innerHTML = `
  <div class="calendar-task-time">${task.scheduled_start} – ${task.scheduled_end}</div>
  <div class="calendar-task-title">${task.title}</div>
  <div class="calendar-task-meta">
    <span class="status-badge ${statusClass}">${task.status}</span>
    <span class="priority-pill ${priorityClass}">${task.priority} Priority</span>
    <span class="task-meta-pill">${task.effort_level} Effort</span>
    <span class="task-meta-pill">${task.category}</span>
  </div>
  <div class="due-meta" style="margin-top:10px;">
    Due: ${task.due_date}
  </div>
`;

      dayCard.appendChild(taskCard);
    });

    grid.appendChild(dayCard);
  }

  if (!hasAnyTasks) {
    scheduleMessage.textContent = "No tasks available to schedule.";
    scheduleMessage.className = "message error";
  }
}

async function handleGenerateSchedule() {
  if (!scheduleMessage || !scheduleOutput) return;

  scheduleMessage.textContent = "";
  scheduleMessage.className = "message";

  const days = scheduleRange ? Number(scheduleRange.value) : 7;
  const max_tasks_per_day = maxTasksPerDay ? Number(maxTasksPerDay.value) : 4;

  try {
    const res = await fetch("/api/schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ days, max_tasks_per_day })
    });

    const data = await res.json();

    if (!res.ok) {
      scheduleMessage.textContent = data.error || "Failed to generate schedule.";
      scheduleMessage.className = "message error";
      return;
    }

    scheduleMessage.textContent = data.message || "Schedule generated successfully.";
    scheduleMessage.className = "message success";

    renderSchedule(data.schedule || {});
  } catch (err) {
    scheduleMessage.textContent = "Failed to generate schedule.";
    scheduleMessage.className = "message error";
    console.error(err);
  }
}

if (generateScheduleBtn) {
  generateScheduleBtn.addEventListener("click", handleGenerateSchedule);
}

// ---------- Dashboard ----------
const totalTasksEl = document.getElementById("totalTasks");
const pendingTasksEl = document.getElementById("pendingTasks");
const completedTasksEl = document.getElementById("completedTasks");
const recentTasksBody = document.getElementById("recentTasksBody");

async function loadDashboard() {
  if (!totalTasksEl || !pendingTasksEl || !completedTasksEl || !recentTasksBody) return;

  try {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();

    if (!res.ok) {
      throw new Error(tasks.error || "Failed to load dashboard data.");
    }

    totalTasksEl.textContent = tasks.length;
    pendingTasksEl.textContent = tasks.filter(t => t.status !== "Completed").length;
    completedTasksEl.textContent = tasks.filter(t => t.status === "Completed").length;

    recentTasksBody.innerHTML = "";

    if (!tasks.length) {
      recentTasksBody.innerHTML = `
        <tr>
          <td colspan="4">No tasks available.</td>
        </tr>
      `;
      return;
    }

    const recentTasks = tasks.slice(0, 5);

    recentTasks.forEach((task) => {
      let statusClass = "status-pending";
      if (task.status === "In Progress") statusClass = "status-progress";
      if (task.status === "Completed") statusClass = "status-completed";

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${task.title}</td>
        <td><span class="status-badge ${statusClass}">${task.status}</span></td>
        <td>${task.due_date}</td>
        <td>${task.priority}</td>
      `;
      recentTasksBody.appendChild(row);
    });
  } catch (err) {
    console.error(err);
    recentTasksBody.innerHTML = `
      <tr>
        <td colspan="4">Failed to load dashboard data.</td>
      </tr>
    `;
  }
}



// ---------- Initial load ----------
if (tbody && sortSelect) {
  fetchTasks();
}

loadDashboard();