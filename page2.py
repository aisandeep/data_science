from email.policy import default
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


s3 = boto3.client("s3", aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'],aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'])


tf = supabase.table("tools_frameworks").select("*").execute()
ai_br = supabase.table("AI_branches").select("*").execute()
ind_opt = supabase.table("Industries").select("*").execute()
ind_use_map = supabase.table("industries_usecases_mapping").select("*").execute()
use_opt = supabase.table("use_cases").select("*").execute()

#tools&frameworks options
tf_opt = []
for i in tf.data:
    tf_opt.append(i['name'])

#applications of AI options
app_opt = []
for j in ai_br.data:
    app_opt.append(j['name'])

#industries options
opt1 = []
for row in ind_opt.data:
    opt1.append(row['name'])

def in_options():
    return(i for i in opt1 if i not in opt_list)

#industries and use_cases options
def options(a):
    for row in ind_opt.data:
        if row['name'] == a:
            us = row['id']
    us_id = []
    for k in ind_use_map.data:
        if k['industry_id'] == us:
            id1 = k['usecase_id']
            us_id.append(id1)
    fin_opt = []
    for i in us_id:
        for j in use_opt.data:
            if j['id'] == i:
                id2 = j['name']
                fin_opt.append(id2)
    return fin_opt


header = st.container()
form = st.form(key='form1',clear_on_submit=True)

with header:
    st.title('Welcome to AIDETIC')
    st.text('please fill the details.')

    name = st.text_input('Name')
    email = st.text_input('Email')
    tools = st.multiselect('Select the Tools or Frameworks or languages',options=tf_opt)
    app = st.multiselect('Select the Application of AI',options=app_opt)
    
        
    if 'n_rows' not in st.session_state:
        st.session_state.n_rows = 1
    
    opt_list = []
    ind_list = []
    for i in range(st.session_state.n_rows):
        col1, col2 = st.columns(2)
        with col1:
            ind = st.selectbox('Select the Industries',options=in_options(),key=f'form{i}')
            opt_list.append(ind)
        with col2:
            opt2 = options(ind)
            usecase = st.multiselect('use',options=opt2,key=f'game{i}')
        ind_dict = {}
        ind_dict[ind] = usecase
        ind_list.append(ind_dict)

    add = st.button(label="add")

    if add:
        if st.session_state.n_rows < (len(opt1)):
            st.session_state.n_rows += 1
            st.experimental_rerun()
        else:
            st.session_state.n_rows += 0
            st.experimental_rerun()

with form:
    uploaded_file = st.file_uploader('please upload your resume')
    submit = st.form_submit_button("Submit")
    
    if submit:
        dict1 = {}
        dict1['name']=name
        dict1['email'] = email
        dict1['tools_frameworks'] = tools
        dict1['applications_ai'] = app
        dict1['industry_usecases'] = ind_list
        if uploaded_file is not None:
            resume_file_name = uploaded_file.name
            s3 = boto3.resource('s3')
            bucket_name = 'datasciencehiring'
            object_name = resume_file_name
            bucket = s3.Bucket(bucket_name)
            file_name = f'resume/{resume_file_name}'
            with open(file_name, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            bucket.upload_file(file_name, object_name)
            url = f'''https://{bucket_name}.s3.amazonaws.com/{urllib.parse.quote(resume_file_name, safe="~()*!.'")}'''
    
        dict1['resume_link'] = url 
        supabase.table('candidate_details').insert(dict1).execute()
