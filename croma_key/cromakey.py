import cv2
import sys

woman = cv2.VideoCapture('woman.mp4')
field = cv2.VideoCapture('jungle.mp4')
if not woman.isOpened or not woman.isOpened():
    print('동영상을 열 수 없습니다')
    sys.exit()

fps = woman.get(cv2.CAP_PROP_FPS)
w = round(woman.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(woman.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_cnt1 = round(woman.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(field.get(cv2.CAP_PROP_FRAME_COUNT))

print('1.가로 사이즈 : ', int(woman.get(cv2.CAP_PROP_FRAME_WIDTH)))
print('1.세로 사이즈 : ', int(woman.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('1.프레임 수: ', int(woman.get(cv2.CAP_PROP_FRAME_COUNT)))
print('1.FPS', fps)
print('2.프레임 수: ', int(field.get(cv2.CAP_PROP_FRAME_COUNT)))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
delay = round(1000/fps)

finout = cv2.VideoWriter('finVid.mp4', fourcc, fps, (w, h))

for i in range(frame_cnt1):
    ret1, frame1 = woman.read()
    ret3, frame3 = field.read()
    src_hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    frame2 = cv2.inRange(src_hsv, (50, 150, 0), (80, 255, 255))

    cv2.copyTo(frame1, ~frame2, frame3)

    finout.write(frame3)
    cv2.imshow('frame', frame3)
    cv2.waitKey(delay)

woman.release()
field.release()
cv2.destroyAllWindows()

