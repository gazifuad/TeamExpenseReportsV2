import pandas as pd
import os

class Receipt:
    '''
    Wrapper class around each receipt.
    '''
    data_folder_path = ""       # string filepath to the Data folder containing all receipts
    doc_id = ""                 # string documentid of this receipt

    has_user = False            # boolean whether Users.csv contains a line for this receipt 
    has_image = False           # boolean whether Data\img contains an image for this receipt
    has_ocr = False             # boolean whether Data\csv contains an image for this receipt

    users_index = None          # integer index of this receipt in Users.csv
    image_filepath = None       # string filepath to this receipt's image
    ocr_filepath = None         # string filepath to this receipt's ocr csv output


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
        ocr_filepath_temp = self.data_folder_path + '/ocr/' + self.doc_id + '.csv'
        if os.path.isfile(ocr_filepath_temp):
            self.has_ocr = True
            self.ocr_filepath = ocr_filepath_temp
            return True

        ocr_filepath_temp = self.data_folder_path + '/ocr-2/' + self.doc_id + '.csv'
        if os.path.isfile(ocr_filepath_temp):
            self.has_ocr = True
            self.ocr_filepath = ocr_filepath_temp
            return True
            
        self.has_ocr = False
        self.ocr_filepath = None
        return False

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
        collected_doc_ids = collected_doc_ids.union(set([did[: -4] for did in os.listdir(data_folder_path + '/ocr') if did[-4] == '.csv']))

        for did_raw in os.listdir(data_folder_path + '/img'):
            if did_raw[-4] == '.jpg':
                if '(1)' == did_raw[-7 : -4]:
                    did = did_raw[: -7]
                else:
                    did = did_raw[: -4]
                collected_doc_ids = collected_doc_ids.union(set([did]))
        return [Receipt(data_folder_path, did, users_df) for did in collected_doc_ids]


    