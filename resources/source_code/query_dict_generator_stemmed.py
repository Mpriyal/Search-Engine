
stem_query_dict = {}

file = open('../given_resources/cacm_stem.query.txt','rU')

i = 1
for line in file:
    stem_query_dict[i] = line.strip()
    i += 1

file.close()


file = open('../query_dict_stemmed.txt','w')
file.write(str(stem_query_dict))
file.close()