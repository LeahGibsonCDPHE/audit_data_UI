"""
Constructs the UI and pulls in analysis from other files
"""

import streamlit as st
from dataHandling import ProcessFiles, CheckInputs

### TO DO: make login ###

# initialize necessary classes
check = CheckInputs()

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
    files = ProcessFiles(uploaded_files)

    # once files are merged, show dataframe
    merge_status.write('Audit Data')
    displayed_audit_data = st.dataframe(files.display_data, width=800, height=400, use_container_width=True)

    # audit type tabs
    zero_air_tab, calibration_tab, mdl_tab, imet_tab, gps_tab = st.tabs(["Zero Air Audit", "Calibration Audit", "MDL Check", "iMet Audit", "GPS Check"])

    # create display for each tab
    with zero_air_tab:
        st.header("Zero Air Audit Analysis")

        # user input boxes
        if 'start_time' not in st.session_state:
            st.session_state['start_time'] = None

        start_time = st.text_input("Start Time:", value=st.session_state['start_time'])
        # update session state
        st.session_state['start_time'] = start_time
        start_error = st.empty()
        
        end_time = st.text_input("End Time: ")
        end_error = st.empty()
        compound = st.text_input("Compound Name: ")
        compound_error = st.empty()

        analyze_button = st.button("Analyze")

        if analyze_button:
            # check that the inputs are valid
            start_check = check.check_time(start_time)
            end_check = check.check_time(end_time)
            compound_check = check.check_compound(compound)

            # if all passes, continue with analysis
            if start_check and end_check and compound_check:
                # proceed with analysis
                print('proceeding with analysis')

            else:
                if not start_check:
                    start_error.error('Invalid Start Time')
                if not end_check:
                    end_error.error('Invalid End Time')
                if not compound_check:
                    st.error('Invalid Compound Name')


            


    with calibration_tab:
        st.header("Calibration Audit Analysis")

    with mdl_tab:
        st.header("MDL Check Analysis")
    
    with imet_tab:
        st.header("iMet Audit Analysis")

    with gps_tab:
        st.header("GPS Check Analysis")







