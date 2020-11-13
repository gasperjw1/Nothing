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

#'path_of_directory'
dirpath = './names' 

output = 'namesFL.csv'

with open(output, 'w') as outfile:
    csvout = csv.writer(outfile)
    csvout.writerow(['Name'])

    files = os.listdir(dirpath)

    for filename in files:
        with open(dirpath + '/' + filename) as afile:
            for line in (afile.read()).split('\n'):
                if len(line) > 1 and not line.isspace() and len(line) <= 10:
                    csvout.writerow([line])
            afile.close()

    outfile.close()