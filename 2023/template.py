import csv
import numpy as np
rows = []
with open('5/data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        rows.append(row)

for idx, row in enumerate(rows):

    
