# Company Policy RAG Chatbot

## Live Demo
(https://rag-chatbot-gcc8r4o8uzmtqjn2qeqrup.streamlit.app/)
                                                                                    (https://github.com/umeshgurjar914042-creator/rag-chatbot-/blob/025d7550105d7f3e7016df18f593bf074f806115/screenshot](screenshot.png)

## What it does
Answers employee questions from a company policy document.
Says "I don't know" when the answer is not in the document.

## Tech
Python, Gemini API, ChromaDB, Streamlit

## How it works
1. Policy text is split into chunks
2. Chunks are converted to embeddings and stored in ChromaDB
3. The question is matched to the closest chunks
4. Gemini answers using only those chunks
