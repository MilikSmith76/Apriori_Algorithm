# Apriori Algorithm

An example of how the apriori can be implemented using python.

## How to use

The method apriori(fileName, frequent, maxSize) takes three parameters fileName, frequent, maxSize and returns two dictionaries.

## Parameters

|Name | Datatype | What is it|
|------|-----------|----------------------|
| fileName | String | The name of the file to be used |
| frequent | Integer | The minimum support to be frequent |
| maxSize | Integer | The frequent k-itemset to be found |

## Return

The first dictionary returned contains the support of the frequent maxSize-itemset, the next dictionary contains the support of the frequent (maxSize - 1)-itemset. The dictionaries follow this format:
* keys: A frequent itemset
* values: A list containing the itemset combinations (not really useful), then itemset support. [combinations, support].

