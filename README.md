- [Stats](#stats)
  - [Input](#input)
  - [Sentence extraction](#sentence-extraction)
  - [Output](#output)
    - [vanilla oneshot classification on 303 extracted sentences](#vanilla-oneshot-classification-on-303-extracted-sentences)
    - [agentic classification on 303 extracted sentences](#agentic-classification-on-303-extracted-sentences)
    - [Cost for Processing using vanilla oneshot prompt](#cost-for-processing-using-vanilla-oneshot-prompt)
    - [Cost for Processing using ReAct Agents](#cost-for-processing-using-react-agents)
- [How to Run?](#how-to-run)
  - [Setup](#setup)
  - [Set ENV](#set-env)
  - [Language of Text](#language-of-text)
  - [The Execution](#the-execution)


[Original Article](https://www.linkedin.com/pulse/does-size-matter-ai-model-performance-smart-chunking-guckes-gm0le/)

# Stats
## Input
- [youtube video Source](https://youtu.be/syDpQtORBzg)
- [yt_transcript](./assets/yt_transcript.txt) containing 1440 Lines
- extracted using [tactic.io](https://tactiq.io/tools/youtube-transcript)
- no temperature was set, default applied

## Sentence extraction
- 303 Sentences extracted using `SpaCy` NLP Package `en_core_web_lg`

## Output
### vanilla oneshot classification on 303 extracted sentences

modelname | chunk_to_sentence_ratio | number_of_chunks | words_per_chunk
--- | --- | --- | ---
llama-3.3-70b-versatile | 1:11,7 | 26 | 411.9
gpt-4o-2024-08-06 | 1:5.6 | 54 | 202.2
gemma2-9b-it | 1:1.8 | 173 | 63.9
mixtral-8x7b-32768 | 1:1.3 | 246 | 45.0
gpt-4o-mini-2024-07-18 | 1:1.2 | 261 | 42.4

### agentic classification on 303 extracted sentences
modelname | chunk_to_sentence_ratio | number_of_chunks | words_per_chunk
--- | --- | --- | ---
llama-3.3-70b-versatile | 1:15.9 | 19 | 556.0
gpt-4o-2024-08-06 | 1:9.5 | 32 | 337
gemma2-9b-it | - | - | -
mixtral-8x7b-32768 | - | - | -
gpt-4o-mini-2024-07-18 | 1:4.7 | 64 | 171.1

### Cost for Processing using vanilla oneshot prompt
Based on aforementioned 303 Sentences rounded up to full cents:

Model | Total Cost
--- | ---
llama-3.3-70b-versatile | 0.09$
gpt-4o-2024-08-06 | 0.38$
gemma2-9b-it | 0.01$
mixtral-8x7b-32768 | 0.02$
gpt-4o-mini-2024-07-18 | 0.01$

---

### Cost for Processing using ReAct Agents
> TRL: Token Rate Limit exceeded - size of chunk exceeded Model Providers limit on tokens/Minute before any usable result was produced, not testable in current setup

Model | Total Cost
--- | ---
llama-3.3-70b-versatile | 1.23$
gpt-4o-2024-08-06 | 9.40$
gemma2-9b-it | TRL
mixtral-8x7b-32768 | TRL
gpt-4o-mini-2024-07-18 | 0.48$

> Processing time went up significantly with an agentic approach, mostly because of getting ratelimited by APIs or because responsetimes slowed down to one response in 6-25s. 

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

