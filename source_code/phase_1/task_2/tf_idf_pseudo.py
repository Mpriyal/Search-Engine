import sys
import os
import ast
import math

# constant
# total number of documents
N = 3204

#dict to store top documents for each query
# key : queryID
# value: list of top ranked documents for the query
top_docs_dict = {}

# dict to store the query terms with -
# key: query id
# value: list of terms in the query
query_dict = {}

#dict to store inverted index 
# key : term
# value: list of list consisting of
#        docID term frequency pairs 
index_dict = {}

#dict to store document term frequency
# key : docID
# value: list of tuples(of two elements)
#        containing term and its frequency in the document
doc_term_freq_dict = {}

#dict to store the new queries-
# key: query id
# value: list of terms in the query
new_query_dict = {}

#list to hold common words or stop words
stop_list = []

# dict to store document lengths with-
# key: doc id 
# value: number of token in the document
total_tokens_dict = {}

# dict to store new tf idf values
# key: query id 
# value: list of tuples containing document id and tf_idf scores
new_tf_idf_dict = {}

# main function to call each step of the program
def main():
    
    print('\ngetting top documents for each query\n')
    get_top_docs()
    
    print('\ngetting queries\n')
    get_queries()
    
    print('\ngetting index\n')
    get_index()
    
    print('\ngetting frequency of terms in documents\n')
    get_document_term_frequency()
    
    print('getting common words\n')
    get_common_words()
    
    print('\ngenearting new queries\n')
    pseudo()
    
    print('\ngetting total tokens\n')
    get_total_tokens()
    
    print('\ncalculating new tf idf scores\n')
    new_tf_idf()
    
    print('\nsaving results\n')
    save_top_100()
    
        
# function to get top docs for a query into a dict
def get_top_docs():
    
    global top_docs_dict
    file_list = os.listdir('../../../output/system_run_output/bm_25/')
    query_id = 0
    
    for file_name in file_list:
        
        file = open('../../../output/system_run_output/bm_25/'+file_name,'rU')
        temp_list = []
        for line in file:
            list = line.split()
            query_id = list[0]

            if int(list[3]) > 5: # value of k
                break
            
            temp_list.append(list[2])
            
        file.close()
        top_docs_dict[query_id] = temp_list

# function to get the query terms into a dict        
def get_queries():
    
    global query_dict
    file = open('../../../resources/query_dict.txt','rU',encoding = 'utf-8')
    query_dict = ast.literal_eval(file.read())
    file.close()
    
# function to get the inverted index into a dict
def get_index():
    
    global index_dict
    file = open('../../../resources/index.txt','rU',encoding = 'utf-8')
    index_dict = ast.literal_eval(file.read())
    file.close()
        
# function to get the total tokens in a document into a dict    
def get_total_tokens():
    global total_tokens_dict
    file = open('../../../resources/docs_length.txt','rU',encoding = 'utf-8')
    total_tokens_dict = ast.literal_eval(file.read())
    file.close()        
# function to get the common words into a list
def get_common_words():
    global stop_list
    
    file = open('../../../resources/given_resources/common_words','rU')
    stop_list = file.read().split('\n')
    file.close()
        
#function to calculate and store document term frequency        
def get_document_term_frequency():

    global index_dict
    for term in index_dict:
        for tuple in index_dict[term]:
            if tuple[0] not in doc_term_freq_dict:
                doc_term_freq_dict[tuple[0]] = [(term,tuple[1])]
            else:
                doc_term_freq_dict[tuple[0]].append((term,tuple[1]))
                            
#function to get most frequent words from top docs and to
#generate and store new queries by adding those words to the
#old queries
def pseudo():
    
    global new_query_dict
    global query_dict
    global stop_list
    global doc_term_freq_dict
    
    for query_id in top_docs_dict:
        
        new_query_dict[query_id] = query_dict[query_id]
        
        count = 0
        for doc in top_docs_dict[query_id]:
            sorted_tuples = sorted(doc_term_freq_dict[doc],key=lambda x:x[1],reverse=True)
            
            for tuple in sorted_tuples:
                if count > 5: # num of terms to get from each top doc
                    break
                elif tuple[0] in stop_list:
                    pass
                else:
                    new_query_dict[query_id].append(tuple[0])
                    count += 1
                                   
#function to calculate the new_tf_idf score from the new queries
# genearted through query expansion    
def new_tf_idf():
    global N
    global index_dict
    global total_tokens_dict
    global new_query_dict
    global new_tf_idf_dict
    
    for query_id in new_query_dict:
        dict = {}
        for term in new_query_dict[query_id]:
            
            if term not in index_dict.keys():
                pass
                
            else:
            
                for doc_id in index_dict[term]: # doc_id is list of two elements doc id and tf
                    tf = doc_id[1]/total_tokens_dict[doc_id[0]]
                    idf = math.log(N/len(index_dict[term]))
                    score = tf * idf
                
                    
                    if doc_id[0] in dict:
                        dict[doc_id[0]]+=score
                    else:
                        dict[doc_id[0]] = score
                
                
        new_tf_idf_dict[query_id] = dict
        
# function to save top 100 ranked documents into a file        
def save_top_100():
    global new_tf_idf_dict
    
    for query_id in new_query_dict.keys():
        
        result_list = new_query_dict[query_id]
        sorted_tuples = sorted(new_tf_idf_dict[query_id].items(),key=lambda x:x[1],reverse=True)
        
        out_file = open('../../../output/system_run_output/tf_idf_pseudo/'+'query_'+query_id+'.txt','w')
        rank = 0
        for tuple in sorted_tuples[:100]:
            rank += 1
            out_file.write(query_id+' Q0 '+tuple[0]+' '+str(rank)+' '+str(tuple[1])+' tf_idf_pseudo\n')
    out_file.close()
    

    
if __name__ == '__main__':
    main()