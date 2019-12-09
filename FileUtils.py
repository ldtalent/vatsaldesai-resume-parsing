import codecs
import json
import ntpath
import os
import time
from io import StringIO
from os import path

import PyPDF2
import objectpath
import pdf2image
import requests
import textract
from PIL import Image
from PyPDF2.utils import PdfReadWarning
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    engineer_name = extract_developer_name(path)
    return engineer_name, text


def extract_text_from_pdf(filename, call_textract=0):
    egineer_name = extract_developer_name(filename)
    text = ""

    try:
        if call_textract > 0:
            text = textract.process(filename, method='tesseract', language='eng', encoding="utf-8")
            return egineer_name, text

        with open(str(filename), 'rb') as f:

            pdfReader = PyPDF2.PdfFileReader(f)
            print("Encrypted-", pdfReader.isEncrypted)
            # discerning the number of pages will allow us to parse through all #the pages

            num_pages = pdfReader.numPages
            page_count = 0

            # The while loop will read each page
            while page_count < num_pages:
                pageObj = pdfReader.getPage(page_count)
                print(page_count)
                page_count += 1
                try:
                    text += pageObj.extractText()
                except TypeError as terror:
                    print("While processing file->", filename, "Page Number->", page_count, terror)
                    text = codecs.decode(text, encoding='utf-8', errors='strict') + pageObj.extractText()
                    print(text.strip())
                # This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
                if text != "":
                    text = text
                    print("PDF Processed using PYPDF2 Sucessfully")
                    print(text.strip())
                # If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
                else:
                    print("Using textract since PyPDF2 raised error/exception")
                    text = text + textract.process(filename, method='tesseract', language='eng', encoding="utf-8")
                    print(text.strip())
    except PdfReadWarning:
        print(PdfReadWarning, filename)
        print("PDF READ WARNING CAUGHT..")
    except IOError:
        print(IOError, 'An error occurred trying to read the file =====>', filename)
    except ValueError:
        print(ValueError, 'Non-numeric data found in the file. =====>', filename)
    except UnicodeDecodeError:
        print(UnicodeDecodeError, "UnicodeDecodeError : Using os.system pdf2text =====>", filename)
        os.system("pdf2txt.py  '" + (filename) + "'> tmp")
        text = open('tmp', 'r').read()
        print(text)
        os.remove('tmp')
    else:
        print("Things went smoothly!")

    return egineer_name, text


def pdf_2_pil_images(pdf_file_path, op_folder):
    # This method reads a pdf and converts it into a sequence of images
    # PDF_PATH sets the path to the PDF file
    # dpi parameter assists in adjusting the resolution of the image
    # output_folder parameter sets the path to the folder to which the PIL images can be stored (optional)
    # first_page parameter allows you to set a first page to be processed by pdftoppm
    # last_page parameter allows you to set a last page to be processed by pdftoppm
    # fmt parameter allows to set the format of pdftoppm conversion (PpmImageFile, TIFF)
    # thread_count parameter allows you to set how many thread will be used for conversion.
    # userpw parameter allows you to set a password to unlock the converted PDF
    # use_cropbox parameter allows you to use the crop box instead of the media box when converting
    # strict parameter allows you to catch pdftoppm syntax error with a custom type PDFSyntaxError

    start_time = time.time()
    pil_images = pdf2image.convert_from_path(pdf_file_path, dpi=DPI, output_folder=op_folder, first_page=FIRST_PAGE,
                                             last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD,
                                             use_cropbox=USE_CROPBOX, strict=STRICT)
    print("Time taken : " + str(time.time() - start_time))
    return pil_images


def concat_and_save_images(pil_images, devname):
    # This method helps in converting the images in PIL Image file format to the required image format
    index = 1
    X_coordinate = 0
    Y_coordinate = 0

    for img in pil_images:
        if index == 1:
            dst = Image.new('RGB', (img.width, img.height * len(pil_images)))
            dst.paste(img, (X_coordinate, Y_coordinate))

        else:
            dst.paste(img, (X_coordinate, Y_coordinate))

        Y_coordinate += img.height
        index += 1

    new_filename = devname + "_page_" + str(index) + ".jpg"
    print("new_filename", new_filename)
    dst.save(new_filename)
    return new_filename


def extract_text_from_json(filename):
    encoding = 'utf-8'
    errors = 'strict'
    try:
        if filename.endswith(".json"):

            print(filename, "=========================================================================")

            with open(filename) as f:
                data = json.load(f)

                for majorkey, subdict in data.items():

                    print(majorkey)
                    json_tree = objectpath.Tree(data[majorkey])

                    # print('json_tree', json_tree)
                    result_tuple = tuple(json_tree.execute('$..text'))

                    for var in result_tuple:
                        if result_tuple.index(var) == 0:
                            print(result_tuple.index(var), var)
                            return var

    except json.decoder.JSONDecodeError as j:
        print(j, "File encountered error ", filename)

    return ""


TARGET_DIRECTORY = '.'
DPI = 200
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False


def extract_developer_name(filename):
    # src = pathlib.Path(filename).resolve()

    fname_w_extn = ntpath.basename(filename)

    fname, fextension = os.path.splitext(fname_w_extn)

    # print(fextension)
    # print(fname)
    return fname


def download_gdoc_in_pdf(fileId, file_name, location = '', chunk_size=2000):
    if location == '':
        filename_with_location = os.getcwd() + "/" +  file_name
    else:
        filename_with_location = os.getcwd() + "/" + location + "/" + file_name

    url = f"https://www.googleapis.com/drive/v3/files/{fileId}/export"
    params = {
        "mimeType": 'application/pdf',
        "key": '' #enter your key here
    }
    res = requests.get(url, params, stream=True)
    print(type(res))
    print(filename_with_location)

    with open(filename_with_location, 'wb') as fd:
        for chunk in res.iter_content(chunk_size):
            fd.write(chunk)

def get_gdoc_metadata(fileId):
    url = f"https://www.googleapis.com/drive/v3/files/{fileId}"
    params = {
        "key": '' #enter your key here
    }
    res = requests.get(url, params)
    print(type(res))
    print(res.json())
    #print('content', res.content)
    #print('text', res.text)
    file_metatdata = res.json()
    print(file_metatdata['name'])
    return file_metatdata

def get_file_name(fileId):
    f_metadata = get_gdoc_metadata(fileId)
    if f_metadata['mimeType'] == 'application/vnd.google-apps.document':
        file_name = f_metadata['name']
        return file_name.replace(' ', '_') + '.pdf'

def download_gdrive_files(file_name):

    with open(file_name, 'r') as file_names:
        for record in file_names:
            path_list = record.split('/')
            print(path_list[-1])
            file_name_retrived = get_file_name(path_list[-1].rstrip('\n'))
            if file_name_retrived != '':
                download_gdoc_in_pdf(path_list[-1], file_name_retrived)

