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
        ax.legend()
        st.pyplot(fig)
    
    def histogram_plot(self, analysis_series, ideal_series):
        """
        Produces a histogram of data in the analysis window vs the ideal window

        Inputs:
        - analysis_aeries: pandas series of the full analysis window
        - ideal_series: pandas series of the delected ideal series subset
        """

        # # plot distributions of data with stats
        # plt.figure(figsize=(8,6))
        # sns.histplot(audit_series, kde=True, stat="density", element="step", color='blue', bins=25, label='Selected Audit Window')
        # sns.histplot(audit_series_no_outliers, kde=True, stat="density", element="step", color='orange', bins=25, label='Selected Audit Window (No Outliers)')
        # sns.histplot(ideal_data_series, kde=True, stat="density", element="step", color='green', bins=25, label='Ideal Analysis Data')
        # plt.legend()
        # plt.title(f'{compound}')
        # plt.ylabel('Frequency')
        # plt.axvline(audit_mean, color='blue' , linestyle='--')
        # plt.axvline(no_outliers_mean, color='orange', linestyle='--')
        # plt.axvline(ideal_mean, color='green', linestyle='--')    