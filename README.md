- [Stats](#stats)
  - [Input](#input)
  - [Sentence extraction](#sentence-extraction)
  - [Output](#output)
    - [latest testrun on 303 extracted sentences](#latest-testrun-on-303-extracted-sentences)
    - [old output](#old-output)
  - [Cost for Processing](#cost-for-processing)
- [How to Run?](#how-to-run)
  - [Setup](#setup)
  - [Set ENV](#set-env)
  - [Language of Text](#language-of-text)
  - [The Execution](#the-execution)


# Stats
## Input
- [youtube video Source](https://youtu.be/syDpQtORBzg)
- [yt_transcript](./assets/yt_transcript.txt) containing 1440 Lines
- extracted using [tactic.io](https://tactiq.io/tools/youtube-transcript)
- no temperature was set, default applied

## Sentence extraction
- 303 Sentences extracted using `SpaCy` NLP Package

## Output
### latest testrun on 303 extracted sentences

modelname | chunk_to_sentence_ratio | number_of_chunks | words_per_chunk
--- | --- | --- | ---
llama-3.3-70b-versatile | 1:11,7 | 26 | 411.9
gpt-4o-2024-08-06 | 1:5.6 | 54 | 202.2
gemma2-9b-it | 1:1.8 | 173 | 63.9
mixtral-8x7b-32768 | 1:1.3 | 246 | 45.0
gpt-4o-mini-2024-07-18 | 1:1.2 | 261 | 42.4


### old output
(ratios calculated on original 329 extracted sentence dataset -> see [compressed.txt](./assets/compressed.txt))

modelname | chunk_to_sentence_ratio | number_of_chunks | words_per_chunk
--- | --- | --- | ---
llama-3.3-70b-versatile | 1:12.7 | 26 | 428.6
gpt-4o-2024-08-06 | 1:10.3 | 32 | 348.2
gemma2-9b-it | 1:1.8 | 184 | 60.5
mixtral-8x7b-32768 | 1:1.3 | 252 | 44.2
gpt-4o-mini-2024-07-18 | 1:1.2 | 266 | 41.8



## Cost for Processing
Based on aforementioned 303 Sentences rounded up to full cents:

Model | Total Cost
--- | ---
llama-3.3-70b-versatile | 0.09$
gpt-4o-2024-08-06 | 0.38$
gemma2-9b-it | 0.01$
mixtral-8x7b-32768 | 0.02$
gpt-4o-mini-2024-07-18 | 0.01$

---

# How to Run?
## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
```

## Set ENV
you will want to at least set these two variables
```bash
LLM_MODEL=groq/llama-3.3-70b-versatile
LLM_API_KEY='your-api-key-here'
# ...
INPUT_TRANSCRIPT_PATH='./assets/yt_transcript.txt' # adjust to whatever file you want to chunk
```


## Language of Text
If you do not work with an english text you may want to switch this model

You will find available SpaCy Models [here](https://spacy.io/usage/models#languages)
```bash
python -m spacy download en_core_web_lg # if you don't use english texts, this needs to be switched out
```

And in the .env file again:
```bash
NLP_MODEL=en_core_web_lg
```

## The Execution
```bash
python src/main.py
```
