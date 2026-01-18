from datetime import datetime

def log_event(event):
    with open("activity_log.txt", "a") as f:
        time = datetime.now().strftime("%H:%M:%S")
        f.write(f"{time} - {event}\n")
