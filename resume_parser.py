import re
import os
import pandas as pd
import spacy
import sys, fitz

class Parser:
    
    def __init__(self,skills = "skills.csv") -> None:
        
        self.nlp_name = spacy.load("ner_model")
        self.nlp_others = spacy.load('en_core_web_sm')
        self.skills = list(pd.read_csv(skills).columns.values)

    def read_pdf(self,pdf_file):

        # read pdf
        doc = fitz.open(pdf_file)
        text = ""
        for page in doc:
            text = text+str(page.get_text())
        text = text.strip()
        text_for_name = text.split("\n")
        text = " ".join(text_for_name)
        return text


    def extract_mobile(self,text):

        '''
        Helper function to extract mobile number from text

        param text: plain text extracted from resume file
        return: string of extracted mobile numbers
        '''        
        mob_num_regex = r'''([0][-\.\s]??\d{10}|[+]\d{2}[-\.\s]??\d{10}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}|[+]\d{2}[-\.\s]??\d{5}[-\.\s]\d{5})'''
        phone = re.findall(re.compile(mob_num_regex), text)

        if phone:
            number = ''.join(phone[0])
            return number
    
    def extract_email(self,text):
        '''
        Helper function to extract email id from text

        :param text: plain text extracted from resume file
        '''
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None
    
    def extract_skills(self,text):

        doc = self.nlp_others(text)
        
        # extract skills from noun chunks
        skill1 = [str(token).lower().strip() for token in doc.noun_chunks if str(token).lower().strip() in self.skills]

        # extract sklls from tokens
        skill2 = [str(token).lower().strip() for token in doc if str(token).lower().strip() in self.skills]
        
        #all skills
        return skill1+skill2
    
    def extract_name(self,text):

        # reading only first thousand characters in resume text to reduce inference time
        doc = self.nlp_name(text[:1000])

        for ent in doc.ents:
            if ent.label_ == "Name":
                return ent.text
            else:
                return None
    
    def skill_scorer(self,resume_text,jd_text):

        resume_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(jd_text)
        matching_skills = set(resume_skills).intersection(set(jd_skills))
        similarity_score = len(matching_skills)/len(set(jd_skills))
        return similarity_score, matching_skills
    
    def parsed_and_matched_resume(self,resume_text,jd_text):

        name = self.extract_name(resume_text)
        email = self.extract_email(resume_text)
        phone = self.extract_mobile(resume_text)
        similarity_score, matching_skills = self.skill_scorer(resume_text,jd_text)

        return name,phone,email,similarity_score,matching_skills

# if __name__=="__main__":
#     details_list = []
#     parser = Parser()
#     resume_text = parser.read_pdf(r'C:\Users\Sandeep\Desktop\Aidetic\parser\sandeep_resume.pdf')
#     jd_text = "python"
#     name,phone,email,similarity_score,matching_skills = parser.parsed_and_matched_resume(resume_text,jd_text)
#     details = {}
#     details['name'] = name
#     details['phone'] = phone
#     details['email'] = email
#     details['similarity_score'] = similarity_score
#     details['matching_skills'] = matching_skills
#     details_list.append(details)
#     # print(name,phone,email,similarity_score,matching_skills)    

