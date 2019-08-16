import os

corpus_file_names = os.listdir('../corpus/')


with open('../given_resources/common_words', "r", encoding='utf-8') as c:
    common_words = []
    for ci in c.read().split():
        common_words.append(ci)


# get length of all documents
def get_len_all_doc():
    dl = {}
    for file_name in corpus_file_names:
        length = 0
        f = open('../corpus/' + file_name, 'r',  encoding='utf-8')
        for line in f:
            no_of_words = 0
            for word in line.split():
                if word not in common_words:
                    no_of_words += 1
            length = length + no_of_words
        dl[file_name.replace(".txt", '')] = length

    fw = open('../docs_length_stopped.txt', 'w', encoding='utf-8')
    fw.write(str(dl))
    fw.close()


get_len_all_doc()
