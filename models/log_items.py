"""Log-Items Class"""
import datetime
from enum import Enum
from time import sleep

class LogItem:
    """The actual class (why is a docstring needed?)"""
    class Actions(Enum):
        """Valid actions, and their nice-labels"""
        IN = "in"
        OUT = "out"


    def __init__(self, key: str, action: Actions, timestamp: datetime.datetime) -> None:
        self.item = key
        self.action = action
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"{self.timestamp.strftime(format="%d/%m/%Y, %H:%M:%S")} - " + \
            f"{self.item} changed to {self.action.value}"


def main():
    """Testing"""
    my_first_action = LogItem("Luke B", LogItem.Actions.IN, datetime.datetime.now())
    sleep(1)
    my_second_action = LogItem("Luke B", LogItem.Actions.OUT, datetime.datetime.now())
    print(f"{my_first_action}")
    print(f"{my_second_action}")

if __name__=="__main__":
    main()
