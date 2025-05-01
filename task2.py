import cv2

# Global variables to store click status, color, and coordinates
clicked = False
bgr_color = (0, 0, 0)
x_pos, y_pos = 0, 0
exit_program = False  # Flag to detect if close button is clicked

# Mouse callback function to handle clicks
def show_color_name(event, x, y, flags, param):
    global clicked, bgr_color, x_pos, y_pos, exit_program

    if event == cv2.EVENT_LBUTTONDOWN:
        # Checking if click is within the "Close" button area
        if 550 <= x <= 640 and 20 <= y <= 60:
            exit_program = True  # User clicked close
        else:
            clicked = True
            x_pos, y_pos = x, y
            bgr_color = frame[y, x].tolist()

# Open webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Color Detector')
cv2.setMouseCallback('Color Detector', show_color_name)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw the "Close" button
    cv2.rectangle(frame, (550, 20), (640, 60), (0, 0, 255), -1)
    cv2.putText(frame, "Close", (565, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2)

    if clicked:
        b, g, r = bgr_color
        text = f"BGR: ({b}, {g}, {r})"
        cv2.rectangle(frame, (20, 20), (300, 60), (int(b), int(g), int(r)), -1)
        cv2.putText(frame, text, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

    cv2.imshow('Color Detector', frame)

    # Exit conditions: ESC key or Close button clicked
    if cv2.waitKey(1) & 0xFF == 27 or exit_program:
        break

cap.release()
cv2.destroyAllWindows()
