import sys
import ast
from bs4 import BeautifulSoup
import math

# constant
# total number of documents
N = 3204

# global dicts

#dict to store inverted index 
# key : term
# value: list of list consisting of
#        docID term frequency pairs 
index_dict = {}

# dict to store document lengths with-
# key: doc id 
# value: number of token in the document
total_tokens_dict ={}

# dict to store the query terms with -
# key: query id
# value: list of terms in the query
query_dict = {}

#dict to store tf_idf score
# key: query id 
# value: list of tuples containing document id and tf_idf scores
tf_idf_dict = {}

# main function to call each step of the program
def main():
    
    print("\n getting inverted index\n")
    get_index()
    
    print("\n getting total tokens\n")
    get_total_tokens()
    
    print("\n getting queries\n")
    get_queries()
    
    print("\ncalculating tf.idf\n")
    tf_idf()
    
    print("\ngenerating top 100 results\n")
    save_top_100()
    
    print('\nScores Saved')
    
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
   
# function to get the query terms into a dict
def get_queries():
    global query_dict
    file = open('../../../resources/query_dict.txt','rU',encoding = 'utf-8')
    query_dict = ast.literal_eval(file.read())
    file.close()
        
# function to calculate the tf_idf score and save in tf_idf_dict
def tf_idf():
    global N
    global index_dict
    global total_tokens_dict
    global query_dict
    
    for query_id in query_dict:
        dict = {}
        for term in query_dict[query_id]:
            
            if term not in index_dict.keys():
                pass
                
            else:
            
                for doc_id in index_dict[term]: # doc_id is list of two elements (doc id and tf)
                    tf = doc_id[1]/total_tokens_dict[doc_id[0]]
                    idf = math.log(N/len(index_dict[term]))
                    score = tf * idf
                
                    
                    if doc_id[0] in dict:
                        dict[doc_id[0]]+=score
                    else:
                        dict[doc_id[0]] = score
                
                
        tf_idf_dict[query_id] = dict
        
        
# function to save top 100 ranked documents into a file
def save_top_100():
    global tf_idf_dict
    
    for query_id in query_dict.keys():
        
        result_list = query_dict[query_id]
        sorted_tuples = sorted(tf_idf_dict[query_id].items(),key=lambda x:x[1],reverse=True)
        
        out_file = open('../../../output/system_run_output/tf_idf/'+'query_'+query_id+'.txt','w')
        rank = 0
        for tuple in sorted_tuples[:100]:
            rank += 1
            out_file.write(query_id+' Q0 '+tuple[0]+' '+str(rank)+' '+str(tuple[1])+' tf_idf\n')
    out_file.close()

    
if __name__=='__main__':
    main()