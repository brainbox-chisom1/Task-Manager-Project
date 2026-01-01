const taskInput = document.getElementById("taskInput");
    const addBtn = document.getElementById("addBtn");
    const taskList = document.getElementById("taskList");
    const progressText = document.getElementById("progressText");
    const clearCompleted = document.getElementById("clearCompleted");

    function updateProgress() {
      const tasks = document.querySelectorAll(".task");
      const completed = document.querySelectorAll(".task.completed");
      progressText.textContent = `${completed.length}/${tasks.length} Completed`;
    }

    function toggleComplete(taskElement, checkbox) {
      taskElement.classList.toggle("completed", checkbox.checked);
      updateProgress();
    }

    function addTask(text) {
      if (!text.trim()) return;
      const date = new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
      const task = document.createElement("div");
      task.classList.add("task");
      task.innerHTML = `
        <div class="d-flex align-items-center gap-2">
          <input class="form-check-input" type="checkbox">
          <span>${text}</span>
        </div>
        <small>${date}</small>
        <div>
          <i class="fa-solid fa-pen mx-2 text-secondary"></i>
          <i class="fa-solid fa-trash text-danger"></i>
        </div>
      `;

      const checkbox = task.querySelector("input");
      const trash = task.querySelector(".fa-trash");

      checkbox.addEventListener("change", () => toggleComplete(task, checkbox));
      trash.addEventListener("click", () => {
        task.remove();
        updateProgress();
      });

      taskList.prepend(task);
      taskInput.value = "";
      updateProgress();
    }

    addBtn.addEventListener("click", () => addTask(taskInput.value));
    taskInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") addTask(taskInput.value);
    });

    clearCompleted.addEventListener("click", (e) => {
      e.preventDefault();
      document.querySelectorAll(".task.completed").forEach(task => task.remove());
      updateProgress();
    });

    // Initialize progress on load
    document.querySelectorAll(".task input").forEach(checkbox => {
      checkbox.addEventListener("change", (e) => toggleComplete(e.target.closest(".task"), e.target));
    });
    updateProgress();