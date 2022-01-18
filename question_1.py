import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# -----Question 1: Part A-----

# Recreating problematic calculation

data = pd.DataFrame(pd.read_csv("dataset.csv"))

print('Question 1 - Part A')
print('Naive calculation of AOV: ', end='')
print(sum(data['order_amount']) / len(data))  # Naive calculation of AOV (returns $3145.13)


# Removing outlier data

def outliers(values):
    outlier_idxs = []
    thres = 0.4
    mean = np.mean(values)
    std = np.std(values)
    idx = 0

    for x in values:
        z_score = (x - mean) / std
        if np.abs(z_score) > thres:
            outlier_idxs.append(idx)
        idx += 1
    return outlier_idxs


data2 = data[~data.index.isin(outliers(data['order_amount']))]  # Removing outliers from data
print('AOV after processing: ', end='')
print(sum(data2['order_amount']) / len(data2))  # Printing new AOV (returns $302.58, which is a reasonable value)
print()

# -----Question 1: Part B-----

data = data2
data['item_cost'] = data['order_amount'] / data[
    'total_items']  # Calculating item cost using mean, since only one unique item is being sold.

# Aggregating revenue for different individual item costs. Using buckets to smooth data.

itemCountsForPrice = {}

bucketSize = 5

for idx, row in data.iterrows():
    itemCost = round(row['item_cost'] / bucketSize) * bucketSize
    if itemCost not in itemCountsForPrice:
        itemCountsForPrice[itemCost] = row['order_amount']
    else:
        itemCountsForPrice[itemCost] += row['order_amount']

plt.bar(list(itemCountsForPrice.keys()), list(itemCountsForPrice.values()))
plt.show()

# As seen from the graph, there is a range of optimal item prices, where the revenue generated is highest. Thus,
# a metric showing the optimal item price would be very helpful to sellers. Obviously, when showing the data to
# sellers we must ensure that the data the analysis is performed on includes only data from their store,
# and not other sellers' stores.

# -----Question 1: Part C-----

# Smoothing data using moving average

sortedPrices = sorted(itemCountsForPrice.keys())

windowSize = 5

windowKeys = [0] + (sortedPrices[0:windowSize])
maverage = []

for x in range(windowSize, len(sortedPrices) - (windowSize + 1)):
    windowKeys.append(sortedPrices[windowSize + x])
    del windowKeys[0]

    windowVals = []

    for y in windowKeys:
        windowVals.append(itemCountsForPrice[y])

    maverage.append(np.mean(windowVals))

print('Question 1 - Part C')
print("Optimal item pricing: $", end='')
print(sortedPrices[maverage.index(
    max(maverage)) + windowSize])  # Finding optimal item price by finding item pricing with highest revenue
