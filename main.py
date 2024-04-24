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

welcome = st.write("To begin, please upload all data files from the audit.")

# upload files
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

if uploaded_files:
    # load and merge files
    files = ProcessFiles(uploaded_files)

    # once files are merged, show dataframe
    st.write('Raw Audit Data')
    displayed_audit_data = st.dataframe(files.display_data, width=800, height=400, use_container_width=True)

    # audit type tabs
    zero_air_tab, calibration_tab, mdl_tab, imet_tab, gps_tab = st.tabs(["Zero Air Audit", "Calibration Audit", "MDL Check", "iMet Audit", "GPS Check"])

    # display for zero air tab
    with zero_air_tab:
        st.header("Zero Air Audit Analysis")

        zero_air_form = st.form(key='zero_air', clear_on_submit=False, border=True)

        start_time = zero_air_form.text_input("Start Time (hh&#58;mm)")
        start_error = zero_air_form.empty()
        end_time = zero_air_form.text_input("End Time (hh&#58;mm)")
        end_error = zero_air_form.empty()
        compound = zero_air_form.text_input("Compound Name (as it appears in the data)")
        compound_error = zero_air_form.empty()

        submit_button = zero_air_form.form_submit_button('Analyze')

        if submit_button:
            # check that the inputs are valid
            start_check = check.check_time(start_time)
            end_check = check.check_time(end_time)
            compound_check = check.check_compound(compound, files.analysis_data)

            # if all passes, continue with analysis
            if start_check and end_check and compound_check:
                # proceed with analysis
                print('proceeding with analysis')
                ######## ZERO AIR ANALYSIS HERE ####################

            else:
                if not start_check:
                    start_error.error('Invalid Start Time')
                if not end_check:
                    end_error.error('Invalid End Time')
                if not compound_check:
                    compound_error.error('Invalid Compound Name')


            

    # display for calibration tab
    with calibration_tab:
        st.header("Calibration Audit Analysis")

        calibration_form = st.form(key='calibration', clear_on_submit=False, border=True)

        start_time = calibration_form.text_input('Start Time (hh&#58;mm)')
        start_error = calibration_form.empty()
        end_time = calibration_form.text_input('End Time (hh&#58;mm)')
        end_error = calibration_form.empty()
        compound = calibration_form.text_input('Compound Name (as it appears in the data)')
        compound_error = calibration_form.empty()
        gas_concentration = calibration_form.number_input('Calibration Gas Concentration', min_value=0)
        gas_error = calibration_form.empty()

        submit_button = calibration_form.form_submit_button('Analyze')

        if submit_button:
            # check that the inputs are valid
            start_check = check.check_time(start_time)
            end_check = check.check_time(end_time)
            compound_check  = check.check_compound(compound, files.analysis_data)

            # if all passes, continue with analysis
            if start_check and end_check and compound_check:
                # proceed with analysis
                print('proceeding with analysis')
                ############## CALIBRATION ANALYSIS HERE #################

            else:
                if not start_check:
                    start_error.error('Invalid Start Time')
                if not end_check:
                    end_error.error('Invalid End Time')
                if not compound_check:
                    compound_error.error('Invalid Compound Name')


    # display for mdl check tab
    with mdl_tab:
        st.header("MDL Check Analysis")

        mdl_form = st.form(key='mdl_form', clear_on_submit=False, border=True)

        spike_start_time = mdl_form.text_input('Spike Start Time (hh&#58;mm)')
        spike_start_error = mdl_form.empty()
        spike_end_time = mdl_form.text_input('Spike End Time (hh&#58;mm)')
        spike_end_error = mdl_form.empty()
        blank_start_time = mdl_form.text_input('Blank Start Time (hh&#58;mm)')
        blank_start_error = mdl_form.empty()
        blank_end_time = mdl_form.text_input('Blank End Time (hh&#58;mm)')
        blank_end_error = mdl_form.empty()
        compound = mdl_form.text_input('Compound Name (as it appears in the data)')
        compound_error = mdl_form.empty()

        submit_button = mdl_form.form_submit_button('Analyze')

        if submit_button:
            # check that the inputs are valid
            spike_start_check = check.check_time(spike_start_time)
            spike_end_check = check.check_time(spike_end_time)
            blank_start_check = check.check_time(blank_start_time)
            blank_end_check = check.check_time(blank_end_time)
            compound_check  = check.check_compound(compound, files.analysis_data)

            # if all passes, continue with analysis
            if spike_start_check and spike_end_check and blank_start_check and blank_end_check and compound_check:
                # proceed with analysis
                print('proceeding with analysis')
                ############## MDL ANALYSIS HERE #################

            else:
                if not spike_start_check:
                    spike_start_error.error('Invalid Start Time')
                if not spike_end_check:
                    spike_end_error.error('Invalid End Time')
                if not blank_start_check:
                    blank_start_error.error('Invalid Start Time')
                if not blank_end_check:
                    blank_end_error.error('Invalid End Time')
                if not compound_check:
                    compound_error.error('Invalid Compound Name')



    with imet_tab:
        st.header("iMet Audit Analysis")

        imet_form = st.form(key='imet_form', clear_on_submit=False, border=True)

        start_time = imet_form.text_input('Start Time (hh&#58;mm)')
        error_start = imet_form.empty()
        end_time = imet_form.text_input('End Time (hh&#58;mm)')
        error_end = imet_form.empty()

        # upload for kestrel data   
        uploaded_files = imet_form.file_uploader("Upload met data for comparison", accept_multiple_files=True)

        submit_button = imet_form.form_submit_button('Analyze')

        
        if submit_button:
            # check that the inputs are valid
            start_check = check.check_time(start_time)
            end_check = check.check_time(end_time)

            # if all passes, continue with analysis
            if start_check and end_check:
                # proceed with analysis
                print('proceeding with analysis')
                ############## imet ANALYSIS HERE #################

            else:
                if not start_check:
                    start_error.error('Invalid Start Time')
                if not end_check:
                    end_error.error('Invalid End Time')



    with gps_tab:
        st.header("GPS Check Analysis")

        ### GPS ANALYSIS HERE ####









