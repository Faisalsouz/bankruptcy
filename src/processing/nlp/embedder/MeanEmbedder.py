from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors
import numpy as np
import os
import fnmatch
import pickle

class MeanEmbedder:
    """
    This class creates the mean embedding of all text files in a specific directory.
    For the word emdeddings the word2vec of Google is used. It also can store this
    values in a pickle file which contains a list of lists. Each list contains
    the CIK, the timestamp and the mean embedding.
    """


    def __init__(self, word2vec_model_path):
        """
        Initializes the MeanEmbedder.

        Args:
            word2vec_model_path (str): The path to the storred word2vec model.
        """
        self.model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
        self.stopwords = set(stopwords.words('english'))
        self.mean_embeddings = []


    def create_embeddings(self, dir_path):
        """
        Creates all mean embeddings for the text files in the directory.

        Args:
            dir_path (str): The path to the directory that contains the text files.
        """
        # reset the saved mean embeddings
        self.mean_embeddings = []

        # iterate over all text files
        for file_name in os.listdir(dir_path):
            if fnmatch.fnmatch(file_name, '*.txt'):
                embedding = None
                # get the mean embedding
                with open(os.path.join(dir_path, file_name), 'r') as file:
                    embedding = self._get_mean_embedding(file)

                # get CIK and timestamp from file name
                cik, timestamp = os.path.splitext(file_name)[0].split('_')

                # save the mean embedding with the CIK and timestamp
                self.mean_embeddings.append([cik, timestamp, embedding])


    def save_embeddings(self, file_path):
        """
        Saves the mean embeddings as a pickle file.

        Args:
            file_path (str): The path of the output file.
        """
        with open(file_path, "wb") as file:
            pickle.dump(self.mean_embeddings, file)


    def _get_mean_embedding(self, file):
        """
        Gets the mean embedding of a text file.

        Args:
            file (file): A text file that can be read.

        Returns:
            The mean embedding of the file.
        """
        words = self._tokenize_and_remove_stopwords(file)
        embeddings = []

        # create the word embeddings
        for word in words:
            try:
                embeddings.append(self.model[word])
            except KeyError as e:
                # we just ignore the word if it does not exist
                pass

        # return the mean embedding
        return np.array(embeddings).mean(axis=0)

    def _tokenize_and_remove_stopwords(self, file):
        """
        Tokenizes the file and remove the stop words.

        Args:
            file (file): A text file that can be read.

        Returns:
            A list of words with removed stop words.
        """
        # use a tokenizer that removes the punctuation and numbers
        tokenizer = RegexpTokenizer(r"\w+'\w+|\w+")
        tokenized_words = tokenizer.tokenize(file.read())

        # remove the stop words and return the list
        return [w for w in tokenized_words if not w.lower() in self.stopwords]
