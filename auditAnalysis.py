"""
Code for the analysis of the audit data
"""


import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import scipy.stats as stats
from pyproj import CRS
from dataHandling import DataAnalysisTools, FlagData
from dataVisualization import DataVisualization

class ZeroAirAnalysis:

    def __init__(self, start_time, end_time, audit_date, compound, analysis_data, display_data):
        """
        Inputs:
        - start_time: 'hh'mm' start time
        - end_time: 'hh:mm' end time
        - audit_date: 'yyyymmdd' date of the audit
        - compound: compround for analysis
        - analysis_data: data to be used in the analysis
        - display_data: the complete dataset that is updated with flags
        
        Returns: none, updates display data
        """

        self.analysis_tools = DataAnalysisTools()
        self.plot = DataVisualization()


        # convert times to datetimes
        self.start_time = self.analysis_tools.localize_time_inputs(start_time, audit_date) 
        self.end_time = self.analysis_tools.localize_time_inputs(end_time, audit_date) 

        self.compound = compound

        # flag the display data (and update state)
        FlagData(display_data, self.start_time, self.end_time, type='zero')

        self.zero_air_analysis(analysis_data)

    
    def zero_air_analysis(self, analysis_data):
        """
        Perform analysis
        """

        # shorted df to the timeframe to analyze
        analysis_series = self.analysis_tools.shorten_to_analysis(analysis_data, self.start_time, self.end_time, self.compound)

        # if there is no remaining data
        if analysis_series.empty:
            st.write('No data to process. Please check that there is data between the given Start Time and End Time.')
       
        # find ideal grouping of points
        ideal_data = self.analysis_tools.find_ideal_grouping(analysis_series)

        # compute basic and display basic stats
        stats = self.analysis_tools.compute_basic_stats(ideal_data)

        # display series of ideal data
        self.analysis_tools.display_table(ideal_data)

        st.write('Plots')

        # plot scatter of data
        self.plot.scatter_plot(analysis_data[self.compound], analysis_series, ideal_data)


        # plot histogram of data
        self.plot.histogram_plot(ideal_data, mean=stats['Mean'])

    

class CalGasAnalysis:

    def __init__(self, start_time, end_time, audit_date, compound, cal_gas_conc, analysis_data, display_data):
        """
        Inputs:
        - start_time: 'hh'mm' start time
        - end_time: 'hh:mm' end time
        - audit_date: 'yyyymmdd' date of the audit
        - compound: compround for analysis
        - cal_gas_conc: the calibration gas concentration (int)
        - analysis_data: data to be used in the analysis
        - display_data: the complete dataset that is updated with flags
        
        Returns: none, updates display data
        """

        self.analysis_tools = DataAnalysisTools()
        self.plot = DataVisualization()


        # convert times to datetimes
        self.start_time = self.analysis_tools.localize_time_inputs(start_time, audit_date) 
        self.end_time = self.analysis_tools.localize_time_inputs(end_time, audit_date) 

        self.compound = compound
        self.cal_gas_conc = cal_gas_conc

        # flag the display data (and update state)
        FlagData(display_data, self.start_time, self.end_time, type='cal')

        self.cal_analysis(analysis_data)
    
    def cal_analysis(self, analysis_data):
        """
        Performs analysis
        """

        
        # shorted df to the timeframe to analyze
        analysis_series = self.analysis_tools.shorten_to_analysis(analysis_data, self.start_time, self.end_time, self.compound)
       
        # find ideal grouping of points
        ideal_data = self.analysis_tools.find_ideal_grouping(analysis_series)

        # compute basic and display basic stats
        stats = self.analysis_tools.compute_basic_stats(ideal_data)

        # compute the audit stats
        self.analysis_tools.compute_audit_stats(stats, self.cal_gas_conc)


        # display series of ideal data
        self.analysis_tools.display_table(ideal_data)

        st.write('Plots')

        # plot scatter of data
        self.plot.scatter_plot(analysis_data[self.compound], analysis_series, ideal_data)

        # plot histogram of data
        self.plot.histogram_plot(ideal_data, mean=stats['Mean'])





class MDLCheckAnalysis:

    def __init__(self, spike_start, spike_end, blank_start, blank_end, audit_date, compound, analysis_data, display_data):
        """
        Inputs:
        - spike_start: start time for spike
        - spike_end: end time for spike
        - blank_start: start time for blank
        - blank_end: end time for blank
        - audit_date: 'yyyymmdd'
        - compound: compound header strv
        - analysis_data: df to be used in analydid
        - display_data: df that is updated with flags
        """
        self.analysis_tools = DataAnalysisTools()
        self.plot = DataVisualization()


        # convert times to datetimes
        self.spike_start = self.analysis_tools.localize_time_inputs(spike_start, audit_date)
        self.spike_end = self.analysis_tools.localize_time_inputs(spike_end, audit_date)
        self.blank_start = self.analysis_tools.localize_time_inputs(blank_start, audit_date)
        self.blank_end = self.analysis_tools.localize_time_inputs(blank_end, audit_date)

        self.compound = compound
        
        # curve fit for t-stat data
        epa_t_statistic = {
            'n': [7, 8, 9, 10, 11, 16, 21, 26, 31, 32, 48, 50, 61, 64, 80, 96, 100], # number of data points
            't': [3.143, 2.998, 2.896, 2.821, 2.764, 2.602, 2.528, 2.485, 2.457, 2.453, 2.408, 2.405, 2.39, 2.387, 2.374, 2.366, 2.365] # t stat value
        }

        self.popt = self.analysis_tools.curve_fit(epa_t_statistic['n'], epa_t_statistic['t'])




        # flag the display data (and update state)
        FlagData(display_data, self.spike_start, self.spike_end, type='mdl') 

        self.mdl_analysis(analysis_data)
    
    def mdl_analysis(self, analysis_data):
        """
        Performs analysis
        """

        # shorted df to the timeframe to analyze
        spike_series = self.analysis_tools.shorten_to_analysis(analysis_data, self.spike_start, self.spike_end, self.compound)
        # find ideal grouping of points
        spike_data = self.analysis_tools.find_ideal_grouping(spike_series)


        # shorted df to the timeframe to analyze
        blank_series = self.analysis_tools.shorten_to_analysis(analysis_data, self.blank_start, self.blank_end, self.compound)
        # find ideal grouping of points
        blank_data = self.analysis_tools.find_ideal_grouping(blank_series)

        # plot data
        self.plot.scatter_selection(analysis_data[self.compound], spike_series, blank_series, spike_data, blank_data)

        st.markdown('**Spike**')

        # compute stats for both and display
        spike_stats = self.analysis_tools.compute_basic_stats(spike_data)
        self.analysis_tools.display_table(spike_data)


        st.markdown('**Blank**')

        blank_stats = self.analysis_tools.compute_basic_stats(blank_data)
        self.analysis_tools.display_table(blank_data)



        # compute MDL

        st.markdown('**MDL$_s$ Computation**')
        number_points = len(spike_data)
        st.write(f'Number of Points =', number_points)
        t_stat = round(stats.t.ppf(0.99, number_points-1),3)
        st.write(f't-statistic = {t_stat}')
        sd = spike_stats['SD']
        st.write(f'SD = {sd}')
        mdl_s = t_stat * sd
        st.write(f'MDL$_s$ = {mdl_s}')


        st.markdown('**MDL$_b$ Computation**')
        number_points = len(blank_data)
        st.write(f'Number of Points =', number_points)
        if number_points <= 100:
            st.write('Since the degrees of freedom are less than 100, the MDL will be computed using the Students t-statistic.')
            x_bar = np.max([blank_stats['Mean'], 0])
            st.write(f'Mean = {x_bar}')
            t_stat = round(stats.t.ppf(0.99, number_points-1),3)
            st.write(f't-statistic = {t_stat}')
            sd = blank_stats['SD']
            st.write(f'SD = {sd}')
            mdl_b = x_bar + t_stat * sd
            st.write(f'MDL$_b$ = {mdl_b}')
        else:
            st.write('Since there are more than 100 samples available, the MDL is set to the 99th percentile of the samples, sorted in in rank order. See the EPA MDL Procedure document for a detailed description of this process.')
            ordered_data = np.sort(blank_data)
            rank = round(number_points*0.99)
            mdl_b = ordered_data[rank-1]
            st.write(f'MDL$_s$ = {mdl_b}')


        mdl = np.max([mdl_s, mdl_b])
        st.markdown(f'**MDL = {mdl}**')





class iMetAnalysis:

    def __init__(self, start_time, end_time, audit_date, kestrel_data, analysis_data, display_data):
        """
        Inputs:
        - start_time: start time 
        - end_time: end time
        - audit_date: 'yyyymmdd'
        - upload: kestral data upload
        - analysis_data: dataframe of data to be analyzed
        - display_data: data to be flagged
        """

        self.analysis_tools = DataAnalysisTools()
        self.plot = DataVisualization()

        # convert times to datetimes
        self.start_time = self.analysis_tools.localize_time_inputs(start_time, audit_date) 
        self.end_time = self.analysis_tools.localize_time_inputs(end_time, audit_date) 

        # flag the display data (and update state)
        FlagData(display_data, self.start_time, self.end_time, type='imet')

        self.imet_analysis(analysis_data, kestrel_data)
    
    def imet_analysis(self, analysis_data, kestrel_data):
        """
        Performs the analysis
        """
        
        # shorted df to the timeframe to analyze
        analysis_data = analysis_data[(analysis_data.index >= self.start_time) & (analysis_data.index <= self.end_time)]

        kestrel_data['FORMATTED DATE_TIME'] = pd.to_datetime(kestrel_data['FORMATTED DATE_TIME']).dt.tz_localize('America/Denver')
        # set index to be datetime column
        kestrel_data = kestrel_data.set_index('FORMATTED DATE_TIME')

        # conver data to preoper units
        kestrel_data['Temperature'] = (kestrel_data['Temperature'] - 32) * (5/9) # F -> C
        kestrel_data['Barometric Pressure'] = kestrel_data['Barometric Pressure'] * 25.3 # inHg -> mmHg
        kestrel_data['Wind Speed'] = kestrel_data['Wind Speed'] * (1609.34 / 3600)
        analysis_data['Pressure (hPa)'] = analysis_data['Pressure (hPa)'] * 0.7500637554 # hPa -> mmHg

        # plot timeseries for all variables
        self.plot.met_plot(analysis_data, kestrel_data)

        # compute the mean, min, and max of the absolute differences and display table
        self.analysis_tools.met_difference_computations(analysis_data, kestrel_data)

        





class GPSCheck:
    
    def __init__(self, analysis_data):
        """
        Plots the GPS locations for the entire audit
        """

        self.plot = DataVisualization()

        # just saves GPS related columns
        df = analysis_data[['GPS Number Of Satellites', 'GPS Latitude (\u00b0N)', 'GPS Longitude (\u00b0E)']]

        self.gps_analysis(df)
    
    def gps_analysis(self, df):
        """
        Performs GPS analysis
        """

        # convert into geopandas df
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['GPS Longitude (\u00b0E)'], df['GPS Latitude (\u00b0N)']), crs=CRS('EPSG:4326'))
        gdf_wm = gdf.to_crs('EPSG:3857')

        self.plot.gps_map(df, gdf_wm)



       
           

