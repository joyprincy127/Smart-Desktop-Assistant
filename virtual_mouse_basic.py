import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import sys
from logger import log_event

pyautogui.FAILSAFE = False

# =========================
# GLOBAL STATE
# =========================
click_cooldown = 0
slide_cooldown = 0
mouse_active = True   # PAUSE / RESUME

# =========================
# MEDIAPIPE SETUP
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
draw = mp.solutions.drawing_utils

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    sys.exit(1)

# =========================
# GESTURE HELPERS
# =========================
def fingers_up(hand):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    fingers.append(hand.landmark[4].x < hand.landmark[3].x)  # thumb
    for tip in tips[1:]:
        fingers.append(hand.landmark[tip].y < hand.landmark[tip - 2].y)

    return fingers

def thumb_gesture(hand):
    thumb_tip = hand.landmark[4]
    thumb_ip = hand.landmark[2]
    index_tip = hand.landmark[8]
    index_pip = hand.landmark[6]

    index_folded = index_tip.y > index_pip.y
    margin = 0.04

    if index_folded:
        if thumb_tip.y < thumb_ip.y - margin:
            return "next"
        elif thumb_tip.y > thumb_ip.y + margin:
            return "prev"
    return None

print("Gesture Controller Started")

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    h, w, _ = frame.shape

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        finger_state = fingers_up(hand)

        # =========================
        # PAUSE / RESUME
        # =========================
        if finger_state == [1, 1, 1, 1, 1]:
            mouse_active = False
            cv2.putText(frame, "PAUSED ✋", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        elif finger_state == [0, 0, 0, 0, 0]:
            mouse_active = True
            cv2.putText(frame, "ACTIVE ✊", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        if mouse_active:
            # =========================
            # MOUSE MOVEMENT
            # =========================
            ix = int(hand.landmark[8].x * w)
            iy = int(hand.landmark[8].y * h)

            sw, sh = pyautogui.size()
            pyautogui.moveTo(
                np.interp(ix, (0, w), (0, sw)),
                np.interp(iy, (0, h), (0, sh))
            )

            # =========================
            # LEFT CLICK (Thumb + Index)
            # =========================
            tx = int(hand.landmark[4].x * w)
            ty = int(hand.landmark[4].y * h)
            dist_left = np.hypot(ix - tx, iy - ty)

            # Right click (Thumb + Middle)
            mx = int(hand.landmark[12].x * w)
            my = int(hand.landmark[12].y * h)
            dist_right = np.hypot(mx - tx, my - ty)

            if dist_left < 35 and click_cooldown == 0:
                pyautogui.click()
                log_event("Left Click")
                click_cooldown = 12

            elif dist_right < 35 and click_cooldown == 0:
                pyautogui.rightClick()
                log_event("Right Click")
                click_cooldown = 12

            # =========================
            # SLIDE CONTROL 👍👎
            # =========================
            if slide_cooldown == 0:
                gesture = thumb_gesture(hand)

                if gesture == "next":
                    pyautogui.press("n")
                    log_event("Next Slide")
                    slide_cooldown = 25

                elif gesture == "prev":
                    pyautogui.press("p")
                    log_event("Previous Slide")
                    slide_cooldown = 25

    click_cooldown = max(0, click_cooldown - 1)
    slide_cooldown = max(0, slide_cooldown - 1)

    cv2.imshow("Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == 27:   # ESC to exit safely
        break

cap.release()
cv2.destroyAllWindows()
