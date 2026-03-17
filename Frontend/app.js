const form = document.getElementById("taskForm");
const msg = document.getElementById("message");
const tbody = document.getElementById("taskTableBody");
const sortSelect = document.getElementById("sortSelect");
const scheduleList = document.getElementById("scheduleList");
const scheduleEmptyState = document.getElementById("scheduleEmptyState");
const generateScheduleButton = document.getElementById("generateScheduleButton");

function renderSchedule(tasks) {
  scheduleList.innerHTML = "";

  if (!tasks.length) {
    scheduleList.hidden = true;
    scheduleEmptyState.hidden = false;
    return;
  }

  tasks.forEach(t => {
    const card = document.createElement("article");
    card.className = "schedule-item";
    card.innerHTML = `
      <div class="schedule-item__time">${t.display_time_range}</div>
      <div class="schedule-item__details">
        <h3>${t.title}</h3>
        <p>Due ${t.due_date}</p>
        <p>${t.duration_minutes} min · ${t.priority} priority</p>
      </div>
      <div class="schedule-item__status">${t.is_scheduled ? "Scheduled" : "Needs review"}</div>
    `;
    scheduleList.appendChild(card);
  });

  scheduleEmptyState.hidden = true;
  scheduleList.hidden = false;
}

async function fetchTasks() {
  const sort = sortSelect.value;
  const url = sort ? `/api/tasks?sort=${encodeURIComponent(sort)}` : "/api/tasks";
  const res = await fetch(url);
  const tasks = await res.json();

  tbody.innerHTML = "";
  tasks.forEach(t => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${t.title}</td>
      <td>${t.status}</td>
      <td>${t.due_date}</td>
      <td>${t.priority}</td>
      <td>${t.duration_minutes} min</td>
    `;
    tbody.appendChild(tr);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  msg.textContent = "";
  msg.className = "message";

  const title = document.getElementById("title").value.trim();
  const dueInput = document.getElementById("dueDate").value.trim();

  const dueDateMsg = document.getElementById("dueDateMsg");
  // Clear previous field message
  dueDateMsg.textContent = "";

  // Validate due date exists
  if (!dueInput) {
    dueDateMsg.textContent = "Required";
    return;
  }

  // Parse `datetime-local` (YYYY-MM-DDTHH:MM) into a Date object (local time)
  let dueDateObj;
  if (dueInput.includes("T")) {
    const [datePart, timePart] = dueInput.split("T");
    const [y, m, d] = datePart.split("-").map(Number);
    const [h = 0, min = 0] = (timePart || "").split(":").map(Number);
    dueDateObj = new Date(y, m - 1, d, h, min);
  } else {
    dueDateObj = new Date(dueInput);
  }

  if (isNaN(dueDateObj.getTime())) {
    dueDateMsg.textContent = "Invalid date";
    return;
  }

  const now = new Date();
  if (dueDateObj <= now) {
    dueDateMsg.textContent = "Due date must be in the future.";
    return;
  }

  // Format to backend-friendly string: `YYYY-MM-DD HH:MM` when coming from datetime-local
  let due_date = dueInput.includes("T") ? dueInput.replace("T", " ") : dueInput;
  const priority = document.getElementById("priority").value;
  const duration_minutes = Number.parseInt(
    document.getElementById("durationMinutes").value,
    10
  );

  // client-side validation (simple)
  if (!title || !due_date || !Number.isInteger(duration_minutes) || duration_minutes <= 0) {
    msg.textContent = "Title, due date, and duration are required.";
    msg.className = "message error";
    return;
  }

  const res = await fetch("/api/tasks", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ title, due_date, priority, duration_minutes })
  });

  const data = await res.json();
  if (!res.ok) {
    msg.textContent = data.error || "Failed to create task.";
    msg.className = "message error";
    return;
  }

  form.reset();
  msg.textContent = "✓ Task created successfully!";
  msg.className = "message success";
  // clear inline due date message after success
  dueDateMsg.textContent = "";
  await fetchTasks();
  
  // Clear message after 5 seconds
  setTimeout(() => {
    msg.textContent = "";
    msg.className = "message";
  }, 5000);
});

sortSelect.addEventListener("change", fetchTasks);
generateScheduleButton.addEventListener("click", async () => {
  const res = await fetch("/api/schedule/generate", { method: "POST" });
  const tasks = await res.json();
  renderSchedule(tasks);
});

// initial load
fetchTasks();
