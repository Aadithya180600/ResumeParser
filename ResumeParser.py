import spacy
from spacy import displacy
import sys
import re
import nltk

# Using Spacy NER
NER = spacy.load("en_core_web_sm")
raw_text_f = open('ResumeText.txt', 'r')
raw_text = raw_text_f.read()
raw_text_lines = raw_text.split("\n")
text1 = NER(raw_text)

# Skills List Database hardcoded with different types of skills related to the software job.
# Tried to add as many skills as possible and can be easily updated with new ones.
skills_list = ['c', 'cpp', 'c++', 'java', 'python', 'C#', 'SQL', 'HTML',
               'JavaScript', 'XML', 'C', 'Perl', 'Python', 'PHP', 'Objective-C',
               'AJAX', 'ASP.NET', 'Ruby', 'MS Office', 'Google Drive', 'spreadsheets',
               'email', 'PowerPoint', 'databases', 'social media', 'web', 'enterprise systems',
               'HTML', 'CSS', 'Javascript', 'WordPress', 'Content Management Systems', 'CMS',
               'React', 'Angular', 'Vue', 'Flutter', 'Bootstrap', 'Node js', 'Js', 'react js', 'angular js', 'vue js',
               'node', 'react native', 'react-native',
               'Photoshop', 'Illustrator', 'InDesign', 'Acrobat', 'Free Hand', 'Corel Draw',
               'Analysis', 'conceptual skills', 'brainstorming', 'decision-making', 'Excel',
               'forecasting', 'logistics', 'problem-solving skills',
               'problem', 'solving', 'stastics', 'Kubernetes', 'Docker', 'Azure', 'AWS', 'cloud',
               'django', 'spring', 'spring microservices', 'spring mvc', 'spring boot', 'springboot',
               'spring framework',
               'rest', 'rest api', 'restful web services', 'restapi', 'flask', 'php', 'express', 'express js', 'pearl',
               'kotlin', 'scala',
               'pascal', '.net', 'laravel', 'postman', 'git', 'jira',
               'sql', 'mysql', 'oracle', 'oracle sql', 'azure', 'aws', 'google cloud', 'quickbase', 'prostgresql',
               'prostgre sql',
               'kintone', 'kafka', 'mongo db', 'mongoDB', 'AutoCAD', 'MATLAB', 'Verilog', 'Simulink', 'Pspice',
               'Multisim', 'ETAP',
               'CouchDB', 'Oracle NoSQL', 'Riak']

for i in range(len(skills_list)):
    skills_list[i] = skills_list[i].lower()


# Different Parts of the Resume hardcoded as a List.
# Tried to add as many headings as possible and can be easily updated with new ones.
resume_parts = ['education', 'experience', 'professional experience', 'work experience', 'work history',
                'skills', 'professional career', 'employement', "certifications", 'awards', 'personal information',
                'achievements', 'projects', 'academic projects']


# Resume Parser Class
class ResumeParser:

    # Initialization
    def __init__(self) -> None:
        self.firstName = ''
        self.phoneNum = ''
        self.phoneNumAlt = ''
        self.emaiId = ''
        self.linkedInURL = ''
        self.gitHubURLs = []
        self.otherURLS = []
        self.skills = []
        self.education = ''
        self.experience = ''


    # Method for Extracting Names
    def ExtractName(self):
        for i in raw_text_lines:
            if i == '\n':
                raw_text_lines.remove(i)
            else:
                break
        name = raw_text_lines[0]

        # for word in text1.ents:
        #     if(word.label_ == "PERSON"):
        #         name = word.text
        #         break

        nameword = name.split(" ")
        namewords = []
        for i in nameword:
            if i != '':
                namewords.append(i)
        firstName = " ".join(namewords[0:-1])
        lastName = namewords[-1]
        self.firstName = firstName
        self.lastName = lastName


    # Method to format the phone number into universal format
    def format_phn_num(self, phnno):
        raw_num = []
        for i in phnno:
            if i.isdigit():
                raw_num.append(i)
            if len(raw_num) == 3:
                raw_num.append(") ")
            if len(raw_num) == 7:
                raw_num.append("-")
        if len(raw_num) >= 10:
            raw_num.insert(0, "(")
        return "".join(raw_num)


    # Method for Extracting Phone Numbers
    def ExtractPhoneNum(self):
        phn_no = []

        PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        for word in text1.ents:
            if word.label_ == 'CARDINAL' and PHONE_REG.match(word.text):
                phn_no.append(word.text)

        phone_number = ''
        phone_number_alt = ''
        if len(phn_no) == 1:
            phone_number = phn_no[0]
        elif len(phn_no) > 1:
            phone_number = phn_no[0]
            phone_number_alt = phn_no[1]
        
        self.phoneNum = self.format_phn_num(phone_number)
        self.phoneNumAlt = self.format_phn_num(phone_number_alt)


    # Method for Extracting Email Id    
    def ExtractingEmailId(self):
        EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
        emails = re.findall(EMAIL_REG, raw_text)
        self.emaiId = emails[0]

    
    # Method for Extracting URLS
    def ExtractingURLs(self):
        url_reg = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        urls = re.findall(url_reg, raw_text)

        linkedIn_URL = ""
        github_url = []
        other_urls = []
        for url in urls:
            if "linkedin" in url.split("."):
                linkedIn_URL = url
            elif "github" in url.split("."):
                github_url.append(url)
            else:
                other_urls.append(url)
        
        self.linkedInURL = linkedIn_URL
        self.gitHubURLs = github_url
        self.otherURLS = other_urls


    # Comparing Text with Skills List
    def ComparingTextwithSkills(self, text):

        # Tokenizing the Text
        text_tokens = nltk.word_tokenize(text)

        extractedSkills = []
        for i in text_tokens:
            if i.lower() in skills_list:
                extractedSkills.append(i)

        bigram_skills = list(nltk.bigrams(text_tokens))
        for i in bigram_skills:
            if " ".join(i).lower() in skills_list:
                extractedSkills.append(" ".join(i))

        trigram_skills = list(nltk.trigrams(text_tokens))
        for i in trigram_skills:
            if " ".join(i).lower() in skills_list:
                extractedSkills.append(" ".join(i))

        skills_set = set(extractedSkills)
        extractedSkills = list(skills_set)
        extractedSkills.sort()
        return extractedSkills


    # Method for Extracting Applicant Skills
    def ExtractingSkills(self):
        self.skills = self.ComparingTextwithSkills(raw_text)

    
    # Method for Extracting Education Details
    def ExtractEducation(self):

        education = []

        flag = 0
        for line in raw_text_lines:
            line = line.lower()
            if flag == 0 and (line.split(" ")[0].lower() == 'education' or line.split(" ")[1].lower() == 'education'):
                flag = 1
                continue
            if flag == 1:
                line_words = nltk.word_tokenize(line)[0:3]
                bigram_skills = list(nltk.bigrams(line_words))

                if any(l in resume_parts for l in line_words):
                    break
                elif any(l in resume_parts for l in bigram_skills):
                    break
                else:
                    education.append(line)
        
        self.education = "\n".join(education)

    
    # Method for Extracting Experience Data
    def ExtractingExperience(self):

        # Different types of Experience Headings are hardcoded
        resume_experience = ['experience', 'professional experience', 'work experience', 'work history',
                        'professional career', 'employement']
        
        experience = []

        flag = 0
        for line in raw_text_lines:
            line = line.lower()
            if flag == 0:
                line_words = line.split(" ")[0:3]
                if any(l in resume_experience for l in line_words):
                    flag = 1
                    continue
                bigram_skills = list(nltk.bigrams(line_words))
                if any(l in resume_experience for l in bigram_skills):
                    flag = 1
                    continue

            if flag == 1:
                line_words = nltk.word_tokenize(line)[0:3]
                bigram_skills = list(nltk.bigrams(line_words))

                if any(l in resume_parts for l in line_words):
                    break
                elif any(l in resume_parts for l in bigram_skills):
                    break
                else:
                    experience.append(line)
        self.experience = "\n".join(experience)


    # Method for Printing the Extracted Data
    def PrintingExtractedData(self):

        # Printing Names
        print()
        print("First_Name: " + self.firstName)
        print("Last_Name: " + self.lastName)
        print()

        # Printing Phone Numbers
        print("Phone Number: "+self.phoneNum)
        print("Alternate Phone Number: "+self.phoneNumAlt)
        print()

        # Printing Email Id
        print("Email Id: " + self.emaiId)
        print()

        # Printing URLS
        print("Linked URL: " + self.linkedInURL)
        print("Github URL: ")
        for url in self.gitHubURLs:
            print(url)
        print("Other URLS: ")
        for url in self.otherURLS:
            print(url)
        print()

        # Printing Applicant Skills
        print("Applicant Skills: " + ", ".join(self.skills[0:-2]) + self.skills[-1])
        print()

        # Printing Education Details
        print("Education Details: ")
        print(self.education)
        print()

        # Printing Experience Details
        print("Experience Details: ")
        print(self.experience)
        print()
