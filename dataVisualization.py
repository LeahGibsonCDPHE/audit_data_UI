"""
Code for making plots in streamlit
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_scalebar.scalebar import ScaleBar
from pyproj import CRS, Proj, Transformer, transform


# Customize fonts and sizes
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.titlesize": 12,
        "axes.labelsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
    }
)


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
        fig, ax = plt.subplots(nrows=2, figsize=(7, 5))

        ax[0].plot(analysis_series, color="orange", label="Selected Audit Window")
        ax[0].plot(
            ideal_data,
            color="green",
            linestyle="None",
            marker="^",
            label="Ideal Analysis Data",
        )
        ax[0].legend()
        ax[0].set_ylabel("ppb")

        ax[1].plot(full_dataset, color="black", linestyle="-")
        ax[1].plot(ideal_data, color="green", linestyle="None", marker="^")
        ax[1].set_ylabel("ppb")

        fig.tight_layout()

        # fig_html = mpld3.fig_to_html(fig)
        # st.components.v1.html(fig_html, height=600)
        st.pyplot(fig)

    def scatter_selection(
        self, full_dataset, spikes, blanks, analysis_spike, analysis_blank
    ):
        """
        For plotting MDL data

        Inputs:
        - full_dataset: column of data from the entire audit dataset
        - spikes: mdl data of spikes
        - blanks: series of blanks
        """

        fig, ax = plt.subplots(nrows=3, figsize=(7, 7))
        ax[0].plot(spikes, color="blue", marker="o")
        ax[0].plot(analysis_spike, linestyle="None", marker="^", color="green")
        ax[0].set_title("Spikes")
        ax[0].set_ylabel("ppb")

        ax[1].plot(blanks, color="orange", marker="o")
        ax[1].plot(analysis_blank, linestyle="None", marker="^", color="green")
        ax[1].set_title("Blanks")
        ax[1].set_ylabel("ppb")

        ax[2].plot(full_dataset, color="black", linestyle="-")
        ax[2].plot(
            spikes, color="blue", linestyle="None", marker="o", label="Spike Data"
        )
        ax[2].plot(
            blanks, color="orange", linestyle="None", marker="o", label="Blank Data"
        )
        ax[2].set_ylabel("ppb")
        ax[2].legend()
        fig.tight_layout()

        # fig_html = mpld3.fig_to_html(fig)
        # st.components.v1.html(fig_html, height=600)
        st.pyplot(fig)

    def histogram_plot(self, ideal_data_series, mean):
        """
        Produces a histogram of data in the analysis window vs the ideal window

        Inputs:
        - ideal_series: pandas series of the delected ideal series subset
        - mean: mean of the provided data series
        """

        # plot distributions of data with stats
        fig = plt.figure(figsize=(8, 6))
        sns.histplot(
            ideal_data_series,
            kde=True,
            stat="density",
            element="step",
            color="green",
            bins=25,
            label="Ideal Analysis Data",
        )
        plt.ylabel("Frequency")
        plt.axvline(mean, color="green", linestyle="--")

        fig.tight_layout()

        # fig_html = mpld3.fig_to_html(fig)
        # st.components.v1.html(fig_html, height=600)
        st.pyplot(fig)

    def met_plot(self, analysis_data, kestrel_data):
        """
        Plots the imet and kestrel data
        """

        imet_headers = [
            "Temperature (\u00b0C)",
            "Corrected Wind Direction (\u00b0)",
            "Pressure (hPa)",
            "Relative Humidity (%)",
            "Corrected Wind Speed (m/s)",
        ]

        kestrel_headers = [
            "Temperature",
            "Compass True Direction",
            "Barometric Pressure",
            "Relative Humidity",
            "Wind Speed",
        ]  # units: Temp: F, Pressure: inHg, Wind Speed: mph,

        titles = ["\u00b0C", "Wind Dir (\u00b0)", "mmHg", "RH (%)", "Wind (m/s)"]

        fig, axs = plt.subplots(nrows=5, sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(analysis_data[imet_headers[i]], label="iMet", color="blue")
            ax.plot(kestrel_data[kestrel_headers[i]], label="Kestrel", color="orange")
            ax.set_ylabel(titles[i])
        ax.tick_params(axis="x", rotation=45)
        ax.legend()
        plt.tight_layout()

        fig.tight_layout()

        # fig_html = mpld3.fig_to_html(fig)
        # st.components.v1.html(fig_html, height=600)
        st.pyplot(fig)

    # def gps_map(self, df, gdf):
    #     """
    #     plots gps data
    #     """

    #     fig, ax = plt.subplots()
    #     ax.plot(df['GPS Number Of Satellites'])
    #     st.pyplot(fig)

    #     # plot
    #     ax = gdf.plot(markersize=5, column=df['GPS Number Of Satellites'], cmap='viridis', legend=True)
    #     cx.add_basemap(ax, zoom=15, source=cx.providers.Esri.WorldImagery)

    #     # Add scale bar
    #     scalebar = ScaleBar(1, location='lower right')  # 1 pixel = 1 unit (you can adjust this)
    #     ax.add_artist(scalebar)
    #     ax.set_axis_off()

    #     # Label the legend
    #     ax.legend(title='GPS Number Of Satellites')

    #     fig.tight_layout()

    #     #fig_html = mpld3.fig_to_html(fig)
    #     #st.components.v1.html(fig_html, height=600)
    #     st.pyplot(ax.figure)
