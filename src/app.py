import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
finger_list = [8, 12, 16, 20]
counter = 0

while True:

    _ , frame = cap.read()

    framRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(framRGB)
    counter = 0
    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:
            # mp_draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmark = hand.landmark
            for tip in finger_list:
                if landmark[tip].y < landmark[tip-2].y :
                    counter +=1
            if landmark[4].x > landmark[3].x:
                counter +=1
    if counter == 0:
        hands_fist = 'OK'
        file_name = './images/test.png'
        cv2.imwrite(file_name, frame)
    else:
        hands_fist = 'NOT OK'
    cv2.putText(frame, str(hands_fist),(50,100), 
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 3)


    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()