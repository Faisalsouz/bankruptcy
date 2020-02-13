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
    labels = df_shuffled['Bankrupt']
    data = df_shuffled.drop(columns=['Bankrupt', 'CIK', 'Year']).to_numpy()
    # prepare the data and label for the generator
    prepared_data, prepared_labels = _prepare_data_for_generator(data, labels)
    # calculate the split points
    test_split = int((len(prepared_data)//5) * test_ratio) * 5
    val_split = int((len(prepared_data)//5) * val_ratio) * 5

    # do the split (to use the full data we need to extend the ranges by one (last label of sequence))
    val_data = prepared_data[:val_split+1]
    val_labels = prepared_labels[:val_split+1]
    test_data = prepared_data[val_split:test_split+val_split+1]
    test_labels = prepared_labels[val_split:test_split+val_split+1]
    train_data = prepared_data[test_split+val_split:]
    train_labels = prepared_labels[test_split+val_split:]

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


def _prepare_data_for_generator(data, labels):
    """
    Prepares the data and labels for our timeseries generator. The generator expects the data and label in the following format:
    data = np.array([['1_1'], ['1_2'], ['1_3'], ['1_4'], ['1_5'], ['2_1'], ['2_2'], ['2_3'], ['2_4'], ['2_5'], ..., ['dummy']])
        where the first number identify the data sample and the second number the year, we need to at a dummy data sample at the end to use the full data
    labels = np.array([-1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 0, ..., 0])
        where labels have the same length as data, -1 means no label and labels are shifted by one so that i+1 is the label for data sample i-4 to i

    Args:
        data: the 2d-data array of length n
        label: the 1d-label array of length n

    Returns
        prepared_data = 2d-array of length n+1
        prepared_label = 1d-array of length n+1
    """
    # prepare labels
    # replace first 4 labels by placeholder (-1)
    idx = np.array([True, True, True, True, False] * (len(labels) // 5))
    labels[idx] = -1
    # now we need to add another placeholder (-1) at the front
    prepared_labels = np.zeros(shape=(len(labels)+1), dtype=np.int64)
    prepared_labels[0] = -1
    prepared_labels[1:] = labels
    
    # prepare data
    # just add another dummy data sample
    r, c = data.shape
    prepared_data = np.zeros(shape=(r + 1, c))
    prepared_data[:-1] = data

    return prepared_data, prepared_labels


if __name__ == "__main__":
    load_data()
