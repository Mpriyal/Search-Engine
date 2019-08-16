import math
import ast
import operator

# reads queries and makes it a dict
with open('../../../../resources/query_dict_stemmed.txt', "r", encoding='utf-8') as f1:
    queries_dict = ast.literal_eval(f1.read())
    f1.close()

# reads index and makes it a dict
with open('../../../../resources/index_stemmed.txt', "r", encoding='utf-8') as f2:
    index = ast.literal_eval(f2.read())
    f2.close()

# reads document length and makes it in a dict.
with open('../../../../resources/docs_length_stemmed.txt', "r", encoding='utf-8') as f3:
    dl = ast.literal_eval(f3.read())
    f3.close()


def get_total_words_in_coll():
    total = 0
    for key in dl.keys():
        total += dl[key]

    return total


def get_freq_term_in_coll(term):
    count = 0
    if term in index.keys():
        for docs_and_frequencies in index[term]:
            count += docs_and_frequencies[1]

    return count


def get_doc_length(doc_id):
    if doc_id in dl.keys():
        return dl[doc_id]

    return 0


def get_freq_term_in_doc(term, doc_id):
    if term in index.keys():
        for docs_and_frequencies in index[term]:
            if docs_and_frequencies[0] == doc_id:
                return docs_and_frequencies[1]

    return 0


def get_docs_for_term(term):
    docs_id = []
    if term in index.keys():
        for docs_and_frequencies in index[term]:
            docs_id.append(docs_and_frequencies[0])

    return docs_id


def get_score(query_terms):
    score = {}
    lam = 0.35
    total_words_in_coll = get_total_words_in_coll()
    for term in query_terms:
        docs_id_with_term = get_docs_for_term(term)
        freq_term_in_coll = get_freq_term_in_coll(term)
        y = (lam * freq_term_in_coll) / total_words_in_coll
        for doc_id in dl.keys():
            doc_id = doc_id.replace(".txt", '')
            if doc_id in docs_id_with_term:
                freq_term_in_doc = get_freq_term_in_doc(term, doc_id)
                document_length = get_doc_length(doc_id)
                x = ((1 - lam) * freq_term_in_doc) / document_length
                s = math.log2(x+y)
            elif y != 0:
                s = math.log2(y)
            else:
                s = 0
            if doc_id in score.keys():
                score[doc_id] += s
            else:
                score[doc_id] = s
    sorted_dict = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dict


def main():
    for query_id in queries_dict.keys():
        score = get_score(queries_dict[query_id])
        file = open('../../../../output/system_run_output/sqlm_stemmed/query_' + str(query_id) + '.txt', 'w')
        rank = 0
        for doc_id_score in score:
            rank += 1
            file.write(str(query_id) + ' Q0 ' + str(doc_id_score[0]) + ' ' + str(rank) + ' ' + str(doc_id_score[1]) +
                       ' sqlm_stemmed\n')
            if rank == 100:
                break
        file.close()

    print('calculated Smoothed Query Likelihood Model Scores for queries')


main()
