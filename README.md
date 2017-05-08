This program was written by Katherine Howitt and Meredith Lancaster under the supervision of Prof. William Sakas
at Hunter College, Computer Science and the Graduate Center, Linguistics and Computer Science of the City University
of New York. It is written in Python 2.7.

sakas@hunter.cuny.edu

The program implements a learner that weights parameters on a continuum from 0 to 1, using human-like language e-triggers grounded in Chomsky's principles
and parameters framework. The learning model is one of first language acquisition, i.e., acquisition by a child of approximately 2 years of age.

The learner and the abstract domain over which it operates is in detail in:

Sakas, W.G. & Fodor, J.D. (2012) Disambiguating Syntactic Triggers, Language Acquisition (19) pp 83-143.

The paper and domain and other relevant information are downloadable here:

http://www.colag.cs.hunter.cuny.edu/downloadables.html

-----

5/7/2017: The program is currently being maintained by Katherine Howitt & Meredith Lancaster

kghowitt@gmail.com
mlancaster16@huntersoe.edu

The most recent data generated by the program are currently available in the results folder.

###Running the program
The program must be run with a Python interpreter that supports Python 2.7. It can run with
`python main.py <number of learners> <number of sentences to be processed> <language name> [-c, --convergence] [-p, --plots]`

###Language Code #Language Name is used in lieu of Language code in current versions
The file EngFrJapGerm.txt contains 3522 sentences, corresponding to fake languages which represent (and mimic the grammatical structure of) either English, French, Japanese, or German. Each language has a code associated with it, allowing the user to specify which language the learners should be trained on.

French=584, English=611, German=2253, and Japanese=3856

###Output
The program will write simulation results to a csv to a folder whose name starts with the used language followed by the number of learners, and a timestamp. For example:
English_100_32016-06-09T14.17.54.747187 will contain the results of simulation using 100 learners with English.
