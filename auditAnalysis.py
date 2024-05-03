"""
Code for the analysis of the audit data
"""


import streamlit as st
import numpy as np
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
        #FlagData(display_data, self.start_time, self.end_time, type='mdl') 

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
        self.plot.scatter_selection(analysis_data[self.compound], spike_series, blank_series)

        st.write('Spike')

        # compute stats for both and display
        spike_stats = self.analysis_tools.compute_basic_stats(spike_series)
        self.analysis_tools.display_table(spike_series)


        st.write('Blank')

        blank_stats = self.analysis_tools.compute_basic_stats(blank_data)
        self.analysis_tools.display_table(blank_data)



        # compute MDL

        st.markdown('**MDL$_s$ Parameters**')
        number_points = len(spike_data)
        t_stat = self.analysis_tools._func(number_points, *self.popt)
        st.write(f't-statistic = {t_stat}')
        sd = spike_stats['SD']
        st.write(f'SD = {sd}')
        mdl_s = t_stat * sd
        st.write(f'MDL$_s$ = {mdl_s}')

        st.markdown('**MDL$_b$ Parameters**')
        x_bar = np.max([blank_stats['Mean'], 0])
        st.write(f'Mean = {x_bar}')
        number_points = len(blank_data)
        t_stat = self.analysis_tools._func(number_points, *self.popt)
        st.write(f't-statistic = {t_stat}')
        sd = blank_stats['SD']
        st.write(f'SD = {sd}')
        mdl_b = x_bar + t_stat * sd
        st.write(f'MDL$_b$ = {mdl_b}')

        mdl = np.max([mdl_s, mdl_b])
        st.markdown(f'**MDL = {mdl}**')



 

    
    # def _linear_interpolation(self, x0):
    #     """
    #     Does linear interpolation for t-statistic

    #     Inputs:
    #     - x0: number of datapoints
    #     """

    #     x_values = self.epa_t_statistic['n']
    #     y_values = self.epa_t_statistic['t']

    #     # Find the index of the nearest x value in the list
    #     i = min(range(len(x_values)), key=lambda i: abs(x_values[i] - x0))
        
    #     # Perform linear interpolation
    #     if x_values[i] == x0:
    #         y_o = y_values[i]
    #     else:
    #         slope = (y_values[i+1] - y_values[i]) / (x_values[i+1] - x_values[i])
    #         y0 = y_values[i] + slope * (x0 - x_values[i])
        
    #     return y0

    def _func(x,a,b,c):
        return a*(1/(x+b))+c



class iMetAnalysis:

    def __init__(self):
        pass

class GPSCheck:
    
    def __init__(self):
        pass

