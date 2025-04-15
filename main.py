"""
Constructs the UI and pulls in analysis from other files
"""

import streamlit as st
from dataHandling import *
from auditAnalysis import * 


# initialize necessary classes
check = CheckInputs()

# make title header
st.markdown("<h1 style='font-size:50px'>Audit Data Processor</h1>", unsafe_allow_html=True)

# date selector
#audit_date = st.date_input('Select date of audit.', format='YYYY/MM/DD')

welcome = st.write("Upload all data files from the audit. Please only upload data of a single type (i.e. all only .csv or all only .dat).")

# upload files
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, type=['csv', 'dat'])

if uploaded_files:
    # load and merge files
    files = ProcessRawFiles(uploaded_files)

    # once files are merged, show dataframe
    st.write('Uploaded Audit Data')
   
    displayed_audit_data = st.dataframe(files.session_state_data, width=800, height=400, use_container_width=True)

    st.write('Flag Meanings: 0 = audit zero, 1 = cal gas, 2 = mdl check, 3 = imet')
    # download button
    finish = AnalysisFinisher()

    download_button = st.download_button('Download CSV', *finish.download_csv(st.session_state.dataframe), key='download-csv')

    # audit type tabs
    zero_air_tab, calibration_tab, mdl_tab, imet_tab, gps_tab = st.tabs(["Zero Air Audit", "Calibration Audit", "MDL Check", "iMet Audit", "GPS Check"])

    # df that gets actively edited throughout
    audit_df = files.session_state_data

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
                ZeroAirAnalysis(start_time, end_time, files.audit_date, compound, files.analysis_data, audit_df)



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
        gas_concentration = calibration_form.number_input('Calibration Gas Concentration', step=0.01, min_value=0.00)
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
                CalGasAnalysis(start_time, end_time, files.audit_date, compound, gas_concentration, files.analysis_data, audit_df)

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
        time_averaging = mdl_form.radio(
            "Apply time averaging?",
            options=['None', '1 minute', '5 minutes'],
            horizontal=True  # This makes the options appear in a row
        )

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
                MDLCheckAnalysis(spike_start_time, spike_end_time, blank_start_time, blank_end_time, time_averaging, files.audit_date, compound, files.analysis_data, audit_df)

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
        uploaded_file = imet_form.file_uploader("Upload met data for comparison", type=['csv'], key='uploaded_file')
        if uploaded_file:
            # read in the uploaded file
            kestrel_df = pd.read_csv(uploaded_file, skiprows=[0,1,2,4])

        submit_button = imet_form.form_submit_button('Analyze')

        
        if submit_button:
            # check that the inputs are valid
            start_check = check.check_time(start_time)
            end_check = check.check_time(end_time)

            # if all passes, continue with analysis
            if start_check and end_check:
                # proceed with analysis
                print('proceeding with analysis')
                iMetAnalysis(start_time, end_time, files.audit_date, kestrel_df, files.analysis_data, audit_df)

            else:
                if not start_check:
                    start_error.error('Invalid Start Time')
                if not end_check:
                    end_error.error('Invalid End Time')



    with gps_tab:
        st.header("GPS Check Analysis")

        st.write("GPS section under development. No data to display.")

        # analyze_button = st.button('View GPS Analysis')

        # if analyze_button:
        #     GPSCheck(files.analysis_data)




    # st.write('Press the Finish Analsyis button to end the analysis of this data.')

    # end_button = st.button('Finish Analysis')
    # if end_button:
    #     # end the analysis
    #     files.end_analysis(finish.display_data)




