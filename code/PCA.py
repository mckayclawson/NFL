from matplotlib.mlab import PCA
from sklearn.decomposition import PCA as sPCA
import csv
import math
import numpy as np

def loadDataset(filename, testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)[2:]
        for x in range(len(dataset)-1):
            #print "before: ",dataset[x]
            #convert columns from str to float
            for y in [3,5,6,7,8,9,10,11,12,13,21,22,27]:
                try:
                    #normalize the age value to the average age of a starting NFL QB(28)
                    if y == 3:
                        dataset[x][y] = int(dataset[x][y]) - 28
                        #convert integer fields to integers
                    elif y == 5 or y == 7 or y == 8 or y == 10 or y == 11 or y == 12 or y == 22 or y == 27:
                        dataset[x][y] = int(dataset[x][y])
                    #convert the QBR to float
                    elif y == 21:
                        dataset[x][y] = float(dataset[x][y])
                    #convert percentages from strings to floats
                    elif y == 9 or y == 11:
                        tempStr = dataset[x][y].strip('%')
                        tempFloat = float(tempStr)
                        tempResult = tempFloat/100
                        dataset[x][y] = tempResult
                    #convert QB-Record into win loss ratio
                    elif y == 6:
                        tempStr = dataset[x][y].split('-')
                        winPerc = float(tempStr[0])/(float(tempStr[0]) + float(tempStr[1]))
                        dataset[x][y] = winPerc
                    #convert the avg-pick number into a round number for use as the target variable
                    elif y == 29:
                        tempInt = int(dataset[x][y])
                        dataset[x][y] = tempInt/10
                except ValueError:
                    continue

            #print "after: ", dataset[x]
            dataset[x] = dataset[x][3:]
            dataset[x] = dataset[x][:-1]
            temp1 = dataset[x][:3]
            temp2 = dataset[x][4:]
            dataset[x] = temp1 + temp2
            for y in range(0,len(dataset[x])):
                if(dataset[x][y] == ''):
                    dataset[x][y] = 0
                dataset[x][y] = float(dataset[x][y])
            testSet.append(dataset[x])


def main():
    testSet = []
    loadDataset('../data/years_2013_passing_passing.csv', testSet)
    dataMatrix =  np.array(testSet)
    dataMatrix.astype(float)


    #cov_mat = np.cov(dataMatrix)
    #print dataMatrix.shape," cov ",cov_mat.shape,  " len: ", len(cov_mat)

    #vals = np.linalg.eigvals(dataMatrix)
    #print vals, " len ", len(vals)
    #eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)
    #print eig_val_cov[0], " len ", len(eig_val_cov)
    #eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]

    #eig_pairs = sorted(eig_pairs, key=lambda entry: entry[0], reverse=True)
    #print "len ", len(eig_pairs)
    #for i in eig_pairs:
    #    print(i[0])

    #print(dataMatrix[0])
    '''
    pca = sPCA(n_components=26)
    pca.fit(dataMatrix)
    #PCA(n_components=26, whiten=False)
    print(pca.explained_variance_ratio_)
    sum = 0.0
    for i in range(0,len(pca.explained_variance_ratio_)):
        sum+= pca.explained_variance_ratio_[i]
        print "{0:.10f}".format(pca.explained_variance_ratio_[i])
    '''    



    
    myPCA = PCA(dataMatrix)
    print "The EigenVectors are: \n", myPCA.Wt, " len: ", len(myPCA.Wt) 
    sum = 0.0
    for i in range(0,len(myPCA.fracs)):
        sum+= myPCA.fracs[i]
        print "{0:.3f}".format(myPCA.fracs[i])
    print sum
    print myPCA.fracs, " len ", len(myPCA.fracs)



main()
