import cv2
import mediapipe as mp
import pyautogui
import numpy as np

mouse_active = True

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

click_cooldown = 0


def fingers_up(hand_landmarks, w, h):
    """Return which fingers are up [thumb, index, middle, ring, pinky]"""
    tips = [4, 8, 12, 16, 20]
    finger_states = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        finger_states.append(1)
    else:
        finger_states.append(0)

    # Other 4 fingers
    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states.append(1)
        else:
            finger_states.append(0)

    return finger_states


print("Virtual Mouse Starting...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    h, w, c = frame.shape

    if result.multi_hand_landmarks:
        hand_lms = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

        finger_state = fingers_up(hand_lms, w, h)

        # STOP MODE (Open Palm)
        if finger_state == [1, 1, 1, 1, 1]:
            mouse_active = False
            cv2.putText(frame, "MOUSE PAUSED", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # RESUME MODE (Fist)
        elif finger_state == [0, 0, 0, 0, 0]:
            mouse_active = True
            cv2.putText(frame, "MOUSE ACTIVE", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        if mouse_active:
            # cursor movement + click code here

            # Index finger position
            index_x = int(hand_lms.landmark[8].x * w)
            index_y = int(hand_lms.landmark[8].y * h)

            screen_w, screen_h = pyautogui.size()
            screen_x = np.interp(index_x, (0, w), (0, screen_w))
            screen_y = np.interp(index_y, (0, h), (0, screen_h))
            pyautogui.moveTo(screen_x, screen_y)

            # Get Thumb position for click detection
            thumb_x = int(hand_lms.landmark[4].x * w)
            thumb_y = int(hand_lms.landmark[4].y * h)
            distance = np.hypot(index_x - thumb_x, index_y - thumb_y)

            # LEFT CLICK (thumb + index pinch)
            if distance < 35 and click_cooldown == 0:
                pyautogui.click()
                click_cooldown = 10
                cv2.putText(frame, "LEFT CLICK", (index_x, index_y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

            # RIGHT CLICK (index + middle finger pinch)
            mid_x = int(hand_lms.landmark[12].x * w)
            mid_y = int(hand_lms.landmark[12].y * h)
            dist_right = np.hypot(index_x - mid_x, index_y - mid_y)

            if dist_right < 35 and click_cooldown == 0:
                pyautogui.rightClick()
                click_cooldown = 10
                cv2.putText(frame, "RIGHT CLICK", (index_x, index_y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    if click_cooldown > 0:
        click_cooldown -= 1

    cv2.imshow("Virtual Mouse Basic", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
