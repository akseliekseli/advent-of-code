import csv
import numpy as np


def parse_data():
    rows = []
    with open('5/test.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')
        for row in spamreader:
            rows.append(row)
    return rows


def first(rows):
    seeds = []
    help_map = []

    row = rows[0]
    for id, value in enumerate(row):
        if not value.isdigit():
            continue
        if value.isdigit() and ((id % 2) == 0):
            seeds.extend([int(i) for i in range(int(row[id-1]), int(row[id])+1)])

    for idx, row in enumerate(rows[1:]):
        if not row:
            continue

        if help_map and not row[0].isdigit():
            seeds.extend(help_map)
            help_map = []
            print('Here')
            continue
        elif not row[0].isdigit():
            continue
        
        row_list = [int(i) for i in row]

        for idx, seed in enumerate(seeds):
            
            if (seed > row_list[1]) and (seed <= row_list[1]+row_list[2]):
                help_map.append(row_list[0] + (seed-row_list[1]))
                seeds.pop(idx)
            elif (row_list[2] == 0):
                help_map.append(seed)
                seeds.pop(idx)
        
        print(len(seeds), len(help_map))

    seeds.extend(help_map)
    print(f'min {min(seeds)}')


def second_another(rows):
    seeds_range = []
    seeds_lower = []
    help_map = []
    range_help = []

    row = rows[0]
    for id, value in enumerate(rows[0]):
        if not value.isdigit():
            continue
        if ((id % 2) == 0):
            seeds_range.append(int(value))
        elif ((id % 2) != 0):
            seeds_lower.append(int(value))
    
    seeds_lower = np.array(seeds_lower)
    seeds_range = np.array(seeds_range)
    idx = np.argsort(seeds_lower)
    
    seeds_lower = np.sort(seeds_lower)
    seeds_range = seeds_range[idx]


    seeds = list(range(seeds_lower[0], seeds_lower[0] + seeds_range[0] + 1))
    for ii, item in enumerate(seeds_lower[1:]):
        if (item < seeds[-1]) and (item + seeds_range[ii] > seeds[-1]):
            seeds.extend(list(range(seeds[-1]+1, item + seeds_range[ii] + 1)))

    for idx, row in enumerate(rows[1:]):
        if not row:
            continue

        if help_map and not row[0].isdigit():
            seeds.extend(help_map)
            help_map = []
            print('Here')
            continue
        elif not row[0].isdigit():
            continue
        
        row_list = [int(i) for i in row]

        for idx, seed in enumerate(seeds):
            
            if (seed > row_list[1]) and (seed <= row_list[1]+row_list[2]):
                help_map.append(row_list[0] + (seed-row_list[1]))
                seeds.pop(idx)
            elif (row_list[2] == 0):
                help_map.append(seed)
                seeds.pop(idx)
        
        print(len(seeds), len(help_map))

    seeds.extend(help_map)
    print(f'min {min(seeds)}')

def second_force(rows):
    seeds = []
    help_map = []

    row = rows[0]
    for id, value in enumerate(row):
        if not value.isdigit():
            continue
        if value.isdigit() and ((id % 2) == 0):
            seeds.extend([int(i) for i in range(int(row[id-1]), int(row[id])+1)])

    
    for idx, row in enumerate(rows[1:]):
        if not row:
            continue

        if help_map and not row[0].isdigit():
            seeds.extend(help_map)
            help_map = []
            print('Here')
            continue
        elif not row[0].isdigit():
            continue
        
        row_list = [int(i) for i in row]

        for idx, seed in enumerate(seeds):
            
            if (seed > row_list[1]) and (seed <= row_list[1]+row_list[2]):
                help_map.append(row_list[0] + (seed-row_list[1]))
                seeds.pop(idx)
            elif (row_list[2] == 0):
                help_map.append(seed)
                seeds.pop(idx)
        
        print(len(seeds), len(help_map))

    seeds.extend(help_map)
    print(f'min {min(seeds)}')



def second_new(rows):
    seeds_range = []
    seeds_lower = []
    help_map = []
    range_help = []

    row = rows[0]
    for id, value in enumerate(rows[0]):
        if not value.isdigit():
            continue
        if ((id % 2) == 0):
            seeds_range.append(int(value))
        elif ((id % 2) != 0):
            seeds_lower.append(int(value))

    seeds = [(a, a + b) for a, b in zip(seeds_lower, seeds_range)]
    new_seeds = []
    for idx, row in enumerate(rows[1:]):
        
        if not row:
            continue

        elif not row[0].isdigit():
            continue
        
        dest = int(row[0])
        source = int(row[1])
        ran = int(row[2])
        upper = source + ran
        
        seeds_to_append = []
        seeds.extend( new_seeds)
        new_seeds = []
        seeds = merge_overlapping_ranges(seeds)

        for ii, seed in enumerate(seeds):

            if seed == (0,1):
                pass
            
            if seed[0] == source:
                if seed[0] == seed[1]:
                    new_seeds.append((dest, dest))
                elif seed[1] <= upper:
                    lb = 0
                    ub = seed[1]-seed[0]
                    new_seeds.append((dest + lb, dest + ub))
                    
                elif seed[1] > upper:
                    lb = 0
                    ub = ran
                    new_seeds.append((dest+lb, dest + ub))
                    seeds_to_append.append((upper+1, seed[1]))
                    
            if seed[0] < source:
                if seed[0] == seed[1]:
                    continue
                elif seed[1] == upper:
                    lb = 0
                    ub = ran
                    new_seeds.append((dest+ lb, dest + ub))
                    seeds_to_append.append((seed[0], source-1))
                    
                elif seed[1] < upper:
                    if seed[1] < source:
                        continue
                    else:
                        lb = 0
                        ub = seed[1]-source
                        new_seeds.append((dest, dest+ub))
                        seeds_to_append.append((seed[0], source-1 ))
                        seeds_to_append.append((seed[1]+1, upper ))
                        
                elif seed[1] > upper:
                    lb = source-seed[0]
                    ub = upper-source
                    new_seeds.append((dest, dest + ub))
                    seeds_to_append.append((seed[0], source-1))
                    seeds_to_append.append((upper+1, seed[1]))
                    

            if seed[0] > source:
                if seed[0] == seed[1]:
                    new_seeds.append((dest + (seed[0]-source), dest + (seed[0]-source)))
                elif seed[0] > upper:
                    continue
                elif seed[1] == upper:
                    lb = seed[0]-source
                    ub = upper - seed[0]
                    new_seeds.append((dest + lb, dest +lb+ ub))
                    
                elif seed[1] < upper:
                    lb = (seed[0]-source)
                    ub = seed[1]-seed[0]
                    new_seeds.append((dest + lb, dest +lb + ub))
                    
                elif (seed[1] > upper):
                    lb = seed[0]-source
                    ub = upper - seed[0]
                    new_seeds.append((dest + lb, dest +lb + ub))
                    seeds_to_append.append((upper+1, seed[1]))
        seeds.extend(seeds_to_append)
        seeds_to_append = []
    
    seeds.extend(new_seeds)
    seeds = merge_overlapping_ranges(seeds)
    
    print("Minimum of first components:", seeds[0][0])
    

    print(seeds)



def merge_overlapping_ranges(ranges):
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges = [sorted_ranges[0]]

    for current_range in sorted_ranges[1:]:
        last_range = merged_ranges[-1]

        if current_range[0] <= last_range[1]:
            # Merge overlapping ranges
            merged_ranges[-1] = (last_range[0], max(last_range[1], current_range[1]))
        else:
            # No overlap, add the current range to the result
            merged_ranges.append(current_range)

    return merged_ranges




if __name__ == '__main__':
    rows = parse_data()
    second_new(rows)


    '''for idx, seed in enumerate(seeds_lower):
            
            diff_seed = seed-source
            diff_ran = seeds_range[idx] - ran

            if diff_seed == 0:
                help_map.append(dest)
                if diff_ran = 0:
                    range_help.append(ran)
                elif diff_ran <0:
                    range_help.append(seeds_range[idx])
                else:
                    range_help.append(ran)
                    help_map.append(dest + ran+1)
                    range_help.append(diff_seed)
            
            elif diff_seed > 0:
                if source+ran < seed:
                    continue
                else:
                    r = source + ran - seed
                    help_map.append(seed + r)
                    range_help.append(r)
                    seeds_lower[idx] -= r
            else:
                help_map.append(dest)
                if diff_ran = 0:
                    range_help.append(ran)
                elif diff_ran <0:
                    range_help.append(seeds_range[idx])
                else:
                    range_help.append(ran)
                    help_map.append(dest + ran+1)
                    range_help.append(diff_seed)'''
