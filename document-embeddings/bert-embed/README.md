Setup
```
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install -r requirements.txt
```

Quickstart
```
python3 src/python/embed.py --bert_model bert-base-uncased --do_lower_case --max_seq_length 512 --output_file test-output.txt --input_file test-input.txt --layers="-2"
```
