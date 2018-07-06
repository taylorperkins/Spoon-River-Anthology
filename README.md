## Spoon River Anthology

### Overview
Spoon River Anthology is a book of poems written by Edgar Lee Masters written in the early 1900's.
Every poem in the book is told by a fictional character (some based on people Edgar knew) that have died in this town.
Given that each character has passed away, the characters will talk about any number of things..
Love, loss, regret, guilt, joy, what it is like in the afterlife, or how people are currently attending to their gravestones.
It is an incredible novel, with so much spirit and emotion.

For this particular project, I hope to do two things.
1. Uncover the relationships in the book.
Since the characters are from the same town, many of them knew each other.
It is an interesting project to uncover those relationships, and be able to view the town at a high level.
2. Second is to cluster the characters based on sentiment.
An easy question to ask is..
Which characters are talking about the same things?
Is there a way to determine similarities?
I think so, and I would love to solve this using nlp and a graphing interface, such as networkx.

### My Thought Process, Order to Completion
1. I need the data!
This dataset is pretty easy to obtain overall.
I programmatically went through the contents of the book found [here](https://www.bartleby.com/84/index1.html) and scraped out what I needed.
You can find the code for my process [here](./notebooks/scraping_data/Scrape_Poems.ipynb).
2. Now that I have the text for the poems, I need to clean them a bit.
There are new lines at the beginning of the files, and sometimes in the middle of the poems.
For every 5th line in a poem, there number representing the line number at the very end of that line.
In addition to this..
Every poem has either the first or first and second words completely capitalized.
This makes it a pretty difficult to appropriately identify names, or other words of importance.
This need to be normalized as every other line in the poems.
These processes are relatively simple, and you can find the code for that process [here](./notebooks/scraping_data/Clean_Scraped_Poems.ipynb).
3. Model on

### Determining Similarities

I want to have a simple and understandable approach/alogorithm for determining if two poems are similar.
From there, I can break it down further and get more granular.
With that being said, this is my first approach.

Each poem is a document, since that is what we will be comparing, making the book the corpus.
After vectorizing the documents, I will perform a TF-IDF process over all of them.
The TF-IDF will assign weights to every word in the document within the context of the document while considering both how many documents are present.
This makes it easier to compare one poem against another using a numeric score.

During this process, I will also be converting each unique word to a numeric representation and storing the results as a dictionary for further use.
This is better for both memory and speed when processing my results.

In this scenario, the TF-IDF will not be enough to compare the documents.
In addition to TF-IDF, I will also use synonyms to help determine weight.

Given two poems and after normalizing the current scores, the rules will be as follows:
* For any word in P1 that is also found in P2, we sum the TF-IDF scores of all instances from both poems.
* For any word in P1 that has a synonym that is _also_ a synonym to a different word in P2, we sum all TF-IDF scores for those instances and divide by 2.
* For words without a direct match, and no synonym mapping to a different word, their score does not contribute to the overall similarity score.

#### Technologies To Use
1. [Gensim](https://radimrehurek.com/gensim/).
Really killer nlp library.
I will be using this for a few things during this process.
Converting [strings to vectors](https://radimrehurek.com/gensim/tut1.html#from-strings-to-vectors),
storing their vectors in a re-useable [dictionary](https://radimrehurek.com/gensim/corpora/dictionary.html),
and their [TF-IDF](https://radimrehurek.com/gensim/models/tfidfmodel.html) model.
2. [NLTK](https://www.nltk.org/).
I will be using this package for their [wordnet](http://www.nltk.org/howto/wordnet.html) module.
They have a fantastic synonym set to map between words.
3. [NetworkX](https://networkx.github.io/).
Python graph library used for..
Graphs.
This will help find the open triangle relationships I will need to for synonym matching between poems.

