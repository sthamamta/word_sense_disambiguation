# word_sense_disambiguation
This project is designed to disambiguate the following word pairs using a Naive Bayes algorithm:

1. night, seat (pseudoword: nightseat)
2. kitchen, cough (pseudoword: kitchencough)
3. car, bike (pseudoword: carbike)
4. manufacturer, bike (pseudoword: manufacturerbike)
5. big, small (pseudoword: bigsmall)
6. huge, heavy (pseudoword: hugeheavy)

The input directory for this project must contain the file 'amazon_reviews.txt'. The code files and input directory must be in the same directory for the program to run correctly.

### Usage
1. Clone the repository to your local machine.
   ```sh
   git clone https://github.com/sthamamta/word_sense_disambiguation.git
   ```
2. Ensure that you have Python 3 and the necessary dependencies installed which include nltk.
3. Go to codes directory
4. To run the code, specify the shell script by running:
```sh
  ./run.sh
   ```
This will run two code files: generate_context_word.py and naive_bayes.py.

The first code file will generate a dataset with context words for all pseudowords. The second code file performs train and test, and the results will be saved in the outputs directory.

After the program has finished running, the user will be prompted whether they want to run train and test again with a dataset containing equal examples in the trainset for both senses. If the user answers yes, the results will be generated and saved in the outputs directory.

### Phases of the project
The project is broken down into the following phases:

Phase 0: Word Pair Disambiguation
Use the 6 word pairs listed above to disambiguate.

Phase I: Extracting Contexts
For each word in the ambiguous pair, extract a context of plus/minus 10 words from the corpus.
Set 80% of the contexts aside for training and 20% for testing.

Phase II: Creating Pseudowords
For each of the word pairs, replace the word in the corpus with the pseudoword, and create a truth file of which was the original word.

Phase III: Training
From the training corpus, calculate the probabilities for each of the two senses for each pseudoword.
From the training corpus, using a window of size plus/minus 10, calculate the frequencies of each word seen in the window around each pseudoword occurrence. These words are the context features.

Phase IV: Testing
Use the 20% of the contexts reserved for testing, to disambiguate the pseudowords.

Phase V: Evaluation
For each sense, determine whether the identified sense is correct or not. 