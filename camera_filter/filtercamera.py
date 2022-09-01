import cv2
import sys

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('카메라를 열 수 없습니다')
    sys.exit()

mode = ['normal', 'reverse', 'dark', 'blur'] # 모드 배열
modes = 'normal' # 초기 모드값
cnt = 0

def cameraFilter(frame, modes): # 프레임별 모드 전환
    if modes == 'reverse':
        return ~frame
    if modes == 'dark':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if modes == 'blur':
        return cv2.GaussianBlur(frame, (0, 0), 3)
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(10) == 13: #enter 키
        cnt += 1
        if cnt == len(mode):
            cnt = 0
        modes = mode[cnt]
    frame = cameraFilter(frame, modes)
    desc = "mode : {}".format(modes)
    cv2.putText(frame, desc, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, 255, 1, cv2.LINE_AA)
    cv2.imshow('filterCam', frame)

    if cv2.waitKey(10) == 27: #esc 키
        break

cap.release()
cv2.destroyAllWindows()