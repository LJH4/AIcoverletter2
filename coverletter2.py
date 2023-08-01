# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 19:01:37 2023

COVERLETTER
"""

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from trubrics.integrations.streamlit import FeedbackCollector


#from docx import Document

if "response" not in st.session_state:
    st.session_state["response"] = ""

st.set_page_config(page_title="Cover Letter Generator")
st.title("Create Amazing Cover Letters")

#openai_api_key=st.secrets.openai_api_key
openai_api_key=st.secrets["openai"]["openai_api_key"]

template = """
You are an expert in writing cover letters for job applicants.

Write a cover letter for the following job description in a professional tone

{job_description}

The cover letter should consist of two paragraphs.  The cover letter should start as follows:  Dear [Recipient's Name] I am writing to apply for the position of

Personalize with relevant experience and skills from the following description of the applicant:

{applicant_description}

"""

prompt = PromptTemplate(
    input_variables=["job_description", "applicant_description"],
    template=template
)


#user_email = st.sidebar.text_input('Provide your email to be first to receive updates and access to new tools:')

def generate_response(job_details, applicant_details):
  llm = OpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=openai_api_key)
  finalPrompt = prompt.format(job_description=job_details, applicant_description=applicant_details)
  #st.info(llm(finalPrompt))
  return llm(finalPrompt)

with st.form('my_form'):
  job_details = st.text_area('Paste the job description here, or write a few sentences about the role.','Role CEO X.AI. Lead the team whose goal is to understand the true nature of the universe.  Report directly to Elon.')
  applicant_details = st.text_area('Paste your resume here, or write a few sentences about yourself.','Bodybuilder, Conan, Terminator and former governor of California.  I killed the Predator.') 
  submitted = st.form_submit_button('Submit')

  if submitted and openai_api_key.startswith('sk-'):
    st.session_state["response"]=generate_response(job_details, applicant_details)
  
  if st.session_state["response"]:
    response_text = st.session_state["response"].choices[0].text
    #response_text = st.session_state["response"].choices[0].text.replace("\n", "")
    

collector = FeedbackCollector(
    component_name="evaluate_letter",
    email=st.secrets.TRUBRICS_EMAIL, # Store your Trubrics credentials in st.secrets:
    password=st.secrets.TRUBRICS_PASSWORD, # https://blog.streamlit.io/secrets-in-sharing-apps/
)
    
if submitted:   
    st.write('How did the AI do?')
    collector.st_feedback(
        feedback_type="thumbs",
        model="your_model_name",
        open_feedback_label="Any additional feedback?",
        metadata={"response": st.session_state["response"], "prompt": prompt},
    )    
