import csv
import numpy as np


rows = []
with open('7/data.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        rows.append(row)


hands = np.array([])
bids = np.array([])


help_5 = np.array([])
help_4 = np.array([])
help_23 = np.array([])
help_3 = np.array([])
help_22 = np.array([])
help_1 = np.array([])
help_0 = np.array([])

idxs_5 = []
idxs_4 = []
idxs_23 = []
idxs_3 = []
idxs_22 = []
idxs_1 = []
idxs_0 = []

idxs = []

for ii, row in enumerate(rows):
    bids = np.append(bids, int(row[1]))

    cards = [x for x in row[0]]
    card_int = np.array([])
    for idx, card in enumerate(cards):

        if card == 'A':
            card_int = np.append(card_int, 14)
        elif card == 'K':
            card_int = np.append(card_int, 13)
        elif card == 'Q':
            card_int = np.append(card_int, 12)
        elif card == 'J':
            card_int = np.append(card_int, 11)
        elif card == 'T':
            card_int = np.append(card_int, 10)
        else:
            card_int = np.append(card_int, int(card))
        
    unique, counts = np.unique(card_int, return_counts=True) 

    

    