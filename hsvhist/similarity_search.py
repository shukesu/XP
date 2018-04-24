# "CBIR(Content-Base Image Retrieval)--Similarity and Search"  
import numpy as np  
# use for processing index.csv  
import csv  
  
class Searcher:  
    def __init__(self, indexPath):  
        self.indexPath = indexPath  

    def chi2_distance(self, histA, histB, eps=1e-10):  
        # compute the chi-squred distance  
        d = 0.5*np.sum([((a-b)**2)/(a+b+eps) for(a,b) in zip(histA,histB)])  
        return d               
  
    def search(self, queryFeatures, limit=10):  
        results = {}  
  
        # open the index file for reading  
        with open(self.indexPath) as f:  
            # initialize the CSV reader  
            reader = csv.reader(f)
  
            # loop over the rows in the index  
            for row in reader:  
                # parse out the imageID and features,  
                # then compute the chi-squared distance                  
                features = [float(x) for x in row[1:]]  
                d = self.chi2_distance(features, queryFeatures)  
                results[row[0]] = d  
            f.close()  
            results = sorted([(v,k) for (k,v) in results.items()])  
            return results[:limit] 