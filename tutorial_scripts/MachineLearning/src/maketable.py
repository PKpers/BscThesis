from tabulate import tabulate
from texttable import Texttable
import latextable
import sys

if len(sys.argv) != 3:
    print("usage: {} {} {}".format(sys.argv[0], "datafile.txt", "outfile.txt"))
    exit(-1)
#
datafile = sys.argv[1]
with open(datafile, 'r') as f:
    data = f.readlines()
#
outfile = sys.argv[2]

tsc = 0#TrainingSetCount
rows = []
row = []
for i, d in enumerate(data):
    if i==len(data)-1: #append the last row to rows
        rows.append(row)
    #
    if 'TrainingSet' in d:
        # TrainingSet indicates a new row essentially.
        tsc += 1
        if tsc>1:
            # If tsc > 1 then its time time to change row
            rows.append(row)
            row = []
            dnew=d.split(':')[1].split(' ')[1]
            row.append(dnew)
            continue
        else:
            dnew=d.split(':')[1].split(' ')[1]
            row.append(dnew)
            continue
        #
    #
    dnew = d.split(':')[1].split(' ')[1]
    row.append(dnew)
#
# Draw the table
headers = [str(i)+'9s2' for i in [2,3,4,5,6]]
headers.insert(0, 'Training data\Testing data')
rows.insert(0, headers)
table = Texttable()
table.set_cols_align(["c"] * 6)
table.set_deco(Texttable.HEADER | Texttable.VLINES)
table.add_rows(rows)
print(table.draw(), file=open(outfile, 'w')) 
