"""
All handling of data done here:
    - Reading CSVs
    - Merging CSVs
    - Selecting subsets of time
"""

import os
import re
import chardet
import pytz
import pandas as pd
import numpy as np


class ProcessFiles:
    """
    Class for all processing of data, including:
    - loading, merging, cleaning unloaded files
    - adding new columns and flags to the data
    """

    def __init__(self):
        pass

    def load_and_merge_data(self, list_of_uploaded_files):
        """
        Loads and merges data files for the specified vehile and date. 
        If there is no data, tells user there was an error and end program.  
        If all dates are not the same, tells user to upload data from the same day.

        Adds column "DateTime" with time in human reasable format.

        Inputs:
        - list_of_uploaded_files: list from streamlit uplorad button

        Returns: merged data as a df
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
        cleaned_df = self.clean_data(merged_df)
        # add datetimes
        cleaned_df = self.add_datetimes(cleaned_df)

        # made column with just datetimes
        datetime_df = self.add_datetimes(merged_df)

        

        return 

    def clean_data(self, df):
        """
        Makes 2 dataframes, one with the cleaned data for plotting and analysis, and a second with the raw data for saving.
        """
        
        # clean data
        df.loc[df['GSU_PUMP_ON monitor []'] == 0, 'Benzene C6H6+'] = np.nan
        df.loc[df['GSU_VALVE_PR1 monitor []'] == 1, 'Benzene C6H6+'] = np.nan
        df.loc[df['GSU_VALVE_PR2 monitor []'] == 1, 'Benzene C6H6+'] = np.nan

        return df

    def add_datetimes(self, df):
        """
        Adds datetime column to data
        """

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

        return df