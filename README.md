#vatsaldesai-resume-parsing 

vatsaldesai-resume-parsing is a Python script to parse resumes individual or in bulk.

## Installation

Install the packages as per the requirements.txt 

The script is Python 3.6+ compatible.

```bash
pip3 install -r requirements.txt
```

## Usage

The script accepts three parameters (-D is required parameter)

-D   -  the directory where all resumes are placed  
-O   -  True -if you want to use Google Vision API for resumes which can not be parsed by script pdf libraries.This option also needs google vision api key and you need to execute the command mentioned prior to using this switch

Following command needs to be executed before each script run(only if OCR option is enabled/passed in the parameter):-

```bash
export GOOGLE_APPLICATION_CREDENTIALS="<path to google vision api credentials - which will be .json file>"
```
            
-G   -  google-resumes.txt file the format should be as shown below

```
https://docs.google.com/document/d/1u0o4JTg9nlmbHv6SPiaL_pvDN2a7MwsIqCmQHuGXcVA
https://docs.google.com/document/d/<file id>
```

Following command needs to be issued to run the script with all parameters.

```python
python3 analyze_resume.py -D <directory> -O <True>  -G <google-resumes.txt>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
[MIT](https://choosealicense.com/licenses/mit/)
