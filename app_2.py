import cv2
import mediapipe as mp
import speech_recognition as sr

mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_list = [8, 12, 16, 20]
counter = 0
sequence = 0
last_counter = 0

recognizer = sr.Recognizer()

while True:

    _, frame = cap.read()
    framRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(framRGB)
    counter = 0
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmark = hand.landmark
            for tip in finger_list:
                if landmark[tip].y < landmark[tip - 2].y:
                    counter += 1
            if landmark[4].x > landmark[3].x:
                counter += 1

    if counter != last_counter:

        if counter == 1 and sequence == 0:
            sequence = 1
        elif counter == 2 and sequence == 1:
            sequence = 2
        elif counter == 3 and sequence == 2:
            sequence = 3

            cv2.putText(frame,"Microphone ON",(50, 200),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0, 255, 0),3)
            cv2.imshow("Webcam", frame)
            cv2.waitKey(1000)
            print("Microphone is ON")
            print("Say: close")

            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source,duration=1)
                    audio = recognizer.listen(source,timeout=5,phrase_time_limit=3)

                text = recognizer.recognize_google(audio)
                print("You said:", text)

                if text.lower() == "close":
                    break
                else:
                    print("Command not recognized.")
            except sr.WaitTimeoutError:
                print("No voice detected.")
            except sr.UnknownValueError:
                print("I couldn't understand the voice.")
            except sr.RequestError:
                print("Speech recognition service is unavailable.")
        last_counter = counter


    cv2.putText( frame,"Number: " + str(counter),(50, 100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0, 255, 0),3)
    cv2.putText(frame, "Sequence: " + str(sequence),(50, 150),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255, 255, 0),2)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
