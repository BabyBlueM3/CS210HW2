import re
from collections import Counter
import math

def clean(rowRead):


    rowRead = re.sub(r'https?://\S+|\bhttps?\S*', '', rowRead)  # Remove URLs
    rowRead = re.sub(r'[^\w\s]', '', rowRead)  # Remove punctuation
    rowRead = re.sub(r'\s+', ' ', rowRead).strip()  # Remove extra spaces
    rowRead = rowRead.lower()  # Convert to lowercase
    return rowRead

def loadStopWords(stopwordsFile='stopwords.txt'):
    """Load stopwords from a file and return them as a set."""
    try:
        with open(stopwordsFile, 'r') as file:
            stopwords = set(file.read().splitlines())  # Read stopwords into a set for fast lookup
        return stopwords
    except FileNotFoundError:
        print(f"Error: Stopwords file '{stopwordsFile}' not found.")
        return set()  # Return an empty set if file is not found

def cleanStopWords(rowRead, stopWords):
    words = rowRead.split()
    cleanedWords = [word for word in words if word not in stopWords]
    cleanedText = " ".join(cleanedWords)
    return cleanedText

def stemmingLemma(rowRead):
    words = rowRead.split()
    cleanedWords = []  

    for word in words:
        if word[-3:] == 'ing':
            cleanedWord = word[:-3]  
        elif word[-2:] == 'ly':
            cleanedWord = word[:-2]  
        elif word[-4:] == 'ment':
            cleanedWord = word[:-4]  
        else:
            cleanedWord = word  
        cleanedWords.append(cleanedWord)
    
    cleanedText = " ".join(cleanedWords)
    return cleanedText

def write_preprocessed_data(doc_files, stopwordsInput):
    for doc_file in doc_files:
        # Read the document
        with open(doc_file, 'r') as file:
            text = file.read()
            
            # Perform preprocessing steps: cleaning, stopword removal, and stemming
            cleaned_text = clean(text)  # Clean the text
            cleaned_text_stopWords = cleanStopWords(cleaned_text, stopwordsInput)  # Remove stopwords
            cleaned_text_stemming = stemmingLemma(cleaned_text_stopWords)  # Perform stemming/lemmatization
            
            # Write to new file with prefix "preproc_"
            output_file = f"preproc_{doc_file}"
            with open(output_file, 'w') as out_file:
                out_file.write(cleaned_text_stemming)
            print(f"Preprocessed data written to {output_file}")






def compute_tf(doc):
    word_count = Counter(doc.split())
    total_words = len(doc.split())
    tf = {word: count / total_words for word, count in word_count.items()}
    return tf

def compute_idf(documents):
    num_documents = len(documents)
    word_document_count = {}

    for doc in documents:
        words_in_doc = set(doc.split())  # Avoid counting the same word multiple times in the same doc
        for word in words_in_doc:
            word_document_count[word] = word_document_count.get(word, 0) + 1

    idf = {word: (math.log(num_documents / count) + 1 ) for word, count in word_document_count.items()}
    print(num_documents)
    return idf

def compute_tfidf(documents):
    tfidf_scores = []
    idf = compute_idf(documents)

    for doc in documents:
        tf = compute_tf(doc)
        tfidf = {word: tf[word] * idf[word] for word in tf}

        # Sort the words based on their TF-IDF score (in descending order)
        sorted_tfidf = sorted(tfidf.items(), key=lambda x: (-x[1], x[0]))  # Sort by TF-IDF score, then by word
        tfidf_scores.append(sorted_tfidf[:5])  # Keep top 5
    return tfidf_scores

def print_top_words(tfidf_scores):
    top_words = []  # List to hold the tuples of (word, score)
    for tfidf in tfidf_scores:
        top_words.append([(word, round(score, 2)) for word, score in tfidf])  # Append rounded tuples
    return top_words  # Return the list of tuples

def write_tfidf_to_file(tfidf_scores, doc_files):
    top_words = print_top_words(tfidf_scores)  # Get the formatted, rounded top words
    
    for i, tfidf in enumerate(top_words):
        output_file = f"tfidf_{doc_files[i]}"
        
        with open(output_file, 'w') as file:
            file.write(str(tfidf))  # Write the list of tuples as a string to the file
            print(f"TF-IDF results written to {output_file}")

def main():
    input_file = 'tfidf_docs.txt'
    
    # Read the list of document filenames
    with open(input_file, 'r') as file:
        doc_files = file.read().splitlines()
    
    # Load stopwords from file
    stopwordsInput = loadStopWords()    

    # Write preprocessed documents to new files with "preproc_" prefix
    write_preprocessed_data(doc_files, stopwordsInput)

    # Read preprocessed documents
    documents = [open(f"preproc_{doc_file}", 'r').read() for doc_file in doc_files]  
    tfidf_scores = compute_tfidf(documents)

    # Write TF-IDF results to files with "tfidf_" prefix
    write_tfidf_to_file(tfidf_scores, doc_files)

main()

