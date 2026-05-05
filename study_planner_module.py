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