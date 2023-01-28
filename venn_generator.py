import numpy as np
import pandas as pd
import glob
import os

#Function to standardize document ids that end in (1)
def DeDuplicator(ids):
    newIDs = []
    for i in range(len(ids)):
        if ids[i][-3:] == '(1)':
            newIDs.append(ids[i][:-3])
        else:
            newIDs.append(ids[i])
    return newIDs

#Read in all the file names and users csv
df = pd.read_csv('data/Users.csv')
img = DeDuplicator([os.path.basename(glob)[:-4] for glob in glob.glob('data/img/*.jpg')])
ocr = [os.path.basename(glob)[:-4] for glob in glob.glob('data/ocr/*.csv')]
users = df.documentid
lists = [img, ocr, users]

#Intersections between sets
intersectImgOcr = set(img).intersection(set(ocr))
intersectImgUsers = set(img).intersection(set(users))
intersectOcrUsers = set(ocr).intersection(set(users))

#Each section of the venn diagram
JPG_ONLY = set(img).difference(set(ocr).union(set(users)))
OCR_ONLY = set(ocr).difference(set(img).union(set(users)))
USERS_ONLY = set(users).difference(set(ocr).union(set(img)))
JPG_OCR_INTERSECT = set(set(img).difference(set(users))).difference(JPG_ONLY)
JPG_USERS_INTERSECT = intersectImgUsers.difference(set(ocr))
OCR_USER_INTERSECT = intersectOcrUsers.difference(set(img))
JPG_OCR_USERS_INTERSECT = set.intersection(*map(set,lists))

#Union of all sets
JPG_OCR_USERS_UNION = set(JPG_ONLY).union(JPG_OCR_INTERSECT).union(JPG_USERS_INTERSECT).union(JPG_OCR_USERS_INTERSECT)

#Output venn diagram as dictionary
f = open('venn_diagram.txt', 'w')
f.write(str({'JPG':JPG_ONLY, 'OCR': OCR_ONLY, 'USERS': USERS_ONLY, 'JPG_OCR': JPG_OCR_INTERSECT, 
'JPG_USERS': JPG_USERS_INTERSECT, 'OCR_USERS': JPG_OCR_USERS_INTERSECT, 
'JPG_OCR_USERS_INTERSECT': JPG_OCR_USERS_INTERSECT, 'JPG_OCR_USERS_UNION': JPG_OCR_USERS_UNION}))
