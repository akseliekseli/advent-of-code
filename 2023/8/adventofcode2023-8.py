import csv
import numpy as np

def first():
    rows = []
    with open('8/data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')
        for row in spamreader:
            rows.append(row)

    leftright = rows[0][0]
    
    idx = 0
    nodes = {}
    for idx, row in enumerate(rows[2:]):
        
        new_node = row[0]

        l_node = ''.join(e for e in row[2] if e.isalnum())
        r_node = ''.join(e for e in row[3] if e.isalnum())

        nodes[new_node] = (l_node, r_node)

    idx = 0
    num_steps = 0
    current_node = 'AAA'
    if idx == len(leftright):
        idx = 0
    if leftright[0] == 'L':
        next_node = nodes[current_node][0]
    elif leftright[0] == 'R':
        next_node = nodes[current_node][1]
    current_node = next_node
    idx += 1
    num_steps += 1

    while current_node != 'ZZZ':
        if idx == len(leftright):
            idx = 0
        if leftright[idx] == 'L':
            next_node = nodes[current_node][0]
        elif leftright[idx] == 'R':
            next_node = nodes[current_node][1]

        current_node = next_node
        idx += 1
        num_steps += 1

    print(f'Result 1: {num_steps}')


def second():
    '''
    Calculating how long it takes to get from each starting node to end and
    then taking the least common multiple of them. (When all the
    processes finished at the same time?)
    '''

    rows = []
    # Can be also tested with test-2. It is extended version of the test data
    with open('8/data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')
        for row in spamreader:
            rows.append(row)

    leftright = rows[0][0]
    
    idx = 0
    nodes = {}
    for idx, row in enumerate(rows[2:]):
        
        new_node = row[0]

        l_node = ''.join(e for e in row[2] if e.isalnum())
        r_node = ''.join(e for e in row[3] if e.isalnum())

        nodes[new_node] = (l_node, r_node)

    start_nodes = [key for key in nodes.keys() if key[2]=='A']
    all_steps = []
    print(start_nodes)

    for node in start_nodes:
         
        idx = 0
        num_steps = 0
        current_node = node
        if idx == len(leftright):
            idx = 0
        if leftright[0] == 'L':
            next_node = nodes[current_node][0]
        elif leftright[0] == 'R':
            next_node = nodes[current_node][1]
        current_node = next_node
        idx += 1
        num_steps += 1

        while current_node[2] != 'Z':
            if idx == len(leftright):
                idx = 0
            if leftright[idx] == 'L':
                next_node = nodes[current_node][0]
            elif leftright[idx] == 'R':
                next_node = nodes[current_node][1]

            current_node = next_node
            idx += 1
            num_steps += 1
        all_steps.append(num_steps)
    
    print(f'All steps {all_steps}')
    lowest_com_multiple = np.lcm.reduce(all_steps)
    print(f'Result {lowest_com_multiple}')



def second_old():
    rows = []
    with open('8/data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')
        for row in spamreader:
            rows.append(row)

    leftright = rows[0][0]
    
    idx = 0
    nodes = {}
    for idx, row in enumerate(rows[2:]):
        
        new_node = row[0]

        l_node = ''.join(e for e in row[2] if e.isalnum())
        r_node = ''.join(e for e in row[3] if e.isalnum())

        nodes[new_node] = (l_node, r_node)

    
    start_nodes = [key for key in nodes.keys() if key[2]=='A']
    all_steps = []
    print(start_nodes)

    current_node = start_nodes
    idx = 0
    num_steps = 0
    if idx == len(leftright):
        idx = 0
    if leftright[0] == 'L':
        next_node = [nodes[key][0] for key in current_node]
    elif leftright[0] == 'R':
        next_node = [nodes[key][1] for key in current_node]
    current_node = next_node
    idx += 1
    num_steps += 1

    while not all(n[2]=='Z' for n in current_node):

        if idx == len(leftright):
            idx = 0
        if leftright[idx] == 'L':
            next_node = [nodes[key][0] for key in current_node]
        elif leftright[idx] == 'R':
            next_node = [nodes[key][1] for key in current_node]

        current_node = next_node
        idx += 1
        num_steps += 1
        
        print(num_steps)

    all_steps.append(num_steps)







if __name__== '__main__':
    first()
    second()
