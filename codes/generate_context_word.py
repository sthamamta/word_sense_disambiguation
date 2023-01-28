
import sys,io,os,glob,nltk, re, string
from nltk.corpus import stopwords
from timeit import default_timer as timer
from datetime import timedelta
import time
import random
     
def removeStopwords(line):
    nonstopword = []
    stop_words = set(stopwords.words('english'))
    for word in line:
        if word not in stop_words:
            nonstopword.append(word)
    return nonstopword
  
def removeNonAlpha(line):
    for word in line:
        if word.isalpha()==False:
            line = line.replace(word, " ")
    line = nltk.tokenize.word_tokenize(line)
    return line
        
def remove_short_form(line):
    line = re.sub(r"what's", "what is ", line)
    line = re.sub(r"\'s", " ", line)
    line = re.sub(r"\'ve", " have ", line)
    line = re.sub(r"can't", "cannot ", line)
    line = re.sub(r"n't", " not ", line)
    line = re.sub(r"i'm", "i am ", line)
    line = re.sub(r"\'re", " are ", line)
    line = re.sub(r"\'d", " would ", line)
    line = re.sub(r"\'ll", " will ", line)
    line = re.sub(r" e g ", " eg ", line)
    line = re.sub(r" b g ", " bg ", line)
    line = re.sub(r" u s ", " american ", line)
    line = re.sub(r"\0s", "0", line)
    line = re.sub(r"e - mail", "email", line)
    
    return line

def preprocess(line):
    line  = remove_short_form(line)
    line  = removeNonAlpha(line)
    line  = removeStopwords(line)
    return line

# extract the context words within given window
def get_context_words(input_file, words,window):
    with open(input_text_file) as f:
        try:
            # print("Parsing file: "+ input_text_file)
            lines = f.readlines()
            size = len(lines)
            context_words = {}  #dictionary with values as list ; key is word name 
          
            for i,line in enumerate(lines): #iterating through lines
                line1 = preprocess(line)
                for idx,element in enumerate(line1):  #iterating through word in line
                    for word in words:
                        if element == word:
                            prior_context = line1[max(0,idx-window): idx] 
                            post_context = line1[min(len(line1)-1,idx+1):min(len(line1)-1,idx+1+window)]
                            context = prior_context + post_context
                            try:
                                context_words[word].append(context)  # try if key is present
                            except:
                                context_words[word]=[context]
        except IOError:
            print("Cannot read input file "+input_file)
    return context_words


# write the result to text file 
def write_file(context_words,window,output_dir, split=0.8): 
    '''
    @param context_words: dictionary of list of words for each words for a single window
    '''

    if not os.path. exists(output_dir):
        os.makedirs(output_dir)  

    for key in context_words.keys():
        random.seed(123)
        random.shuffle(context_words[key])  #shuffle before splittint into train and test set
        split_index = int(len(context_words[key])* split) 
        path = key+'_train_w'+ str(window)+'.txt'
        path = os.path.join(output_dir,path)
        try:
            with open(path, 'w+') as output_file:
                for idx,item in enumerate(context_words[key][:split_index]):
                    output_file.write(' '.join(item)+'\n')

        except IOError:
            print("Cannot write output file "+output_file)

        path = key+'_test_w'+ str(window)+'.txt'
        path = os.path.join(output_dir,path)
        try:
            with open(path, 'w+') as output_file:
                for idx,item in enumerate(context_words[key][split_index:]):
                    item = [x.lower() for x in item]
                    output_file.write(' '.join(item)+'\n')

        except IOError:
            print("Cannot write output file "+output_file)


if __name__=="__main__":
    input_text_file = sys.argv[1]
    words = ['car','night','seat', 'bike', 'kitchen', 'cough','manufacturer','big','small','huge','heavy']
    windows = [5,10,20]
    for window in windows:
        print("Generating data for window size ", window)
        start = time.time()
        context_words = get_context_words(input_text_file, words,window)
        write_file(context_words, window,'dataset/')
        end = time.time()
        print("Total time taken is {} seconds ".format (end-start))


        