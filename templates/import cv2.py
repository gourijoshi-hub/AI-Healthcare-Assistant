import cv2
import os

name = input("Enter your name: ")

path = "dataset/" + name
os.makedirs(path, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Look at the camera... Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capturing...", frame)

    if count % 5 == 0:
        cv2.imwrite(f"{path}/{count}.jpg", frame)
        print("Saved picture:", count)

    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Done capturing your face!")
