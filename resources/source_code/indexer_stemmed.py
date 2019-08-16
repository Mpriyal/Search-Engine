
content_dict = {}


file = open('../given_resources/cacm_stem.txt','rU') 
for line in file:
    if line[0] == '#':
        i = line.split()[1]
        content_dict['CACM-'+str(i).zfill(4)] = ''
        
    else:
        content_dict['CACM-'+str(i).zfill(4)] += line+' '
        


# given a integer n
# returns index of word n gram
def make_index_n():
    index = {}
    doc_length_dict = {}
    for file_name in content_dict:
        doc_length_dict[file_name] = len(content_dict[file_name].split())
        print("Processing : "+file_name)
        term_freq_in_doc = {}
        
        word_list = content_dict[file_name].split()
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
    save_index(index, doc_length_dict)
    print('Index Created')


# given index and integer n
# saves the index
def save_index(i,j):
    fw = open('../index_stemmed' + '.txt', 'w',  encoding='utf-8')
    fw.write(str(i))
    fw.close()

    file = open('../docs_length_stemmed.txt','w')
    file.write(str(j))
    file.close()

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