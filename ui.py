import tkinter as tk
import subprocess
import sys

# =========================
# UI WINDOW
# =========================
root = tk.Tk()
root.title("HandsFree AI")
root.attributes("-fullscreen", True)
root.configure(bg="#050A30")

# =========================
# EXIT FULLSCREEN
# =========================
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# =========================
# GLOBAL STATE
# =========================
voice_process = None

# =========================
# FUNCTIONS
# =========================
def glow_effect(widget, colors, index=0):
    widget.config(bg=colors[index])
    root.after(500, glow_effect, widget, colors, (index + 1) % len(colors))

def start_system():
    global voice_process
    if voice_process is None:
        voice_process = subprocess.Popen(
            [sys.executable, "voice_assistant.py"]
        )
        status_label.config(text="SYSTEM RUNNING", fg="#00FFEA")

def stop_system():
    global voice_process
    if voice_process:
        voice_process.terminate()
        voice_process = None
        status_label.config(text="SYSTEM STOPPED", fg="red")

def refresh_mode():
    try:
        with open("mode.txt") as f:
            mode = f.read().strip()
            mode_label.config(text=f"MODE: {mode}")
    except:
        pass
    root.after(1000, refresh_mode)

# =========================
# TITLE
# =========================
title = tk.Label(
    root,
    text="HANDSFREE AI",
    font=("Orbitron", 48, "bold"),
    fg="#00FFEA",
    bg="#050A30"
)
title.pack(pady=40)

subtitle = tk.Label(
    root,
    text="Voice & Gesture Based Intelligent Desktop Assistant",
    font=("Arial", 18),
    fg="white",
    bg="#050A30"
)
subtitle.pack(pady=10)

# =========================
# MODE LABEL
# =========================
mode_label = tk.Label(
    root,
    text="MODE: STUDY",
    font=("Arial", 22, "bold"),
    fg="#00FFEA",
    bg="#050A30"
)
mode_label.pack(pady=20)

refresh_mode()

# =========================
# BUTTONS
# =========================
start_btn = tk.Button(
    root,
    text="START SYSTEM",
    font=("Arial", 24, "bold"),
    width=20,
    bg="#00FFEA",
    fg="black",
    command=start_system
)
start_btn.pack(pady=30)

stop_btn = tk.Button(
    root,
    text="STOP SYSTEM",
    font=("Arial", 24, "bold"),
    width=20,
    bg="#FF004D",
    fg="white",
    command=stop_system
)
stop_btn.pack(pady=10)

# =========================
# STATUS
# =========================
status_label = tk.Label(
    root,
    text="SYSTEM STOPPED",
    font=("Arial", 16),
    fg="red",
    bg="#050A30"
)
status_label.pack(pady=30)

# =========================
# FOOTER
# =========================
footer = tk.Label(
    root,
    text="Study | Presentation | Idle Modes Enabled",
    font=("Arial", 14),
    fg="#00FFEA",
    bg="#050A30"
)
footer.pack(side="bottom", pady=20)

# =========================
# GLOW EFFECT (AFTER BUTTON EXISTS)
# =========================
glow_colors = ["#00FFEA", "#00CCFF", "#0099FF"]
glow_effect(start_btn, glow_colors)

# =========================
# MAIN LOOP
# =========================
root.mainloop()
