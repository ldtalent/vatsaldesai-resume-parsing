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
-O   -  True if you want to use Google Vision API for resumes which can not be parsed by script pdf libraries  
-G   -  google-resumes.txt file the format should be as shown in the attached sample file in the repository  


```python
python3 analyze_resume.py -D <directory> -O <True>  -G <google-resumes.txt>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
[MIT](https://choosealicense.com/licenses/mit/)
