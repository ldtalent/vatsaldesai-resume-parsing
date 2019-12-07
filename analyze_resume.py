import csv
import json
import os
import sys
from datetime import datetime
import requests

import argparse

import imagetotext as im2text

from FileUtils import convert_pdf_to_txt, extract_text_from_pdf, pdf_2_pil_images, concat_and_save_images, \
    extract_text_from_json, TARGET_DIRECTORY, extract_developer_name, download_gdrive_files
from SkillParser import match_skill_category

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-D", "--directory", required=True,
                help="Directory/folder having resumes")
ap.add_argument("-O", "--ocr", required=False, default=False,
                help="Want to use Google Vision API?")
ap.add_argument("-G", "--google", required=False, default=False,
                help="google-resume-file-text file name")


args = vars(ap.parse_args())

fmt = "%Y_%m_%d_%I_%M_%S_%p"
now = datetime.now()
new_skill_list_filename = 'engineerlist_' + now.strftime(fmt) + '.csv'

LEARNING = 0
BEGINNER = 1
MODERATE = 2
ADVANCED = 3
EXPERIENCE = (
    (LEARNING, 'LEARNING'),
    (BEGINNER, 'BEGINNER'),
    (MODERATE, 'MODERATE'),
    (ADVANCED, 'ADVANCED')
)


class FreelancerSkill(object):

    def __init__(self, email, skill, years_of_experience, experience_level):
        self.freelancer_email = email
        self.skill = skill
        self.years_of_experience = years_of_experience
        self.experience_level = experience_level

    def __str__(self):
        return 'Freelancer ' + self.freelancer_email + \
               ' has skill ' + json.dumps(self.skill) + \
               ' with ' + str(self.years_of_experience) + ' years of experience;' + \
               ' at ' + str(EXPERIENCE[self.experience_level]) + ' level'


# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.


def main(directory, filetype='pdf', ocr=False):
    # print directory
    # print os.listdir('.')
    # print(os.listdir(directory))

    # print(filename)
    # os.chdir(sys.argv[1])
    print("Current working directory in main()", "=>", os.getcwd())
    engineer = ''

    # os.chdir(sys.argv[1])

    print("Current working directory after os.getcwd()", "=>", os.getcwd())

    conversion_candidates = dict()
    # paths, fname = os.path.split(filename)

    # print("ntpath basename", "=>", ntpath.basename(filename))
    # print("ospath asename", "=>", os.path.basename(filename))

    count = 0
    other_filetype_counter = 0
    with open(new_skill_list_filename, 'a', encoding='utf-8') as csv_data_file:
        writer = csv.writer(csv_data_file)

        writer.writerow(["ENGINEER", "Skills"])

        for filename in os.listdir(directory):
            # if count == 0:
            #   os.chdir(directory)

            if filename.lower().endswith(".pdf") and filetype == 'pdf':

                count = count + 1

                print("processing file", "=>", filename)

                filename = "" + filename + ""
                skills_retrieved = []

                try:
                    engineer, text = convert_pdf_to_txt(filename)

                    skills_retrieved = match_skill_category(text)

                    if len(skills_retrieved) == 0:
                        print("No Skills Found.Trying PYPDF for", filename)
                        engineer, text = extract_text_from_pdf(filename)
                        skills_retrieved = match_skill_category(text)

                    if len(skills_retrieved) == 0:
                        print("No Skills Found.Trying Textract Explicitly for ", filename)
                        engineer, text = extract_text_from_pdf(filename, 1)
                        skills_retrieved = match_skill_category(text)

                    print(engineer)
                    # text = codecs.decode(text, encoding='utf-8', errors='strict')
                    # print text

                except TypeError as e:
                    print(e, "While processing file:- ", filename)
                except Exception as oth:
                    print(oth, "While processing file:- ", filename)

                if len(skills_retrieved) == 0 and ocr:
                    print("Converting to images since no skills were found and OCR is True")
                    conversion_candidates[extract_developer_name(filename)] = filename
                    # conversion_candidates.append(filename)

            elif filename.lower().endswith('.json'):
                print("JSON file.")
                engineer = extract_developer_name(filename)
                text = extract_text_from_json(filename)
                skills_retrieved = match_skill_category(text)
            else:
                print("File name with other extension", filename)
                other_filetype_counter = other_filetype_counter + 1
                continue

            writer.writerow([engineer, skills_retrieved])
            fs = FreelancerSkill(engineer, skills_retrieved, 30., ADVANCED)
            print(fs)

    if len(conversion_candidates) > 0:
        print("List of files to be converted", conversion_candidates)
        tmp_path = os.path.join(os.getcwd(), "converted_resumes")
        try:
            os.mkdir("converted_resumes")
        except FileExistsError:
            print("converted_resumes directory already exists!")

        for devname, fname in conversion_candidates.items():
            pil_images = pdf_2_pil_images(fname, tmp_path)
            concat_and_save_images(pil_images, devname)
        im2text.process_directory(os.getcwd())
        main(os.getcwd(), 'json')
    print("Resumes processed:-", count)
    print("Other Format Files:-", other_filetype_counter)


if __name__ == '__main__':

    TARGET_DIRECTORY = args["directory"]
    os.chdir(TARGET_DIRECTORY)
    TARGET_DIRECTORY = os.getcwd()  # Setting  target directory value to new current working directory

    if args["google"]:
        download_gdrive_files(args["google"])

    if args["ocr"]:
        main(TARGET_DIRECTORY, True)
    else:
        main(TARGET_DIRECTORY)
