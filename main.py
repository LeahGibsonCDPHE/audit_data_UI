"""
Constructs the UI and pulls in analysis from other files
"""

import streamlit as st
from dataHandling import ProcessFiles

### TO DO: make login ###

# make title header
st.markdown("<h1 style='font-size:50px'>Audit Data Processor</h1>", unsafe_allow_html=True)

welcome = st.write("To begin, please upload all data files from the audit. Once all files have been uploaded, press the continue button.")

# upload files
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)


# make continue button
continue_button_clicked = st.button("Continue")

if continue_button_clicked:
    merge_status = st.empty()
    merge_status.write("Merging files. This may take a few minutes.")

    # load and merge files
    process_files = ProcessFiles()
    audit_data = process_files.load_and_merge_data(uploaded_files)

    # once files are merged, show dataframe
    merge_status.write('Audit Data')
    displayed_audit_data = st.dataframe(audit_data, width=800, height=400, use_container_width=True)

    # audit type tabs
    zero_air_tab, calibration_tab, mdl_tab, imet_tab, gps_tab = st.tabs(["Zero Air Audit", "Calibration Audit", "MDL Check", "iMet Audit", "GPS Check"])

    # create display for each tab
    with zero_air_tab:
        st.header("Zero Air Audit Analysis")

        # user input boxes
        start_time = st.text_input("Start Time: ")
        end_time = st.text_input("End Time: ")
        compound = st.text_input("Compound Name: ")

        analyze_button = st.button("Analyze")

        if analyze_button:
            # check that the inputs are valid (make function)

            # analysis (make function)


    with calibration_tab:
        st.header("Calibration Audit Analysis")

    with mdl_tab:
        st.header("MDL Check Analysis")
    
    with imet_tab:
        st.header("iMet Audit Analysis")

    with gps_tab:
        st.header("GPS Check Analysis")







