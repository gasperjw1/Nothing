import os
import csv


#'path_of_directory'
dirpath = './setOfScripts' 

output = 'bunchOfScripts.csv'

with open(output, 'w') as outfile:
    csvout = csv.writer(outfile)
    csvout.writerow(['Content'])

    files = os.listdir(dirpath)

    for filename in files:
        with open(dirpath + '/' + filename) as afile:
            csvout.writerow([afile.read()])
            afile.close()

    outfile.close()