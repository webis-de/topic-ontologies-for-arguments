Setup
```
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

Quickstart
```
python3 src/python/preprocess-for-esa.py --help
python3 src/python/preprocess-for-esa.py --input-file test-topics.csv --text-columns text --kept-columns topic.id --output-file test-topics-preprocessed.csv
python3 src/python/preprocess-for-esa.py --input-file test-documents.csv --text-columns text --kept-columns document.id --output-file test-documents-preprocessed.csv

python3 src/python/get-vocabulary.py --help
python3 src/python/get-vocabulary.py --input-file test-topics-preprocessed.csv --text-columns text-preprocessed --output-file test-topics-vocabulary.csv

python3 src/python/represent-by-esa.py --help
python3 src/python/represent-by-esa.py --input-file test-topics-preprocessed.csv --id-column topic.id --text-column text-preprocessed --vocabulary-file test-topics-vocabulary.csv --output-file test-topics-esa.csv
python3 src/python/represent-by-esa.py --input-file test-documents-preprocessed.csv --id-column document.id --text-column text-preprocessed --vocabulary-file test-topics-vocabulary.csv --output-file test-documents-esa.csv

python3 src/python/reduce-esa-representation.py --help
python3 src/python/reduce-esa-representation.py --input-file test-topics-esa.csv --num-entries 3 --output-file test-topics-esa-reduced.csv

vocabulary_size=$(($(cat test-topics-vocabulary.csv | wc -l) - 1))
python3 src/python/suggest-for-esa.py --help
python3 src/python/suggest-for-esa.py --documents-file test-documents-esa.csv --topics-file test-topics-esa.csv --vocabulary-size $vocabulary_size --output-file test-suggestions.csv
python3 src/python/suggest-for-esa.py --documents-file test-documents-esa.csv --topics-file test-topics-esa-reduced.csv --vocabulary-size $vocabulary_size --method "esa@3" --output-file test-suggestions-reduced.csv

python3 src/python/get-topk-suggestions.py --help
python3 src/python/get-topk-suggestions.py test-suggestions.csv test-suggestions-reduced.csv --k 1 --output-file test-top-suggestions.csv
```
