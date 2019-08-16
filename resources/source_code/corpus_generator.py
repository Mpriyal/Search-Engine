from bs4 import BeautifulSoup
import os

corpus_file_names = os.listdir('../given_resources/cacm')


# finds all the occurrences of ch in s
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


# clean all document in corpus, removes images, markup notation (HTML tags),
# URLs, tables, formulas, and navigational components
def main():
    document_length = {}
    i=0
    for file_name in corpus_file_names:
        print("Number of files cleaned : "+str(i+1))
        f = open('../given_resources/cacm/' + file_name, "r", encoding='utf-8')
        soup = f.read()
        f.close()
        bs = BeautifulSoup(soup, "html.parser")
        contents = bs.get_text().lower()
        p_list = [".", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", '"', "'", '“', '”', '[',
                  ']', '’', '^', '#', '$', '%', '*', '_', '|', "{", "}", '<', '>', '/', '~', '`', '=', '+']
        new_words = []
        word_list = contents.split()
        document_length[file_name.replace(".html", '')] = len(word_list)
        for word in word_list:
            for p in p_list:
                indexes = find(word, p)
                for index in indexes:
                    if not ((p == ',' or p == '.', p) and
                            (len(word) - 1 > index > 0 and
                                 word[index - 1].isdigit() and word[index + 1].isdigit())):
                        word = word.replace(p, '')
            new_words.append(word)
        contents = ' '.join(new_words)
        save_contents(contents, file_name)
        i += 1
    fw = open('../docs_length.txt', 'w', encoding='utf-8')
    fw.write(str(document_length))
    fw.close()
    print('All files cleaned')


# given content and filename
# saves the content at given filename
def save_contents(contents, file_name):
    fw = open('../corpus/' + file_name.replace('.html', '') + '.txt', 'w',  encoding='utf-8')
    fw.write(str(contents))
    fw.close()


main()
