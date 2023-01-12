"""
Autorzy:
    Damian Kijańczuk s20154
    Szymon Ciemny    s21355

Przygotowanie środowiska:
    Oprócz języka Python, potrzebne takze będzie:
    - mediapipe
    - opencv

Uruchomienie oraz instrukcja:
    By uruchomić wpisz:
    'python3 main.py'

    Obsługiwane są 4 gesty:
    - wskazanie palcem w górę
      - zwiększa głośność
    - wskazanie palcem w dół
      - zmniejsza głośność
    - kciuk w górę
      - odcisza muzyke
    - 'znak stop'
      - wycisza muzyke

    By program wykrył gest nalezy przycisnąć SPACJA
"""

import cv2
import mediapipe as mp
import os
from math import sqrt, pow
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getDistance(A, B):
  return isFar(sqrt(pow(A.x-B.x ,2) + pow(A.y-B.y ,2)))

def isFar(number):
  if number < 0.1:
    return False
  return True

def detectGesture(H):
  # Stop gesture
  if (getDistance(H.landmark[8], H.landmark[5])  and
      getDistance(H.landmark[12], H.landmark[9])  and 
      getDistance(H.landmark[16], H.landmark[13]) and
      getDistance(H.landmark[20], H.landmark[17])):
    print("Stop")
    return "Stop"

  if not (getDistance(H.landmark[12], H.landmark[9])  and 
      getDistance(H.landmark[16], H.landmark[13]) and
      getDistance(H.landmark[20], H.landmark[17])):


    if not (getDistance(H.landmark[8], H.landmark[5])) and H.landmark[4].y - H.landmark[2].y < 0.1:
      print("Thumbs up")
      return "Thumbs up"

    if H.landmark[8].y - H.landmark[5].y > 0.1:
      print("Point Down")
      return "Point Down"
    if H.landmark[8].y - H.landmark[5].y < 0.1:
      print("Up")
      return "Point Up"

  print("Nic")
  return "Nothing"



# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # If you press space, gesture will be detected
    if cv2.waitKey(33) == ord(' '):
      result = detectGesture(results.multi_hand_landmarks[0])
    else:
      result = " "

    if result == "Point Up":
      os.system('osascript -e "set volume output volume (output volume of (get volume settings) + 10)"')
    elif result == "Point Down":
      os.system('osascript -e "set volume output volume (output volume of (get volume settings) - 10)"')
    elif result == "Thumbs up":
      os.system('osascript -e "set volume output volume 40"')
    elif result == "Stop":
      os.system('osascript -e "set volume output volume 0"')

    cv2.putText(image, result, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()












