import secrets
import streamlit as st
from supabase import create_client, Client
import os
import boto3
import pathlib
import urllib

@st.experimental_singleton
def init_connection():
    url = st.secrets['supabase_url']
    key = st.secrets['supabase_key']
    return create_client(url,key)

supabase = init_connection()

#resume_path = r'C:\Users\Sandeep\Desktop\Resume'

s3 = boto3.client("s3", aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'], aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'])


tf = supabase.table("tools_frameworks").select("*").execute()
ai_br = supabase.table("AI_branches").select("*").execute()

tf_opt = []
for i in tf.data:
    tf_opt.append(i['name'])
    
header = st.container()
form = st.form(key='form1',clear_on_submit=True)

with header:
    st.title('Welcome to AIDETIC')
    st.text('please fill the details.')
with form:
    name = st.text_input('Name')
    email = st.text_input('Email')
    tools = st.multiselect('Select the Tools or Frameworks or languages',options=tf_opt)
    app_opt = []
    for j in ai_br.data:
        app_opt.append(j['name'])
    app = st.multiselect('Select the Application of AI',options=app_opt)
    uploaded_file = st.file_uploader('please upload your resume')
    submit = st.form_submit_button("Submit")
    
    
    if submit:
        dict1 = {}
        dict1['name']=name
        dict1['email'] = email
        dict1['tools_frameworks'] = tools
        dict1['applications_ai'] = app
        if uploaded_file is not None:
            resume_file_name = uploaded_file.name
            s3 = boto3.resource('s3')
            bucket_name = 'datasciencehiring'
            object_name = resume_file_name
            file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), resume_file_name) #os.path.join(resume_path, resume_file_name) 
            bucket = s3.Bucket(bucket_name)
            file_path = bucket.upload_file(file_name, object_name)
            url = f'''https://{bucket_name}.s3.amazonaws.com/{urllib.parse.quote(resume_file_name, safe="~()*!.'")}'''
    
        dict1['resume_link'] = url 
        supabase.table('candidate_details').insert(dict1).execute()
