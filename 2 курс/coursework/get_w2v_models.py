from new_w2v_model import get_new_model


path = 'data/word2vec_models/'
name = 'model_%s_%s_300_w5_it3.wv'

#skip-gram with hierarchical softmax
get_new_model(path, name % ('sg', 'hs'), size=300, sg=1, hs=1, min_count=5, window=5, iter=3)
print('ok')
#cbow with hierarchical softmax
get_new_model(path, name % ('cbow', 'hs'), size=300, sg=0, hs=1, min_count=5, window=5, iter=3)
print('ok')
#skip-gram with negative sampling
get_new_model(path, name % ('sg', 'ns') + '_ns5', size=300, sg=1, hs=0, min_count=5, window=5, iter=3, negative=5)
print('ok')
#cbow with negative sampling
get_new_model(path, name % ('cbow', 'ns') + '_ns5', size=300, sg=0, hs=0, min_count=5, window=5, iter=3, negative=5)
print('ok')
