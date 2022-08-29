import cv2
import sys
import numpy as np

cap = cv2.VideoCapture('firVid.mp4')
cap2 = cv2.VideoCapture('secVid.mp4')
if not cap.isOpened or not cap2.isOpened():
    print('동영상을 열 수 없습니다')
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_cnt1 = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
effect_frames = int(fps*2)

print('1.가로 사이즈 : ', int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print('1.세로 사이즈 : ', int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('1.프레임 수: ', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
print('1.FPS', fps)
print('2.프레임 수: ', int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)))

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
delay = round(1000/fps)

out = cv2.VideoWriter('finVid.avi', fourcc, fps, (w, h))

if not out.isOpened():
    print('파일을 저장할 수 없습니다')
    cap.release()
    sys.exit()

for i in range(frame_cnt1 - effect_frames):
    ret1, frame1 = cap.read()

    if not ret1:
        break

    out.write(frame1)
    cv2.imshow('frame', frame1)
    cv2.waitKey(delay)

# 합성하기
for i in range(effect_frames):  
    ret1, frame1 = cap.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print('frame read error!')
        sys.exit()

    dx = int((w / effect_frames) * i)

    frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame[:, 0:dx, :] = frame2[:, 0:dx, :]
    frame[:, dx:w, :] = frame1[:, dx:w, :]
    out.write(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(delay)

for i in range(effect_frames, frame_cnt2):
    ret2, frame2 = cap2.read()

    if not ret2:
        break

    out.write(frame2)
    cv2.imshow('frame', frame2)
    cv2.waitKey(delay)
cap.release()
cap2.release()
out.release()
cv2.destroyAllWindows()

