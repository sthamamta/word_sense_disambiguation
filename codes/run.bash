python3 generate_context_word.py input/amazon_reviews.txt
python3 naive_bayes.py
echo "Do you want to run equal trainset training?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) python3 naive_bayes_equal_train.py; break;;
        No ) exit;;
    esac
done