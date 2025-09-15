import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize video capture with optimized settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# MediaPipe hands setup
hand_detector = mp.solutions.hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0
)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Control parameters
smoothing_factor = 0.4
prev_x, prev_y = 0, 0
CLICK_THRESHOLD = 30
DRAG_THRESHOLD = 25  # Distance to maintain drag
MOVE_THRESHOLD = 100

# Drag state variables
is_dragging = False
drag_start_time = 0

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        continue
        
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    
    if output.multi_hand_landmarks:
        for hand_landmarks in output.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            frame_height, frame_width, _ = frame.shape
            
            # Index finger (Landmark 8)
            index = landmarks[8]
            index_x = int(index.x * frame_width)
            index_y = int(index.y * frame_height)
            
            # Thumb (Landmark 4)
            thumb = landmarks[4]
            thumb_x = int(thumb.x * frame_width)
            thumb_y = int(thumb.y * frame_height)
            
            # Middle finger (Landmark 12) - for drag activation
            middle = landmarks[12]
            middle_y = int(middle.y * frame_height)
            
            # Convert to screen coordinates
            screen_x = np.interp(index.x, [0, 1], [0, screen_width])
            screen_y = np.interp(index.y, [0, 1], [0, screen_height])
            
            # Apply smoothing
            smooth_x = prev_x + smoothing_factor * (screen_x - prev_x)
            smooth_y = prev_y + smoothing_factor * (screen_y - prev_y)
            
            # Calculate distances
            index_thumb_dist = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2)**0.5
            index_middle_dist = index_y - middle_y  # Vertical distance between index and middle
            
            # Visual feedback
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), cv2.FILLED)  # Index (yellow)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), cv2.FILLED)    # Thumb (green)
            cv2.circle(frame, (int(middle.x * frame_width), middle_y), 10, (255, 0, 0), cv2.FILLED)  # Middle (blue)
            
            # Drag activation (middle finger below index finger)
            if (index_middle_dist > 20 and 
                index_thumb_dist < DRAG_THRESHOLD and 
                not is_dragging):
                pyautogui.mouseDown()
                is_dragging = True
                drag_start_time = cv2.getTickCount()
                cv2.putText(frame, "Drag Start", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Continue dragging
            elif is_dragging:
                # Check if we should stop dragging (fingers too far apart)
                if index_thumb_dist > DRAG_THRESHOLD + 15:
                    pyautogui.mouseUp()
                    is_dragging = False
                    cv2.putText(frame, "Drag End", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    pyautogui.moveTo(smooth_x, smooth_y)
                    cv2.putText(frame, "Dragging", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Normal click (index and thumb close together)
            elif index_thumb_dist < CLICK_THRESHOLD:
                pyautogui.click()
                cv2.putText(frame, "Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                pyautogui.sleep(0.1)  # Prevents double clicks
            
            # Regular cursor movement
            elif index_thumb_dist < MOVE_THRESHOLD:
                pyautogui.moveTo(smooth_x, smooth_y)
                prev_x, prev_y = smooth_x, smooth_y
            
            # Draw connection lines for visualization
            cv2.line(frame, (index_x, index_y), (thumb_x, thumb_y), (255, 0, 0), 2)
            cv2.line(frame, (index_x, index_y), (int(middle.x * frame_width), middle_y), (0, 0, 255), 2)
    
    # Display instructions
    cv2.putText(frame, "Index+Thumb: Click", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, "Index+Thumb+Middle down: Drag", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, "Press 'q' to quit", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow('Virtual Mouse with Drag', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if is_dragging:  # Ensure mouse is released when quitting
            pyautogui.mouseUp()
        break

cap.release()
cv2.destroyAllWindows()