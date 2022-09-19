import streamlit as st
from supabase import create_client, Client

@st.experimental_singleton
def init_connection():
    url = st.secrets['supabase_url']
    key = st.secrets['supabase_key']
    return create_client(url,key)

supabase = init_connection()
#@st.experimental_memo
# def ind_options():
#     return supabase.table("Industries").select("name").execute()
# def use_options():  
#     return supabase.table("use_cases").select("name").execute()

ind_opt = supabase.table("Industries").select("*").execute()
ind_use_map = supabase.table("industries_usecases_mapping").select("*").execute()
use_opt = supabase.table("use_cases").select("*").execute()

opt1 = []
for row in ind_opt.data:
    opt1.append(row['name'])

#new = supabase.table("Industries").select("name").execute()

header = st.container()
form = st.form(key='form2',clear_on_submit=True)


with header:
    st.title('Welcome to AIDETIC')
    st.text('please fill the details.')
with form:
    name = st.text_input('Name')
    email = st.text_input('Email')
    company_name = st.text_input('Company Name')
    url = st.text_input('URL')
    industry = st.selectbox('Select the industry',options=opt1)
    for row in ind_opt.data:
        if row['name'] == industry:
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
    use_cases = st.multiselect('Select the use-cases',options=fin_opt)
    submit = st.form_submit_button('submit')

    if submit:
        dict1 = {}
        dict1['name'] = name
        dict1['email'] = email
        dict1['company_name'] = company_name
        dict1['url'] = url
        dict1['industry'] = industry
        dict1['usecases'] = use_cases
        supabase.table('company_details').insert(dict1).execute()