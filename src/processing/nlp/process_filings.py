from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors
import numpy as np
import os
import logging
import csv
import json

# prepare the logging
logger = logging.getLogger('process_filings')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
fh = logging.FileHandler('./process_fillings.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
fh.setFormatter(formatter)
logger.addHandler(fh)


class Embedding_Helper:
    """
    This class helps to calculate the mean embedding of a text and to get the distances to certain words.
    """
    model = None
    stopwords = None
    min_text_length = None
    dist_words = None

    def __init__(self, word2vec_model_path, min_text_length, dist_words):
        """
        Initializes the embedding helper.

        Args:
            word2vec_model_path (str): The path to the storred word2vec model.
            min_text_length (int): The minimum number of words.
            dist_words (list of strings): A word list for the distance measuring. 
        """
        logger.info('Load model')
        self.model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
        logger.info('Loaded model')
        self.stopwords = set(stopwords.words('english'))
        self.min_text_length = min_text_length
        self.dist_words = dist_words


    def _tokenize_and_remove_stopwords(self, text):
        """
        Tokenizes the text and remove the stop words.

        Args:
            text (str): The text to be tokenized.

        Returns:
            A list of words with removed stop words.
        """
        # use a tokenizer that removes the punctuation and numbers
        tokenizer = RegexpTokenizer(r"\w+'\w+|\w+")
        tokenized_words = tokenizer.tokenize(text)

        # remove the stop words and return the list
        return [w for w in tokenized_words if not w.lower() in self.stopwords]

    
    def _get_mean_embedding(self, text):
        """
        Gets the mean embedding of a text.

        Args:
            text (str): A text for which the mean embedding should be calculated.

        Returns:
            The mean embedding of the text.
        """
        words = self._tokenize_and_remove_stopwords(text)
        embeddings = []
        if len(words) >= self.min_text_length:
            # create the word embeddings
            for word in words:
                try:
                    embeddings.append(self.model[word])
                except KeyError as e:
                    # we just ignore the word if it does not exist
                    pass

        # return the mean embedding
        return (True, np.array(embeddings).mean(axis=0)) if embeddings else (False, 0)

    
    def get_distances(self, text):
        """
        Calculates the distances between the mean embedding of the text.

        Args:
            text (str): A text for which the mean embedding should be calculated.

        Returns:
            A dictionary with the distances to certain words.
        """
        success, mean_embedding = self._get_mean_embedding(text)
        dist = {}
        # fill distances with NaNs
        for word in self.dist_words:
            dist[word] = np.NaN
        if success:
            for word in self.dist_words:
                word_embedding = self.model[word]
                cosine_dist = np.inner(mean_embedding, word_embedding) / (np.linalg.norm(mean_embedding) * np.linalg.norm(word_embedding))
                dist[word] = cosine_dist
        return dist


def main(model_path, filings_path, output_file):
    dist_words = ['income', 'loss', 'increase', 'decrease', 'strong', 'discontinued', 'international', 'focus', 'repurchase', 'service', 'goodwill', 'reset', 'expenditure', 'stress', 'exit', 'tranche', 'accordingly']
    helper = Embedding_Helper(model_path, 200, dist_words)

    # we will write everything in a single csv file
    with open(output_file, 'w', newline='') as csv_file:
        # create the csv writer
        writer = csv.writer(csv_file)
        header = ['CIK', 'Year']
        header.extend(['d_{}'.format(word) for word in dist_words])
        writer.writerow(header)
        # iterate over the directory tree
        for root, _, files in os.walk(filings_path):
            logger.debug(root)
            # iterate over the files
            for filing in files:
                if filing[-5:] == '.json':
                    with open(os.path.join(root, filing)) as json_file:
                        data = json.load(json_file)
                        if data['code'] == 1 and data['extracted'] == True:
                            distances = helper.get_distances(data['section'])
                            row = [data['CIK'], data['year']]
                            row.extend([distances[word] for word in dist_words])
                            writer.writerow(row)


if __name__ == "__main__":
    model_path = '/Users/kdoennebrink/Repositories/bankruptcy/model/GoogleNews-vectors-negative300.bin'
    filings_path = '/Users/kdoennebrink/Documents/ExtractedData'
    output_file = '/Users/kdoennebrink/Repositories/bankruptcy/data/processed/word_distances_200.csv'
    logger.info('Process filings')
    main(model_path, filings_path, output_file)
    logger.info('Processed filings')