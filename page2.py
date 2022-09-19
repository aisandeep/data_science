import streamlit as st
from supabase import create_client, Client
import os

@st.experimental_singleton
def init_connection():
    url = st.secrets['supabase_url']
    key = st.secrets['supabase_key']
    return create_client(url,key)

supabase = init_connection()

tf = supabase.table("tools_frameworks").select("*").execute()
ai_br = supabase.table("AI_branches").select("*").execute()

tf_opt = []
for i in tf.data:
    tf_opt.append(i['name'])
    
header = st.container()
form = st.form(key='form1',clear_on_submit=True)

resume_path = r'C:\Users\Sandeep\Desktop\Aidetic\data_science\resume'


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
            file_name = uploaded_file.name
            new_path = os.path.join(resume_path,file_name)
            with open(new_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
        dict1['resume'] = new_path
        supabase.table('candidate_details').insert(dict1).execute()
