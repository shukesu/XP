"CBIR(Content-Base Image Retrieval)--Extract Features and Indexing"
import color_descriptor
import argparse
import glob
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Path to the directory that cntains the images to be indexed")
ap.add_argument("-i", "--index", required=True, help="Path to where the computed index will be stored")
args = vars(ap.parse_args())
cd = color_descriptor.ColorDescriptor((8,12,3))

#Open the output index file for writing
output = open(args["index"],"w")

# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"]+"/*.jpg"):
    # extract the image ID from the image
    imageID = imagePath[imagePath.rfind("/")+1:]
    image = cv2.imread(imagePath)

    # describe the image
    features = cd.describe(image)

    # write feature to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" %(imageID,",".join(features)))
# close index file
output.close()
