Run on python as "py main.py"

Needs directories '../Images/' & '../Results/' , similar to the paths for the assignments done in class

Required Libraries:
	cv2
	numpy
	matplotlib.pyplot
	os

Images in image folder should be named 'image_0N' where N is its image number

Constants in program:
	N - (int) image number to apply effect to
	H - (int > 0) how large to make the depth of field
	F - (int > H/2) how drastic the blurriness should be

After program is run you are prompted with a diagram of the image,
left-click a spot on the image where you would like the focus plane to be

Images taht were taken above the subject and slightly angled produce the best results