u'''

Resume analysis task

The task involves reading a PDF file and producing FreelancerSkill object
with years_of_experience and experience_level.

The PDF file needs to be parsed carefully so that candidates skills are identified.
Note that some of them are single character long, so searches need to
be carefully managed.  Also, case sensitivity may not always be appropriate.
Some are even written in mixed case.  Further, there may be multiple words
and acronyms involved.  Some type of "fuzzy" match is needed.

One needs to estimate the years of experience - presumably there are dates
in the resume to figure that out.  Otherwise, some guess work based on the
dates in the resume is useful.

One also needs to estimate the level of experience and categorize in the
candidate appropriately.  

The skill list and categories are defined here.

'''
from __future__ import with_statement
from __future__ import absolute_import
import re
import io
import json
import argparse
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from io import open

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(u"-r", u"--resume", required=True,
    help=u"path to resume")
args = vars(ap.parse_args())


Software_Engineering = [
u"C\+\+",   
u"J2EE",
u"Git",
u"OpenShift",
u"Singularity Containerization",
u"Regex",
u"UML Diagrams",
u"Apache Kafka",
u"Scala",
u"VBA",
u"Rust",
u"LISP",
u"Perl",
u"Fortran",
u"Golang",
u"Assembly",
u"Clojure",
u"Kotlin",
u"Dart",
u"WebAssembly",
u"\.NET",
u"\.NET Core",
u"Ansible",
u"Elixir",
u"Erlang",
u"NoSQL",
u"WebRTC",
u"C#",
u"C",
u"SQL",
u"Java",
u"HTML",
u"CSS",
u"JSX",
u"Python",
u"R",
u"UNIX",
u"Ruby",
u"XML",
u"PHP",
u"Docker",
u"Objective C",
u"JavaScript",
u"REST API"
]

Web_Mobile_and_Desktop_Application_Development = [
u"Elm",
u"Mocha",
u"Chai",
u"Bulma",
u"Semantic-UI",
u"Swift",
u"Ember.js",
u"VulcanJS",
u"MeteorJS",
u"Google Tag Manager",
u"Google Analytics",
u"WebSockets",
u"Gatsby",
u"Postman",
u"Cucumber",
u"Wix",
u"Bootstrap",
u"GraphQL",
u"Angular",
u"Typescript",
u"MongoDB",
u"ExpressJS",
u"Data Semantic Layers",
u"SEO",
u"Redux",
u"Webpack",
u"Apollo GraphQL",
u"ECMA",
u"CSS Flex",
u"jQuery",
u"UI Design",
u"UX Design",
u"Interaction Design",
u"Material Design",
u"Flow JS",
u"Babel JS",
u"Ionic",
u"Grind Rocks for Node",
u"Postgres",
u"MySQL",
u"Vagrant",
u"VirtualBox",
u"WebGL",
u"DevOps",
u"Site Reliability",
u"ASP.NET",
u"Drupal",
u"Cordova",
u"Xamarin",
u"Flutter",
u"Microsoft SQL Server",
u"SQLite",
u"Redis",
u"MariaDB",
u"OracleDB",
u"DynamoDB",
u"Cassandra",
u"Couchbase",
u"Chef",
u"ReasonML",
u"Django",
u"Nodejs",
u"Laravel",
u"Flask",
u"React",
u"Ruby on rails",
u"React native",
u"Wordpress",
u"Android native app development",
u"iOS native app development",
u"Windows Application Development",
u"Mac Application Development",
u"Chrome Extension Development",
u"Firefox Extension Development",
u"Safari Extension Development",
u"Internet Explorer Extension Development",
u"XCode",
u"Vue.js",
u"Visual Studio",
u"Android Studio"
]

Artificial_Intelligence = [
u"keras",
u"KNIME",
u"OCR",
u"PyTorch",
u"Torch",
u"Autonomous Vehicles and Self Driving Cars",
u"Artificial intelligence",
u"Machine learning",
u"Deep learning",
u"Natural language processing",
u"Speech recognition",
u"Probabilistic graphical models",
u"Robotics",
u"Computer vision",
u"Reinforcement learning",
u"Data mining",
u"Quadrocopters",
u"Drones"
]

Special_Technologies_and_Expertise_Areas = [
u"Cyber Security",
u"Hackintosh",
u"Sound Engineering",
u"GDPR Compliance",
u"Logic Pro X",
u"Final Cut Pro",
u"Pro Tools",
u"Autodesk Maya",
u"Salesforce Development",
u"Photoshop",
u"Adobe Premiere Pro",
u"IBM DB2",
u"Maven",
u"Turtle Logo",
u"Lego Mindstorms",
u"Autodesk Revit",
u"Google Sketchup",
u"Rhino",
u"3Dmax",
u"CorelDraw",
u"Canva",
u"Inkscape",
u"GIMP",
u"InDesign",
u"Proteomics",
u"Microsoft Excel",
u"Design Modo",
u"Salesforce Pardot",
u"EMR Software",
u"Data Analytics",
u"R for Statistics",
u"Data Science",
u"Adobe Illustrator",
u"3D modeling",
u".obj files",
u"Marketplaces",
u"Product Lifecycle Management",
u"Agile",
u"SCRUM",
u"Kanban",
u"Kaizen",
u"Lean",
u"JMP",
u"Minitab",
u"Shopify",
u"Unreal Engine Game Development",
u"Computational Linguistics",
u"Fourier Transforms",
u"Kubernetes",
u"Microservices",
u"Jupyter",
u"Augmented Reality AR",
u"Virtual Reality VR",
u"Apache Spark",
u"Puppet",
u"CryEngine",
u"QTP/ HP for QA Testing",
u"Appium for QA Testing",
u"Seetest for QA Testing",
u"Apache Jmeter",
u"Load runner",
u"SOAP UI",
u"HP Quality Centre",
u"Version One",
u"Bugzilla",
u"TestCaseLab",
u"qTest",
u"TestRail",
u"TestLink",
u"PractiTest",
u"TestLodge",
u"QACoverage",
u"Fogbuz",
u"TFS",
u"Serverless Architecture",
u"Blockchain",
u"iOT",
u"Bioinformatics",
u"Unity Game Design and Development",
u"Chatbots",
u"Data visualization",
u"Web scrapers",
u"Unity Augmented Reality Design and Development",
u"Browser automation",
u"Mapreduce",
u"Unity Virtual Reality Design and Development",
u"Solidity",
u"Genomics",
u"Ethereum"
]

APIs_and_Packages = [
u"Google NLP API",
u"Socket.IO",
u"Sequelize",
u"Mapbox",
u"Github API",
u"Matplotlib",
u"scikit-learn",
u"PyQt5",
u"ADA Compliance",
u"Pandas",
u"Slack API",
u"Tensorflow",
u"Blockchain API",
u"Ripple API",
u"D3",
u"Vega",
u"Vega Lite",
u"Biopython",
u"Python Selenium",
u"Selenium",
u"Google Maps API",
u"Mailchimp API",
u"Sendgrid API",
u"Twitter APIs",
u"Stripe API",
u"Twilio API",
u"Apache Hadoop",
u"Facebook API",
u"Google Computer Vision API",
u"Google API",
u"AWS Cloud Compliance",
u"HIPAA Cloud Compliance",
u"Finance Cloud Compliance",
u"Government Cloud Compliance (US DoD)",
u"Paypal API"
]

Electrical_and_Mechanical_Engineering = [
u"Autodesk",
u".dxf files",
u"Digital Manufacturing",
u"AutoCAD",
u"MATLAB",
u"Verilog",
u"VHDL",
u"LabVIEW",
u"ANSYS",
u"Intel x86",
u"Hypermesh",
u"SolidWorks",
u"Medical Devices",
u"SPICE (ic design)"
]

Other_Skills = [
u"AWS EC2",
u"AWS Redshift",
u"AWS CloudFront",
u"AWS S3",
u"AWS DynamoDB",
u"AWS ECR",
u"AWS Elastic Beanstalk",
u"Amazon ElastiCache",
u"AWS ElasticMapReduce",
u"AWS IoT",
u"AWS Key Management Service",
u"AWS RDS",
u"Electronic Health Records",
u"Embedded Software",
u"Microcontrollers",
u"Multithreaded Programming",
u"ARM Programming",
u"RTOS",
u"Quality Assurance QA",
u"Oracle BI",
u"SAP",
u"Plotly",
u"Eclipse",
u"Cloud Foundry",
u"Kubernetes",
u"Terraform",
u"Product Management",
u"Google Cloud",
u"AWS",
u"Firebase",
u"SWOT Analysis",
u"FMEA Analysis",
u"VoC Strategy Analysis",
u"PEST Analysis",
u"Pareto Analysis",
u"JIRA",
u"Trello",
u"Asana",
u"Microsoft Project",
u"SAP",
u"Tableau",
u"AWS Elasticsearch",
u"Linux",
u"Windows",
u"MacOS",
u"Raspberry Pi",
u"Azure",
u"Arduino",
u"Heroku",
u"IBM Cloud Watson",
u"AWS Lambda",
u"Spring",
u"Hibernate",
u"DROOLS",
u"OSCache",
u"SOAP",
u"Actuate Espreadsheet",
u"Autosys",
u"XSLT",
u"Cocoon"
]


LEARNING = 0
BEGINNER = 1
MODERATE = 2
ADVANCED = 3
EXPERIENCE = (
    (LEARNING, u'LEARNING'),
    (BEGINNER, u'BEGINNER'),
    (MODERATE, u'MODERATE'),
    (ADVANCED, u'ADVANCED')
)

class FreelancerSkill(object):

    def __init__(self, email, skill, years_of_experience, experience_level):
        self.freelancer_email = email
        self.skill = skill
        self.years_of_experience = years_of_experience
        self.experience_level = experience_level
        
    def  __str__(self):
        return u'Freelancer ' + self.freelancer_email + \
            u' has skill ' + json.dumps(self.skill) + \
            u' with ' + unicode(self.years_of_experience) + u' years of experience;' + \
            u' at ' + unicode(EXPERIENCE[self.experience_level]) + u' level'



def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, u'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text

def match_skill(skill_to_match, filetext):
    
    #skill_to_check =
    skill_to_check = ur"("+skill_to_match+u")"
    print skill_to_check
    regex = skill_to_check
    # regex = r"(Core Java)"
    #skills = 

    test_str = (u"Skill Tags: Keras,TensorFlow, Numpy,Javascript, Python, Nodejs, socket.io, websockets,\n"
                u"Core Java,JSP/Servlet, Google Dialogflow, Android(native-android studio),\n"
                u"Kotlin,Swift, Google MAP API, Facebook API, JavaFX, REST API, HTML,Unix,CSS, SQL,XML, TIBCO EMC Documentum,jQuery\n\n"
                u"Skills used: Python, NodeJS, JavaScript, socket.io, websockets, Java, Android(native ),\n"
                u"Servlet, HTML, NodeJS, Socket.io, jQuery, HTML, CSS, Google MAP API, Facebook API\n\n"
                u"Skills used: Core Java, EJB, J2EE\n\n"
                u"Skills used: JavaScript,Java,JSP,Servlet,Dojo,jQuery,EMC Documentum,TIBCO\n"
                u"EAI,EMS\n\n"
                u"Skills used: Java, JSP, Servlet, SQL, HTML, CSS, JavaScript")
    if(len(skill_to_match) <= 5):
        regex =  ur"[\s\,]"+skill_to_match+u"[\s\,]"

    #    matches = re.finditer(regex, filetext, re.MULTILINE | re.IGNORECASE)

    #if (len(skill_to_match)>1 and  len(skill_to_match)<= 3) :
       # matches = re.finditer(regex, filetext, re.MULTILINE)
    #else :
    matches = re.finditer(regex, filetext, re.MULTILINE | re.IGNORECASE)
    #print(matches.__sizeof__)
    count = 0
    
    for matchNum, match in enumerate(matches, start=1):
        count = count + 1

        #print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
        #                                                                    end=match.end(), match=match.group()))

        for groupNum in xrange(0, len(match.groups())):
            groupNum = groupNum + 1

            #print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
            #                                                                start=match.start(groupNum),
            #                                                                end=match.end(groupNum),
            #                                                                group=match.group(groupNum)))
    #print("count", count)
    return (count > 0)


# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
def match_skill_category(filename):
    skills = dict()
    filetext = extract_text_from_pdf(filename)
    print filetext
    Software_Engineering_Lst = list()
    Web_Mobile_and_Desktop_Application_Development_Lst = list()
    Artificial_Intelligence_Lst= list()
    Special_Technologies_and_Expertise_Areas_Lst= list()
    APIs_and_Packages_Lst= list()
    Other_Skills_Lst= list()

    for i in Software_Engineering:
        if(match_skill(i, filetext)):
            Software_Engineering_Lst.append(i)

    skills[u'Software_Engineering'] = Software_Engineering_Lst;
    

    for k in Web_Mobile_and_Desktop_Application_Development:
        if(match_skill(k, filetext)):
            Web_Mobile_and_Desktop_Application_Development_Lst.append(k)
    skills[u'Web_Mobile_and_Desktop_Application_Development'] = Web_Mobile_and_Desktop_Application_Development_Lst;
    

    for l in Artificial_Intelligence:
        if(match_skill(l, filetext)):
            Artificial_Intelligence_Lst.append(l)

    skills[u'Artificial_Intelligence'] = Artificial_Intelligence_Lst;
    

    for m in Special_Technologies_and_Expertise_Areas:
        if(match_skill(m, filetext)):
            Special_Technologies_and_Expertise_Areas_Lst.append(m)

    skills[u'Special_Technologies_and_Expertise_Areas'] = Special_Technologies_and_Expertise_Areas_Lst;
    

    for p in APIs_and_Packages:
        if(match_skill(p, filetext)):
            APIs_and_Packages_Lst.append(p)

    skills[u'APIs_and_Packages'] = APIs_and_Packages_Lst;

    

    for q in Other_Skills:
        if(match_skill(q, filetext)):
            Other_Skills_Lst.append(q)

    skills[u'Other_Skills'] = Other_Skills_Lst;
    

    #print("skills ", skills)

    return skills

if __name__ == u'__main__':
    skills_retrieved =  match_skill_category(args[u"resume"])

    fs = FreelancerSkill(u"vatsaldin@gmail.com", skills_retrieved, 30., ADVANCED)
    print fs
    #'VatsalD Resume.pdf'