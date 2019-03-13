'''
@author: MilikSmith76

Description: Performs apriori algorithm on transactions of a given file.
'''

from math import factorial

"""
Class for determining the confidence of rules and sorting them from highest confidence to lowest confidence.
"""


class RuleConfidence:
    """
    Parameters:
        - x(set of string): The itemset that will be correlate with another item.
        - y(string): The item that should appear when the itemset does.
        - xCount(int): The number of times the itemset appears in a transaction.
        - yCount(int): The number of times the item appears when the itemset is present in a transaction.
    """

    def __init__(self, x, y, xCount, yCount):
        self.x = x
        self.y = y
        self.confidence = yCount / xCount

    def __eq__(self, other):
        if type(other) is RuleConfidence:
            xFlag = self.x == other.x
            yFlag = self.y == self.y
            cFlag = self.confidence == other.confidence
            return xFlag and yFlag and cFlag
        else:
            return False

    def __gt__(self, other):
        flag = False
        if type(other) is RuleConfidence:
            if self.confidence > other.confidence:
                flag = True
            elif self.confidence == other.confidence:
                index = 0
                loopFlag = True
                self_list = list(self.x)
                self_list.sort()
                other_list = list(other.x)
                other_list.sort()
                while index < len(self.x) and loopFlag:
                    if self_list[index] < other_list[index]:
                        flag = True
                        loopFlag = False
                    elif self_list[index] > other_list[index]:
                        loopFlag = False
                    index += 1
                if self.y < other.y and loopFlag and index >= len(self.x):
                    flag = True
        return flag

    def __lt__(self, other):
        return not self.__gt__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __repr__(self):
        self_list = list(self.x)
        self_list.sort()
        self_list_string = "{"
        for i in self_list:
            if i != self_list[0]:
                self_list_string += ", {}".format(i)
            else:
                self_list_string += "{}".format(i)
        self_list_string += "}"
        return "{} -> {}: {:f}".format(self_list_string, self.y, self.confidence)


"""
Description: Performs apriori on transactions in a given file, and prints out confidences for frequent rules
Parameters:
    - fileName(String): The name of the file to be searched for associations
    - frequent(int): The number of times an itemset has to appear in transactions to be frequent
    - maxSize(int): The max number of items to appear in an itemset
Return:
    - frequentDictionary (Dictionary): A dictionary containing keys for all maxSize-itemsets, with the corresponding value being a list(0 - combination#, 1 - support) 
    - prevFrequentDictionary (Dictionary): A dictionary containing keys for all (maxSize - 1)-itemsets, with the corresponding value being a list(0 - combination#, 1 - support)
"""


def apriori(fileName, frequent, maxSize):
    transactions = []
    # the values in frequentDictionary are represent as [number of combinations that create this itemset, support of itemset]
    frequentDictionary = {}

    # Reads the file and gets the transactions
    with open(fileName, "r") as transactionFile:
        for line in transactionFile:
            lineItems = set(line.split())
            transactions.append(lineItems)

    # Gets each individual item's support
    print("Getting each individual item's support")
    for transaction in transactions:
        for item in transaction:
            if frequentDictionary.get((item,)) is None:
                frequentDictionary[(item,)] = [1, 1]
            else:
                frequentDictionary[(item,)][1] += 1

    # Remove items that are not frequent from the frequent item dictionary
    for key, value in list(frequentDictionary.items()):
        if value[1] < frequent:
            del frequentDictionary[key]

    if maxSize < 1:
        return None, None
    elif maxSize == 1:
        return frequentDictionary, None

    itemsetSize = 1

    # Loops until the frequent maxSize-itemsets are found
    while itemsetSize < maxSize:
        itemsetSize += 1
        prevFrequentDictionary = frequentDictionary
        frequentDictionary = {}

        # Getting the frequent (groupsize-1)-itemsets
        itemsets = [set(itemset) for itemset in prevFrequentDictionary.keys()]

        # Creating all possible frequent groupsize-itemsets by combining the frequent (groupsize-1)-itemsets
        position = 1
        print("Creating all potential frequent {}-itemsets".format(itemsetSize))
        for i in itemsets[0:-1]:
            for j in itemsets[position:]:
                newGroup = i.union(j)
                if len(newGroup) == itemsetSize:
                    newGroup = tuple(sorted(newGroup))
                    if frequentDictionary.get(newGroup) is None:
                        frequentDictionary[newGroup] = [1, 0]
                    else:
                        frequentDictionary[newGroup][0] += 1
            position += 1

        # Finding each potential frequent itemset's support
        print("Finding support of potential frequent {}-itemsets".format(itemsetSize))
        combinations = factorial(itemsetSize) / (factorial(2) * factorial(itemsetSize - 2))
        for key in frequentDictionary.keys():
            if frequentDictionary[key][0] == combinations:
                itemset = set(key)
                for transaction in transactions:
                    if itemset.issubset(transaction):
                        frequentDictionary[key][1] += 1

        # Remove itemsets that are not frequent
        for key, value in list(frequentDictionary.items()):
            if value[1] < frequent:
                del frequentDictionary[key]

        print()

    return frequentDictionary, prevFrequentDictionary


"""
Main script
"""
# frequentDictionary, prevFrequentDictionary = apriori("testing.txt", 3, 3)
frequentDictionary, prevFrequentDictionary = apriori("testing2.txt", 3, 3)

# Determining frequent rules and their confidence
itemsetList = []
for itemset in frequentDictionary.keys():
    for item in itemset:
        x = sorted(set(itemset) - {item})
        itemsetList.append(RuleConfidence(x, item, prevFrequentDictionary[tuple(x)][1], frequentDictionary[itemset][1]))

# Print the rules for all frequent itemsets
print("Frequent Rules:")
itemsetList.sort(reverse=True)

# # Print the top 5 rules
# for i in range(0,5):
#     if i < len(itemsetList):
#         print(itemsetList[i])

# Print all the rules
for i in itemsetList:
    print(i)
print()
