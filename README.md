# Stats
## Input
- [youtube video Source](https://youtu.be/syDpQtORBzg)
- [yt_transcript](./assets/yt_transcript.txt) containing 1440 Lines
- extracted using [tactic.io](https://tactiq.io/tools/youtube-transcript)

## Sentence extraction
- 303 Sentences extracted using `SpaCy` NLP Package

## Output
(ratios calculated on original 329 extracted sentence dataset -> see [compressed.txt](./assets/compressed.txt))

modelname | chunk_to_sentence_ratio | number_of_chunks | words_per_chunk
--- | --- | --- | ---
llama-3.3-70b-versatile | 1:12.7 | 26 | 428.6
gpt-4o | 1:10.3 | 32 | 348.2
gemma2-9b-it | 1:1.8 | 184 | 60.5
mixtral-8x7b-32768 | 1:1.3 | 252 | 44.2
gpt-4o-mini | 1:1.2 | 266 | 41.8

## Cost for Processing
Based on aforementioned 303 Sentences rounded up to full cents:

Model | Total Cost
--- | ---
llama-3.3-70b-versatile | 0.09$
gemma2-9b-it | 0.01$
