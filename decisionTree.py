import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import sys

inputTable = 0
depth = 13
target = "Class"
testTable = 0
classList =[[]]
class Node:

    def __init__(self, depth, constraintVal={}):
        self.id ="leaf"
        self.depth = depth
        self.constraint = constraintVal
        self.child = {}
        self.classLabel = ""
    
    def get_classLabel(self):
        return self.classLabel

    def __iter__(self):
        return iter(self.child.values())

    def __repr__(self):
        return str(self.id)

    def add_neighbor(self, neighbor, depth=0, contraint={}):
        self.child[neighbor] = Node(depth, contraint)

    def get_connections(self):
        return self.child.values()

    def get_child(self,key):
            return self.child.get(key)

    def get_id(self):
        return self.id

    def get_depth(self):
        return self.depth

    def get_constraint(self):
        return self.constraint

    def get_weight(self, neighbor):
        if neighbor in self.child.keys():
            return self.child[neighbor]


def calcEntropy(a,b):
    ratio1 = float(a)/(a+b)
    ratio2 = float(b)/(a+b)
    entropy = math.log(ratio1,2)*ratio1+math.log(ratio2,2)*ratio2
    #print entropy
    return -entropy;

def findBestSplit(node):
    global target
    global inputTable
    constraints = node.constraint

    modifiedTable = inputTable
    if len(constraints.keys()) != 0:
        #print "inside if"
        modifiedTable = inputTable.loc[inputTable[constraints.keys()].
            apply(lambda x: x.tolist() == constraints.values(),axis=1)]
        for key in constraints:
            modifiedTable = modifiedTable.drop(key,1)

    outerdict = {}

    totalRows = len(modifiedTable.index)
    #print 'Total rows: ',totalRows
    for cols in modifiedTable:
        colname = cols;
        if colname == target:
            continue
        innerdict = {}
        for index, row in modifiedTable.iterrows():
            innerkey = row[cols]
            list=[0,0]
            if innerkey in innerdict:
                list = innerdict.get(innerkey)

            if row[target] == 'Yes' or row[target] == 'Y' or row[target] == 1:
                list[1]+=1
            else:
                list[0]+=1
            innerdict[innerkey]=list
        outerdict[colname]=innerdict

    minEntopy = 1       # initialize to 1 as 1 is maximum value that entropy can take
    getOneKey=True
    for key in outerdict:
        feature = key
        if getOneKey:
            getOneKey=False
        break

    #feature = outerdict.get
    for key,value in outerdict.iteritems():
        entropy = helper(value,totalRows)
        #print 'Attribute entropy',entropy
        if entropy < minEntopy:         # check for minEntropy
            minEntopy = entropy
            feature =  key

    return feature

def helper(innerdict,totalRows):
    attributeEntropy=0.0
    for item in innerdict.itervalues():
        c0=item[0];
        c1=item[1];
        if c0==0 or c1==0:
            continue;
        innertotal=c0+c1;
        innerEntropy = calcEntropy(c0,c1)
        attributeEntropy += (float(innertotal)/totalRows)*innerEntropy;
    return attributeEntropy

def CreateTable(path):
    data = pd.read_csv(path, sep=" ", header=None)
    data = data.dropna(1,'any', thresh=None, subset=None,inplace=False)
    somelist=['Class','A', 'B','C','D','E','F','G','H','I','J','K','L']
    data = pd.DataFrame(data)
    data.columns=somelist[0:len(data.columns)]
    data.drop(somelist[len(data.columns)-1], axis=1, inplace=True)
    return data

def getClassLabel(modifiedTable):
    c0=0
    c1=0
    yesVal =1
    noVal =0
    for index,row in modifiedTable.iterrows():
        if row[target] == 'Yes' or row[target] == 'Y' or row[target] == 1:
            c1+=1
        else:
            c0+=1

    value = modifiedTable.iloc[0][target]

    isString = False
    if value == "Yes" or value =="yes" or value=="no" or value == "No":
        isString = True

    if (c0 <= c1):
        if isString:
            return "Yes"
        return yesVal

    if isString:
        return "No"
    return noVal
#----------------------------------------------------------------------------------------------------------
#------------- Build the Tree-------------------------------------------
#-----------------------------------------------------------------------------------------------------------

def buildTree(node):
    global depth
    global inputTable
    classLabel = "Class"
    modifiedTable = inputTable
    nodeContraints = node.get_constraint()
    if len(nodeContraints.keys()) != 0:
        modifiedTable = inputTable.loc[inputTable[nodeContraints.keys()].apply(lambda x: x.tolist() == nodeContraints.values(),axis=1)]

    # Base case 1 : If Depth is reached, assign class label as ID;
    if node.get_depth() == depth:
            node.id = "leaf"
            node.classLabel =  getClassLabel(modifiedTable)
            return

    #Base case 2  All unique values in the record
    if len(pd.unique(modifiedTable[classLabel].values)) == 1:
        node.id = "leaf"
        node.classLabel =  getClassLabel(modifiedTable)
        return


    #Find best feature and their attributes
    feature = findBestSplit(node)
    node.id = feature
    attributes = pd.unique(modifiedTable[feature].values)

    #create children with the attribute list
    for attribute in attributes:
        toMerge = node.get_constraint()
        newConstraint = {}
        newConstraint[feature] = attribute
        newConstraint.update(toMerge)
        newDepth =  node.get_depth() + 1
        node.add_neighbor(attribute, newDepth, newConstraint)

    # Recursively build the children nodes
    for child in node.get_connections():
        buildTree(child)

#---------------------------------------------------------------------------------------------------
#------------------Traverse The Tree-------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def traverseTree(node):
    if node.id == "leaf":
	print node.get_classLabel()
        return
    print node.id
    for child in node:
        traverseTree(child)

#------------------------------------------------------------------------------------------------------
#--------------------------Get accuracy for plotting graph--------------------------------------------
#------------------------------------------------------------------------------------------------------

def getAccuracyRow(row, node):
    label = node.get_id()
    # Base condition when we hit leaf node
    if node.id == "leaf":
        classLabel = node.get_classLabel()
        return classLabel

    #Base case 2, when there is no training path available
    child = node.get_child(row[label])
    if child is None:
        if random.random()>0.5:
            return 1
        else:
            return 0

    return getAccuracyRow(row, child)


def getAccuracy(node):
    global classList
    countFalse = 0
    countTrue = 0
    total=0
    TP=0; TN=0; FP=0; FN=0
    for index, row in testTable.iterrows():
        myList = []
        myList.append(row['Class'])
        myList.append(getAccuracyRow(row, node))
        classList.append(myList)
    for items in classList:
        if items != []:
            if items[0] == items[1]:
                countTrue=countTrue+1
                total+=1
                if items[0] == 1:
                    TP+=1
                else:
                    TN+=1
            else:
                countFalse = countFalse+1
                total+=1
                if items[0] == 1:
                    FN+=1
                else:
                    FP+=1
    accuracy = float(countTrue)/total
    print "\n\n-------------Accuracy for depth",depth, " is:  " , accuracy*100
    print "\n"
    print "-----------Confusion matrix--------------"
    print "\n            PredictedNo       PredictedYes"
    print "\nActualNo      ",TN,"            ",FP
    print "\nActaulYes     ",FN,"            ",TP,"\n\n"
    return accuracy*100



#-------------------------------------------------------------------------------------------------------
#---------------Main function  --------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: decisionTree.py <depth> <trainFilePath> <testFilePath>"
        sys.exit(0)
    depth = sys.argv[1]
    inputTable = CreateTable(sys.argv[2])
    testTable = CreateTable(sys.argv[3])

    root = Node(0)
    buildTree(root)

    # Plot simple graph
    accuracyPlot =[]
    depthPlot = []
    for i in range(1,int(depth)):
        accuracyPlot.append(getAccuracy(root))
        depthPlot.append(i)

    plt.plot(depthPlot, accuracyPlot, 'ro')
    plt.axis([1, 16, 80, 83])
    plt.show()











