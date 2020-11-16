import os
import csv


#'path_of_directory'
dirpath = './initialInformation/Comedy' 

output = './initialInformation/comedyScripts.csv'

with open(output, 'w') as outfile:
    csvout = csv.writer(outfile)
    csvout.writerow(['Name', 'Content'])

    files = os.listdir(dirpath)

    for filename in files:
        with open(dirpath + '/' + filename) as afile:
            endOfTitle = filename.find('_')
            csvout.writerow([filename[0:endOfTitle], afile.read()])
            afile.close()

    outfile.close()

# #'path_of_directory'
# dirpath = './initialInformation' 

# output = './initialInformation/namesFL.csv'

# with open(output, 'w') as outfile:
#     csvout = csv.writer(outfile)
#     csvout.writerow(['Name'])

#     files = os.listdir(dirpath)

#     for filename in files:
#         with open(dirpath + '/' + filename) as afile:
#             for line in (afile.read()).split('\n'):
#                 if len(line) > 1 and not line.isspace() and len(line) <= 10:
#                     csvout.writerow([line])
#             afile.close()

#     outfile.close()