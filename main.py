"""Log-Items main module"""
import datetime
import pickle
import sys
from time import sleep
from models.log_items import LogItem

log_items: list[LogItem] = []
id_to_name = {}

RED      = '\x1b[31m'
GREEN    = '\x1b[32m'
YELLOW   = '\x1b[33m'
RESET    = '\x1b[0m'
BOLD     = '\x1b[1m'
CUR_TOP  = '\x1b[H'
CLS      = '\x1b[2J'

# TODO: Save statistics for each day

def register_or_get_name(name_id: int, name: str | None= None) -> str:
    """Assigns a name, or gets the name"""
    #global id_to_name
    if name is not None:
        id_to_name[name_id] = name
    return id_to_name.get(name_id, f"Unknown ({name_id})")


def test_load_users_into_mappings() -> None:
    """Add test users to the user mapping"""
    register_or_get_name(7444, "Luke B")
    register_or_get_name(7333, "Megan P")
    register_or_get_name(7222, "Rebekah R")

def test_list() -> None:
    """Tests that I can add items to the list and get them out"""
    print(f"{YELLOW}Testing...{RESET}")
    test_load_users_into_mappings()
    update_entry(register_or_get_name(7444))
    sleep(1)
    update_entry(register_or_get_name(7444))
    sleep(1)
    update_entry(register_or_get_name(7111))
    update_entry(register_or_get_name(7444))
    sleep(1)
    update_entry(register_or_get_name(7444))
    sleep(1)
    update_entry(register_or_get_name(7222))
    update_entry(register_or_get_name(7333))
    sleep(1)
    update_entry(register_or_get_name(7444))
    sleep(1)
    print_log()


def print_log() -> None:
    """Print each log item"""
    # To fix the type annotation
    if len(log_items) == 0:
        print("*** No entries ***")
        return
    for line_item in log_items:
        print(f"{line_item}")


def print_checkedin_items() -> None:
    """Print only items marked as Actions.IN"""
    print("Printing checked in items...")
    if len(log_items) == 0:
        print("*** No entries ***")
        return
    entries: dict[str, str] = {}
    for entry in log_items:
        entries[entry.item] = str(entry.action.value)
    key: str
    value: str
    for key, value in entries.items():
        print(f"{key} is {value}")


def update_entry(entity: str) -> None:
    """Grab the latest entry with the entity, and flip its status. Create a new
    log entry, even if the item does not yet exist"""
    last_entries: list[LogItem] | None = None
    action: LogItem.Actions = LogItem.Actions.IN
    last_entries = next((entry for entry in reversed(log_items) if entry.item == entity), None)
    if last_entries and last_entries.action == LogItem.Actions.IN:
        action = LogItem.Actions.OUT
    log_items.append(LogItem(entity, action, datetime.datetime.now()))


def show_main_menu() -> None:
    """Main menu"""
    answer: str
    while True:
        answer = input(f"{CLS}{CUR_TOP}ID Number [{BOLD}{RED}X{RESET} to exit and print list; " +
                       f"{BOLD}{GREEN}C{RESET} to print checked items; " +
                       f"{BOLD}{GREEN}L{RESET} to list all items; " +
                       f"{BOLD}{RED}D{RESET} to clear list; " +
                       f"{BOLD}{GREEN}S{RESET} for today's stats; " +
                       f"{BOLD}{YELLOW}P{RESET} for new period] ")
        if answer.lower() == "x":
            break
        if answer == "":
            continue
        if answer.lower() == "c":
            print_checkedin_items()
            input("Press Enter to continue...")
        elif answer.lower() == "l":
            print_log()
            input("Press Enter to continue...")
        elif answer.lower() == "d":
            # Delete the current list, start over
            # TODO: Impliment list deletion
            continue
        elif answer.lower() == "s":
            # Print out the stats for the day (how many came "in" today)
            # TODO: Impliment printing stats (and collecting)
            continue
        elif answer.lower() == "p":
            # Next period, mark everyone as Out
            # TODO: Impliment setting everyone as Out
            continue
        elif int(answer) > 0:
            # Assume int
            update_entry(register_or_get_name(int(answer)))
        else:
            # Assume it's a string
            update_entry(answer)
    # Finally, print and save the list so we can exit
    print_checkedin_items()
    save_to_file()
    sys.exit(0)


def save_to_file() -> None:
    """Save the existing LOG_ITEMS to a file."""
    if len(log_items) == 0:
        print("No log items to save")
        return
    today = datetime.datetime.date(datetime.datetime.now())
    # Today is YYYY-MM-DD format
    with open(f"{today}.pkl", 'wb') as f:
        pickle.dump(log_items, f)
        print(f"{today}.db written")
    with open("mappings.pkl", 'wb') as f:
        pickle.dump(id_to_name, f)
        print("ID Mappings saved")


def load_from_file() -> bool:
    """Load the existing log items.
    TODO: Check if the file can be read
    TODO: Check if the unpickling did not succeed"""
    today = datetime.datetime.date(datetime.datetime.now())
    try:
        with open(f"{today}.pkl", 'rb') as f:
            global log_items
            log_items = pickle.load(f)
    except FileNotFoundError:
        return False
    # Attempt to load id mapping list
    try:
        with open ("mappings.pkl", 'rb') as f:
            global id_to_name
            id_to_name = pickle.load(f)
            return True
    except FileNotFoundError:
        return False
    return False


def main():
    """Main program loop"""
    if not load_from_file():
        print("Warning: could not load existing log")
    #test_load_users_into_mappings()
    #test_list()
    show_main_menu()


if __name__ == "__main__":
    main()
