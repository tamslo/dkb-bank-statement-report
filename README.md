# DKB Bank Statement Report

Reporting for DKB bank statements. Uses [`pdfplumber`](https://github.com/jsvine/pdfplumber) to extract data from PDFs.

Build the Docker image and run the sript with the following commands:

```
> docker build -t dkb-report .
> docker run -v $(pwd):/dkb-report dkb-report python3 script.py
```

The PDF bank statements to be analyzed need to be placed in the `bank-statements` diectory.

This project is currently under construction :construction:, please see below for TODOs:

* [x] Read data from PDFs
* [ ] Analyze ingoing and outgoing balance per account
* [ ] Analyze categories per account (probably add config for this)