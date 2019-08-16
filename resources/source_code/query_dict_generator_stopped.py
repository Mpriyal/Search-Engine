import ast

# reads index and makes it a dict
with open('../query_dict.txt', "r", encoding='utf-8') as f1:
    queries_dict = ast.literal_eval(f1.read())
    f1.close()

with open('../given_resources/common_words', "r", encoding='utf-8') as c:
    common_words = []
    for ci in c.read().split():
        common_words.append(ci)

queries_dict_stopped = {}

for query_id in queries_dict.keys():
    new_query_words = []
    for query_word in queries_dict[query_id]:
        if query_word not in common_words:
            new_query_words.append(query_word)

    queries_dict_stopped[query_id] = new_query_words
    fw = open('../query_dict_stopped.txt', 'w', encoding='utf-8')
    fw.write(str(queries_dict_stopped))
    fw.close()
