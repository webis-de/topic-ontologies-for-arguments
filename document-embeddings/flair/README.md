Setup
```
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

Quickstart
```
python3 src/python/embed.py --input-file test-documents.csv --id-column document.id --text-column text --embedding-type bert --output-file test-output.csv 
python3 src/python/weighted-embed.py --input-file test-documents.csv --id-column document.id --text-column text --weights-file test-weights.csv --lemma-column lemma --weight-column weight --embedding-type glove --output-file test-output.csv
```
