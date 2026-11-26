"""Data tool to import names to ID numbers"""
import pickle
import sys

id_to_name = {}

def register_or_get_name(name_id: int, name: str | None= None) -> str:
    """Assigns a name, or gets the name"""
    #global id_to_name
    if name is not None:
        id_to_name[name_id] = name
    return id_to_name.get(name_id, "Unknown")


def test_load_users_into_mappings() -> None:
    """Add test users to the user mapping"""
    register_or_get_name(7444, "Luke B")
    register_or_get_name(7333, "Megan P")
    register_or_get_name(7222, "Rebekah R")


def save_list_to_file() -> None:
    """Save the existing user map to a file."""
    if len(id_to_name) == 0:
        print("No items to save")
        return
    with open("mappings.pkl", 'wb') as f:
        pickle.dump(id_to_name, f)
        print("ID Mappings saved")


def load_existing() -> bool:
    """Load the existing log items.
    TODO: Check if the file can be read
    TODO: Check if the unpickling did not succeed"""
    try:
        with open ("mappings.pkl", 'rb') as f:
            global id_to_name
            id_to_name = pickle.load(f)
            return True
    except FileNotFoundError:
        return False
    return False


def do_delete_id() -> None:
    """Delete based on the ID number"""
    name_id: str
    name_id = input("Enter ID to delete; blank to go back: ")
    id_to_name.pop(name_id, None)


def print_list() -> None:
    """Print the full list of mappings"""
    if not id_to_name:
        print("*** No entries saved ***")
        return
    print("ID:\tName:")
    key: int
    value: str
    for key, value in id_to_name.items():
        print(f"{key}\t{value}")


def ask_for_input() -> None:
    """Ask the user to provide the ID and a name"""
    print("Enter the ID number, a space, then the name (remainder of line).\n" +
          "Q to exit without saving; L to list; S to save and quit\n" +
          "D to delete ID")
    while True:
        line: str
        line = input("<ID Number> <Name> | Q | L | S | D : ")
        if line.lower() == "q":
            print("Exiting, not saving")
            sys.exit(0)
        elif line.lower() == "l":
            print_list()
        elif line.lower() == "s":
            save_list_to_file()
            sys.exit(0)
        elif line.lower() == "d":
            do_delete_id()
            continue
        elif line == "":
            continue
        else:
            # Do the actual parsing
            name: str
            name_id, name = line.split(None, maxsplit=1)
            try:
                if int(name_id) > 0:
                    register_or_get_name(int(name_id), name)
            except ValueError: # We don't care, just go back
                continue


def main():
    """Main program loop"""
    if not load_existing():
        print("Warning: could not load existing list")
    ask_for_input()


if __name__ == "__main__":
    main()
