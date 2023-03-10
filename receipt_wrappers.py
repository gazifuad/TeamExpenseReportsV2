import pandas as pd
import os

class Receipt:
    '''
    Wrapper class around each receipt.
    '''
    data_folder_path = ''       # string filepath to the Data folder containing all receipts
    doc_id = ''                 # string documentid of this receipt

    has_user = False            # boolean whether Users.csv contains a line for this receipt 
    has_image = False           # boolean whether Data\img contains an image for this receipt
    has_ocr = False             # boolean whether Data\csv contains an image for this receipt

    users_index = None          # integer index of this receipt in Users.csv
    image_filepath = None       # string filepath to this receipt's image
    ocr_filepath = None         # string filepath to this receipt's ocr csv output

    ocr_str = None              # the string in the associated ocr file  
    ocr_date = ""               # the full date, if found, in the OCR
    ocr_year = ""                # the year, if found, in the OCR
    users_amount = None          # the monetary amount in the User.csv file
    users_vendor = None          # the vendor name in the User.csv file
    users_address = None         # the vendor address in the User.csv file


    def __init__(self, data_folder_path, doc_id, users_df):
        '''
        Initializes this receipt object
        INPUT
            data_folder_path; string path to the data directory
            doc_id; string documentid
            users_df; pandas dataframe containing Users.csv data
        '''
        self.data_folder_path = data_folder_path
        self.doc_id = doc_id
        self.set_user_index(users_df)
        self.set_img_filepath()
        self.set_ocr_filepath()
        self.set_ocr_date()
        if self.has_ocr:
            self.parse_ocr_tsv()
        if self.has_user:
            self.parse_user_csv()

    def __str__(self):
        '''
        Returns string representation of this receipt
        '''
        msg = 'documentid' + '\t\t' + str(self.doc_id)
        msg += '\n' + 'users_index' + '\t\t' + str(self.users_index)
        msg += '\n' + 'image_filepath' + '\t\t' + str(self.image_filepath)
        msg += '\n' + 'ocr_filepath' + '\t\t' + str(self.ocr_filepath)
        return msg

    def set_user_index(self, users_df):
        '''
        Sets self.user_index and self.has_user based on given users_df
        INPUT
            users_df; pandas dataframe of Users.csv
        RETURN
            boolean whether new values were set
        '''
        users_indices = users_df.index[users_df['documentid']==self.doc_id].tolist()
        if len(users_indices) == 0:
            self.has_user = False
            self.users_index = None
            return False
        if len(users_indices) >= 2:
            self.has_user = True
            raise Exception('Users.csv contains documentid twice: ' + str(self.doc_id))
        self.has_user = True
        self.users_index = users_indices[0]
        return True

    def set_img_filepath(self):
        '''
        Sets self.img_filepath and self.has_img based on files in self.data_folder_path director
        RETURN
            boolean whether new values were set
        '''
        image_filepath_temp = self.data_folder_path + '/img/' + self.doc_id
        if os.path.isfile(str(image_filepath_temp + '.jpg')):
            self.has_image = True
            self.image_filepath = image_filepath_temp + '.jpg'
            return True
        if os.path.isfile(str(image_filepath_temp + '(1).jpg')):
            self.has_image = True
            self.image_filepath = image_filepath_temp + '(1).jpg'
            return True
        self.has_image = False
        self.image_filepath = None    
        return False    
    
    def set_ocr_filepath(self):
        '''
        Sets self.ocr_filepath and self.has_ocr based on files in self.data_folder_path director
        RETURN
            boolean whether new values were set
        '''
        ocr_filepath_temp = self.data_folder_path + '/ocr-3/' + self.doc_id + '.tsv'
        if os.path.isfile(ocr_filepath_temp):
            self.has_ocr = True
            self.ocr_filepath = ocr_filepath_temp
            return True
            
        self.has_ocr = False
        self.ocr_filepath = None
        return False
    
    def set_ocr_date(self):
        '''
        Finds the year, if there is one, and full date for this receipt
        '''
        dates = pd.read_csv("dates.csv")
        dates = dates.fillna("")
        try:
            dates.set_index("documentid")
            dates = dates.set_index("documentid")
            self.ocr_date = dates.loc[self.doc_id].values[0]
        except:
            return False
        if (self.ocr_date != ""):
            self.ocr_year = self.ocr_date[:4]
        return True


    def parse_ocr_tsv(self):
        '''
        Parses the text in the ocr_filepath and stores in self.ocr_str
        '''
        try:
            tsv_df = pd.read_csv(self.ocr_filepath, sep='\t')
            self.ocr_str = ''
            for strline in tsv_df.values.tolist():
                self.ocr_str += ' ' + strline[0].strip() + ' '
            self.ocr_str = self.ocr_str.strip()
        except:
            self.has_ocr = False
            self.ocr_str = None

    def parse_user_csv(self):
        '''
        Parses the fields in User.csv and stores results in self.users_amount, self.users_vendor, self.users_address
        '''
        csv_df = pd.read_csv(self.data_folder_path + '/Users.csv')
        self.users_amount = csv_df.loc[self.users_index, 'amount']
        self.users_vendor = csv_df.loc[self.users_index, 'vendor_name']
        self.users_address = csv_df.loc[self.users_index, 'vendor_address']

    def initialize_batch_receipts(data_folder_path, users_df):
        '''
        STATIC METHOD. NOT TIED TO AN INSTANCE OF RECEIPT.
        Initializes all the receipts found within the given Data folder
        INPUT
            data_folder_path; string path to the Data folder
            users_df; pandas dataframe containing Users.csv
        RETURN
            list of the Receipt objects initialized based on receipts found in Data folder
        '''
        collected_doc_ids = set([did for did in users_df.loc[:, 'documentid']])
        collected_doc_ids = collected_doc_ids.union(set([did[: -4] for did in os.listdir(data_folder_path + '/ocr-3') if did[-4] == '.tsv']))

        for did_raw in os.listdir(data_folder_path + '/img'):
            if did_raw[-4 :] == '.jpg':
                if '(1)' == did_raw[-7 : -4]:
                    did = did_raw[: -7]
                else:
                    did = did_raw[: -4]
                collected_doc_ids = collected_doc_ids.union(set([did]))
        return [Receipt(data_folder_path, did, users_df) for did in collected_doc_ids]


    