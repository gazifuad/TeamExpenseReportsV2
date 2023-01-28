import pytesseract
from PIL import Image
import numpy as np

# Found the documentIDs of receipt images in Users.csv but 
# who do NOT have matching OCR files provided.
need_ocr = ['00d0534693438', '00d0390662905', '00d0735262766', '00d0592371977', '00d0937018331', '00d0987973134', '00d0801912850', '00d0158328888', '00d0388872730', '00d0194076657', '00d0799986048', '00d0975647950', '00d0400234172', '00d0384870576', '00d0194569644', '00d0592118004', '00d0967073777', '00d0708763656', '00d0667839698', '00d0686397126', '00d0571602960', '00d0774018859', '00d0650437495', '00d0266020596', '00d0394257241', '00d0209546609', '00d0542653551', '00d0675769257', '00d0930689679', '00d0980207211', '00d0343987945', '00d0435587221', '00d0119878906', '00d0844818369', '00d0834688755', '00d0957822503', '00d0166829801', '00d0956164753', '00d0477960526', '00d0790157720', '00d0627668053', '00d0849221655', '00d0560446704', '00d0328806229', '00d0202261292', '00d0369571763', '00d0569507667', '00d0416368925', '00d0163078697', '00d0921271701']
file_names = ["data/img/" + docID + ".jpg" for docID in need_ocr]

for file_name in file_names:
        # Extract the text
        image = Image.open(file_name)
        text = pytesseract.image_to_string(image)
        
        # Create a list of the rows
        rows = text.split('\n')
        rows = [row for row in rows if row != '']

        # Extract the documentID again
        docID = file_name[9:-4]

        # Save as a csv file format
        np.savetxt("data/ocr-2/" + docID + ".csv", rows, delimiter =",", fmt ='%s')