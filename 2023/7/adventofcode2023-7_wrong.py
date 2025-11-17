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

    weighted = unique*np.power(counts, 12)
    
    if len(weighted) == 1:
        help_5 = np.append(help_5, np.sum(weighted))
        idxs_5.append(ii)
    elif len(weighted) == 2:
        if 4 in counts:
            help_4 = np.append(help_4, np.sum(weighted))
            idxs_4.append(ii)
        else:
            help_23 = np.append(help_23, np.sum(weighted))
            idxs_23.append(ii)
    elif len(weighted) == 3:
        if 3 in counts:
            help_3 = np.append(help_3, np.sum(weighted))
            idxs_3.append(ii)
        else:
            help_22 = np.append(help_22, np.sum(weighted))
            idxs_22.append(ii)
    elif len(weighted) == 4:
        help_1 = np.append(help_1, np.sum(weighted))
        idxs_1.append(ii)

    else:
        help_0 = np.append(help_0, np.sum(weighted))
        idxs_0.append(ii)


idxs_4 = np.array(idxs_4)
idxs_23 = np.array(idxs_23)
idxs_3 = np.array(idxs_3)
idxs_22 = np.array(idxs_22)
idxs_1 = np.array(idxs_1)
idxs_0 = np.array(idxs_0)




bids_sorted = np.array([])

hands = np.append(hands, help_5)
bids_sorted = np.append(bids_sorted, bids[idxs_5])

l = len(bids_sorted)

sorted_i = np.argsort(help_4)[::-1]


bids_sorted = np.append(bids_sorted, bids[idxs_4[sorted_i]])
l = len(bids_sorted)

sorted_i = np.argsort(help_23)[::-1]

hands = np.append(hands, help_23[sorted_i])
bids_sorted = np.append(bids_sorted, bids[idxs_23[sorted_i]])
l = len(bids_sorted)

sorted_i = np.argsort(help_3)[::-1]

hands = np.append(hands, help_3[sorted_i])
bids_sorted = np.append(bids_sorted, bids[idxs_3[sorted_i]])
l = len(bids_sorted)

sorted_i = np.argsort(help_22)[::-1]

hands = np.append(hands, help_22[sorted_i])
bids_sorted = np.append(bids_sorted, bids[idxs_22[sorted_i]])
l = len(bids_sorted)

sorted_i = np.argsort(help_1)[::-1]

hands = np.append(hands, help_1[sorted_i])
bids_sorted = np.append(bids_sorted, bids[idxs_1[sorted_i]])
l = len(bids_sorted)

sorted_i = np.argsort(help_0)[::-1]

hands = np.append(hands, help_0[sorted_i])
bids_sorted = np.append(bids_sorted, bids[idxs_0[sorted_i]])
l = len(bids_sorted)

order_range = np.arange(1, len(bids_sorted)+1)[::-1]

bids_sorted = np.array(bids_sorted)
result = bids_sorted@order_range
print(result)
