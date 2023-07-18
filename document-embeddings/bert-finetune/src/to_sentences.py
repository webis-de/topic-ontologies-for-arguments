import pandas
import nltk
import sys
nltk.download('punkt')

input = sys.argv[1]
output = sys.argv[2]

def to_sentences(texts, labels, min_characters = 50):
    sentences = []
    sentences_label = []
    for i in range(len(texts)):
        print('Text: ', str(i))
        text_sentences = nltk.tokenize.sent_tokenize(texts[i])
        text_sentences = [s for s in text_sentences if len(s) > min_characters]
        sentences = sentences + text_sentences
        for l in range(len(text_sentences)):
            sentences_label.append(str(i))

    print('Sentences: ' + str(len(sentences)))
    print('Labels:    ' + str(len(sentences_label)))
    frame = pandas.DataFrame({'labels':sentences_label, 'sentences':sentences})
    return frame

def to_sentences_csv(input, output):
    frame = pandas.read_csv(input)
    to_sentences(frame.text.values, frame.concept.values).to_csv(output, index=False)

to_sentences_csv(input, output)

