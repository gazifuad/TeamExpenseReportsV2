import spacy
import pickle

# Load up spaCy
nlp = spacy.load('en_core_web_sm')

# Helper method to convert a nested list to 
# one long string
def create_string(lst):
        string = ""
        for row in lst:
                string += row[0]
                string += " "
        return string

import os
# Holds file names that we couldn't parse
cant_parse = []

# Will map each documentID to its vendor
org_dict = {}

for file_name in os.listdir('data/ocr-3/'):
        path = 'data/ocr-3/' + file_name
        try:
                df = pd.read_csv(path, sep='\t',quoting=3)
        except:
                # Couldn't parse for some reason
                cant_parse.append(file_name)
                continue

        # Examine first 5 rows of receipt
        df = df.iloc[0:5]
        lst = df.values
        # Create a long string of these 5 rows
        string = create_string(lst)
        doc = nlp(string)
        # Extract organizations recognized by spaCy's model
        orgs = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        doc_id = file_name[:-4]
        # If none were found, just keep the first 3 lines of the receipt
        if (len(orgs) == 0):
                df = df.iloc[0:3]
                lst = df.values
                string = create_string(lst)
                org_dict[doc_id] = string
        # Create a string of the vendors found
        else:
                string = ""
                for word in orgs:
                        string += word
                        string += " "
                org_dict[doc_id] = string

# Save to easily share output across devices
with open('org_dict.pickle', 'wb') as file:
    pickle.dump(org_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

with open('cant_parse.pickle', 'wb') as file:
    pickle.dump(cant_parse, file, protocol=pickle.HIGHEST_PROTOCOL)