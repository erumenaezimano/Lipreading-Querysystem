# -*- coding: utf-8 -*-
"""analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A9ky6vSAFemuXNPe_1pxOjftmz5j4EOQ
"""

#install yaml library
pip install ruamel-yaml

#install spacy library
!pip install spacy

#import libraries
import json
import pandas as pd
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from PIL import Image

#load dataset
with open('C:/Users/Guest1/Documents/Lip-Reading/text.json', 'r') as f:
    t = json.load(f)

#t

#transform .json file to a dataframe
df_a = pd.DataFrame(t)

#df_a

"""##Preprocessing"""

#remove whitespace from text using regular expression
import re

#define a regular expression to match whitespace
punct_re = r'^\\W+|\\W+$'

# apply the regular expression to the 'text' column
df_a['text'] = df_a['text'].apply(lambda x: re.sub(punct_re, '', x))

#df_a

#define a function to remove \".txt\" extension from filename
def remove_txt_extension(file_name):
    return file_name[:-4]

df_a['filename'] = df_a['filename'].apply(remove_txt_extension)

#make a duplicate of the dataframe
df_b = df_a.copy()

#df_b

df_a.to_csv("C:/Users/Guest1/Documents/Lip-Reading/text_files")

#downloading the large english language model for spacy
!python -m spacy download en_core_web_lg

#load the english language model
nlp = spacy.load('en_core_web_lg')

#define a function to tokenize a text using spacy
def tokenize_text(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    return tokens

#apply the tokenize_text function to the text column
df_b['tokens'] = df_b['text'].apply(tokenize_text)

#define a function to remove \"'s\" tokens\n",
    def remove_apostrophe_s(tokens):
    return [token for token in tokens if token != "'S"]

    #apply the function to the 'text' column
    df_b['tokens'] = df_b['tokens'].apply(remove_apostrophe_s)

    #df_b

#define custom stop words and add them to the Spacy stopwords list
custom_stop_words = ["'re", "'ve", "'m", "'ll", "n't", "'s", "i'm"]
for word in custom_stop_words:
    nlp.vocab[word].is_stop = True

#add all numbers to the spacy stopwords list
for word in range(10):
    nlp.vocab[str(word)].is_stop = True

#define a function to remove stopwords from a list of tokens
def remove_stopwords(tokens):
    processed_tokens = []
    for token in tokens:
        if not nlp.vocab[str(token)].is_stop:
            processed_tokens.append(token)
    return processed_tokens

df_b['tokens'] = df_b['tokens'].apply(remove_stopwords)

df_c = df_b.copy()

#extract lemmas, POS tags, and dependencies from each token
def preprocess_text(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    pos_tags = [token.pos_ for token in doc]
    dependency = [token.dep_ for token in doc]
    return lemmas, pos_tags, dependency

df_b[['lemmas', 'pos_tags', 'dependency']] = df_b['text'].apply(preprocess_text).apply(pd.Series)\

#df_b

#create a new column to hold the named entities
#df_p["ner"] = ""

#process each text and extract the named entities
#for i, row in df_t.iterrows():
    #texts = row["text"]
    #ner = nlp(texts)
    #entities = []
    #for ent in ner.ents:
        #entities.append({"text": ent.text, "label": ent.label_})
    #save the named entities as a string in the DataFrame
    #df_p.at[i, "ner"] = str(entities)

    #for tag in ner.ents:
        #print(tag.text, f"({tag.label_})")

#select a row  to display the dependency parse tree
row_index = 54246
text = df_b.loc[row_index, "text"]
#parse the text using the spacy model
doc = nlp(text)
for token in doc:
    print(token.text, "-->", "pos: "+token.pos_, "|", "dep: "+token.dep_, "")

"""The POS and dependencies gives insight into the structure and relationships of the words in the text"""

#import the displacy module to visualise the POS and dependency
from spacy import displacy

#display the dependency parse tree
displacy.render(doc, style="dep", jupyter=True, options={"distance":80})

#remove space and empty string tokens from the 'tokens' column
tokens = df_b['tokens'].explode().reset_index(drop=True)
tokens = tokens[tokens.str.strip().astype(bool)]

#count the frequencies of each token
token_counts = tokens.value_counts().reset_index().rename(columns={'index': 'token', 'tokens': 'count'})

#select the top 20 most frequent tokens
top_tokens = token_counts.head(20)

top_tokens.head()

#visualise top 20 tokens
plt.figure(figsize=(10,6))
sns.barplot(y='count', x='token', data=top_tokens, palette='twilight_shifted_r')
plt.title('Top 20 Token')
plt.xticks(rotation=45,ha='right')
plt.show()

"""The bar chart shows the frequency of the top 20 tokens in the corpus"""

#install the worldcloud library
pip install wordcloud

#import libraries for wordcloud visualisation
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud

#explode the 'tokens' column to flatten the list
tokens = df_b['tokens'].explode().reset_index(drop=True)

#define a function to remove stopwords from the tokens
def remove_stopword(tokens):
    processed_tokens = []
    for token in tokens:

#check if token is a valid string or integer
        if isinstance(token, str) or isinstance(token, int):
#check if token is not a stopword
            if not nlp.vocab[token.lower()].is_stop:
                processed_tokens.append(token)
    return processed_tokens

#process the tokens using the remove_stopwords function
processed_tokens = remove_stopword(tokens)

#load an image as a mask for the wordcloud
mask = np.array(Image.open("C:/Users/Guest1/Documents/Lip-Reading/trump.png"))

#generate a wordcloud with the specified mask
wordcloud = WordCloud(background_color='white', mask = mask).generate(' '.join(processed_tokens))

#visualise the wordcloud
plt.figure(figsize=(10,60))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

"""The word cloud visually represents the most frequent tokens, with larger tokens indicating higher frequencies

##Extract Video Clips Duration
"""

#import garbage collection
import gc

#path for input folder and folder to save the output
input_folder = "C:/Users/Guest1/Documents/Lip-Reading//pretrain_duration"
output_folder = "C:/Users/Guest1/Documents/Lip-Reading/duration_csv"

#specify the name of the column to drop
column_to_drop = "asdscore"

#specify the batch size
batch_size = 1000

i = 0

#loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        #transform the files to dataframe
        filepath = os.path.join(input_folder, filename)
        df_w = pd.read_csv(filepath)

        #drop the specified column
        df_w.drop(columns=[column_to_drop], inplace=True)

        # Save the output in the folder for output
        output_filename = filename
        output_filepath = os.path.join(output_folder, output_filename)
        df_w.to_csv(output_filepath, index=False)

        #print(f"{filename}\n")
        #print(df_w)
        #print("\n")

        i += 1
        #reset the dataframe and clear the memory after processing a batch
        if (i+1) % batch_size == 0:
            df_w = None
            gc.collect()

"""The garbage collection was used to process the dataset efficiently in smaller batches, effectively managing memory due to its size during the operation."""

#check the number of files
path = "C:/Users/Guest1/Documents/Lip-Reading/duration_csv"
num_files = len(os.listdir(path))
print(num_files)

#path to the folder to save the output
duration = "C:/Users/Guest1/Documents/Lip-Reading/process"

#specify the batch size
batch_size = 1000

i = 0

#loop through each file in the input folder
for filename in os.listdir(output_folder):
    if filename.endswith(".csv"):
        #path for files
        input_file_path = os.path.join(output_folder, filename)
        output_file_path = os.path.join(duration, filename)

        df_w= pd.read_csv(input_file_path)

        df_w["duration"] = df_w["end"] - df_w["start"]

        #save the output
        df_w.to_csv(output_file_path, index=False)

        i += 1
        #reset the dataframe and clear the memory after processing a batch
        if (i+1) % batch_size == 0:
            df_w = None
            gc.collect()

#= 0

#for filename in os.listdir(duration):
    #if filename.endswith('.csv'):
        #df_w = pd.read_csv(os.path.join(duration, filename))
        #
       # word_count = df_w['word'].value_counts()
        #avg_duration = df_w['duration'].mean()

        ## filter out any rows that contain missing or NaN values
        #df_w = df_w.dropna()

        # create a new column for frequency and average duration for each file
        #df_w['freq'] = df_w['word'].apply(lambda x: word_count[x])
       # df_w['avg_duration'] = round(avg_duration, 2)

        # save output
        #df_w.to_csv(os.path.join(duration, filename), index=False)

        # print the output
        #print(f" {filename}:")
        #print(df_w)

       # i += 1
        # reset the dataframe and clear the memory after processing a batch
        #if (i+1) % batch_size == 0:
            #df_w = None
            #gc.collect()

#specify the video clip to use
dt = '0067430.csv'

#transform the file to a dataframe
filepath = os.path.join(duration, dt)
fn = pd.read_csv(filepath)

#visualise the words and their duration
plt.figure(figsize=(12, 5))
ax = sns.barplot(x='word', y='duration', data=fn, palette='twilight_shifted_r')
ax.set(xlabel='Word', ylabel='Duration', title=f'Bar Chart of Word and Duration for {filename}')
plt.xticks(rotation=45)
plt.show()

"""The bar chart visually represents the duration of each word in the video clip"""

#make a duplicate of the folder with word duration
import shutil

#specify the paths to the source and destination folders
dup = "C:/Users/Guest1/Documents/Lip-Reading/process_c"

#create the folder if it does not exist
if not os.path.exists(dup):
    os.makedirs(dup)

#get a list of all the files in the source folder
files = os.listdir(duration)

#copy each file in the source folder to the destination folder
for file in files:
    src_file = os.path.join(duration, file)
    dest_file = os.path.join(dup, file)
    shutil.copy(src_file, dest_file)

#get the minimum and maximum duration of each sentence
#initialize an empty list to store the results
mn = []

for filename in os.listdir(dup):
    if filename.endswith(".csv"):
        df_mn = pd.read_csv(os.path.join(dup, filename))
        #extract the min and max of "end" from the dataframe
        max_end = df_mn["end"].max()
        #append the results to the list
        mn.append((filename, max_end))

#save the results to a new
with open("minmax.txt", "w") as f:
    for result in mn:
        f.write(f"{result[0]}, {result[1]}\n")

with open('minmax.txt', 'r') as f:
    lines = f.readlines()

#split each string into columns and store in a list of lists
l = [line.strip().split(', ') for line in lines]

#create dataframe from list of lists
min_max = pd.DataFrame(l, columns=['filename', 'duration'])

#convert min duration and max duration columns to numeric
min_max['duration'] = pd.to_numeric(min_max['duration'])

min_max = min_max.apply(lambda x: x.str.replace(".csv", "", regex=False) if x.dtype == "object" else x)

min_max

"""The table holds the video files ID and the duration of each video clip"""

#drop the column holding minimum duration
#df_d = min_max.drop(['min_d'], axis = 1)

#df_d=df_d.rename(columns={'max_d':'duration'})

#df_d

#get the average duration of each sentence
# Create an empty list to store the filename and average durations
#a_time = []

#for filename in os.listdir(dup):
   # if filename.endswith(".csv"):
       #transform the files to a dataframe
       # filepath = os.path.join(dup, filename)
       # df_avg = pd.read_csv(filepath)

        # Extract the average duration from the dataframe and append it to the list
       # avg_duration = df_avg["avg_duration"].iloc[0]
       # a_time.append((filename, avg_duration))

# Save the list of filename and average durations to a new file
#with open("avg_durations.txt", "w") as f:
   # for file_duration in a_time:
       # f.write(file_duration[0] + ": " + str(file_duration[1]) + "\n")

#create a dataframe with average duration and filename
#with open('avg_durations.txt', 'r') as f:
    #avg_d = f.read()

# Split the text based
#rows = avg_d.split("\n")

# Split each row based on ":" and create a list of dictionaries
#a_d = []
#for row in rows:
   # split_row = row.split(": ")
   # if len(split_row) == 2:
       # filename, value = split_row
      #  a_d.append({"filename": filename, "avg_duration": float(value)})
  #  else:
        #print()

# Create a Pandas dataframe
#avg = pd.DataFrame(a_d)

# remove the .csv extension from all columns
#avg = avg.apply(lambda x: x.str.replace(".csv", "", regex=False) if x.dtype == "object" else x)

#avg

df_e=df_a.copy()

#merge the average duration dataframe and max duration dataframe with text data frame
df_e = pd.merge(df_e, min_max, left_on='filename', right_on='filename')

df_e

"""The table shows the video clip IDs, the text from the clips and their duration"""

#count the number of tokens in each sentence
df_e['word_count'] = df_e["text"].apply(lambda x: len(str(x).split(" ")))
 #count the number of characters in each sentence
df_e['char_count'] = df_e["text"].apply(lambda x: sum(len(word) for word in str(x).split(" ")))
#avg_wc = df_e['char_count'] / df_e['word_count'] #average word count of each sentence
#df_e['avg_wd_count'] = round(avg_wc, 2)

df_e

#extract the columns with numeric values
n_cols = ['duration', 'word_count', 'char_count']

#extract the min and max values and video clip ID for each column
min_vals = [df_e[col].min() for col in n_cols]
max_vals = [df_e[col].max() for col in n_cols]
min_files = [df_e.loc[df_e[col].idxmin(), 'filename'] for col in n_cols]
max_files = [df_e.loc[df_e[col].idxmax(), 'filename'] for col in n_cols]

#create a new dataframe with the min and max values
minmax = pd.DataFrame({
    'column': n_cols,
    'min_value': min_vals,
    'min_file': min_files,
    'max_value': max_vals,
    'max_file': max_files
})

#print the output
minmax

"""The table shows the video clip with minimum and maximum duration, word count and character count"""

#extract the longest and shortest video clips
longest_sentence = df_e.loc[df_e['duration'].idxmax()]
shortest_sentence = df_e.loc[df_e['duration'].idxmin()]

#create a new dataframe to store the results
df_z = pd.DataFrame(columns=['filename', 'duration', 'word_count'])

#append the results to the new dataframe using pandas.concat
df_z = pd.concat([df_z, longest_sentence[['filename', 'duration', 'word_count']].to_frame().T], ignore_index=True)
df_z = pd.concat([df_z, shortest_sentence[['filename', 'duration', 'word_count']].to_frame().T], ignore_index=True)

#print the result
df_z

"""Video clips with ID 9537 is the longest and 34119 is the shortest

##Extract Negative Words from Video Clips
"""

#extract negative words from the video clips using regular expression
import re

#define a regular expression pattern to match negative words
pattern = r'\b\w+(?:n\'t\b)|\b(?:no|not|never)\b'

#define a function to extract negative words from a string
def extract_negative_words(text):
    matches = re.findall(pattern, text.casefold())
    return ', '.join(matches)

#apply the function to the "text" column and store the results in a new column
df_e['Negative_words'] = df_e['text'].apply(extract_negative_words)

df_e

"""The table shows the video clips that have negative words. Video clip with ID 5 has "DON'T" and video clip with ID 96314 has "NO"
"""

#frequency of the negative words
nw = df_e['Negative_words'].explode().reset_index(drop=True)
nw_counts = nw.value_counts().reset_index().rename(columns={'index': 'N_words', 'nw_counts': 'count'})

#rename the 'Negative_words' column to 'count'
nw_counts = nw_counts.rename(columns={'Negative_words': 'count'})

nw_counts = nw_counts.drop(0)

#nw_counts

#import counter
from collections import Counter

#initialize a counter object to store the individual words and their counts
nw_counter = Counter()

#iterate through the dataframe and update the word_counter with individual words and their counts
for index, row in nw_counts.iterrows():
    words = row['N_words'].split(', ')
    count = row['count']
    for word in words:
        nw_counter[word] += count

#create a new dataframe from the word_counter and sort it by the 'count' column in descending order
df_nw = pd.DataFrame.from_dict(nw_counter, orient='index', columns=['count']).reset_index()
df_nw.columns = ['N_words', 'count']
df_nw.sort_values(by='count', ascending=False, inplace=True)
df_nw.reset_index(drop=True, inplace=True)

#print the unique_words_df
df_nw

"""The table displays the frequency of negative words"""

#visualise the frequency of the negative words
plt.figure(figsize=(15,6))
ax = sns.barplot(x='N_words', y='count', data=df_nw, palette = 'twilight_shifted_r')
plt.title('Negative Words Distribution')
plt.xlabel('Negative Words')
plt.xticks(rotation=45,ha='right')
plt.show()

"""The bar chart shows that the words "NOT," "DON'T," and "NO" have higher frequencies"""

#save the dataframe to a new file
df_e.to_csv("sentences.csv", sep="\t", index=False)
df_e.to_csv("C:/Users/Guest1/Documents/Lip-Reading/sentences")

#make a duplicate of the dataframe
df_f = df_c.copy()

df_g = df_c.copy()

"""##Bag of Words Generation"""

#import the required libraries
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from string import digits

#define custom stop words
custom_stop_words = ["'re", "'ve", "'m", "'ll", "n't", "'s", "i'm"]

#define a function to preprocess the text column using nltk
def preprocess_text(text):
    # Remove digits
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)
    # Tokenize the text using nltk
    tokens = nltk.word_tokenize(text)
    # Remove custom stop words and nltk stop words
    stop_words = set(stopwords.words('english') + custom_stop_words)
    tokens = [token for token in tokens if not (token.lower() in stop_words)]
    # Return the preprocessed text as a string
    return ' '.join(token for token in tokens)

#apply the preprocess_text function to the 'text' column
df_g['text'] = df_g['text'].apply(preprocess_text)

#import the CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#convert the text data into a bag-of-words matrix
bow = CountVectorizer()
bow_features = bow.fit_transform(df_g["text"])

#print the vocabulary of the bag of words
print(bow.vocabulary_)

"""The vocabulary dictionary indexes words in the Bag of Words"""

#access the vocabulary of the bag of words and retrieve the index of the word "chip"
dic_vocabulary = bow.vocabulary_
word = "chip"
dic_vocabulary[word]

#get the count frequency for each word in the vocabulary
word_count = np.array(bow_features.sum(axis=0)).flatten()
sorted_indices = word_count.argsort()[::-1]
sorted_word_count = word_count[sorted_indices]
sorted_vocabulary = np.array(bow.get_feature_names_out())[sorted_indices]

#visualise the count frequency
#plt.figure(figsize=(10, 5))
#plt.bar(sorted_vocabulary[:20], sorted_word_count[:20])
#plt.xticks(rotation=90)
#plt.xlabel('Word')
#plt.ylabel('Count Frequency')
#plt.title('Top 20 Words by Count Frequency')
#plt.show()

#get the feature names
feature_names = bow.get_feature_names_out()

# Iterate through each sentence in the DataFrame and its corresponding Bag of Words feature array
for sentence, feature in zip(df_g['text'], bow_feature_array):
    # Print the first 50 characters of the sentence
    print(sentence[:50])

    # Print the first 10 elements of the Bag of Words feature array for the current sentence
    print(feature[:10])

#convert the BOW features to a dense array
bow_feature_array = bow_features.toarray()
#print the feature names corresponding to the columns in the feature array
print(bow.get_feature_names_out())
#iterate through each sentence in the dataframe and its corresponding BOW feature array
for sentence, feature in zip(df_g['text'], bow_feature_array):
  #print the first 50 characters of the sentence
    #print(sentence[:50])
    #print the first 10 elements of the Bag of Words feature array for the current sentence
    #print(feature[:10])

#path to the folder to save visemes, phonemes and homophones
lp = "C:/Users/Guest1/Documents/Lip-Reading/words"

#create the folder if it does not exist
if not os.path.exists(lp):
    os.makedirs(lp)

for filename in os.listdir(duration):
    if filename.endswith(".csv"):
        filepath = os.path.join(duration, filename)
        ph = pd.read_csv(filepath)

        #drop redundant columns
        ph = ph.drop(columns=["start", "end"])

        #save the output
        output_filename = filename
        output_filepath = os.path.join(lp, output_filename)
        ph.to_csv(output_filepath, index=False)