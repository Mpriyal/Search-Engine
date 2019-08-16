from __future__ import division
import os
import ast

#system name for which the evaluation need to be run.(change according to requirement)
#results are saved in the output folder, inside respective system folder.
# 8 systems as follows -> 
# bm_25, bm_25_stopped, tf_idf, tf_idf_pseudo, tf_idf_stopped, lucene, smoothed_query_likelihood, sqlm_stopped

system_name = 'sqlm_stopped'

# dictionary of relevant documents for a query
relevant_dict = {}

# dictionary of all documents for a query
document_dict = {}


def get_relevant_docs():
    relevant_data = open("../../resources/given_resources/cacm.rel.txt", 'r')
    for relevant_row in relevant_data:
        relevant_info = relevant_row.split()
        if relevant_info[0] in relevant_dict.keys():
            relevant_dict[relevant_info[0]].append(relevant_info[2])
        else:
            relevant_dict[relevant_info[0]] = [relevant_info[2]]


def get_all_docs():
    file_list = os.listdir("../../output/system_run_output/"+system_name)
    for file_name in file_list:
        file = open("../../output/system_run_output/"+system_name+'/'+file_name, 'r')
        temp_list = []
        for line in file:
            bm25_list = line.split()
            query_id = bm25_list[0]
            temp_list.append(bm25_list[2])
        file.close()
        document_dict[query_id] = temp_list


def calculate_precision_and_recall():
    #  query id
    p_5 = {}
    p_20 = {}
    avg_p = {}
    rr = {}
    for query_id in document_dict.keys():
        rel_so_far = 0
        doc_so_far = 0
        if query_id in relevant_dict.keys():
            sum = 0
            fp = open('../../output/evaluation_output/'+system_name+'/precision/precision_' + query_id + '.txt', 'w')
            fr = open('../../output/evaluation_output/'+system_name+'/recall/recall_' + query_id + '.txt', 'w')
            
            # for all 100 docs for that query id
            for doc_id in document_dict[query_id]:
                doc_so_far += 1
                # relevant
                if doc_id in relevant_dict[query_id]:
                    rel_so_far += 1
                    sum += rel_so_far / doc_so_far

                if rel_so_far == 1:
                    rr[query_id] = 1/doc_so_far

                precision = str(rel_so_far) + '/' + str(doc_so_far)
                recall = str(rel_so_far) + '/' + str(len(relevant_dict[query_id]))

                if doc_so_far == 5:
                    p_5[query_id] = precision

                if doc_so_far == 20:
                    p_20[query_id] = precision

                fp.write(str(doc_so_far) + "\t\t" + precision + '\n')
                fr.write(str(doc_so_far) + "\t\t" + recall + '\n')
        if rel_so_far != 0:
            avg_p[query_id] = sum/rel_so_far
    save_dict(p_5, '../../output/evaluation_output/'+system_name+'/p@5.txt')
    save_dict(p_20, '../../output/evaluation_output/'+system_name+'/p@20.txt')
    save_mrr_map(cal_mrr(rr), cal_map(avg_p))


def save_dict(d, filename):
    file = open(filename, 'w')

    for query_id in sorted(map(int,d.keys())):
        file.write(str(query_id) + " " + d[str(query_id)] + '\n')

    file.close()


def cal_mrr(rr):
    sum = 0
    for query_id in rr.keys():
        sum += rr[query_id]

    return sum/len(rr.keys())


def cal_map(avg_p):
    sum = 0
    for query_id in avg_p.keys():
        sum += avg_p[query_id]

    return sum / len(avg_p.keys())


def save_mrr_map(mrr, m):
    file = open('../../output/evaluation_output/'+system_name+'/map_mrr.txt','w')
    file.write('MAP = ' + str(m) + '\n' + 'MRR = '+ str(mrr))
    file.close()


if __name__ == '__main__':
    get_relevant_docs()
    get_all_docs()
    calculate_precision_and_recall()
    print("Evaluation Done")
