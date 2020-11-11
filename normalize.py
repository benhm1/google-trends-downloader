import os
import csv
import sys

def normalize(f1_maps, f2_maps):

    overlap = [ x for x in f1_maps if x in f2_maps ]

    coefficients = [ 1.0 * f2_maps[x] / f1_maps[x] for x in overlap if
                     f2_maps[x] > 0 and f1_maps[x] > 0 ]
    if len(coefficients) == 0:
        coefficient = 1
    else:
        coefficient = sum(coefficients) / len(coefficients)

    for x in f1_maps:
        f2_maps[x] = f1_maps[x] * coefficient

    return f2_maps

def normalize_all(files_list):

    start = open(files_list[0]).readlines()
    start_lines = [ x.replace('<1', '0.5') for x in start if x.startswith('20') ]
    start_maps = { x.split(',')[0] : float(x.split(',')[1].strip()) for x in start_lines }

    normalized = start_maps

    for i in range(1, len(files_list)):
        new = open(files_list[i]).readlines()
        new_lines = [ x.replace('<1', '0.5') for x in new if x.startswith('20') ]
        new_maps = { x.split(',')[0] : float(x.split(',')[1].strip()) for x in new_lines }

        normalized = normalize(normalized, new_maps)

    # Bring everything between 0 and 100
    max_value = max( normalized.values() )
    for each in normalized:
        normalized[each] = 100.0 / max_value * normalized[each]

    return normalized

def normalize_directory(dirpath):

    ls = os.listdir(dirpath)
    ls = [ os.path.join( dirpath, x) for x in ls if x.endswith('csv') ]
    ls = [ x for x in ls if not x.endswith('normalized.csv') ]
    ls.sort( key = lambda x: int(x.split('(')[1].split(')')[0]) if x.find('(') >= 0 else 0 )

    for each in ls:
        print(each)

    normalized = normalize_all(ls) 
    
    ret_data = []

    for k in sorted(normalized.keys()):
        ret_data.append( (k, normalized[k]) )

    return ret_data

if __name__ == '__main__':
    dirname = sys.argv[1]
    output = os.path.join(dirname, 'normalized.csv')
    normalized = normalize_directory(dirname)

    with open(output, 'w', newline='') as csvfile:
        outwriter = csv.writer(csvfile, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for val in normalized:
            outwriter.writerow(val)
            
    print(f"Wrote normalized data to {output}")
