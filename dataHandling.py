"""
All handling of all incoming data done here:
    - Reading & merging files
    - Checking and handling inputs
"""

import os
import base64
import re
import chardet
import pytz
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from scipy.optimize import curve_fit



class ProcessRawFiles:

    """
    Class for all processing of data, including:
    - loading, merging, cleaning unloaded files
    - adding new columns and flags to the data
    """
    
    
    def __init__(self, uploaded_files):
        """
        Processes uploaded data files

        Created two dfs; one with the cleaned data for analysis (analysis data), and the second is the working df
        that is used to add new columns and flags, and is also displayed at the top of the UI.

        Inputs:
        - uploaded_files: list of uploaded files from streamlit

        Returns: none
        """

        self.analysis_data, self.display_data, self.audit_date = self.load_and_merge_data(uploaded_files)

        # preserve display_data after button clicks
        if 'dataframe' not in st.session_state:
            st.session_state.dataframe = self.display_data  
        
        self.session_state_data = st.session_state.dataframe
        
        
    @st.cache_data
    def load_and_merge_data(_self, list_of_uploaded_files):
        """
        Loads and merges data files for the specified vehile and date. 
        If there is no data, tells user there was an error and end program.  
        If all dates are not the same, tells user to upload data from the same day.

        Adds column "DateTime" with time in human reasable format.

        Inputs:
        - list_of_uploaded_files: list from streamlit uplorad button

        Returns: df of cleaned data for analysis and raw df with only datetime column added and the date of analysis
        """

        # load data
        merged_df = pd.DataFrame()
        for file in list_of_uploaded_files:
            print(f'loading {file.name}')
            audit_date = file.name[0:8]

            # read file into pandas df
            if file.size > 0:
                # Save file locally
                with open(file.name, 'wb') as f:
                    f.write(file.read())
                with open(file.name, 'rb') as f:
                    result = chardet.detect(f.read())
                df = pd.read_csv(file.name, encoding=result['encoding'], dtype={'UTC Time': float})

                merged_df = pd.concat([merged_df, df], ignore_index=True)
        
        
        # clean data
        cleaned_df = _self.clean_data(merged_df)
        # add datetimes
        cleaned_df = _self.add_datetimes(cleaned_df)

        # made column with just datetimes
        datetime_df = _self.add_datetimes(merged_df)

        # add flag column
        datetime_df = _self.add_flag_column(datetime_df)

        return cleaned_df, datetime_df, audit_date

    def clean_data(self, df):
        """
        Cleans data for autocalibrations
        """
        
        # clean data
        if 'GSU_PUMP_ON monitor []' in df.columns: 
            df.loc[df['GSU_PUMP_ON monitor []'] == 0, 'Benzene C6H6+'] = np.nan
        if 'GSU_VALVE_PR1 monitor []' in df.columns:
            df.loc[df['GSU_VALVE_PR1 monitor []'] == 1, 'Benzene C6H6+'] = np.nan
        if 'GSU_VALVE_PR2 monitor []' in df.columns:
            df.loc[df['GSU_VALVE_PR2 monitor []'] == 1, 'Benzene C6H6+'] = np.nan

        return df

    def add_datetimes(self, df):
        """
        Adds datetime column to data
        """

        if 'UTC Time' in df.columns:

            # sort by UTC time
            df = df.sort_values(by='UTC Time')

            # change type of UTC columns from floats -> ints -> strings
            df['UTC Date'] = df['UTC Date'].astype(int).astype(str)
            df['UTC Time'] = df['UTC Time'].round().astype(int).astype(str)

            # convert times to datetimes (in UTC for now)
            df['DateTime'] = pd.to_datetime(df['UTC Date'] + df['UTC Time'], format='%d%m%Y%H%M%S')

            # make DateTime column the index
            df.set_index(['DateTime'], inplace=True)

            # convert times to local mountain time
            mountain_time = pytz.timezone('America/Denver')
            df.index = df.index.tz_localize('UTC').tz_convert(mountain_time)
        
        elif 'time' in df.columns:

            # convert to datetimes and sort
            df['DateTime'] = pd.to_datetime(df['time'])
            df = df.sort_values(by='DateTime')

            # drop time column
            df.drop('time', axis=1, inplace=True)

            # make Datetimes col the index 
            df.set_index(['DateTime'], inplace=True)

            # set timesone to local    
            mountain_time = pytz.timezone('America/Denver')
            df.index = df.index.tz_localize('America/Denver').tz_convert(mountain_time)

        return df
    
    def add_flag_column(self, df):
        """
        Adds column for flagging different types of audits.

        Inputs:
        - df: pandas dataframe

        Returns: pandas dataframe
        """

        df['Audit Flag'] = np.nan

        return df

class CheckInputs:
    """
    Checks the user inputs are valid
    """

    def __init__(self):
        pass
    
    def check_time(self, input_time):
        """
        Checks that time is of the form hh:mm

        Inputs:
        - input_time: string

        Returns: True/False
        """

        time_pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')

        if time_pattern.match(input_time):
            return True
        else:

            return False
    
    def check_compound(self, compound, data):
        """
        Cheks that the compound is one of the headers of the analysis df.
        
        Inputs:
        - compound: string
        - data: df of data used in analysis
        
        Returns: True/False
        """

        headers = data.columns.tolist()
 

        if compound in headers:
            return True
        else:
            return False


    def check_concentration(self, concentration):
        """
        Checks that the calibration gas concentration is a positive number.
        
        Inputs: 
        - compound
        
        Returns: True/False
        """
        if concentration.isdecimal():
            return True
        else:
            return False


class DataAnalysisTools:
    """
    Class with functions that do the various analysis.
    """

    def __init__(self):
        pass

    def localize_time_inputs(self, time_entry, audit_date):
        """
        Turns user's time input into a datetime and sets the timezone as MT.
        """

        # convert to datetime
        dt = datetime.strptime(audit_date + ' ' + time_entry, '%Y%m%d %H:%M')

        # set local timezone
        local_tz = pytz.timezone('America/Denver')

        # localize the datetime
        localized_dt = local_tz.localize(dt)

        print(f'{time_entry} converted to {localized_dt}')

        return localized_dt

    def shorten_to_analysis(self, df, start_time, end_time, compound):
        """
        Shortens data to the start and end time given for analysis.
        
        Returns series
        """

        # select chunk of data for specified time range and turn to series
        analysis_data = df[(df.index >= start_time) & (df.index <= end_time)][compound]

        return analysis_data
    
    def find_ideal_grouping(self, audit_series):
        """ 
        Finds the ideal grouping of data that minimized the variance 
        while ensuring that the data removed is not necessary.
        
        Idea: 
        First remove outliers user IQR's
        Start with full, outliers removed data series and compute the variance.
        Remove the data point p that is the farthest from the mean, i.e. the largest (p-u)^2
        This rejected data is put into its own group.
        Compute the silhoutte score of p in it's outsiders group.
        Once s.score of p <0, stop removing data points or once set contains 15 data points, 
        whichever comes first

        Returns set of data to use for analysis, with its associated datetime
        """

        # remove outliers
        audit_series = self._remove_outliers(audit_series)

        # begin removing data
        variances = []
        means = []
        sil_scores = []
        above_mean_removed_data = []
        below_mean_removed_data = []
        while len(audit_series) > 15:
            # compute variance, mean, and squared distance from data to mean
            variance = audit_series.var()
            data_mean = audit_series.mean()

            variances.append(variance)
            means.append(data_mean)

            squared_distances = (audit_series - data_mean)**2

            # Find the maximum absolute value among the squared differences
            max_distance = squared_distances.max()

            max_distance_index = squared_distances.abs().idxmax()


            # add this value to its own set 
            remove_point = audit_series[max_distance_index]

            if isinstance(remove_point, pd.core.series.Series):
                print('MULTIPLE REMOVE POINTS')
                for value in remove_point.values:
                    if (value - data_mean)**2 == max_distance:
                        remove_point = value
                        break

            # remove the point from the audit series
            removed_series = audit_series.drop(max_distance_index)

            # compute silhoutte score of the removed point

            # apply modified s.score where between cluster distance is distance from avg of 25th percentile
            Q1 = np.nanpercentile(audit_series, 10)
            Q3 = np.nanpercentile(audit_series, 90)
            low_percentile = removed_series[removed_series <= Q1]
            high_percentile = removed_series[removed_series >= Q3]


            if remove_point > data_mean:
                above_mean_removed_data.append(remove_point)
                if len(above_mean_removed_data) == 1:
                    avg_within_cluster_distance = 0
                else:
                    avg_within_cluster_distance = np.nanmean([abs(remove_point - p) for p in above_mean_removed_data if p != remove_point])
                between_cluster_distance = np.nanmean([abs(remove_point - val) for val in high_percentile.values])
            if remove_point < data_mean:
                below_mean_removed_data.append(remove_point)
                if len(below_mean_removed_data) == 1:
                    avg_within_cluster_distance = 0
                else:
                    avg_within_cluster_distance = np.nanmean([abs(remove_point - p) for p in below_mean_removed_data if p != remove_point])
                between_cluster_distance = np.nanmean([abs(remove_point - val) for val in low_percentile.values])
           

            # # minimum distance between removed point and points in cluster
            #between_cluster_distance = np.nanmin([abs(remove_point - p) for p in removed_series.values])
            print('the distance between clusters is', between_cluster_distance)

            # compute
            sil_score = (between_cluster_distance - avg_within_cluster_distance)/max(between_cluster_distance, avg_within_cluster_distance)
            # add to list of silhoutte scores
            sil_scores.append(sil_score)

            # add in conditions to break
            if sil_score < 0:
                break
            else:
                # remove data from audit_series and loop again
                audit_series = removed_series
        
        # # plot data do far
        # plt.plot(variances, marker='*', label='variance')
        # plt.plot(means, marker='o', label='mean')
        # plt.legend()
        # plt.show()

        return audit_series

    def _remove_outliers(self, audit_series):
        """
        Uses IQR to remove outliers.

        Returns series with outliers removed
        """

        # remove outliers
        Q1 = np.nanpercentile(audit_series, 25)
        Q3 = np.nanpercentile(audit_series, 75)
        IQR = Q3 - Q1
        audit_data_no_outliers = audit_series[(audit_series >= (Q1 - 1.5*IQR)) & (audit_series <= (Q3 + 1.5*IQR))]

        return audit_data_no_outliers
    
    def display_table(self, data):
        """ Displays the given data in streamlit"""

        st.write('Data used in analysis:')
        st.dataframe(data, width=800, height=400, use_container_width=True)

    def compute_basic_stats(self, analysis_series):
        """
        Computes min, max, median, std for the given data series

        Displays in table

        Returns: stats
        """

        stats = {}

        stats['Minimum'] = analysis_series.min()
        stats['Median'] = analysis_series.median()
        stats['Maximum'] = analysis_series.max()
        stats['Mean'] = analysis_series.mean()
        stats['SD'] = analysis_series.std()

        stats_df = pd.DataFrame.from_dict(stats, orient='index').T

        # display
        st.write('Statistics:')
        st.dataframe(stats_df, hide_index=True, use_container_width=True)

        return(stats)
    
    def compute_audit_stats(self, analysis_series_stat, cal_gas_conc):
        """
        Compute audit stats and displays table
        """

        audit_stats = {}

        audit_stats['Percent Recovery'] = (analysis_series_stat['Mean'] / cal_gas_conc)*100
        audit_stats['Max % Recovery'] = (analysis_series_stat['Maximum'] / cal_gas_conc)*100
        audit_stats['Min % Recovery'] = (analysis_series_stat['Minimum'] / cal_gas_conc)*100
        audit_stats['Percent Difference'] = (np.abs(analysis_series_stat['Mean'] - cal_gas_conc)/cal_gas_conc)*100
        avg_val = (analysis_series_stat['Maximum'] + analysis_series_stat['Minimum'])/2
        audit_stats['Range % Difference'] = ((analysis_series_stat['Maximum'] - analysis_series_stat['Minimum'])/avg_val) * 100

        audit_stats_df = pd.DataFrame.from_dict(audit_stats, orient='index').T
        # display
        st.write('Audit Statistics:')
        st.dataframe(audit_stats_df, hide_index=True, use_container_width=True)
    

    def curve_fit(self, x_values, y_values):
        """
        Does curve fit for t-stat data
        """
        popt, pcov = curve_fit(self._func, x_values, y_values)

        return popt
    
    def _func(self, x, a, b, c):
        return a*(1/(x+b))+c
    
    def met_difference_computations(self, analysis_data, kestrel_data):
        """
        Computes the absolute difference between the two data streams when their times overlap.

        Retuns: displays a df where the columns are the met variables and the rows are the stats
        """

        imet_headers = ['Temperature (\u00b0C)', 'Corrected Wind Direction (\u00b0)', 'Pressure (hPa)', 
                        'Relative Humidity (%)', 'Corrected Wind Speed (m/s)']
        
        kestrel_headers = ['Temperature', 'Compass True Direction', 'Barometric Pressure', 'Relative Humidity', 'Wind Speed'] # units: Temp: F, Pressure: inHg, Wind Speed: mph, 


        titles = ['Temperature (\u00b0C)', 'Wind Dir (\u00b0)', 'Pressure (mmHg)', 'RH (%)', 'Wind Speed (m/s)']

        stats_df = pd.DataFrame(columns=titles, index=['Minimum', 'Median', 'Maximum', 'Mean'])
        display_df = pd.DataFrame()
        # Align the DataFrames based on datetime indices
        for i, (imet_header, kestrel_header) in enumerate(zip(imet_headers, kestrel_headers)):
            # Align the dataframes based on the datetime index
            df = pd.merge(analysis_data[imet_header], kestrel_data[kestrel_header], how='inner', left_index=True, right_index=True)
            # Calculate the absolute difference between the two data streams
            diff = 100 * abs(df[imet_header] - df[kestrel_header])/df[imet_header]

            # add to display df
            display_df['iMet '+titles[i]] = df[imet_header]
            display_df['Kestrel '+titles[i]] = df[kestrel_header]


            # fill the stats df
            stats_df.loc['Minimum', titles[i]] = diff.min()
            stats_df.loc['Median', titles[i]] = diff.median()
            stats_df.loc['Maximum', titles[i]] = diff.max()
            stats_df.loc['Mean', titles[i]] = diff.mean()
        
        display_df.reset_index(inplace=True)
        # rename index 
        display_df.rename(columns={'index': 'DateTime'}, inplace=True)
        display_df.set_index('DateTime', inplace=True)
        st.write('Met Data')
        st.dataframe(display_df, width=800, height=400, use_container_width=True)

        st.write('Percent Difference')
        st.dataframe(stats_df, use_container_width=True)
        


    






class FlagData:
    """
    Class for flagging data. Will be set up so that it persist past streamlit recompiling code
    """

    def __init__(self, df, start_time, end_time, type):
        """
        Class for flagging data. 

        Inputs:
        - df: dataframe to be flagged
        - start_time: start time of the data to be flagged
        - end_time: end time of the data to be flagged
        - type: pe of audit/check so the data is properly flagged: 'zero', 'cal', 'mdl', 'met'
        """

        # convert start and end times to time aware

        self.start_time = start_time
        self.end_time = end_time
        self.type = type

        self.type_to_flag = {
            'zero': 0,
            'cal': 1,
            'mdl': 2,
            'imet': 3
        }

        self.flag_data(df)
    
    def flag_data(self ,df):
        """
        Flags data and updates session state to repserve the df
        """

        df.loc[self.start_time:self.end_time, 'Audit Flag'] = self.type_to_flag[self.type]

        # update session state
        self.update_session_state(df)



    def update_session_state(self, df):
        """
        Updates the session state of the display data so that it persists past refreshes.
        """

        st.session_state.dataframe = df

class AnalysisFinisher:
    """
    Class for functions relatted to ending the analysis and saving data
    """

    def __init__(self):
        pass


    def download_csv(self, df):
        """
        Function for downloading df to csv data
        
        Inputs:
        - df: display df to save
        """

        download_csv = df.to_csv(index=False).encode('utf-8')

        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f'{current_date}_audit_analysis.csv'

        return download_csv, filename
    
    def end_analysis(self):
        """
        Called when 'End Analysis' button is pressed.
        
        Lets user save file id desired and ends persistence of dataframe.

        Input:
        - df: display df that has haf flags added to it
        """

        if 'dataframe' in st.session_state:
            del st.session_state.dataframe
