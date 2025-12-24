import json
from datetime import date, timedelta
import os


class Habit:
    def __init__(self, name, completed_days=None):
        self.name = name
        self.completed_days = completed_days or []

    def mark_done_today(self):
        today = date.today().isoformat()
        if today not in self.completed_days:
            self.completed_days.append(today)

    def streak(self):
        streak = 0
        current = date.today()
        days = {date.fromisoformat(d) for d in self.completed_days}

        while current in days:
            streak += 1
            current -= timedelta(days=1)

        return streak

    def weekly_count(self):
        today = date.today()
        last_week = {today - timedelta(days=i) for i in range(7)}
        days = {date.fromisoformat(d) for d in self.completed_days}
        return len(days & last_week)

    def to_dict(self):
        return {
            "name": self.name,
            "completed_days": self.completed_days
        }

    @staticmethod
    def from_dict(data):
        return Habit(data["name"], data["completed_days"])


class Storage:
    FILE = "habits.json"

    @staticmethod
    def load():
        if not os.path.exists(Storage.FILE):
            return []

        with open(Storage.FILE, "r") as f:
            data = json.load(f)
            return [Habit.from_dict(h) for h in data]

    @staticmethod
    def save(habits):
        with open(Storage.FILE, "w") as f:
            json.dump([h.to_dict() for h in habits], f, indent=4)


class HabitTracker:
    def __init__(self):
        self.habits = Storage.load()

    def get_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                return habit
        return None

    def add_habit(self, name):
        if self.get_habit(name):
            print("Habit already exists.")
            return
        self.habits.append(Habit(name))
        Storage.save(self.habits)
        print("Habit added.")

    def delete_habit(self, name):
        habit = self.get_habit(name)
        if not habit:
            print("Habit not found.")
            return
        self.habits.remove(habit)
        Storage.save(self.habits)
        print("Habit deleted.")

    def mark_done(self, name):
        habit = self.get_habit(name)
        if not habit:
            print("Habit not found.")
            return
        habit.mark_done_today()
        Storage.save(self.habits)
        print("Marked as done today.")

    def show_report(self):
        if not self.habits:
            print("No habits found.")
            return

        print("\nHabit Report:")
        for habit in self.habits:
            print(
                f"- {habit.name} | "
                f"Streak: {habit.streak()} days | "
                f"Last 7 days: {habit.weekly_count()} times"
            )


def main():
    tracker = HabitTracker()

    while True:
        print("\n--- Habit Tracker ---")
        print("1. Add habit")
        print("2. Mark habit as done today")
        print("3. Delete habit")
        print("4. Show report")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Habit name: ").strip()
            tracker.add_habit(name)
        elif choice == "2":
            name = input("Habit name: ").strip()
            tracker.mark_done(name)
        elif choice == "3":
            name = input("Habit name: ").strip()
            tracker.delete_habit(name)
        elif choice == "4":
            tracker.show_report()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
