import pandas as pd
import math

inputTable = 0
depth = 3
target = "Class"

class Node:

    def __init__(self, depth, constraintVal={}):
        self.id = "leaf"
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

    #print modifiedTable
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
            c1 = "Yes"
        return c1

    if isString:
        c0 = "No"
        return c0
#----------------------------------------------------------------------------------------------------------
#------------- Build the Tree-------------------------------------------
#-----------------------------------------------------------------------------------------------------------

def buildTree(node):
    global depth
    global inputTable
    classLabel = "Class"
    # Base case 1 : If Depth is reached, assign class label as ID;
    if node.get_depth() == depth:
        modifiedTable = inputTable
        nodeContraints = node.get_constraint()
        if len(nodeContraints.keys()) != 0:
            modifiedTable = inputTable.loc[inputTable[nodeContraints.keys()].
            apply(lambda x: x.tolist() == nodeContraints.values(),axis=1)]
            node.classLabel =  getClassLabel(modifiedTable)
        return

    #Base case 2  All unique values in the record
    nodeContraints = node.get_constraint()
    if len(nodeContraints.keys()) != 0:
        modifiedTable = inputTable.loc[inputTable[nodeContraints.keys()].
            apply(lambda x: x.tolist() == nodeContraints.values(),axis=1)]

        if len(pd.unique(modifiedTable[classLabel].values)) == 1:
            node.classLabel =  getClassLabel(modifiedTable)
            return


    #Find best feature and their attributes
    feature = findBestSplit(node)
    print "Node id is " + feature
    node.id = feature
    attributes = pd.unique(inputTable[feature].values)

    #create children with the attribute list
    for attribute in attributes:
        toMerge = node.get_constraint()
        newConstraint = {}
        newConstraint[feature] = attribute
        newConstraint.update(toMerge)
        newDepth =  node.get_depth() + 1
        node.add_neighbor(attribute, newDepth, newConstraint)

    print "Constraint for " + node.get_id()
    print node.get_constraint()
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


#-------------------------------------------------------------------------------------------------------
#---------------Main function  --------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    inputTable = CreateTable("/home/soumya/Desktop/Train_1.txt")
    print inputTable
    root = Node(0)
    buildTree(root)

    print "Printing tree \n"
    traverseTree(root)














