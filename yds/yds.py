#pylint: disable=I0011,R0903

"""Calculate a scheduling with the offline YDS-Algorithm

See: https://en.wikipedia.org/wiki/YDS_algorithm
"""

class Task:
    """A Task

    Args:
      nr (any): An identifier for this task
      release (real): The task's release time
      dead (real): The task's deadline
      c (real): The task's workload
    """
    def __init__(self, nr, release, dead, c):
        self.nr = nr
        self.release = release
        self.dead = dead
        self.c = c
        self.offset = 0.0
    def __repr__(self):
        return (str(self.nr) + ": " + str(self.release) + " - "
                "" + str(self.dead) + ", c=" + str(self.c))

    def cut(self, start, end):
        """Cut task according to interval"""
        distance = end - start

        # task after interval
        if self.release >= end:
            self.dead -= distance
            self.release -= distance
            self.offset += distance
            return self

        # task before interval
        if self.dead <= start:
            return self

        # interval inside task
        if self.release < start and self.dead > end:
            self.dead -= distance
            return self

        # task covers beginning of interval
        if self.dead > start and self.release < start:
            self.dead = start
            return self

        # task covers ending of interval
        if self.release < end and self.dead > end:
            self.offset += distance
            self.release = start
            self.dead -= distance
            return self

        # should not happen
        raise Exception("uncatched, please file issue")


class Interval:
    """An interval

    Args:
      start (real): beginning of the interval
      end (real): ending of the interval
      tasks ([Task]): all tasks contained in this interval
    """
    def __init__(self, start, end, tasks):
        self.start = start
        self.end = end
        self.tasks = tasks
        tmp = 0.0
        for task in self.tasks:
            tmp += task.c
        self.intensity = tmp / (self.end - self.start)
    def __repr__(self):
        return str(self.start) + " - " + str(self.end) + ": " + str(self.tasks)


class Execution:
    """Planned execution time and frequency of a task

    Args:
      nr (any): An identifier for this task
      start (real): The task's beginning time in the scheduling
      end (real): The task's ending time in the scheduling
      frequency (real): CPU-factor required for this task
    """
    def __init__(self, nr, start, end, frequency):
        self.nr = nr
        self.start = start
        self.end = end
        self.frequency = frequency
    def __repr__(self):
        return (str(self.nr) + ": " + str(self.start) + " - "
                "" + str(self.end) + ", f=" + str(self.frequency))


def get_intervals(tasks):
    """Calculate all possible intervals relative to a list of tasks

    Args:
      tasks ([Task]): List of tasks

    Returns:
      List of all possible Intervals
    """
    releases = set([t.release for t in tasks])
    deads = set([t.dead for t in tasks])

    intervals = []

    for start in releases:
        for end in deads:
            if start < end:
                contained = [task for task in tasks if task.release >= start and
                                                       task.dead <= end]
                intervals.append(Interval(start, end, contained))

    # (start, end, tasks)
    return intervals


def max_intensity_interval(intervals):
    """From a list of intervals, filter the one with maximum intensity

    Args:
      intervals ([Interval]): List of Intervals

    Returns:
      The Interval with the highest intensity
    """
    return max(intervals, key=lambda interval: interval.intensity)


def calc_scheduling(tasks):
    """Run the YDS-Algorithm on a list of Tasks

    Args:
      tasks ([Task]): List of tasks

    Returns:
      A scheduling for dynamic speed scaling processors which minimizes
      the total energy consumption
    """
    scheduling = []
    # As long there are tasks left
    while len(tasks) > 0:
        # find interval with highest intensity
        intervals = get_intervals(tasks)
        max_int = max_intensity_interval(intervals)

        # sort the tasks in this interval, earliest deadline first
        to_execute = sorted(max_int.tasks, key=lambda task: task.dead)
        # calculate the length of this interval
        int_length = float(max_int.end - max_int.start)
        offset = float(max_int.start)
        # sum all calculation times of all tasks in this interval
        c_sum = float(sum([t.c for t in to_execute]))

        # for any task in this interval
        for task in to_execute:
            # calculate the duration in the scheduling
            task_length = (task.c / c_sum) * int_length
            # add the task to the scheduling
            scheduling.append(Execution(task.nr, offset + task.offset,
                offset + task.offset + task_length, max_int.intensity))
            offset += task_length
            # remove the added task from the todo-task-list
            tasks.remove(task)

        # cut remaining tasks according to the interval
        tasks = [task.cut(max_int.start, max_int.end) for task in tasks]

    # return scheduling with sorted tasks (sorted by start time in scheduling)
    return sorted(scheduling, key=lambda execute: execute.start)


def main():
    """ Some examples """
    import pprint
    pp = pprint.PrettyPrinter(indent=4, width=15)

    tasks = [
        # (id, a, d, c)
        Task(1, 3, 6, 5),
        Task(2, 2, 6, 3),
        Task(3, 0, 8, 2),
        Task(4, 6, 14, 6),
        Task(5, 10, 14, 6),
        Task(6, 11, 17, 2),
        Task(7, 12, 17, 2)
    ]

    tasks = [
        Task("t1",  0, 17,  5),
        Task("t2",  1, 11,  3),
        Task("t3", 12, 20,  4),
        Task("t4",  7, 11,  2),
        Task("t5",  1, 20,  4),
        Task("t6", 14, 20, 12),
        Task("t7", 14, 17,  4),
        Task("t8",  1,  7,  2)
    ]

    scheduling = calc_scheduling(tasks)

    print "Scheduling:"
    pp.pprint(scheduling)

if __name__ == '__main__':
    main()
