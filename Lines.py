import time
from plyer import notification

while True:
    notification.notify(
        title = "Remainder",
        message = "Drink some water!"
    ) 
    time.sleep(10)