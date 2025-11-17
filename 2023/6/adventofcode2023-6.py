import csv
import numpy as np

def first():
    rows = []
    with open('6/data.csv', newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=' ')
        for row in spamreader:
            rows.append(row)

    time = [int(i) for i in rows[0] if i.isnumeric()]
    distance = [int(i) for i in rows[1] if i.isnumeric()]

    time = np.array(time)
    distance = np.array(distance)

    # Using the quadratic formula to solve where the function
    # x*(time-x) >= distance equals to 0

    plus = (time + np.sqrt(np.power(time, 2) - 4*distance))/2
    print(plus)

    minus = (time - np.sqrt(np.power(time, 2) - 4*distance))/2

    print(minus)
    
    # Rounding the boundaries 
    result_arr = np.floor(plus)-np.ceil(minus)+1
    result = np.prod(result_arr)
    print(f'Task 1 result: {result}\n')


def second():
    rows = []
    with open('6/data.csv', newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=' ')
        for row in spamreader:
            rows.append(row)

    time = [i for i in rows[0] if i.isnumeric()]
    distance = [i for i in rows[1] if i.isnumeric()]

    time = int(''.join(time))
    distance = int(''.join(distance))

    plus = (time + np.sqrt(np.power(time, 2) - 4*distance))/2

    print('Boundaries: ')
    print(plus)

    minus = (time - np.sqrt(np.power(time, 2) - 4*distance))/2

    print(minus)

    result = np.floor(plus) - np.ceil(minus) + 1
    
    print(f'Task 2 result: {result}')
if __name__=='__main__':
    first()
    second()