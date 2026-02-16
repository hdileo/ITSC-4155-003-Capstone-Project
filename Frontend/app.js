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
  const due_date = document.getElementById("dueDate").value.trim();
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
  await fetchTasks();
});

sortSelect.addEventListener("change", fetchTasks);

// initial load
fetchTasks();