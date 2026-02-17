const form = document.getElementById("taskForm");
const msg = document.getElementById("message");
const tbody = document.getElementById("taskTableBody");
const sortSelect = document.getElementById("sortSelect");

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
    `;
    tbody.appendChild(tr);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  msg.textContent = "";

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

  // client-side validation (simple)
  if (!title || !due_date) {
    msg.textContent = "Title and due date are required.";
    return;
  }

  const res = await fetch("/api/tasks", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ title, due_date, priority })
  });

  const data = await res.json();
  if (!res.ok) {
    msg.textContent = data.error || "Failed to create task.";
    return;
  }

  form.reset();
  msg.textContent = "Task created successfully!";
  // clear inline due date message after success
  dueDateMsg.textContent = "";
  await fetchTasks();
});

sortSelect.addEventListener("change", fetchTasks);

// initial load
fetchTasks();