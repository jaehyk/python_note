import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--dir")
ap.add_argument("--src")
ap.add_argument("--dst")
args = vars(ap.parse_args())

cap = cv2.VideoCapture("{}/{}".format(args['dir'], args['src']))
bg = None
frame_cnt = 0
frame_cnt2 = 0

while True:
	res, frame = cap.read()
	if not res:
		break

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (0, 0), 1.0)
	
	if bg is None:
		bg = gray
		continue

	diff = cv2.absdiff(bg, gray)
#	diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
	diff_value = (diff.sum()/(diff.shape[1]*diff.shape[0]))

	print(diff_value)

	if diff_value > 70 and frame_cnt > 1:
		frame_cnt = 0

	elif diff_value > 55 and frame_cnt > 10:
		frame_cnt = 0

	elif diff_value > 35 and frame_cnt > 30:
		frame_cnt = 0
	
	if frame_cnt == 0:
		cv2.imwrite('{}/{}_{:05d}.jpg'.format(args['dst'], args['src'], frame_cnt2), frame)
		frame_cnt2 += 1
	
	frame_cnt += 1
	if frame_cnt > 90:
		frame_cnt = 0

	k = cv2.waitKey(1) & 0xFF
	if k == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
