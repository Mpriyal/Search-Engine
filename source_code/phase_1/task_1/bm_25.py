import ast
import math
import operator

# reads query_dict and makes it a dict
with open('../../../resources/query_dict.txt', "r", encoding='utf-8') as f1:
    queries_dict = ast.literal_eval(f1.read())
    f1.close()

# reads index and makes it a dict
with open('../../../resources/index.txt', "r", encoding='utf-8') as f2:
    index = ast.literal_eval(f2.read())
    f2.close()

# reads docs_length and makes it a dict
with open('../../../resources/docs_length.txt', "r", encoding='utf-8') as f3:
    dl = ast.literal_eval(f3.read())
    f3.close()


# calculates bm25 score
def get_bm25_score(query_terms):
    n = 3204
    k1 = 1.2
    k2 = 100
    b = 0.75
    
    avdl = get_avg_length_doc()
    query_term_with_freq = get_query_term_with_freq(query_terms)
    score = {}
    
    for term in query_term_with_freq.keys():
    
        no_doc_terms_appears = get_no_of_doc(term)
        docs_with_count_for_term = []
        
        if term in index.keys():
            docs_with_count_for_term = index[term]
            
        for doc_with_count in docs_with_count_for_term:
        
            doc_id = doc_with_count[0].replace(".txt", '')
            count_term_in_doc = doc_with_count[1]
            K = k1 * ((1 - b) + b * (dl[doc_id] / avdl))
            x = 1 / ((no_doc_terms_appears + 0.5) / (n - no_doc_terms_appears + 0.5))
            y = ((k1 + 1) * count_term_in_doc) / (K + count_term_in_doc)
            z = ((k2 + 1) * query_term_with_freq[term]) / (k2 + query_term_with_freq[term])
            
            if doc_id in score.keys():
                score[doc_id] += math.log2(x) * y * z
            else:
                score[doc_id] = math.log2(x) * y * z

    return sorted(score.items(), key=operator.itemgetter(1), reverse=True)


# get number of documents containing the term.
def get_no_of_doc(term):
    if term not in index.keys():
        return 0

    return len(index[term])


def get_avg_length_doc():
    tl = 0
    for key in dl.keys():
        tl = tl + dl[key]

    return tl/3204


def get_query_term_with_freq(query_terms):
    query_term_with_freq = {}
    
    for term in query_terms:
        if term not in query_term_with_freq.keys():
            query_term_with_freq[term] = 1
        else:
            query_term_with_freq[term] += 1

    return query_term_with_freq


def main():
    for query_id in queries_dict.keys():
    
        score = get_bm25_score(queries_dict[query_id])
        file = open('../../../output/system_run_output/bm_25/query_' + query_id + '.txt', 'w')
        rank = 0
        
        for doc_id_score in score:
            rank += 1
            file.write(query_id + ' Q0 ' + doc_id_score[0] + ' ' + str(rank) + ' ' + str(doc_id_score[1]) +
                       ' bm_25\n')
            if rank == 100:
                break
        file.close()

    print('calculated BM25 Scores for queries')


main()
