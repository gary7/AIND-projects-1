import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    for i in range(0, len(test_set.get_all_sequences())):
        prob_dict = {}
        X, lengths = test_set.get_item_Xlengths(i)

        for word, model in models.items():
            try:
                logL = model.score(X, lengths)
                prob_dict[word] = logL
            except:
                prob_dict[word] = float('-inf')

        probabilities.append(prob_dict)
        guess = max([(max_log_value, max_word) for max_word, max_log_value in prob_dict.items()])[1]
        guesses.append(guess)

    return probabilities, guesses
