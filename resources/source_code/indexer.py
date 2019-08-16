import os

corpus_file_names = os.listdir('../corpus/')


# given a integer n
# returns index of word n gram
def make_index_n():
    index = {}
    for file_name in corpus_file_names:
        f = open('../corpus/' + file_name, "r", encoding='utf-8')
        print("Processing : "+file_name)
        file_name = file_name.replace('.txt', '')
        term_freq_in_doc = {}
        for line in f:
            word_list = line.split()
            word_list = filter_ascii(word_list)

            for word in word_list:
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
    print('Index Created')


# given index and integer n
# saves the index
def save_index(i):
    fw = open('../index' + '.txt', 'w',  encoding='utf-8')
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