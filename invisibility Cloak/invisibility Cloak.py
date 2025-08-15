import cv2
import numpy as np
import time

# 🎥 Step 1: Start the webcam
video = cv2.VideoCapture(0)

# Let the camera warm up
time.sleep(2)

# 📸 Step 2: Capture the background (without the cloak)
print("Capturing background... Please step out of the frame!")
for i in range(30):   # Take multiple frames for a cleaner background
    ret, background = video.read()

# Flip background for a mirror-like view
background = np.flip(background, axis=1)

print("Background captured! Wear your BLUE cloak and get ready to disappear...")

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Flip frame for natural webcam behavior
    frame = np.flip(frame, axis=1)

    # 🎨 Step 3: Convert BGR image to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 🔵 Step 4: Define the blue cloak color range in HSV
    lower_blue = np.array([94, 80, 2])      # Adjust if detection is off
    upper_blue = np.array([126, 255, 255])
    cloak_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # 🔍 Step 5: Clean up the mask
    cloak_mask = cv2.morphologyEx(cloak_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cloak_mask = cv2.dilate(cloak_mask, np.ones((3, 3), np.uint8))

    # 🎭 Step 6: Extract cloak area from the background
    invisible_part = cv2.bitwise_and(background, background, mask=cloak_mask)

    # Extract everything except the cloak from the current frame
    visible_part = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(cloak_mask))

    # 🪄 Step 7: Merge both parts to create the invisibility effect
    final_frame = cv2.addWeighted(invisible_part, 1, visible_part, 1, 0)

    # Show magic on screen
    cv2.imshow("🪄 Invisibility Cloak (Blue)", final_frame)

    # Press ESC to quit
    if cv2.waitKey(1) == 27:
        break

# 🛑 Step 8: Cleanup
video.release()
cv2.destroyAllWindows()
