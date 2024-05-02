"""
Code for the analysis of the audit data
"""

import streamlit as st
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
        
        Returns: updated display data
        """

        self.analysis_tools = DataAnalysisTools()
        self.plot = DataVisualization()


        # convert times to datetimes
        self.start_time = self.analysis_tools.localize_time_inputs(start_time, audit_date) 
        self.end_time = self.analysis_tools.localize_time_inputs(end_time, audit_date) 

        print(self.start_time, self.end_time)
        self.compound = compound


        # # flag the display data
        # display_data = FlagData(display_data)


        self.zero_air_analysis(analysis_data, display_data)


        #return display_data
    
    def zero_air_analysis(self, analysis_data, display_data):
        """
        Preform analysis
        """

        # shorted df to the timeframe to analyze
        analysis_series = self.analysis_tools.shorten_to_analysis(analysis_data, self.start_time, self.end_time, self.compound)
        print(analysis_series)

        # find ideal grouping of points
        ideal_data = self.analysis_tools.find_ideal_grouping(analysis_series)

        # display series of ideal data
        self.analysis_tools.display_table(ideal_data)

        # plot scatter of data
        self.plot.scatter_plot(analysis_data[self.compound], analysis_series, ideal_data)

        # compute all stats and display in table

        # plot histogram of data

        


        




class CalGasAnalysis:

    def __init__(self):
        pass

class MDLCheckAnalysis:

    def __init__(self):
        pass

class iMetAnalysis:

    def __init__(self):
        pass

class GPSCheck:
    
    def __init__(self):
        pass

