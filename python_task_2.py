Distance Matrix Calculation:
import pandas as pd

def calculate_distance_matrix(dataframe):
    # Extract relevant columns from the dataset
    df_subset = dataframe[['ID_A', 'ID_B', 'Distance']]

    # Create a DataFrame with unique pairs of toll locations and their corresponding distances
    distance_df = df_subset.groupby(['ID_A', 'ID_B']).agg({'Distance': 'sum'}).reset_index()

    # Create a DataFrame with all unique toll locations
    unique_locations = pd.unique(distance_df[['ID_A', 'ID_B']].values.ravel('K'))

    # Create an empty distance matrix with unique toll locations as both index and columns
    distance_matrix = pd.DataFrame(0, index=unique_locations, columns=unique_locations)

    # Populate the distance matrix with cumulative distances
    for _, row in distance_df.iterrows():
        distance_matrix.at[row['ID_A'], row['ID_B']] = row['Distance']
        distance_matrix.at[row['ID_B'], row['ID_A']] = row['Distance']  # Accounting for bidirectional distances

    return distance_matrix

# Example usage:
# Read the dataset-3.csv into a DataFrame
df = pd.read_csv('dataset-3.csv')

# Call the function with the DataFrame as input
result_matrix = calculate_distance_matrix(df)

# Display the result
print(result_matrix)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Unroll Distance Matrix:
import pandas as pd

def unroll_distance_matrix(input_matrix):
    # Create a DataFrame with the upper triangle (excluding the diagonal) of the input matrix
    unroll_df = pd.DataFrame({
        'id_start': input_matrix.index.repeat(len(input_matrix.columns)),
        'id_end': input_matrix.columns.tolist() * len(input_matrix),
        'distance': input_matrix.values.flatten()
    })

    # Exclude rows where id_start and id_end are the same
    unroll_df = unroll_df[unroll_df['id_start'] != unroll_df['id_end']]

    return unroll_df

# Example usage:
# Assuming 'result_matrix' is the DataFrame from Question 1
# You can call the function like this:
unrolled_df = unroll_distance_matrix(result_matrix)

# Display the result
print(unrolled_df)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Finding IDs within Percentage Threshold:
import pandas as pd

def find_ids_within_ten_percentage_threshold(input_dataframe, reference_value):
    # Filter the DataFrame based on the reference value
    reference_data = input_dataframe[input_dataframe['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    avg_distance = reference_data['distance'].mean()

    # Find ids within 10% threshold
    lower_threshold = 0.9 * avg_distance
    upper_threshold = 1.1 * avg_distance

    # Filter the DataFrame based on the 10% threshold
    filtered_ids = input_dataframe[
        (input_dataframe['distance'] >= lower_threshold) &
        (input_dataframe['distance'] <= upper_threshold)
    ]['id_start'].unique()

    # Sort the list of values
    sorted_filtered_ids = sorted(filtered_ids)

    return sorted_filtered_ids

# Example usage:
# Assuming 'unrolled_df' is the DataFrame from the previous step
# You can call the function like this:
reference_value = 123  # Replace with the actual reference value
result_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)

# Display the result
print(result_ids)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Calculate Toll Rate:
import pandas as pd

def calculate_toll_rate(input_dataframe):
    # Add columns for toll rates based on vehicle types
    input_dataframe['moto'] = 0.8 * input_dataframe['distance']
    input_dataframe['car'] = 1.2 * input_dataframe['distance']
    input_dataframe['rv'] = 1.5 * input_dataframe['distance']
    input_dataframe['bus'] = 2.2 * input_dataframe['distance']
    input_dataframe['truck'] = 3.6 * input_dataframe['distance']

    return input_dataframe

# Example usage:
# Assuming 'unrolled_df' is the DataFrame from the previous step
# You can call the function like this:
result_dataframe = calculate_toll_rate(unrolled_df)

# Display the result
print(result_dataframe)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Calculate Time-Based Toll Rates:
import pandas as pd
from datetime import datetime, time, timedelta

def calculate_time_based_toll_rates(input_dataframe):
    # Create a DataFrame with unique pairs of (id_start, id_end)
    unique_pairs_df = input_dataframe[['id_start', 'id_end']].drop_duplicates()

    # Initialize an empty list to store the resulting data
    result_data = []

    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_range = (time(0, 0, 0), time(23, 59, 59))

    # Iterate over each unique pair of (id_start, id_end)
    for _, pair in unique_pairs_df.iterrows():
        id_start, id_end = pair['id_start'], pair['id_end']

        # Iterate over each day of the week
        for day in range(7):
            # Iterate over each time range
            for start_time, end_time in weekday_time_ranges:
                # Calculate start and end datetime objects
                start_datetime = datetime.combine(datetime.now(), start_time) + timedelta(days=day)
                end_datetime = datetime.combine(datetime.now(), end_time) + timedelta(days=day)

                # Apply discount factors based on time ranges
                time_based_toll = input_dataframe[
                    (input_dataframe['id_start'] == id_start) &
                    (input_dataframe['id_end'] == id_end) &
                    (input_dataframe['startDay'] == day) &
                    (input_dataframe['start_timestamp'] >= start_datetime) &
                    (input_dataframe['start_timestamp'] <= end_datetime)
                ]['distance'].sum()

                discount_factor = 0.8 if 0 <= start_time.hour < 10 else (1.2 if 10 <= start_time.hour < 18 else 0.8)
                time_based_toll *= discount_factor

                # Append the result to the list
                result_data.append([id_start, id_end, day, start_datetime.time(), day, end_datetime.time(), time_based_toll])

            # Apply discount factor for the weekend time range
            time_based_toll_weekend = input_dataframe[
                (input_dataframe['id_start'] == id_start) &
                (input_dataframe['id_end'] == id_end) &
                (input_dataframe['startDay'] == day)
            ]['distance'].sum()

            time_based_toll_weekend *= 0.7

            # Append the result to the list
            result_data.append([id_start, id_end, day, weekend_time_range[0], day, weekend_time_range[1], time_based_toll_weekend])

    # Create the resulting DataFrame
    result_dataframe = pd.DataFrame(result_data, columns=['id_start', 'id_end', 'start_day', 'start_time', 'end_day', 'end_time', 'time_based_toll'])

    return result_dataframe

# Example usage:
# Assuming 'result_dataframe' is the DataFrame from the previous step
# You can call the function like this:
result_time_based_toll = calculate_time_based_toll_rates(result_dataframe)

# Display the result
print(result_time_based_toll)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




