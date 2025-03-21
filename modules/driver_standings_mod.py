import pandas as pd


# Get list of drivers with x amount of races
def driver_list(number,df):
    counts = df['driver_name'].value_counts()
    list = counts[counts >= number].index.tolist()
    return list

# Get list of circuits with x amount of races
def circuit_list(number,df):
    counts = df['circuit_id'].value_counts()
    list = counts[counts >= number].index.tolist()
    return list

# Get df of driver with all his grid pos
def driver_grid_pos(name,df):
    df_filtered = df[df["driver_name"] == name]
    # Häufigkeiten berechnen   
    grid_position_count = df_filtered["grid_position"].value_counts().reset_index()
    grid_position_count.columns = ["grid_position", "count_grid"]
    return grid_position_count

#Get df of driver with all his finish pos
def driver_finish_pos(name,df):
    df_filtered = df[df["driver_name"] == name]
    # Häufigkeiten berechnen   
    finish_position_count = df_filtered["finish_position"].value_counts().reset_index()
    finish_position_count.columns = ["finish_position", "count_finish"]
    return finish_position_count

#Get all time grid and finish driver standings
def get_all_standings(df):
    df_all_standings_count = pd.DataFrame()
    for grid_pos in range(1,29) : 
        df_filtered = df[df["grid_position"] == grid_pos]
        df_temp = df_filtered["finish_position"].value_counts().reset_index()
        df_temp["grid_position"] = grid_pos
        df_temp = df_temp[["grid_position", "finish_position", "count"]]
        df_all_standings_count = pd.concat([df_all_standings_count, df_temp], ignore_index=True)
    return df_all_standings_count
