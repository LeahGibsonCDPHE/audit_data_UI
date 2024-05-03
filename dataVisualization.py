"""
Code for making plots in streamlit
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    """
    Contains the functions for making the various plots
    """

    def __init__(self):
        pass

    def scatter_plot(self, full_dataset, analysis_series, ideal_data):
        """
        Plots the different parts of the data in different colors

        Inputs:
        - full_datatset: column of data from entire audit dataset
        - analysis_series: column of data from the analysis series
        - ideal_data: subset of data that will be used for the final analysis
        """

        # plot the timeseries with color selection
        fig, ax = plt.subplots()
        ax.plot(full_dataset, color='black', linestyle='-')
        ax.plot(analysis_series, color='orange', linestyle='None', marker='^', label='Selected Audit Window')
        ax.plot(ideal_data, color='green', linestyle='None', marker='^', label='Ideal Analysis Data')
        ax.set_ylabel('ppb')
        ax.legend()
        st.pyplot(fig)
    
    def scatter_selection(self, full_dataset, spikes, blanks):
        """
        For plotting MDL data

        Inputs:
        - full_dataset: column of data from the entire audit dataset
        - spikes: mdl data of spikes
        - blanks: series of blanks
        """

        fig, ax = plt.subplots()
        ax.plot(full_dataset, color='black', linestyle='-')
        ax.plot(spikes, color='blue', linestyle='None', marker='o', label='Spike Data')
        ax.plot(blanks, color='orange', linestyle='None', marker='o', label='Blank Data')
        ax.set_ylabel('ppb')
        ax.legend()
        st.pyplot(fig)
    
    def histogram_plot(self, ideal_data_series, mean):
        """
        Produces a histogram of data in the analysis window vs the ideal window

        Inputs:
        - ideal_series: pandas series of the delected ideal series subset
        - mean: mean of the provided data series
        """

        # plot distributions of data with stats
        fig = plt.figure(figsize=(8,6))
        sns.histplot(ideal_data_series, kde=True, stat="density", element="step", color='green', bins=25, label='Ideal Analysis Data')
        plt.ylabel('Frequency')
        plt.axvline(mean, color='green', linestyle='--')    
        st.pyplot(fig)