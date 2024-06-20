import pandas as pd
import os
import json

# Define the directory where your pickle files are stored
package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pickle')
dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv')

# Function to load pickle and convert to CSV
def convert_pickle_to_csv(pickle_file, csv_file, transform_func=None):
    df = pd.read_pickle(pickle_file)
    if transform_func:
        df = transform_func(df)
    df.to_csv(csv_file, index=False)
    print(f"Converted {pickle_file} to {csv_file}")

# Custom transformation functions
def transform_groups(df):
    # Ensure each dictionary in 'members' and 'messages' columns is converted to JSON strings
    df['members'] = df['members'].apply(lambda x: json.dumps(x))
    df['messages'] = df['messages'].apply(lambda x: json.dumps(x))
    return df

def transform_edges(df):
    # Split the 'origin vertices' list into separate columns
    df['origin vertices'] = df['origin vertices'].apply(lambda x: json.dumps(x))
    return df

def transform_set_to_df(s):
    # Convert set to DataFrame
    return pd.DataFrame(list(s), columns=['link'])

# File paths
groups_pickle = os.path.join(package_dir, 'groups')
edges_pickle = os.path.join(package_dir, 'edges')
to_be_processed_pickle = os.path.join(package_dir, 'to_be_processed')
done_pickle = os.path.join(package_dir, 'done')

groups_csv = os.path.join(dest_dir, 'groups.csv')
edges_csv = os.path.join(dest_dir, 'edges.csv')
to_be_processed_csv = os.path.join(dest_dir, 'to_be_processed.csv')
done_csv = os.path.join(dest_dir, 'done.csv')

# Convert pickle files to CSV with appropriate transformations
convert_pickle_to_csv(groups_pickle, groups_csv, transform_groups)
convert_pickle_to_csv(edges_pickle, edges_csv, transform_edges)
convert_pickle_to_csv(to_be_processed_pickle, to_be_processed_csv, transform_set_to_df)
convert_pickle_to_csv(done_pickle, done_csv, transform_set_to_df)
