"""Log-Items main module"""
import datetime
#import pickle
import sys
from time import sleep
from models.log_items import LogItem

LOG_ITEMS: list[LogItem] = []

# def load_existing() -> bool:
#     """Load the existing log items.
#     TODO: Check if the file exists and can be read
#     TODO: Check if the unpickling did not succeed"""
#     with open("log-items.db", "rb") as f:
#         LOG_ITEMS = pickle.loads(f)
#         return True
#     return False


def test_list() -> None:
    """Tests that I can add items to the list and get them out"""
    print("Testing...")
    update_entry("Luke B")
    sleep(1)
    update_entry("Luke B")
    sleep(1)
    update_entry("Rebekah R")
    update_entry("Luke B")
    sleep(1)
    update_entry("Luke B")
    sleep(1)
    update_entry("Luke B")
    update_entry("Megan P")
    sleep(1)
    update_entry("Luke B")
    sleep(1)
    #update_entry("Luke B")
    print_log()


def print_log() -> None:
    """Print each log item"""
    # To fix the type annotation
    if len(LOG_ITEMS) == 0:
        print("*** No entries ***")
        return
    for line_item in LOG_ITEMS:
        print(f"{line_item}")


def print_checkedin_items() -> None:
    """Print only items marked as Actions.IN"""
    print("Printing checked in items...")
    if len(LOG_ITEMS) == 0:
        print("*** No entries ***")
        return
    entries: dict[str, LogItem.Actions] = {}
    for entry in LOG_ITEMS:
        entries[entry.item] = entry.action
    key: str
    value: LogItem.Actions
    for key, value in entries.items():
        print(f"{key} is {value}")


def update_entry(entity: str) -> None:
    """Grab the latest entry with the entity, and flip its status. Create a new
    log entry, even if the item does not yet exist"""
    last_entries: list[LogItem] | None = None
    action: LogItem.Actions = LogItem.Actions.IN
    last_entries = next((entry for entry in reversed(LOG_ITEMS) if entry.item == entity), None)
    if last_entries and last_entries.action == LogItem.Actions.IN:
        action = LogItem.Actions.OUT
    LOG_ITEMS.append(LogItem(entity, action, datetime.datetime.now()))


def ask_for_input() -> None:
    """Ask the user for input. X to quit"""
    answer: str
    while True:
        answer = input("Item? [X to exit and print list; L to list items] ")
        if answer.lower() == "x":
            break
        if answer.lower() == "l":
            print_checkedin_items()
        else:
            update_entry(answer)
    print_checkedin_items()
    sys.exit(0)


def main():
    """Main program loop"""
    #if not load_existing():
    #    print("Error: could not load existing log")
    #test_list()
    ask_for_input()
    print_checkedin_items()

if __name__ == "__main__":
    main()
