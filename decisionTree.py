
'''class Node:
    def __init__(self, node):
        self.id = "leaf"
	self.constraint = {}
        self.attributes = []
	self.child = {}
	self.label = ""  


    def __iter__(self):
        return iter(self.child.id())
   
    
    def __repr__(self):
        return str(self.id)

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        if neighbor in self.adjacent.keys():
            #print 'self.adjacent[neighbor %s =' % self.adjacent[neighbor]
            return self.adjacent[neighbor] '''

def find-best-split(inputTable, attributes[]):


def CreateTable():
	inputTable = []
	with open("/home/soumya/Desktop/Train_1.txt") as inFile:
		for line in inFile:
			row = {}
			k = line.split(" ")
			row['A'] = k[2]
			row['B'] = k[3]
			row['C'] = k[4]
			row['D'] = k[5]
			row['E'] = k[6]
			row['F'] = k[7]
			row['class'] = k[1]
			inputTable.append(row)
	return inputTable



if __name__ == '__main__':

	inputTable = CreateTable()
	print inputTable

			


	

	
	
