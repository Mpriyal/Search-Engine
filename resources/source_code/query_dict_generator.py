from bs4 import BeautifulSoup


# finds all the occurrences of ch in s
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


query_dict = {}

file = open('../given_resources/cacm.query.txt','rU',encoding = 'utf-8')
queries = file.read()
file.close()
    
soup = BeautifulSoup(queries,'html.parser')
docs = soup.find_all('doc')
    
for doc in docs:

    p_list = [".", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", '"', "'", '“', '”', '[',
                  ']', '’', '^', '#', '$', '%', '*', '_', '|', "{", "}", '<', '>', '/', '~', '`', '=', '+']
    new_words = []
    word_list = doc.contents[2].lower().strip().replace('\n',' ').split()
        
    for word in word_list:
        for p in p_list:
            indexes = find(word, p)
            for index in indexes:
                if not ((p == ',' or p == '.') and
                        (len(word) - 1 > index > 0 and
                             word[index - 1].isdigit() and word[index + 1].isdigit())):
                    word = word.replace(p, '')
        new_words.append(word)
    
    query_dict[doc.docno.getText().strip()] = new_words


#saving transformed queries to a file
file = open('../query_dict.txt','w')
file.write(str(query_dict))
file.close()

file = open('../queries_lucene.txt', 'w')
for i in range(64):
    
    file.write(str(i+1)+" "+" ".join(query_dict[str(i+1)])+"\n")
    
file.close()

print("Saved query_dict and input queries for lucene")