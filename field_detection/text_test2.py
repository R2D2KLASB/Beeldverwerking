# Import required packages
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

# Read image from which text needs to be extracted
image = cv2.imread("A1.png")
# image = cv2.imread("new_board2.jpg")
# image = cv2.imread("board_clean.png")
 
# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
blur = cv2.GaussianBlur(gray,(5,5),0)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

cv2.imshow('thresh', thresh1)
cv2.waitKey()
# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

cv2.imshow('thresh', dilation)
cv2.waitKey()

# Finding contours
contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_image = cv2.drawContours(image = image.copy(), contours = contours, contourIdx = -1, color = (0, 255, 0), thickness = 1)

cv2.imshow("Board", contour_image)
cv2.waitKey()

# Creating a copy of image
im2 = thresh1.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
	x, y, w, h = cv2.boundingRect(cnt)
	
	# Drawing a rectangle on copied image
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	# Cropping the text block for giving input to OCR
	cropped = im2[y:y + h, x:x + w]
	# cv2.imshow('thresh', cropped)
	# cv2.waitKey()
	# Open the file in append mode
	file = open("recognized.txt", "a")
	
	# Apply OCR on the cropped image
	text = pytesseract.image_to_string(cropped)
	
	# Appending the text into file
	file.write(text)
	file.write("\n")
	
	# Close the file
	file.close
