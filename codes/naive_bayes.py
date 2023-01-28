from hash_table import HashTable
import time
import os


# count total tokens, occurrence of each token and total training set size for single train file
def count_sense(file_path):
    unigram_hash = HashTable(1000)
    total_tokens = 0
    with open(file_path) as f:
        try:
            # print("Parsing file: "+ file_path)
            lines = f.readlines()
            size = len(lines)
            for i,line in enumerate(lines):
                words = line.split( )
                for word in words:
                    unigram_hash.find(word) #add occurrence by 1
                    total_tokens += 1
        except IOError:
            print("Cannot read input file "+input_file)
    return  unigram_hash, total_tokens,size


# count the necessary values 
def get_count_for_senses(train_file_path1=None, train_file_path2=None, sense_label=[]):

    unigram_sense1, total_token_sense1,length_train_set_sense1 = count_sense(train_file_path1)
    unigram_sense2, total_token_sense2,length_train_set_sense2 = count_sense(train_file_path2)

    unique_tokens = set()
    for item in unigram_sense1.getBgs(1000) :
        unique_tokens.add(item[0])
    
    count_sense1_token = len(unique_tokens)

    unique_tokens_sense2 = set()
    for item in unigram_sense2.getBgs(1000):
        unique_tokens.add(item[0])
        unique_tokens_sense2.add(item[0])

    total_no_common_tokens = len(unique_tokens_sense2)+count_sense1_token - len(unique_tokens)

    # print("Total number of common tokens between two senses is", total_no_common_tokens)

    # calculating prior for each class
    length_total_train_set = length_train_set_sense1+length_train_set_sense2
    p_sense1 = length_train_set_sense1 / length_total_train_set
    p_sense2 = length_train_set_sense2 / length_total_train_set
    v = len(unique_tokens)
    count_c_sense1 = total_token_sense1
    count_c_sense2 = total_token_sense2

    return {'p_sense1':p_sense1 , #prior prob of sense1
    'p_sense2': p_sense2 , # prior probability of sense2
    'v': v,  # total number of unique tokens
    'count_sense1':count_c_sense1,  # total number of tokens in sense1
    'count_sense2':count_c_sense2,  #total number of tokens in sense2
    'sense1_uhash':unigram_sense1, # unigram count for sense1
    'sense2_uhash':unigram_sense2, #unigrams count for sense2
    'sense_label':sense_label, # list of actual words represented by sense1 and sense2 variable
    'common_token': total_no_common_tokens # number for common tokens between two senses
    }


# calculate probability on test file
def perform_test(test_file_path, counts, sense_label,label):
    prediction_list = []
    with open(test_file_path) as f:
        try:
            # print("Parsing file: "+ test_file_path)
            lines = f.readlines()
            for i,line in enumerate(lines):
                words = line.split( )
                prob_sense1 = counts['p_sense1']
                prob_sense2 = counts['p_sense2']
                for word in words:
                    # calculate probability
                    if counts['sense1_uhash'].find(word):
                        p_ws1 = (counts['sense1_uhash'].find(word))/ (counts['count_sense1'] + counts['v'])
                    else:
                        p_ws1 = 1 / (counts['count_sense1'])
                    if counts['sense2_uhash'].find(word):
                        p_ws2 = (counts['sense2_uhash'].find(word) +1)/ (counts['count_sense2']+counts['v'])
                    else:
                        p_ws2 = 1/ (counts['count_sense2'])
                    prob_sense1 *=  p_ws1
                    prob_sense2 *= p_ws2
                if prob_sense1 > prob_sense2:
                    prediction = sense_label[0]
                else:
                    prediction = sense_label[1]
                if prediction == label:
                    prediction_list.append(1) #append 1 for correct prediction
                else:
                    prediction_list.append(0) #append 0 for incorrect prediction
        except IOError:
            print("Cannot read input file "+input_file)
    return prediction_list


# performs both training and testing 
def naive_bayes(sense_label=['big','small'],window=None):
    
    train_file_path1 = os.path.join("dataset", sense_label[0]+"_train_w"+str(window)+".txt")
    train_file_path2 = os.path.join("dataset", sense_label[1]+"_train_w"+str(window)+".txt")

    test_file_path1 = os.path.join("dataset", sense_label[0]+"_test_w"+str(window)+".txt")
    test_file_path2 = os.path.join("dataset", sense_label[1]+"_test_w"+str(window)+".txt")

    outfile = open(os.path.join("outputs", sense_label[0]+"_"+sense_label[1]+"_w"+ str(window)+".txt"), "w")

    start= time.time()
    # training naive bayes
    counts = get_count_for_senses(train_file_path1=train_file_path1, train_file_path2=train_file_path2, sense_label=sense_label)
    duration = round(time.time()-start, 3)
    print("Time taken to trainining is {} seconds". format(duration))
    outfile.write("Time taken for training : "+str(duration)+' seconds'+'\n')

    # testing naive bayes
    start = time.time()
    predictions1 = perform_test(test_file_path=test_file_path1,counts=counts,sense_label=sense_label,label=sense_label[0])
    predictions2 = perform_test(test_file_path=test_file_path2,counts=counts,sense_label=sense_label,label=sense_label[1])
    duration = round(time.time()-start, 3)
    print("Time taken to test is {} seconds". format(duration))
    outfile.write("Time taken for testing : "+ str(duration)+' seconds'+'\n')

   # measuring accuracy
    accuracy_sense1 =  round(sum(predictions1)/len(predictions1),4)
    accuracy_sense2 = round(sum(predictions2)/len(predictions2),4)
    total_accuracy = round ((sum(predictions1)+sum(predictions2))/(len(predictions1)+len(predictions2)),3)

    print('Accuracy for sense ' + sense_label[0] + ' is ' + str(accuracy_sense1))
    print('Accuracy for sense ' + sense_label[1] + ' is ' + str(accuracy_sense2))
    print("Total accuracy of classifier is ", total_accuracy)

    print("************************************************************************************************")
    print("\n")

    outfile.write('Accuracy for sense ' + sense_label[0] + ' is ' + str(accuracy_sense1) + '\n')
    outfile.write('Accuracy for sense ' + sense_label[1] + ' is ' + str(accuracy_sense2)+'\n')
    outfile.write("Total accuracy of classifier is "+ str( total_accuracy)+'\n')
    outfile.write("Total number of common token is "+ str( counts['common_token']))

    
if __name__ == "__main__":
    start= time.time()
    windows = [5,10,20]
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    for window in windows:
        print("Result for window size ", window )
        naive_bayes(['night','seat'],window)
        naive_bayes(['kitchen', 'cough'],window)
        naive_bayes(['car','bike'],window)
        naive_bayes(['manufacturer', 'bike'],window)
        naive_bayes(['big','small'],window)
        naive_bayes(['huge','heavy'],window)
    print("Total time taken is for all runs is :", round (time.time()- start,6))
