import codecs
import csv
import json
import ntpath
import os
import re
import sys
# from xpdf_python import to_text
import PyPDF2
import textract
from datetime import datetime

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

Software_Engineering = [
    "C\+\+",
    "J2EE",
    "Git",
    "OpenShift",
    "Singularity Containerization",
    "Regex",
    "UML Diagrams",
    "Apache Kafka",
    "Scala",
    "VBA",
    "Rust",
    "LISP",
    "Perl",
    "Fortran",
    "Golang",
    "Assembly",
    "Clojure",
    "Kotlin",
    "Dart",
    "WebAssembly",
    "\.NET",
    "\.NET Core",
    "Ansible",
    "Elixir",
    "Erlang",
    "NoSQL",
    "WebRTC",
    "C\#",
    "C",
    "SQL",
    "Java",
    "HTML",
    "CSS",
    "JSX",
    "Python",
    "R",
    "UNIX",
    "Ruby",
    "XML",
    "PHP",
    "Docker",
    "Objective C",
    "JavaScript",
    "REST API"
]

Web_Mobile_and_Desktop_Application_Development = [
    "Elm",
    "Mocha",
    "Chai",
    "Bulma",
    "Semantic-UI",
    "Swift",
    "Ember.js",
    "VulcanJS",
    "MeteorJS",
    "Google Tag Manager",
    "Google Analytics",
    "WebSockets",
    "Gatsby",
    "Postman",
    "Cucumber",
    "Wix",
    "Bootstrap",
    "GraphQL",
    "Angular",
    "Typescript",
    "MongoDB",
    "ExpressJS",
    "Data Semantic Layers",
    "SEO",
    "Redux",
    "Webpack",
    "Apollo GraphQL",
    "ECMA",
    "CSS Flex",
    "jQuery",
    "UI Design",
    "UX Design",
    "Interaction Design",
    "Material Design",
    "Flow JS",
    "Babel JS",
    "Ionic",
    "Grind Rocks for Node",
    "Postgres",
    "MySQL",
    "Vagrant",
    "VirtualBox",
    "WebGL",
    "DevOps",
    "Site Reliability",
    "ASP.NET",
    "Drupal",
    "Cordova",
    "Xamarin",
    "Flutter",
    "Microsoft SQL Server",
    "SQLite",
    "Redis",
    "MariaDB",
    "OracleDB",
    "DynamoDB",
    "Cassandra",
    "Couchbase",
    "Chef",
    "ReasonML",
    "Django",
    "Nodejs",
    "Laravel",
    "Flask",
    "React",
    "Ruby on rails",
    "React native",
    "Wordpress",
    "Android native app development",
    "iOS native app development",
    "Windows Application Development",
    "Mac Application Development",
    "Chrome Extension Development",
    "Firefox Extension Development",
    "Safari Extension Development",
    "Internet Explorer Extension Development",
    "XCode",
    "Vue.js",
    "Visual Studio",
    "Android Studio"
]

Artificial_Intelligence = [
    "keras",
    "KNIME",
    "OCR",
    "PyTorch",
    "Torch",
    "Autonomous Vehicles and Self Driving Cars",
    "Artificial intelligence",
    "Machine learning",
    "Deep learning",
    "Natural language processing",
    "Speech recognition",
    "Probabilistic graphical models",
    "Robotics",
    "Computer vision",
    "Reinforcement learning",
    "Data mining",
    "Quadrocopters",
    "Drones"
]

Special_Technologies_and_Expertise_Areas = [
    "Cyber Security",
    "Hackintosh",
    "Sound Engineering",
    "GDPR Compliance",
    "Logic Pro X",
    "Final Cut Pro",
    "Pro Tools",
    "Autodesk Maya",
    "Salesforce Development",
    "Photoshop",
    "Adobe Premiere Pro",
    "IBM DB2",
    "Maven",
    "Turtle Logo",
    "Lego Mindstorms",
    "Autodesk Revit",
    "Google Sketchup",
    "Rhino",
    "3Dmax",
    "CorelDraw",
    "Canva",
    "Inkscape",
    "GIMP",
    "InDesign",
    "Proteomics",
    "Microsoft Excel",
    "Design Modo",
    "Salesforce Pardot",
    "EMR Software",
    "Data Analytics",
    "R for Statistics",
    "Data Science",
    "Adobe Illustrator",
    "3D modeling",
    ".obj files",
    "Marketplaces",
    "Product Lifecycle Management",
    "Agile",
    "SCRUM",
    "Kanban",
    "Kaizen",
    "Lean",
    "JMP",
    "Minitab",
    "Shopify",
    "Unreal Engine Game Development",
    "Computational Linguistics",
    "Fourier Transforms",
    "Kubernetes",
    "Microservices",
    "Jupyter",
    "Augmented Reality AR",
    "Virtual Reality VR",
    "Apache Spark",
    "Puppet",
    "CryEngine",
    "QTP/ HP for QA Testing",
    "Appium for QA Testing",
    "Seetest for QA Testing",
    "Apache Jmeter",
    "Load runner",
    "SOAP UI",
    "HP Quality Centre",
    "Version One",
    "Bugzilla",
    "TestCaseLab",
    "qTest",
    "TestRail",
    "TestLink",
    "PractiTest",
    "TestLodge",
    "QACoverage",
    "Fogbuz",
    "TFS",
    "Serverless Architecture",
    "Blockchain",
    "iOT",
    "Bioinformatics",
    "Unity Game Design and Development",
    "Chatbots",
    "Data visualization",
    "Web scrapers",
    "Unity Augmented Reality Design and Development",
    "Browser automation",
    "Mapreduce",
    "Unity Virtual Reality Design and Development",
    "Solidity",
    "Genomics",
    "Ethereum"
]

APIs_and_Packages = [
    "Google NLP API",
    "Socket.IO",
    "Sequelize",
    "Mapbox",
    "Github API",
    "Matplotlib",
    "scikit-learn",
    "PyQt5",
    "ADA Compliance",
    "Pandas",
    "Slack API",
    "Tensorflow",
    "Blockchain API",
    "Ripple API",
    "D3",
    "Vega",
    "Vega Lite",
    "Biopython",
    "Python Selenium",
    "Selenium",
    "Google Maps API",
    "Mailchimp API",
    "Sendgrid API",
    "Twitter APIs",
    "Stripe API",
    "Twilio API",
    "Apache Hadoop",
    "Facebook API",
    "Google Computer Vision API",
    "Google API",
    "AWS Cloud Compliance",
    "HIPAA Cloud Compliance",
    "Finance Cloud Compliance",
    "Government Cloud Compliance (US DoD)",
    "Paypal API"
]

Electrical_and_Mechanical_Engineering = [
    "Autodesk",
    ".dxf files",
    "Digital Manufacturing",
    "AutoCAD",
    "MATLAB",
    "Verilog",
    "VHDL",
    "LabVIEW",
    "ANSYS",
    "Intel x86",
    "Hypermesh",
    "SolidWorks",
    "Medical Devices",
    "SPICE (ic design)"
]

Other_Skills = [
    "AWS EC2",
    "AWS Redshift",
    "AWS CloudFront",
    "AWS S3",
    "AWS DynamoDB",
    "AWS ECR",
    "AWS Elastic Beanstalk",
    "Amazon ElastiCache",
    "AWS ElasticMapReduce",
    "AWS IoT",
    "AWS Key Management Service",
    "AWS RDS",
    "Electronic Health Records",
    "Embedded Software",
    "Microcontrollers",
    "Multithreaded Programming",
    "ARM Programming",
    "RTOS",
    "Quality Assurance QA",
    "Oracle BI",
    "SAP",
    "Plotly",
    "Eclipse",
    "Cloud Foundry",
    "Kubernetes",
    "Terraform",
    "Product Management",
    "Google Cloud",
    "AWS",
    "Firebase",
    "SWOT Analysis",
    "FMEA Analysis",
    "VoC Strategy Analysis",
    "PEST Analysis",
    "Pareto Analysis",
    "JIRA",
    "Trello",
    "Asana",
    "Microsoft Project",
    "SAP",
    "Tableau",
    "AWS Elasticsearch",
    "Linux",
    "Windows",
    "MacOS",
    "Raspberry Pi",
    "Azure",
    "Arduino",
    "Heroku",
    "IBM Cloud Watson",
    "AWS Lambda",
    "Spring",
    "Hibernate",
    "DROOLS",
    "OSCache",
    "SOAP",
    "Actuate Espreadsheet",
    "Autosys",
    "XSLT",
    "Cocoon"
]

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


def match_skill(skill_to_match, filetext):
    # skill_to_check =
    skill_to_check = r"(" + skill_to_match + ")"
    # print skill_to_check
    regex = skill_to_check
    # regex = r"(Core Java)"
    # skills =

    test_str = ("Skill Tags: Keras,TensorFlow, Numpy,Javascript, Python, Nodejs, socket.io, websockets,\n"
                "Core Java,JSP/Servlet, Google Dialogflow, Android(native-android studio),\n"
                "Kotlin,Swift, Google MAP API, Facebook API, JavaFX, REST API, HTML,Unix,CSS, SQL,XML, TIBCO EMC Documentum,jQuery\n\n"
                "Skills used: Python, NodeJS, JavaScript, socket.io, websockets, Java, Android(native ),\n"
                "Servlet, HTML, NodeJS, Socket.io, jQuery, HTML, CSS, Google MAP API, Facebook API\n\n"
                "Skills used: Core Java, EJB, J2EE\n\n"
                "Skills used: JavaScript,Java,JSP,Servlet,Dojo,jQuery,EMC Documentum,TIBCO\n"
                "EAI,EMS\n\n"
                "Skills used: Java, JSP, Servlet, SQL, HTML, CSS, JavaScript")
    if (len(skill_to_match) <= 5):
        regex = r"[\s\,]" + skill_to_match + "[\s\,]"

    #    matches = re.finditer(regex, filetext, re.MULTILINE | re.IGNORECASE)

    # if (len(skill_to_match)>1 and  len(skill_to_match)<= 3) :
    # matches = re.finditer(regex, filetext, re.MULTILINE)
    # else :
    matches = re.finditer(regex, filetext, re.MULTILINE | re.IGNORECASE)
    # print(matches.__sizeof__)
    count = 0

    for matchNum, match in enumerate(matches, start=1):
        count = count + 1

        # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
        #                                                                    end=match.end(), match=match.group()))

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            # print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
            #                                                                start=match.start(groupNum),
            #                                                                end=match.end(groupNum),
            #                                                                group=match.group(groupNum)))
    # print("count", count)
    return (count > 0)


# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
def match_skill_category(filetext):
    skills = dict()

    # print filetext
    Software_Engineering_Lst = list()
    Web_Mobile_and_Desktop_Application_Development_Lst = list()
    Artificial_Intelligence_Lst = list()
    Special_Technologies_and_Expertise_Areas_Lst = list()
    APIs_and_Packages_Lst = list()
    Other_Skills_Lst = list()
    combined_skill_list = list()

    for i in Software_Engineering:
        if (match_skill(i, filetext)):
            combined_skill_list.append(i.replace('\\', ''))
            Software_Engineering_Lst.append(i)
            skills['Software_Engineering'] = Software_Engineering_Lst;

    for k in Web_Mobile_and_Desktop_Application_Development:
        if (match_skill(k, filetext)):
            Web_Mobile_and_Desktop_Application_Development_Lst.append(k)
            combined_skill_list.append(k)
            skills['Web_Mobile_and_Desktop_Application_Development'] = Web_Mobile_and_Desktop_Application_Development_Lst;

    for l in Artificial_Intelligence:
        if match_skill(l, filetext):
            Artificial_Intelligence_Lst.append(l)
            combined_skill_list.append(l)
            skills['Artificial_Intelligence'] = Artificial_Intelligence_Lst;

    for m in Special_Technologies_and_Expertise_Areas:
        if match_skill(m, filetext):
            Special_Technologies_and_Expertise_Areas_Lst.append(m)
            combined_skill_list.append(m)
            skills['Special_Technologies_and_Expertise_Areas'] = Special_Technologies_and_Expertise_Areas_Lst;

    for p in APIs_and_Packages:
        if match_skill(p, filetext):
            APIs_and_Packages_Lst.append(p)
            combined_skill_list.append(p)
            skills['APIs_and_Packages'] = APIs_and_Packages_Lst;

    for q in Other_Skills:
        if match_skill(q, filetext):
            Other_Skills_Lst.append(q)
            combined_skill_list.append(q)
            skills['Other_Skills'] = Other_Skills_Lst;

    # print("skills ", skills)

    return combined_skill_list


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
    egineer_name = extractDeveloperName(path)
    return egineer_name, text


def extractDeveloperName(filename):
    # src = pathlib.Path(filename).resolve()

    fname_w_extn = ntpath.basename(filename)

    fname, fextension = os.path.splitext(fname_w_extn)

    # print(fextension)
    # print(fname)
    return fname


def extractTextFromPDF(filename, call_textract=0):
    egineer_name = extractDeveloperName(filename)
    text = ""

    if call_textract > 0:
        text = textract.process(filename, method='tesseract', language='eng', encoding="utf-8")
        return egineer_name, text
    try:

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
    except IOError:
        print('An error occurred trying to read the file =====>', filename)
    except ValueError:
        print('Non-numeric data found in the file. =====>', filename)
    except UnicodeDecodeError:
        print("UnicodeDecodeError : Using os.system pdf2text =====>", filename)
        os.system("pdf2txt.py  '" + (filename) + "'> tmp")
        text = open('tmp', 'r').read()
        print(text)
        os.remove('tmp')
    else:
        print("Things went smoothly!")

    return egineer_name, text


# def writeCSV(engineer, skill_list_category_values):

if __name__ == '__main__':

    directory = sys.argv[1]
    fmt = "%Y_%m_%d_%I_%M_%S_%p"
    now = datetime.now()
    new_skill_list_filename = 'engineerlist_' + now.strftime(fmt) + '.csv'
    # print directory
    # print os.listdir('.')
    # print(os.listdir(directory))

    # print(filename)
    print("current working direcotry", "=>", os.getcwd())

    # paths, fname = os.path.split(filename)

    # print("ntpath basename", "=>", ntpath.basename(filename))
    # print("ospath asename", "=>", os.path.basename(filename))

    count = 0
    other_filetype_counter = 0
    with open(new_skill_list_filename, 'w') as csv_data_file:
        writer = csv.writer(csv_data_file)

        writer.writerow(["ENGINEER", "Skills"])

        for filename in os.listdir(directory):
            if count == 0:
                os.chdir(directory)

            if filename.lower().endswith(".pdf"):

                count = count + 1

                print("processing file", "=>", filename)

                filename = "" + filename + ""
                try:
                    engineer, text = convert_pdf_to_txt(filename)

                    skills_retrieved = match_skill_category(text)

                    if len(skills_retrieved) == 0:
                        print("No Skills Found.Trying PYPDF")
                        engineer, text = extractTextFromPDF(filename)
                        skills_retrieved = match_skill_category(text)

                        if len(skills_retrieved) == 0:
                            print("No Skills Found.Trying Textract Explicitly")
                            engineer, text = extractTextFromPDF(filename, 1)
                            skills_retrieved = match_skill_category(text)

                    print(engineer)
                    # text = codecs.decode(text, encoding='utf-8', errors='strict')
                    # print text

                    writer.writerow([engineer, skills_retrieved])
                except TypeError as e:
                    print(e, "While processing file:- ", filename)
                    writer.writerow([engineer, skills_retrieved])
                    continue

                except Exception as oth:
                    print(oth, "While processing file:- ", filename)
                    writer.writerow([engineer, skills_retrieved])
                    continue
                fs = FreelancerSkill(engineer, skills_retrieved, 30., ADVANCED)
                print(fs)
            else:
                print("File name with other extension", filename)
                other_filetype_counter = other_filetype_counter + 1
                continue
    print("Resumes processed:-", count)
    print("Other Format Files:-", other_filetype_counter)
