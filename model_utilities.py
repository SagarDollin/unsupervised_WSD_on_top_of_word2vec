import numpy as np


def remove_stopword(list_words):
    '''this function will intake a list of words and returns a list with no stopwords in it'''

    file = open('stopwords.txt', 'r')
    stopword_list = []

    while (True):
        stopword = file.readline()
        if not stopword:
            break
        buffer = stopword.partition('\n')
        stopword_list.append(buffer[0])

    no_stopword_list = ""

    for word in list_words:
        if word not in stopword_list:
            no_stopword_list += word + ' '
    no_stopword_list = no_stopword_list.rstrip()
    return no_stopword_list.split()


def create_V(stopwordfree_corpus):
    '''This function takes an input as a corpus in the form os list of sentences and returns a dictionary V,
    with keys as words in the corpus and values as their frequency in the corpus '''
    V = {}

    for sentence in stopwordfree_corpus:
        for word in sentence:
            try:
                V[word] += 1
            except:
                V[word] = 1
    return V


def Normalise_W(W, V, track):
    '''This matrix takes the inputs W matrix,V(output of create_V()), and  normalizes the W matrix by dividing the
    co-occurence count value of each cell in the matrix by product of their corresponding words' frequency from the V
    dictionary's values '''
    V_list = list(V.keys())
    Vcount = list(V.values())
    print("Total length=", len(track))
    count = 0
    print("--------Normalising-------------")
    for row, columns in track.items():
        i = row
        count += 1
        for j in columns:
            freq_i = Vcount[i]
            freq_j = Vcount[j]
            W[i][j] = W[i][j] / (freq_i * freq_j)

    return W


def create_W2(stopwordfree_brown, V):
    '''This fuction takes in a corpus data in the form of list of sentences(lists), and V (Vocabulary) dictionary
    {word:count} and returns the W matrix which is a co-occurence matrix. Each cell of co-occurence matrix has the value of number of
    co-occerence of the words corresponding to the row and column of that cell, in the window of 5 words.'''

    track = {}
    W = np.zeros((len(V), len(V)), dtype='float32')
    V_list = list(V.keys())
    Vcount = list(V.values())

    for sentence in stopwordfree_brown:
        window_size = 5
        left_window = int(window_size / 2)

        i = 0
        total_len = len(sentence)
        for target in sentence:

            if (i > left_window and i < total_len - left_window):
                window = sentence[i - left_window:i + left_window + 1]

            elif (i < left_window):
                window = sentence[0:window_size]
            else:
                window = sentence[total_len - window_size:total_len]

            i += 1
            row = V_list.index(target)
            for word in window:
                if word != target:
                    column = V_list.index(word)
                    W[row][column] += 1

                    try:
                        track[row].add(column)
                    except:
                        track[row] = {column}

    return W, track

def read_scws(V_brown,V_wiki):
    '''This function takes the input V_brown dictionary and V_wiki dictionary, and reads the SCWS text file in the 
    directory to return a dictionary of SCWS data with index,targets, contexts and scores anootated'''
    
    scws = open('SCWS/SCWS/ratings.txt')
    scws_data = {}
    while(scws):
        line = scws.readline().split('\t')
        context1 = line[5].replace('<b>','').replace('</b>','')
        context2 = line[6].replace('<b>','').replace('</b>','')
        target1 = line[1]
        target2 = line[3]
        print
        if line[0] not in scws_data:
            if (target1 in V_brown) and (target2 in V_brown) and(target1 in V_wiki) and (target2 in V_wiki):
                scws_data[line[0]] =  {"target1":line[1],"target2":line[3],"context1":context1,"context2":context2,"human_score":line[7]}

        if line[0]=='2003':
            break
            
    return scws_data