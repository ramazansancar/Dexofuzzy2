
# Dexofuzzy: Dalvik EXecutable Opcode Fuzzyhash

Dexofuzzy is a similarity digest hash for Android. It extracts Opcode Sequence from Dex file based on Ssdeep and generates hash that can be used for similarity comparison of Android App. Dexofuzzy created using Dex's opcode sequence can find similar apps by comparing hash.

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg) ![Latest Version](https://img.shields.io/badge/pypi-v3.3-blue.svg) ![Python Versions](https://img.shields.io/badge/python-3-blue.svg)

## Requirements

 Dexofuzzy requires the following modules:
* ssdeep 3.3 or later

## Install

### Install on CentOS 6.10, 7.9, 8.5, Stream 8
```console
$ yum install epel-release
$ yum install libffi-devel ssdeep ssdeep-devel python3-pip python3-devel libtool 
$ pip3 install dexofuzzy
```

### Install on Debian 8.11, 9.13, 10.11
```console
$ apt-get install libffi-dev libfuzzy-dev python3-pip
$ pip3 install dexofuzzy
```

### Install on Ubuntu 14.04 LTS, 16.04 LTS, 18.04 LTS, 20.04 LTS
```console
$ apt-get install libffi-dev libfuzzy-dev
$ pip3 install dexofuzzy
```

### Install on Windows 7, 10
* The ssdeep DLL binaries for Windows are included in ./dexofuzzy/bin/ directory.
  * [intezer/ssdeep-windows](https://github.com/intezer/ssdeep-windows)  is included.
  * [MacDue/ssdeep-windows-32_64](https://github.com/MacDue/ssdeep-windows-32_64)  is included.
```console
$ pip3 install dexofuzzy
```

## Usage
```
usage: dexofuzzy [-h] [-f SAMPLE_FILENAME] [-d SAMPLE_DIRECTORY] [-m] [-g N M]
                 [-s DEXOFUZZY DEXOFUZZY] [-c CSV_FILENAME] [-j JSON_FILENAME]
                 [-l]

Dexofuzzy - Dalvik EXecutable Opcode Fuzzyhash

optional arguments:
  -h, --help                     show this help message and exit
  -f SAMPLE_FILENAME, --file SAMPLE_FILENAME
                                 the sample to extract dexofuzzy
  -d SAMPLE_DIRECTORY, --directory SAMPLE_DIRECTORY
                                 the directory of samples to extract dexofuzzy
  -m, --method-fuzzy             extract the fuzzyhash based on method of the sample
                                 (must include the -f or -d option by default)
  -g N, --clustering N M         N-Gram Tokenizer and M-Partial Matching clustering based on the sample's dexofuzzy
                                 (must include the -d option by default)
  -s DEXOFUZZY DEXOFUZZY, --score DEXOFUZZY DEXOFUZZY
                                 score the dexofuzzy of the sample
  -c CSV_FILENAME, --csv CSV_FILENAME
                                 output as CSV format
  -j JSON_FILENAME, --json JSON_FILENAME
                                 output as json format
                                 (include method fuzzy or clustering)
  -l, --error-log                output the error log
```

### Output Format Example
* *FileName, FileSha256, FileSize, DexoHash, Dexofuzzy*
```bash
$ dexofuzzy -f SAMPLE_FILE
sample.apk,80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835,42959,94d36ca47485ca4b1d05f136fa4d9473bb2ed3f21b9621e4adce47acbc999c5d,48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q
```
* *Method Fuzzy*
```bash
$ dexofuzzy -f SAMPLE_FILE -m 
80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835,80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835,42959,d89c3b2c2620b77b1c0df7ef66ecde6d70f30b8a3ca15c21ded4b1ce1e319d38,48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q
[
    "3:mWc0R2gLkcT2AVA:mWc51cTnVA",
    "3:b0RdGMVAn:MA",
    "3:y+6sMlHdNy+BGZn:y+6sMh5En",
    "3:y4CdNy/GZn:y4C+En",
    "3:dcpqn:WEn",
    "3:EN:EN",
    ...
]
```
* *Clustering using N-Gram and M-Partial Matching*
```bash
$ dexofuzzy -d SAMPLE_DIRECTORY -g 7 3
80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835,80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835,42959,d89c3b2c2620b77b1c0df7ef66ecde6d70f30b8a3ca15c21ded4b1ce1e319d38,48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q
ffe8c426c3a8ade648666bb45f194c1e84fb499b126932997c4d50cdfc4cc8f3,ffe8c426c3a8ade648666bb45f194c1e84fb499b126932997c4d50cdfc4cc8f3,46504,4a7039eefb7a8c292bcbd3e9fa232f4e6b136eedb9a114eb32aa360742b3f28f,48:B2KmUCNc2FuGgy9fbdD7uPrEMc0HZj0/zeGn5:B2+Cap3y9pDHMHZ4/zeG5
[
    {
        "dexohash": "d89c3b2c2620b77b1c0df7ef66ecde6d70f30b8a3ca15c21ded4b1ce1e319d38",
        "dexofuzzy": "48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q",
        "file_name": "80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835",
        "file_sha256": "80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835",
        "file_size": "42959",
        "clustering": [
            {
                "file_name": "80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835",
                "file_sha256": "80cd7786fa42a257dcaddb44823a97ff5610614d345e5f52af64da0ec3e62835",
                "file_size": "42959",
                "dexohash": "d89c3b2c2620b77b1c0df7ef66ecde6d70f30b8a3ca15c21ded4b1ce1e319d38",
                "dexofuzzy": "U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY",
                "signature": [
                    "U7uPrEM",
                    "7uPrEMc",
                    "uPrEMc0"
                ]
            },
            {
                "file_name": "ffe8c426c3a8ade648666bb45f194c1e84fb499b126932997c4d50cdfc4cc8f3",
                "file_sha256": "ffe8c426c3a8ade648666bb45f194c1e84fb499b126932997c4d50cdfc4cc8f3",
                "file_size": "46504",
                "dexohash": "4a7039eefb7a8c292bcbd3e9fa232f4e6b136eedb9a114eb32aa360742b3f28f",
                "dexofuzzy": "B2KmUCNc2FuGgy9fbdD7uPrEMc0HZj0/zeGn5",
                "signature": [
                    "2KmUCNc",
                    "KmUCNc2",
                    "mUCNc2F"
                ]
            }
        ]
    },
    {
        ...
    }
]    
```

### Python API
To compute a Dexofuzzy of ``dex file``, use ``hash`` function:
* *dexofuzzy(dex_binary_data)*
```python
>>> import dexofuzzy
>>> with open('classes.dex', 'rb') as dex:
...     dex_data = dex.read()
>>> dexofuzzy.hash(dex_data)
'48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q'
```
* *dexofuzzy_from_file(apk_file_path or dex_file_path)*
```python
>>> import dexofuzzy
>>> dexofuzzy.hash_from_file('Sample.apk')
'48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q'
>>> dexofuzzy.hash_from_file('classes.dex')
'48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q'
```
The ``compare`` function returns the match between 2 hashes, an integer value from 0 (no match) to 100.
* *compare(dexofuzzy_1, dexofuzzy_2)*
```python
>>> import dexofuzzy
>>> with open('classes.dex', 'rb') as dex:
...     dex_data = dex.read()
>>> hash1 = dexofuzzy.hash(dex_data)
>>> hash1
'48:U7uPrEMc0HZj0/zeGnD2KmUCNc2FuGgy9fY:UHMHZ4/zeGD2+Cap3y9Q'
>>> hash2 = dexofuzzy.hash_from_file('classes2.dex')
>>> hash2
'48:B2KmUCNc2FuGgy9fbdD7uPrEMc0HZj0/zeGn5:B2+Cap3y9pDHMHZ4/zeG5'
>>> dexofuzzy.compare(hash1, hash2)
50
```

## Tested on
* CentOS 6.10, 7.7, 8.5, Stream 8
* Debian 8.11, 9.13, 10.11
* Ubuntu 14.04 LTS, 16.04 LTS, 18.04 LTS, 20.04 LTS, 22.04 LTS
* Windows 7, 10

## Publication
* Shinho Lee, Wookhyun Jung, Sangwon Kim, Eui Tak Kim, [Android Malware Similarity Clustering using Method based Opcode Sequence and Jaccard Index](https://ieeexplore.ieee.org/iel7/8932631/8939563/08939894.pdf), In: Proceedings of the 2019 International Conference on Information and Communication Technology Convergence, ICTC, 16-18 October 2019.
* Shinho Lee, Wookhyun Jung, Sangwon Kim, Jihyun Lee, Jun-Seob Kim, [Dexofuzzy: Android Malware Similarity Clustering Method using Opcode Sequence](https://www.virusbulletin.com/uploads/pdf/magazine/2019/201911-Dexofuzzy-Android-Malware-Similarity-Clustering-Method.pdf), Virus Bulletin, 25 October 2019.
* Shinho Lee, Wookhyun Jung, Wonrak Lee, HyungGeun Oh, Eui Tak Kim, [Android Malware Dataset Construction Methodology to Minimize Bias-Variance Tradeoff](https://www.sciencedirect.com/science/article/pii/S2405959521001351/pdfft?md5=62c643429a39f8f7e31609fbd89c56a0&pid=1-s2.0-S2405959521001351-main.pdf), ICT Express, 8 October 2021.

## License
Dexofuzzy is licensed under the terms of the Apache license. See  [LICENSE](https://github.com/lee1029ng/Dexofuzzy/blob/master/LICENSE) for more information.
