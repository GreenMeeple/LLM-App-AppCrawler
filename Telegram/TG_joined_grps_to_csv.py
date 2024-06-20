import pandas as pd
import json
import os

# Define the directory where your pickle files are stored
package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pickle')

# Load the two pickle files
groups_pickle_1 = os.path.join(package_dir, 'groups')
groups_pickle_2 = os.path.join(package_dir, 'groups2')

df_groups_1 = pd.read_pickle(groups_pickle_1)
df_groups_2 = pd.read_pickle(groups_pickle_2)

# Merge the two DataFrames
df_merged = pd.concat([df_groups_1, df_groups_2], ignore_index=True)

def expand_json_column(df, column_name):
    expanded_rows = []
    for index, row in df.iterrows():
        data = row[column_name]
        if isinstance(data, str):
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                json_data = []
        elif isinstance(data, list):
            json_data = data
        else:
            json_data = []

        if isinstance(json_data, list) and json_data:
            for item in json_data:
                if isinstance(item, str):
                    new_row = row.to_dict()
                    new_row[column_name] = item
                    expanded_rows.append(new_row)
                else:
                    pass
        else:
            expanded_rows.append(row.to_dict())
    
    return pd.DataFrame(expanded_rows)

def remove_dup_and_out(df_in, path):
    df_in.to_csv(path, index=False)
    df = pd.read_csv(path)
    df = df.drop_duplicates()
    df.to_csv(path, index=False)

members_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/expanded_members.csv')
msgs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/expanded_messages.csv')

# Expand the 'members' and 'messages' columns
df_members = expand_json_column(df_merged, 'members')
df_msgs = expand_json_column(df_merged, 'messages')

remove_dup_and_out(df_members, members_path)
remove_dup_and_out(df_msgs, msgs_path)

print(f"Merged data saved to {members_path} and {msgs_path}")
