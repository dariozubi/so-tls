import cv2

c = 0
for i in range(46,1000):
	img = cv2.imread("cda/Diciembre/Video/-2018-mar-17-{:03d}.jpg".format(i))
	crop_img = img[0:880, 0:1920]
	cv2.imwrite("cda/Diciembre/Video/crops/{:04d}.jpg".format(c), crop_img)
	cv2.waitKey(0)
	c = c+1
for i in range(1000,1140):
	img = cv2.imread("cda/Diciembre/Video/-2018-mar-17-{:04d}.jpg".format(i))
	crop_img = img[0:880, 0:1920]
	cv2.imwrite("cda/Diciembre/Video/crops/{:04d}.jpg".format(c), crop_img)
	cv2.waitKey(0)
	c = c+1