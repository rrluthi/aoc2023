from heapq import heappush, heappop
import itertools


class PriorityQ:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = "<removed-task>"
        self.counter = itertools.count()

    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            if self.entry_finder[task][0] < priority:
                # Only update if the current found priority is lower
                return
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, priority
        raise KeyError("Empty pq")
