# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.10.12 or later

## Environment setup

1) Download venv package in python
```bash
$  sudo apt install python3-venv -y
```

2) Create your environment
```bash
$  python3 -m venv myvenv
```

3) Activate your environment
```bash
$  source myvenv/bin/activate
```

## Requirements

### Install the required packages

```bash
$ pip install -r requirements.txt
```

## Setup the environment variables

```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the Uvicorn API server 

```bash 
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```