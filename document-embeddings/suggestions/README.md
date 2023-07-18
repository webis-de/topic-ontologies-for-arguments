Setup
-----
```
python3 -m venv myvenv
pip3 install -r requirements.txt
source myvenv/bin/activate
```

110 Test Arguments
------------------
Copy data from CEPH to data
```
./src/bash/fetch-test-data.sh
```

Execute similarity calculation, write results to output.
```
./src/bash/run-on-test-data.sh
```
