from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2




# create a named tuple which we can use to create locations of the
# input document which we wish to OCR
OCRLocation = namedtuple("OCRLocation", ["id", "bbox",
	"filter_keywords"])
# define the locations of each area of the document we wish to OCR
OCR_LOCATIONS = [
	OCRLocation("first_name", (436, 510, 240, 30),
		["This", "is", "to", "certify" , "that"]),
	# OCRLocation("Date_of_birth", (340, 793, 125, 50),
	# 	["date", "of" , "birth"]),
	OCRLocation("sub1", (166, 876, 250, 30),
		[]),
	OCRLocation("sub1_marks", (500, 876, 70, 50),
		[]),
	OCRLocation("sub2", (166, 900, 250, 30),
		[]),
	OCRLocation("sub2_marks", (500, 900, 50, 50),
		[]),
	OCRLocation("sub3", (166, 940, 250, 30),
		[]),
	OCRLocation("sub3_marks", (500, 940, 50, 50),
		[]),
	OCRLocation("sub4", (166, 980, 250, 30),
		[]),
	OCRLocation("sub4_marks", (500, 980, 50, 50),
		[]),
	OCRLocation("sub5", (166, 1020, 250, 30),
		[]),
	OCRLocation("sub5_marks", (500, 1020, 50, 50),
		[]),
]

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def doOCR(image):
	print("[INFO] loading images...")
	try:
		aligned = cv2.imread(image)
	# template = cv2.imread(args["template"])
	# # align the images
	# print("[INFO] aligning images...")
	# aligned = align_images.align_images(image, template)
	except:
		print("[Error] Can not read Image")
		return -1
	# initialize a results list to store the document OCR parsing results


	print("[INFO] OCR'ing document...")
	parsingResults = []
	# loop over the locations of the document we are going to OCR
	for loc in OCR_LOCATIONS:
		# extract the OCR ROI from the aligned image
		(x, y, w, h) = loc.bbox
		roi = aligned[y:y + h, x:x + w]
		# OCR the ROI using Tesseract
		try:
			rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
		except:
			print("[Error]: Image format not correct")
			return -1
		text = pytesseract.image_to_string(rgb)
		

		# break the text into lines and loop over them
		for line in text.split("\n"):
			# if the line is empty, ignore it
			if len(line) == 0:
				continue
			# convert the line to lowercase and then check to see if the
			# line contains any of the filter keywords (these keywords
			# are part of the *form itself* and should be ignored)
			lower = line.lower()
			count = sum([lower.count(x) for x in loc.filter_keywords])
			# if the count is zero then we know we are *not* examining a
			# text field that is part of the document itself (ex., info,
			# on the field, an example, help text, etc.)
			print(count)
			if count == 0:
				
				# update our parsing results dictionary with the OCR'd
				# text if the line is *not* empty
				parsingResults.append((loc, line))



	# initialize a dictionary to store our final OCR results
	results = {}
	# loop over the results of parsing the document
	for (loc, line) in parsingResults:
		# grab any existing OCR result for the current ID of the document
		r = results.get(loc.id, None)
		# if the result is None, initialize it using the text and location
		# namedtuple (converting it to a dictionary as namedtuples are not
		# hashable)
		if r is None:
			results[loc.id] = (line)
		# otherwise, there exists an OCR result for the current area of the
		# document, so we should append our existing line
		else:
			# unpack the existing OCR result and append the line to the
			# existing text
			print(r)
			existingText = r
			text = "{}\n{}".format(existingText, line)
			# update our results dictionary
			print(loc)
			results[loc.id] = (text)
	
	if(len(results)==0):
		print("[Error]: No data")
		return -1

	results["status"] = "Doc Read Successfully"
	return results

def reader(image):
	return doOCR(image)