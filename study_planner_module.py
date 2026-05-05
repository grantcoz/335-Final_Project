import tkinter as tk
from tkinter import ttk, messagebox

class Task:
    def __init__(self, name, time, value):
        # raises value errors for invalid time/value input
        if time <= 0:
            raise ValueError("The study planner time inputted must be a positive. Please try again.")
        if value <= 0:
            raise ValueError("The study planner value inputted must be positive. Please try again.")

        self.name = name   # name of task
        self.time = time   # length of time for task
        self.value = value # level of importance of task

    def ratio(self):
        """This method for the greedy scheduler prioritizes the
        task that provides the most value per unit of time"""
        return self.value / self.time

    def __repr__(self):
        """This function formats
        the printed schedule info
        even without the gui"""
        return f"Task(name = '{self.name}', time = {self.time}, value = {self.value})"


class StudyPlannerFrame(ttk.Frame):
    """Tkinter frame for the study planner module."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, padding=10)
        self._tasks = []
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(7, weight=1)

        header = ttk.Label(
            self,
            text="Study Planner",
            font=("Segoe UI", 16, "bold"),
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 10))

        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.columnconfigure(3, weight=1)
        entry_frame.columnconfigure(5, weight=1)

        ttk.Label(entry_frame, text="Task name:").grid(row=0, column=0, sticky="w")
        self._name_entry = ttk.Entry(entry_frame)
        self._name_entry.grid(row=0, column=1, sticky="ew", padx=(4, 12))

        ttk.Label(entry_frame, text="Time:").grid(row=0, column=2, sticky="w")
        self._time_entry = ttk.Entry(entry_frame)
        self._time_entry.grid(row=0, column=3, sticky="ew", padx=(4, 12))

        ttk.Label(entry_frame, text="Value:").grid(row=0, column=4, sticky="w")
        self._value_entry = ttk.Entry(entry_frame)
        self._value_entry.grid(row=0, column=5, sticky="ew", padx=(4, 0))

        ttk.Button(self, text="Add Task", command=self._on_add_task).grid(
            row=2, column=0, sticky="w", pady=(0, 10)
        )

        list_frame = ttk.Frame(self)
        list_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)

        self._task_tree = ttk.Treeview(
            list_frame,
            columns=("name", "time", "value"),
            show="headings",
            height=6,
        )
        self._task_tree.heading("name", text="Task")
        self._task_tree.heading("time", text="Time")
        self._task_tree.heading("value", text="Value")
        self._task_tree.column("name", width=240, anchor="w")
        self._task_tree.column("time", width=80, anchor="center")
        self._task_tree.column("value", width=80, anchor="center")
        self._task_tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self._task_tree.yview,
        )
        scroll.grid(row=0, column=1, sticky="ns")
        self._task_tree.configure(yscrollcommand=scroll.set)

        controls = ttk.Frame(self)
        controls.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Available time:").grid(row=0, column=0, sticky="w")
        self._budget_entry = ttk.Entry(controls)
        self._budget_entry.grid(row=0, column=1, sticky="w", padx=(4, 12))
        self._budget_entry.insert(0, "10")

        algo_frame = ttk.LabelFrame(self, text="Algorithm")
        algo_frame.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        self._algo_choice = tk.StringVar(value="Greedy")
        for col, label in enumerate(("Greedy", "DP")):
            ttk.Radiobutton(
                algo_frame,
                text=label,
                value=label,
                variable=self._algo_choice,
            ).grid(row=0, column=col, padx=10, pady=4, sticky="w")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=6, column=0, sticky="w")
        ttk.Button(button_frame, text="Run Scheduler", command=self._on_run).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(button_frame, text="Clear Tasks", command=self._clear_tasks).grid(
            row=0, column=1, sticky="w", padx=(8, 0))

        result_frame = ttk.Frame(self)
        result_frame.grid(row=7, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self._results = tk.Text(
            result_frame,
            wrap="word",
            height=12,
            font=("Consolas", 10),
            state="disabled",
        )
        self._results.grid(row=0, column=0, sticky="nsew")

        scroll2 = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self._results.yview,
        )
        scroll2.grid(row=0, column=1, sticky="ns")
        self._results.configure(yscrollcommand=scroll2.set)

        self._write_results(
            "Add tasks, choose an algorithm, and click Run Scheduler."
        )

    def _on_add_task(self) -> None:
        name = self._name_entry.get().strip()
        time_text = self._time_entry.get().strip()
        value_text = self._value_entry.get().strip()

        if not name:
            messagebox.showerror("Invalid task", "Task name cannot be empty.")
            return

        try:
            time_val = int(time_text)
            value_val = int(value_text)
            task = Task(name, time_val, value_val)
        except ValueError as exc:
            messagebox.showerror("Invalid task", str(exc))
            return

        self._tasks.append(task)
        self._task_tree.insert("", "end", values=(task.name, task.time, task.value))
        self._name_entry.delete(0, tk.END)
        self._time_entry.delete(0, tk.END)
        self._value_entry.delete(0, tk.END)
        self._write_results(f"Added task: {task}")

    def _on_run(self) -> None:
        if not self._tasks:
            messagebox.showinfo("No tasks", "Please add at least one task.")
            return

        time_budget_text = self._budget_entry.get().strip()
        try:
            time_budget = int(time_budget_text)
            if time_budget <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid available time",
                "Enter a positive integer for available time.",
            )
            return

        algorithm = self._algo_choice.get()
        if algorithm == "Greedy":
            result = greedy_scheduler(self._tasks, time_budget)
        else:
            result = dp_optimal_scheduler(self._tasks, time_budget)

        chosen = result["chosen_tasks"]
        lines = [
            f"Algorithm: {algorithm}",
            f"Available time: {time_budget}",
            f"Total chosen tasks: {len(chosen)}",
            f"Total time used: {result['total_time']}",
            f"Total value: {result['total_value']}",
            "",
            "Chosen tasks:",
        ]
        if chosen:
            for task in chosen:
                lines.append(f"  - {task.name} (time={task.time}, value={task.value})")
        else:
            lines.append("  No tasks could fit within the available time.")

        self._write_results("\n".join(lines))

    def _clear_tasks(self) -> None:
        self._tasks.clear()
        for item in self._task_tree.get_children():
            self._task_tree.delete(item)
        self._write_results("Task list cleared.")

    def _write_results(self, text: str) -> None:
        self._results.configure(state="normal")
        self._results.delete("1.0", tk.END)
        self._results.insert(tk.END, text)
        self._results.configure(state="disabled")


def greedy_scheduler(tasks, time_available):
    """This function serves as
    the greedy scheduler logic"""

    # raises value error for invalid time input
    if time_available <= 0:
        raise ValueError("The available time inputted must be positive. Please try again.")

    # sorted function returns new sorted list, does not modify original list
    sorted_tasks = sorted(
        tasks,                         # tasks needed, to sort
        key=lambda task: task.ratio(), # takes task as input then returns tasks's ratio
        reverse = True                 # sorts from largest to smallest ratio
    )

    # tracks greedy scheduling process results then stores them in an empty list
    chosen_tasks = []
    total_time = 0    # starting total task time = 0 since no tasks have been selected
    total_value = 0   # starting total task value = 0 since no tasks have been selected

    # chooses tasks based on available time left without initial consideration of all tasks;
    # the greedy part of the greedy scheduler, making it fast but not optimal
    for task in sorted_tasks:
        if total_time + task.time <= time_available: # confirms the added task stays within available time
            chosen_tasks.append(task)                # adds tasks to list
            total_time += task.time                  # increases total time with each added task
            total_value += task.value                # increases total value with each added task

    # returns tasks chosen by greedy algo, and time/value totals
    return {
        "chosen_tasks": chosen_tasks,
        "total_time": total_time,
        "total_value": total_value
    }

def dp_optimal_scheduler(tasks, time_available):
    """This function serves as the
    dp optimal scheduler logic"""

    if time_available <= 0:
        raise ValueError("The available time inputted must be positive. Please try again.")
    
    num_of_tasks = len(tasks) # stores number of tasks

    # creates the dynamic programming table/matrix
    dynapro = [[0 for _ in range(time_available + 1)] # table's starting time and value is 0
                for _ in range (num_of_tasks + 1)]

    # considers each task one at a time starting at i = task 1, index 0, in the dp table
    for i in range(1, num_of_tasks + 1):
        time_of_task = tasks[i - 1].time   # retrieves current task time
        value_of_task = tasks[i - 1].value # retrieves current task value

        # checks available time amount from 0 to full available time
        for current_time in range(time_available + 1):
            if time_of_task <= current_time: # confirms if current task fits in current time capacity

                include_task = value_of_task + dynapro[i - 1][current_time - time_of_task] # looks at best value before current task, and includes it if current is better
                exclude_task = dynapro[i - 1][current_time]                                # looks at best value before current task, and excludes it if current is worse

                dynapro[i][current_time] = max(include_task, exclude_task) # stores the better task value from previous calculation in dp table
            else:
                dynapro[i][current_time] = dynapro[i - 1][current_time]    # if task doesn't fit current time capacity it proceeds with best value from row above

    chosen_tasks = []
    time_remaining = time_available

    # checks value of tasks going backwards to check if each task changed optimal value
    for i in range(num_of_tasks, 0, -1):
        if dynapro[i][time_remaining] != dynapro[i - 1][time_remaining]: # traces back which task created best value
            chosen_task = tasks[i - 1]                                   # retrieves task object of from original list
            chosen_tasks.append(chosen_task)                             # adds chosen task to final list
            time_remaining -= chosen_task.time                           # chosen tasks's time is subtracted from time remaining

    chosen_tasks.reverse() # counteracts backwards traceback

    total_time = sum(task.time for task in chosen_tasks)   # adds time of all chosen tasks for clean output
    total_value = sum(task.value for task in chosen_tasks) # adds value of all chosen tasks for clean output

    # returns tasks chosen by dp algo, and time/value totals
    return {
        "chosen_tasks": chosen_tasks,
        "total_time": total_time,
        "total_value": total_value
    }