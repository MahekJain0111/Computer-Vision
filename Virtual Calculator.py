import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [
        ["+","-","*","%","/","=", "backspace"],
        ["1","2","3","4","5","6","7","8","9","0"]
                                                      ]
finalText = ""


def drawAll(img, ButtonList):
    for button in ButtonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text


ButtonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        ButtonList.append(Button([100 * j + 50, 100*i+50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img = drawAll(img, ButtonList)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        for button in ButtonList:
            x, y = button.pos
            w, h = button.size

            if x < hand1["lmList"][8][0] < x + w and y < hand1["lmList"][8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h+5  ), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 5, y + 25),
                            cv2.FONT_HERSHEY_PLAIN,4 , (255, 255, 255), 4)
                length, info,img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2],img)

                if length <70 :

                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 55),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    if(button.text=="backspace"):
                        finalText=finalText[0:-1]
                    elif (button.text == "="):
                      finalText = eval(finalText)
                      finalText = str(finalText)


                    else:
                        finalText=finalText+button.text


                    sleep(0.15)
    cv2.rectangle(img, (50, 450), (700, 550), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (100, 530),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
