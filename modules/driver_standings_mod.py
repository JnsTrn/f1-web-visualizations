import pandas as pd


def driver_list(number, df):
    # Get list of drivers with x amount of races
    counts = df['driver_name'].value_counts()
    list = counts[counts >= number].index.tolist()
    return list


def circuit_list(number, df):
    # Get list of circuits with x amount of races
    counts = df['circuit_id'].value_counts()
    list = counts[counts >= number].index.tolist()
    return list


def driver_grid_pos(name, df):
    # Get dataframe of drivers with all their grid posisiton
    df_filtered = df[df['driver_name'] == name]
    grid_position_count = (
        df_filtered['grid_position'].value_counts().reset_index()
    )
    grid_position_count.columns = ['grid_position', 'count_grid']
    return grid_position_count


def driver_finish_pos(name, df):
    # Get dataframe of drivers with all their finish posisiton
    df_filtered = df[df['driver_name'] == name]
    finish_position_count = (
        df_filtered['finish_position'].value_counts().reset_index()
    )
    finish_position_count.columns = ['finish_position', 'count_finish']
    return finish_position_count


def get_all_standings(df, max):
    # Get all time grid and finish driver standings
    df_all_standings_count = pd.DataFrame()
    for grid_pos in range(1, max):
        df_filtered = df[df['grid_position'] == grid_pos]
        df_temp = df_filtered['finish_position'].value_counts().reset_index()
        df_temp['grid_position'] = grid_pos
        df_temp = df_temp[['grid_position', 'finish_position', 'count']]
        df_all_standings_count = pd.concat(
            [df_all_standings_count, df_temp], ignore_index=True
        )
    return df_all_standings_count
