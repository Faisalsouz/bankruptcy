import pandas as pd
import numpy as np


def load_data(path_to_data='../../data/NO_SHUFFLE.csv', test_ratio=0.2, val_ratio=0.1):
    """
    Loads the data.

    Args:
        path_to_data (str): The path to the data csv-file. By default: NO_SHUFFLE.csv
        test_ratio (float): Determines the ratio of the test set. By default: 0.2
        val_ratio (float): Determines the ratio of the validation set. By default: 0.1

    Returns:
        train_data (2d-array): The training data
        train_label (1d-array): The training label
        test_data (2d-array): The test data
        test_label (1d-array): The test label
    """
    # read in the csv file
    df_full_data = pd.read_csv(path_to_data)
    # shuffle the data
    df_shuffled = _shuffle_data(df_full_data)
    # extract the labels from the dataframe and drop unnecessary columns
    all_labels = df_shuffled['Bankrupt'].to_numpy()
    all_data = df_shuffled.drop(columns=['Bankrupt', 'CIK', 'Year']).to_numpy()

    # calculate the split points
    test_split = int((len(all_data)//5) * test_ratio) * 5
    val_split = int((len(all_data)//5) * val_ratio) * 5

    # do the split
    val_data = all_data[:val_split]
    val_labels = all_labels[:val_split]
    test_data = all_data[val_split:test_split+val_split]
    test_labels = all_labels[val_split:test_split+val_split]
    train_data = all_data[test_split+val_split:]
    train_labels = all_labels[test_split+val_split:]

    return train_data, train_labels, test_data, test_labels, val_data, val_labels


def _shuffle_data(data):
    """
    Shuffles the given data frame while keeping the groups. 

    Args:
        data (pandas.DataFrame): The data frame to be shuffled where each group should consist of 5 rows.

    Returns:
        A group shuffled data frame.
    """
    # create a shuffling index
    perm = np.random.permutation(len(data)//5) * 5
    idx = [j for sub in [[i, i+1, i+2, i+3, i+4] for i in perm] for j in sub]
    # create a dataframe from the index
    index_df = pd.DataFrame(data={}, index=idx)
    # join both dataframes
    shuffled_data = pd.concat([index_df, data.reindex(index_df.index)], axis=1)
    return shuffled_data


if __name__ == "__main__":
    load_data()
