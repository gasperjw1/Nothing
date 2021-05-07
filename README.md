# Nothing

We use an LDA topic model approach to analyze the show _Seinfeld_ and whether or not it is a "show about nothing."

## Contributors

- [Yash Mahtani](https://github.com/gasperjw1)
- [Saar Haber]()
- [Andriy Repik]()

## Build

To run the program, run the Python program `Topic_Model_Seinfeld.py`. The program has already been ran, but can be ran again for testing purposes. If ran, all the other files will be overwritten with updated information due to running the program.

## Notes

Packages required to successfully run this program are:

- spacy
- nltk
- gensim
- pickle

All the necessary information to run the program is located in the folder named `initialInformation`.
All the csv files created as a result of running the program will be located in the folder named `results`. Both these folders currently contain files due to the program being ran already.
In terms of reading the results, if any given set of words (that defines a certain topic) does not encompass at least 50% of the entire show, then we deem that that topic (generated from our corpus) does not define the topic of that show.
