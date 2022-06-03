import sys


# contains function to split data array into a train (90%) and test (10%) set
# [in] data dataset in a list
# [out] train training set in a list
# [out] test test set in a list
def split_dataset(data):
    if not isinstance(data, list):
        print("Error passed data to function split data set does not have type list!")
        sys.exit(1)

    train = []
    test = []

    for i in range(len(data)):
        if i % 10 == 0:
            test.append(data[i])
        else:
            train.append(data[i])

    return train, test
