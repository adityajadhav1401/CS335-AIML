from array import array
from cluster import distance_euclidean as distance
import argparse

########################################################################
#                              Task 5                                  #
########################################################################


def read_image(filename):
	'''
	File format: PPM image or PGM image

	Returns image as a 3D list of size [h,w,3] if rgb image and 2D list of size [h,w] if grayscale image

	[Empty RGB image as 3D list] -- img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]
	[Empty grayscale image as 2D list] -- img = [[0 for _ in range(width)] for _ in range(height)]
	'''
	img = None
	# todo: task5
	# Here you need to read the file, and convert the data into a 3D or 2D list depending on the image type.
	# If first 2 bytes of the file are 'P6', it's an RGB image and if first 2 bytes are 'P5', it's a grayscale image.
	# After that, there are 2 numbers written as strings which correspond to the width and height of the image
	# Then there is one more number written as string which corresponds to the max. value of a pixel in the image (not really required here)
	# Afterwards, all data in the file corresponds to the actual image.
	# You can read the data byte by byte and update corresponding element of 'img' variable.
	# For more information on PPM and PGM file formats, refer to the link mentioned in the assignment document.
	
	f = open(filename,'r')
	# Line1 : MagicNum
	# Line2 : Width Height
	# Line3 : Max Gray level
	# Read header information
	count = 0
	while count < 3:
		line = f.readline()
		if line[0] == '#': continue # Ignore comments
		count = count + 1

		if count == 1: 				# Magic num info
			magicNum = line.strip()
		
		if magicNum != 'P5' and magicNum != 'P6':
			f.close()
			print("Not P5/P6 PGM format") 
			exit()

		elif count == 2: 			# Width and Height
			[width, height] = (line.strip()).split()
			width = int(width)
			height = int(height)

		elif count == 3: 			# Max gray level
			maxVal = int(line.strip())

	# Read pixels information
	if (magicNum == 'P5'):
		img = []
		buf = f.read()
		elem = [ord(val) for val in buf]
		if len(elem) != width*height:
			print 'Error in number of pixels'
			exit()
		for i in range(height):
			tmpList = []
			for j in range(width):
				tmpList.append(elem[i*width+j])
			img.append(tmpList)

	elif (magicNum == 'P6'):
		img = []
		buf = f.read()
		elem = [ord(val) for val in buf]
		if len(elem) != width*height*3:
			print 'Error in number of pixels'
			exit()
		for i in range(height):
			tmpList = []
			for j in range(width):
				tmpList.append([elem[(i*width+j)*3],elem[(i*width+j)*3+1],elem[(i*width+j)*3+2]])
			img.append(tmpList)
	return img


def preprocess_image(img):
	'''
	Transforms image into format suitable for clustering.

	Returns data - a list of datapoints where each datapoint is a tuple
	'''
	data = [(None,None,None)]
	# todo: task5
	# You need to convert the image such that data is a list of datapoints on which you want to do clustering and each datapoint in the list is a 3-tuple with RGB values.
	
	data = []
	for row in img: 
		for elem in row: 
			data.append(tuple([float(i) for i in elem]))
	
	return data


########################################################################
#                              Task 6                                  #
########################################################################


def label_image(img, cluster_centroids):
	'''
	img: RGB image as 3D list of size [h,w,3]

	Return a 2D matrix where each point stores the nearest cluster centroid of corresponding pixel in the image
	[Empty 2D list] -- labels = [[0 for _ in range(width)] for _ in range(height)]
	'''

	cluster_labels = None
	# todo: task6
	# Iterate over the image pixels and replace each pixel value with cluster number corresponding to its nearest cluster centroid

	cluster_labels = []
	for row in img:
		tmpList = []
		for elem in row:
			nearest = 0
			min_dist = float('Inf')

			for i in range(len(cluster_centroids)):
				centroid = cluster_centroids[i]
				d = distance(tuple(elem),tuple(centroid))
				if (d < min_dist): 
					min_dist = d
					nearest = i

			tmpList.append(nearest)

		cluster_labels.append(tmpList)

	return cluster_labels


def write_image(filename, img):
	'''
	img: 3D list of size [h,w,3] if rgb image and 2D list of size [h,w] if grayscale image

	File format: PPM image if img is rgb and PGM if image is grayscale
	'''
	# todo: task6
	# Create a new file with the given file name (assume filename already includes extension).
	# First line in the file should contain the format code - P5 for grayscale (PGM) and P6 for RGB (PPM)
	# Next line should contain the width and height of the image in format - width height
	# Next line should contain the maximum value of any pixel in the image (use max function to find it). Note that this should be an integer and within (0-255)
	# Next line onwards should contain the actual image content as per the binary PPM or PGM file format.

	out = ""

	if (isinstance(img[0][0],int)): out += 'P5\n'
	else : out += 'P6\n'

	out += str(len(img[0])) + ' ' + str(len(img)) + '\n'

	if (isinstance(img[0][0],int)): out += str(int(max(max(img)))) + '\n'
	else : out += str(int(max(max(max(img))))) + '\n'

	flat_img = []
	if (isinstance(img[0][0],int)):
		for row in img:
			for ele in row:
				flat_img.append(int(ele))
	else:
		for row in img:
			for ele in row:
				for i in ele:
					flat_img.append(int(i))

	fp = open(filename,'wb')
	fp.write(out)
	fp.write(bytearray(flat_img))
	fp.close()
	


########################################################################
#                              Task 7                                  #
########################################################################


def decompress_image(cluster_labels, cluster_centroids):
	'''
	cluster_labels: 2D list where each point stores the nearest cluster centroid of corresponding pixel in the image
	cluster_centroids: cluster centroids

	Return 3D list of size [h,w,3] if rgb image and 2D list of size [h,w] if grayscale image
	[Empty RGB image as 3D list] -- img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]
	'''

	img = None
	# todo: task7
	# Iterate over the 2D list's elements and replace each value (cluster label) with value of its corresponding cluster centroid
	# Use distance function (using distance from cluster.py to find the nearest cluster)

	img = []
	for row in cluster_labels:
		tmpList = []
		for ele in row:
			if(isinstance(cluster_centroids,float)):
				tmpList.append(int(cluster_centroids[ele]))
			else:
				tmpList.append([int(i) for i in cluster_centroids[ele]])
		img.append(tmpList)

	return img


########################################################################
#                       DO NOT EDIT THE FOLLWOING                      #
########################################################################


def readfile(filename):
	'''
	File format: Each line contains a comma separated list of real numbers, representing a single point.
	Returns a list of N points, where each point is a d-tuple.
	'''
	data = []
	with open(filename, 'r') as f:
		data = f.readlines()
	data = [tuple(map(float, line.split(','))) for line in data]
	return data


def writefile(filename, points):
	'''
	points: list of tuples
	Writes the points, one per line, into the file.
	'''
	if filename is None:
		return
	with open(filename, 'w') as f:
		for m in points:
			f.write(','.join(map(str, m)) + '\n')
	print 'Written points to file ' + filename


def parse():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest='command')

	preprocess_parser = subparsers.add_parser('preprocess')
	preprocess_parser.add_argument(dest='image', type=str, help='Image filename (ppm)')
	preprocess_parser.add_argument('-o', '--output', dest='output', default='image_data.csv', type=str, help='Output Data filename (csv). Default: image_data.csv')

	compress_parser = subparsers.add_parser('compress')
	compress_parser.add_argument(dest='image', type=str, help='Image filename (ppm)')
	compress_parser.add_argument(dest='centroids', type=str, help='Cluster centroids (csv)')
	compress_parser.add_argument('-o', '--output', dest='output', default='labels.pgm', type=str, help='Output Image filename (pgm). Default: labels.pgm')

	decompress_parser = subparsers.add_parser('decompress')
	decompress_parser.add_argument(dest='labels', type=str, help='Labels filename (pgm)')
	decompress_parser.add_argument(dest='centroids', type=str, help='Cluster centroids (csv)')
	decompress_parser.add_argument('-o', '--output', dest='output', default='decompressed.ppm', type=str, help='Output Image filename (ppm). Default: decompressed.ppm')

	return parser.parse_args()


if __name__ == '__main__':

	args = parse()
	if args.command == 'preprocess':
		img = read_image(args.image)
		data = preprocess_image(img)
		writefile(args.output, data)
	elif args.command == 'compress':
		img = read_image(args.image)
		centroids = readfile(args.centroids)
		cluster_labels = label_image(img, centroids)
		write_image(args.output, cluster_labels)
	else:
		cluster_labels = read_image(args.labels)
		centroids = readfile(args.centroids)
		img = decompress_image(cluster_labels, centroids)
		write_image(args.output, img)
