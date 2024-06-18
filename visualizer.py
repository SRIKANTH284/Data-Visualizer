import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Data Visualizer",
    layout='wide',
    page_icon=':bar_chart:',
    initial_sidebar_state='auto'
)

st.title(':bar_chart: Data Visualizer')
st.sidebar.title(':file_folder: Upload Data')

def save_uploaded_file(uploaded_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    with open(os.path.join(target_folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved successfully: {uploaded_file.name}")

def get_uploaded_dataframe():
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv", "xlsx"])
    return uploaded_file

def clear_data_folder(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def app():
    # File uploader
    uploaded_file = get_uploaded_dataframe()

    if uploaded_file is not None:
        target_folder = r"./data"
        save_uploaded_file(uploaded_file, target_folder)

    working_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = r"./data"  # Update this to your folder path

    # Check if the page has been refreshed
    if 'page_refreshed' not in st.session_state:
        st.session_state['page_refreshed'] = False

    if not st.session_state.page_refreshed:
        # Clear the data folder if the page has been refreshed
        clear_data_folder(folder_path)
        # Set page_refreshed flag to True to prevent further clearing
        st.session_state.page_refreshed = True

    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.xlsx', '.json', '.xml'))]

    # Dropdown to select a file
    selected_file = st.selectbox('Select a file', files, index=None)

    if selected_file:
        # Construct the full path to the file
        file_path = os.path.join(folder_path, selected_file)

        # Read the selected file
        if selected_file.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif selected_file.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif selected_file.endswith('.json'):
            df = pd.read_json(file_path)
        elif selected_file.endswith('.xml'):
            df = pd.read_xml(file_path)
        
        return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")

renderer = app()

if renderer:
    renderer.explorer()
