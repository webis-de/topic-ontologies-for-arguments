import sys
import pandas
from transformers import BertTokenizer

def load_data(sentences_file = sys.argv[1]):
    frame = pandas.read_csv(sentences_file)
    sentences = frame.sentences.values
    labels = frame.labels.values
    print('Number of sentences: {:}'.format(len(sentences)))
    return (sentences, labels)

def encode_sentence(sentence, encoder):
    return encoder.encode_plus(sentence, pad_to_max_length = True)

def encode_sentences(sentences, encoder = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)):
    input_ids = []
    attention_masks = []
    for s in range(len(sentences)):
        if s % 1000 == 0:
            print('Sentence {:} of {:}'.format(s, len(sentences)))
        sentence = sentences[s]
        encoding = encode_sentence(sentence, encoder)
        if len(encoding["input_ids"]) > 512:
            input_ids.append(encoding["input_ids"][0:512])
            attention_masks.append(encoding["attention_mask"][0:512])
        else:
            input_ids.append(encoding["input_ids"])
            attention_masks.append(encoding["attention_mask"])
    return input_ids, attention_masks

output_file = sys.argv[2]
sentences, labels = load_data()
input_ids, attention_masks = encode_sentences(sentences)
frame = pandas.DataFrame({'labels':labels, 'input_ids':input_ids, 'attention_masks':attention_masks})
frame.to_csv(output_file, index=False)

