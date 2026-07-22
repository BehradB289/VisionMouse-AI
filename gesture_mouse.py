import cv2
import mediapipe as mp
import numpy as np
import time
import math
import ctypes


try:

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

screen_w = ctypes.windll.user32.GetSystemMetrics(0)
screen_h = ctypes.windll.user32.GetSystemMetrics(1)


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800

def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(int(x), int(y))

def mouse_event(flags, data=0):
    ctypes.windll.user32.mouse_event(flags, 0, 0, data, 0)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0, 
    max_num_hands=2, 
    min_detection_confidence=0.8, 
    min_tracking_confidence=0.8
)


plocX, plocY = 0, 0
smoothening = 9  
pinch_start_time = 0
is_dragging = False
last_right_click = 0

print("--- Manual control system activated ---")
print("Right hand: Mouse movement and right-click (precise)")
print("Left hand: Scroll and left-click / drag")

try:
    while True:
        success, img = cap.read()
        if not success: break
        
        img = cv2.flip(img, 1)
        h_cam, w_cam, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for i, hand_lms in enumerate(results.multi_hand_landmarks):
            
                hand_label = results.multi_handedness[i].classification[0].label 
                lms = hand_lms.landmark
                
              
                x4, y4 = int(lms[4].x * w_cam), int(lms[4].y * h_cam)  
                x8, y8 = int(lms[8].x * w_cam), int(lms[8].y * h_cam)   
                x12, y12 = int(lms[12].x * w_cam), int(lms[12].y * h_cam) 
                
               
                if hand_label == 'Right':
                   
                    fx = np.interp(x8, (130, w_cam - 130), (0, screen_w))
                    fy = np.interp(y8, (130, h_cam - 130), (0, screen_h))
                    
                   
                    currX = plocX + (fx - plocX) / smoothening
                    currY = plocY + (fy - plocY) / smoothening
                    
                    move_mouse(currX, currY)
                    plocX, plocY = currX, currY
                    
                    
                    dist_r = math.hypot(x8 - x4, y8 - y4)
                    if dist_r < 22: 
                        if time.time() - last_right_click > 1.2:
                            mouse_event(MOUSEEVENTF_RIGHTDOWN)
                            mouse_event(MOUSEEVENTF_RIGHTUP)
                            last_right_click = time.time()

               
                elif hand_label == 'Left':
                    
                    if lms[12].y < lms[10].y: 
                        scroll_amount = int((h_cam/2 - y12) / 6)
                        if scroll_amount > 1:
                            mouse_event(MOUSEEVENTF_WHEEL, scroll_amount * 4)
                    
                    elif lms[8].y > lms[6].y: 
                        scroll_amount = int((y8 - h_cam/2) / 6)
                        if scroll_amount > 1:
                            mouse_event(MOUSEEVENTF_WHEEL, -scroll_amount * 4)

                    
                    dist_l = math.hypot(x8 - x4, y8 - y4)
                    if dist_l < 25:
                        if pinch_start_time == 0:
                            pinch_start_time = time.time()
                        
                        
                        if time.time() - pinch_start_time > 0.4:
                            if not is_dragging:
                                mouse_event(MOUSEEVENTF_LEFTDOWN)
                                is_dragging = True
                    else:
                        if pinch_start_time != 0:
                            if is_dragging:
                                mouse_event(MOUSEEVENTF_LEFTUP)
                                is_dragging = False
                            else:
                                
                                mouse_event(MOUSEEVENTF_LEFTDOWN)
                                mouse_event(MOUSEEVENTF_LEFTUP)
                            pinch_start_time = 0

        
        if cv2.waitKey(1) & 0xFF == ord('q'): break

except KeyboardInterrupt:
    pass
finally:
    if is_dragging: mouse_event(MOUSEEVENTF_LEFTUP)
    cap.release()
    cv2.destroyAllWindows()
