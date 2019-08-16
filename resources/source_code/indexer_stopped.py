import os

corpus_file_names = os.listdir('../corpus/')


with open('../given_resources/common_words', "r", encoding='utf-8') as c:
    common_words = []
    for ci in c.read().split():
        common_words.append(ci)


# given a integer n
# returns index of word n gram
def make_index_n():
    index = {}
    for file_name in corpus_file_names:
        f = open('../corpus/' + file_name, "r", encoding='utf-8')
        term_freq_in_doc = {}
        file_name = file_name.replace('.txt', '')
        for line in f:
            word_list = line.split()
            word_list = filter_ascii(word_list)
            for word in word_list:
                if word not in common_words:
                    if word in term_freq_in_doc.keys():
                        term_freq_in_doc[word] += 1
                    else:
                        term_freq_in_doc[word] = 1
        for key in term_freq_in_doc.keys():
            did_freq = [file_name, term_freq_in_doc[key]]
            if key in index.keys():
                index[key].append(did_freq)
            else:
                index[key] = [did_freq]
        f.close()

    save_index(index)
    print('created stopped index')


# given data and batch_size(n)
# returns data with batches of n
def batch_gen(data, batch_size):
    for i in range(0, len(data), batch_size):
            yield data[i:i+batch_size]


# given index and integer n
# saves the index
def save_index(i):
    fw = open('../index_stopped.txt', 'w',  encoding='utf-8')
    fw.write(str(i))
    fw.close()


# given a string s
# return true if string contains ascii characters
def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


# given list of strings
# return all string that can be encoded through ascii
def filter_ascii(words):
    word_list = []
    for word in words:
        if is_english(word):
            word_list.append(word)

    return word_list


make_index_n()
