import streamlit as st
from supabase import create_client, Client
import pandas as pd
import json
st.set_page_config(layout='wide')

@st.experimental_singleton
def init_connection():
    url = st.secrets['supabase_url']
    key = st.secrets['supabase_key']
    return create_client(url,key)

supabase = init_connection()

industries = supabase.table('Industries').select('*').execute()
usecases = supabase.table('use_cases').select('*').execute()
ind_use_mapp = supabase.table('industries_usecases_mapping').select('*').execute()
ml_proc = supabase.table('ML_process').select('*').execute()
tl_fr = supabase.table('tools_frameworks').select('*').execute()
roles = supabase.table('roles').select('*').execute()
ai_b = supabase.table('AI_branches').select('*').execute()
ai_map = supabase.table('AI_branches_mapping').select('*').execute()


col1, col2, col3 = st.columns(3)
with col1:
    col1.header("Industries table")
    ind_df = pd.json_normalize(industries.data)
    ind_df = ind_df.set_index('id')
    col1 = st.write(ind_df)
with col2:
    col2.header('USE CASES Table')
    use_df = pd.json_normalize(usecases.data)
    use_df = use_df.set_index('id')
    col2 = st.write(use_df)
with col3:
    col3.header('mapping table')
    in_us_map = pd.json_normalize(ind_use_mapp.data)
    in_us_map = in_us_map.set_index('id')
    col3 = st.write(in_us_map)


# st.write(ml_proc.data)
# st.write(tl_fr.data)
# st.write(roles.data)


col4, col5, col6 = st.columns(3)
with col4:
    col4.header('ML process table')
    ml_df = pd.json_normalize(ml_proc.data)
    #ml_df = ml_df.set_index('id')
    col4 = st.write(ml_df)
with col5:
    col5.header('tools & frameworks')
    list1 = []
    list2 = []
    for i in tl_fr.data:
        tl_dict = {}
        tl_dict['id'] = i['id']
        tl_dict['name'] = i['name']
        tl_dict['type'] = i['type']
        list1.append(tl_dict)
        list2.append(str(i['ml_process_id']))

    tl_df = pd.DataFrame.from_dict(list1)
    tl_df['ml_process_id'] = list2
    #tl_df = tl_df.set_index('id')
    col5 = st.write(tl_df)
with col6:
    col6.header('Roles')
    role_df = pd.json_normalize(roles.data)
    role_df = role_df.set_index('id')
    col6 = st.write(role_df)

col7, col8 = st.columns(2)
with col7:
    col7.header('AI Branches')
    ai_df = pd.json_normalize(ai_b.data)
    ai_df = ai_df.set_index('id')
    col7 = st.write(ai_df)
with col8:
    col8.header('AI Branches mapping')
    ai_m_df = pd.json_normalize(ai_map.data)
    ai_m_df = ai_m_df.set_index('id')
    col8 = st.write(ai_m_df)