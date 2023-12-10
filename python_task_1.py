Car Matrix Generation:
import pandas as pd

def generate_car_matrix(dataframe):
    # Extract relevant columns from the dataset
    df_subset = dataframe[['id_1', 'id_2', 'car']]

    # Pivot the DataFrame to create a matrix
    car_matrix = pd.pivot_table(df_subset, values='car', index='id_1', columns='id_2', fill_value=0)

    # Set diagonal values to 0
    car_matrix.values[[range(car_matrix.shape[0])]*2] = 0

    return car_matrix

# Read the dataset-1.csv into a DataFrame
df = pd.read_csv('dataset-1.csv')

# Call the function with the DataFrame as input
result_matrix = generate_car_matrix(df)

# Display the result
print(result_matrix)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Car Type Count Calculation:
import pandas as pd

def get_type_count(dataframe):
    # Add a new categorical column 'car_type' based on the values of the 'car' column
    dataframe['car_type'] = pd.cut(dataframe['car'],
                                   bins=[float('-inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'],
                                   right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = dataframe['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

# Example usage:
# Read the dataset-1.csv into a DataFrame
df = pd.read_csv('dataset-1.csv')

# Call the function with the DataFrame as input
result = get_type_count(df)

# Display the result
print(result)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Bus Count Index Retrieval:
import pandas as pd

def get_bus_indexes(dataframe):
    # Calculate the mean value of the 'bus' column
    mean_bus_value = dataframe['bus'].mean()

    # Identify indices where the 'bus' values are greater than twice the mean value
    bus_indexes = dataframe[dataframe['bus'] > 2 * mean_bus_value].index.tolist()

    # Sort the indices in ascending order
    sorted_bus_indexes = sorted(bus_indexes)

    return sorted_bus_indexes

# Example usage:
# Read the dataset-1.csv into a DataFrame
df = pd.read_csv('dataset-1.csv')

# Call the function with the DataFrame as input
result = get_bus_indexes(df)

# Display the result
print(result)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Route Filtering:
import pandas as pd

def filter_routes(dataframe):
    # Filter routes based on the condition: average truck column > 7
    filtered_routes = dataframe.groupby('route')['truck'].mean()
    filtered_routes = filtered_routes[filtered_routes > 7].index.tolist()

    # Sort the list of routes in ascending order
    sorted_filtered_routes = sorted(filtered_routes)

    return sorted_filtered_routes

# Example usage:
# Read the dataset-1.csv into a DataFrame
df = pd.read_csv('dataset-1.csv')

# Call the function with the DataFrame as input
result = filter_routes(df)

# Display the result
print(result)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Matrix Value Modification:
import pandas as pd

def multiply_matrix(input_matrix):
    # Create a copy of the input matrix to avoid modifying the original DataFrame
    modified_matrix = input_matrix.copy()

    # Apply the specified logic to modify each value in the DataFrame
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Example usage:
# Assuming 'result_matrix' is the DataFrame from Question 1
# You can call the function like this:
modified_result_matrix = multiply_matrix(result_matrix)

# Display the modified DataFrame
print(modified_result_matrix)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Time Check:
import pandas as pd

def check_timestamps(dataframe):
    # Combine date and time columns to create datetime objects
    dataframe['start_timestamp'] = pd.to_datetime(dataframe['startDay'] + ' ' + dataframe['startTime'])
    dataframe['end_timestamp'] = pd.to_datetime(dataframe['endDay'] + ' ' + dataframe['endTime'])

    # Check if the timestamp range for each (id, id_2) pair covers a full 24-hour period
    # and spans all 7 days of the week
    def is_valid_timestamp_range(group):
        # Check if the timestamp range covers a full 24-hour period
        full_24_hours = (group['end_timestamp'].max() - group['start_timestamp'].min()).total_seconds() >= 24 * 60 * 60

        # Check if the timestamp range spans all 7 days of the week
        span_all_days = set(group['start_timestamp'].dt.dayofweek.unique()) == set(range(7))

        return full_24_hours and span_all_days

    # Apply the custom function to each (id, id_2) group and create a boolean series
    invalid_timestamps = dataframe.groupby(['id', 'id_2']).apply(is_valid_timestamp_range)

    return invalid_timestamps

# Example usage:
# Read the dataset-2.csv into a DataFrame
df = pd.read_csv('dataset-2.csv')

# Call the function with the DataFrame as input
result = check_timestamps(df)

# Display the result
print(result)


