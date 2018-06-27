# Spoon-River-Anthology
Final project for NSS Data Science cohort. Uses NLP against the Spoon River Anthology to determine relationships and groups amongst the characters. 

### Executive Summary

Given The Spoon River Anthology by Edgar Lee Masters, how can natural language processing draw out the characters and their relationships, as well as interesting aspects about their life?


### Motivation

For this project, I wanted to incorporate natural language processing in some way. 
I really enjoy poetry, and Edgar Lee Masters has some great poems, with Spoon River being one of the most well known books of the 20th Century!
I see this as a great opportunity to dig into a subject I am interested in, and get in some good reading while I do it.


### Data Question

Can I use nlp to sift through the poems in The Spoon River Anthology to determine relationships, hardships, love, or loss?
This is a unique dataset in the sense that every chapter is tied directly to a character in the book, regarding a number topics.
Some of the poems recite their history, turning points in their life, or observations of life from the outside.
Some talk of the treatment of their graves, and few talk of life on the other side.

How are the characters similar? 
Is there a way to cluster the different ways they passed away?
In addition to this information.. 
Is there a way to graph the relationships to bring further insights?

There have been studies on Spoon River, mainly summaries on the book itself.
However, I have not found any useage of nlp regarding the poems, nor a graphical interface to view the characters.


### Data Sources

[Spoon River Anthology](https://www.bartleby.com/84/index1.html) can be read in full through bartleby.

I will also be using some built-in libraries through the popular nltk library for collections on synonym/antonym relationships, stopwords, and others.


### Known Issues and Challenges

While there are 246 chapters in Spoon River, this is still a small dataset.
The ability to accurately cluster groups of people with such a small set should be a difficult task.

My dataset is all poetry which in itself is hard to read; poetry is not as someone speaks naturally.
I can imagine this leading to more unique words within my dataset than someone might normally write. 
This can lead to some challenges regarding clustering, or similar context.


```
"The Hill"

Where are Elmer, Herman, Bert, Tom and Charley,
The weak of will, the strong of arm, the clown, the boozer, the fighter?
All, all are sleeping on the hill.
One passed in a fever,
One was burned in a mine,
One was killed in a brawl,
One died in a jail,
One fell from a bridge toiling for children and wife—
All, all are sleeping, sleeping, sleeping on the hill.
Where are Ella, Kate, Mag, Lizzie and Edith,
The tender heart, the simple soul, the loud, the proud, the happy one?
—
All, all are sleeping on the hill.
One died in shameful child-birth,
One of a thwarted love,
One at the hands of a brute in a brothel,
One of a broken pride, in the search for heart’s desire;
One after life in far-away London and Paris
Was brought to her little space by Ella and Kate and Mag
—
All, all are sleeping, sleeping, sleeping on the hill.
Where are Uncle Isaac and Aunt Emily,
And old Towny Kincaid and Sevigne Houghton,
And Major Walker who had talked
With venerable men of the revolution?
—
All, all are sleeping on the hill.
They brought them dead sons from the war,
And daughters whom life had crushed,
And their children fatherless, crying
—
All, all are sleeping, sleeping, sleeping on the hill.
Where is Old Fiddler Jones
Who played with life all his ninety years,
Braving the sleet with bared breast,
Drinking, rioting, thinking neither of wife nor kin,
Nor gold, nor love, nor heaven?
Lo! he babbles of the fish-frys of long ago,
Of the horse-races of long ago at Clary’s Grove,
Of what Abe Lincoln said
One time at Springfield.
```
