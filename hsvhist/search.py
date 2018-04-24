# "CBIR(Content-Base Image Retrieval)--Search"  
import color_descriptor  
import similarity_search  
import argparse  
import cv2  
      
ap = argparse.ArgumentParser()  
ap.add_argument("-i", "--index", required=True, help="Path to where the computed index will be stored")  
      
ap.add_argument("-q", "--query", required=True, help="Path to query image")  
ap.add_argument("-r", "--result_path", required = True, help="Path to the result Path")  
args = vars(ap.parse_args())  
cd = color_descriptor.ColorDescriptor((8,12,3))  
      
# load the query image and describe it  
query = cv2.imread(args["query"])  
features = cd.describe(query)  
      
# perform the search  
searcher = similarity_search.Searcher(args["index"])  
results = searcher.search(features)  
      
# loop over the results  
for(score, resultID) in results:  
     # load the result image and display it  
    print(args["result_path"]+"/"+resultID)      
    result = cv2.imread(args["result_path"]+"/"+resultID)
    while 1:
        img_shape = result.shape
        if img_shape[0] > 1000 or img_shape[1] > 1000:
            result = cv2.resize(result, (int(img_shape[0]/2), int(img_shape[1]/2)))
        else:
            break
          
    cv2.imshow("Result",result)  
    cv2.waitKey(0)  