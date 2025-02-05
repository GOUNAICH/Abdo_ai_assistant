import time
import cv2
import pyautogui as p

def AuthenticateFace(user_id=1):  # Default user ID is 1
    flag = 0  # Initialize flag
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load trained model
    recognizer.read('C:\\Users\\dell\\Desktop\\Abdo_ai_assistant\\auth\\trainer\\trainer.yml')  

    # Load Haar Cascade for face detection
    cascadePath = "C:\\Users\\dell\\Desktop\\Abdo_ai_assistant\\auth\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Only the user should be recognized
    names = ['', 'Abdeslam']  # Index 1 is "Abdeslam"

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Set frame width
    cam.set(4, 480)  # Set frame height

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    # Add counters for consecutive matches
    consecutive_matches = 0
    required_matches = 2
    
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        found_match = False  # Track if we found a match in this frame
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            detected_id, accuracy = recognizer.predict(gray[y:y + h, x:x + w])

            # Check each face individually
            if detected_id == user_id and accuracy < 65:
                found_match = True  # We found the correct user in this frame
                cv2.putText(img, "Abdeslam", (x + 5, y - 5), font, 1, (0, 255, 0), 2)
                
            else:
                cv2.putText(img, "Unknown", (x + 5, y - 5), font, 1, (0, 0, 255), 2)

            cv2.putText(img, f"Accuracy: {round(100 - accuracy)}%", (x + 5, y + h - 5),
                        font, 1, (255, 255, 0), 1)

        # Update consecutive matches based on if we found the user in this frame
        if found_match:
            consecutive_matches += 1
            if consecutive_matches >= required_matches:
                flag = 1
        else:
            consecutive_matches = 0
            
        # Show matching progress
        cv2.putText(img, f"Matching Progress: {consecutive_matches}/{required_matches}", 
                    (10, 30), font, 1, (255, 255, 255), 2)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff
        if k == 27 or flag == 1:  # Exit if ESC is pressed or user is recognized
            break

    cam.release()
    cv2.destroyAllWindows()

    return flag