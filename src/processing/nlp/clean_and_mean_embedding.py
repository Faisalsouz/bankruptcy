from  extract_data import extract_data
from embedder import MeanEmbedder
import time

print('#### Extract data ####')
start = time.time()
extract_data()
print('#### Data extracted (time: {}) ####'.format(time.time() - start))
print('#### Load word2vec model ####')
start = time.time()
e = MeanEmbedder.MeanEmbedder("/Users/kdoennebrink/Repositories/bankruptcy/model/GoogleNews-vectors-negative300.bin")
print('#### Model loaded (time: {}) ####'.format(time.time() - start))
print('#### Create embeddings ####')
start = time.time()
e.create_embeddings("/Users/kdoennebrink/Desktop/ExtractedData/10-K")
print('#### Embeddings created (time: {}) ####'.format(time.time() - start))
print('#### Save results ####')
start = time.time()
e.save_embeddings("/Users/kdoennebrink/Desktop/ExtractedData/10-K_mean_embedding.pkl")
print('#### Results saved (time: {}) ####'.format(time.time() - start))
