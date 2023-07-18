import pickle
import gensim
import numpy as np
from scipy import sparse
import time


from argument_esa_model.similarity import Similarity
import sys
from argument_esa_model.preprocessor import Preprocessor
import argument_esa_model.matrix
sys.modules['matrix'] = argument_esa_model.matrix


class ESA:
    def __init__(self, matrix_path, model_path, vocab_path = None, similarity = "cos"):
        self._pre = Preprocessor(vocab_path)
        self._esa_model = pickle.load(open(matrix_path, "rb"))
        self._mat= self._esa_model.get_mat().transpose().todense()
        self.index_map = {}
        for term in self._esa_model.get_terms():
            self.index_map[term]=self._esa_model.get_terms().index(term)
        self._sim = similarity
        self.word2vec_model = None
        if similarity != "cos":
            self.word2vec_model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(model_path, binary = True)

    def _to_vector(self, document, lemma):
        if lemma:

            bow = self._pre.to_bow(document, lemma)
            terms_document = tuple(bow.keys())
            length = sum(bow.values())
            vec = sparse.lil_matrix(np.zeros((len(terms_document), 1), dtype = np.longdouble))
            for term in terms_document:
                vec[terms_document.index(term), 0] = bow[term] / length
            vec = sparse.csc_matrix(vec)
            vec.eliminate_zeros()
            return vec, terms_document
        else:
            bow = self._pre.to_bow(document, lemma)
            terms_document = tuple(bow.keys())
            length = sum(bow.values())
            vec = sparse.lil_matrix(np.zeros((len(self._esa_model.get_terms()), 1), dtype = np.longdouble))
            for term in self._esa_model.get_terms():
                try:
                    vec[self.index_map[term], 0] = bow[term] / length
                except:
                    vec[self.index_map[term], 0] = 0.0
            vec = sparse.csc_matrix(vec)
            vec.eliminate_zeros()
            return vec, terms_document


    def process(self, document, word_level = False):
        if not word_level:
            return self._process_document(document)
        else:
            raise NotImplementedError
            #return self._process_words(document)


    def _process_document(self, document):
        lemma = False
        if self._sim != "cos":
            lemma = True
        document_vec, terms_document = self._to_vector(document, lemma)
        result = {}

        if self._sim == "cos":
            result_vector= Similarity.cosine_similarity(document_vec, self._mat)
            for i,concept in enumerate(self._esa_model.get_concepts()):
                result[concept] = result_vector[i]

        elif self._sim == "max":
            for concept in self._esa_model.get_concepts():
                res = Similarity.maximum_matching_similarity(self.word2vec_model, document_vec, self._esa_model[concept], terms_document, self._esa_model._terms)
                result[concept] = res
        elif self._sim == "avg":
                raise NotImplementedError
        return result

'''
    def _process_words(self, document):
        results = {}
        terms = self._mat.get_terms()
        for word in self._pre.to_bow(document):
            if word in terms:
                vec = sparse.lil_matrix(np.zeros((len(terms), 1), dtype = np.longdouble))
                vec[terms.index(word), 0] = 1.0
                vec = sparse.csc_matrix(vec)
                vec.eliminate_zeros()
                intermediate = {}
                for concept in self._mat.get_concepts():
                    intermediate[concept] = self._sim.compute_similarity(vec, self._mat[concept])
                intermediate = sorted(intermediate.items(), key = lambda x : x[1], reverse = True)
                results[word] = intermediate[0][0]
        return results
'''
