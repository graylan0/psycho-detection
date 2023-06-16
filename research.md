Sure, I can help you refine the script. However, it's important to note that AI models, including Llama, are not capable of diagnosing mental health conditions like psychosis. They can help identify patterns in text that might suggest a person is experiencing certain symptoms, but they cannot replace a professional diagnosis. 

Here's an improved version of the script that includes more detailed analysis functions:

```python
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, Y, RIGHT, END, StringVar, IntVar, Checkbutton
from llama_cpp import Llama

# Llama Model
llm = Llama(model_path="D:\\ggml-vicuna-7b-4bit\\ggml-vicuna-7b-4bit-rev1.bin")

def llama_generate(prompt, max_tokens=200):
    output = llm(prompt, max_tokens=max_tokens)
    return output['choices'][0]['text']

def analyze_sentiment(input_text):
    sentiment_prompt = f"What is the sentiment of the following text: {input_text}?"
    sentiment = llama_generate(sentiment_prompt)
    return sentiment

def analyze_spelling_and_grammar(input_text):
    spelling_and_grammar_prompt = "Are there any spelling or grammar mistakes in the following text: {input_text}?"
    spelling_and_grammar = llama_generate(spelling_and_grammar_prompt)
    return spelling_and_grammar

def analyze_vocabulary_changes(input_text):
    vocabulary_changes_prompt = "Are there any unusual or out-of-place words in the following text: {input_text}?"
    vocabulary_changes = llama_generate(vocabulary_changes_prompt)
    return vocabulary_changes

def analyze_topic_shifts(input_text):
    topic_shifts_prompt = "Has the topic changed significantly in the following text: {input_text}?"
    topic_shifts = llama_generate(topic_shifts_prompt)
    return topic_shifts

# ...

def generate_response(input_text):
    global context_history
    context_history.append(input_text)
    context = ' '.join(context_history[-5:])  # Use the last 5 turns as context

    response = ""
    if use_llama:
        # Generate response using Llama
        llama_response = llama_generate(context)
        response += f"Llama: {llama_response}\n"

        # Perform sentiment analysis using Llama
        sentiment = analyze_sentiment(context)
        response += f"Sentiment: {sentiment}\n"

        # Check for spelling and grammar mistakes using Llama
        spelling_and_grammar = analyze_spelling_and_grammar(context)
        response += f"Spelling and Grammar: {spelling_and_grammar}\n"

        # Check for vocabulary changes using Llama
        vocabulary_changes = analyze_vocabulary_changes(context)
        response += f"Vocabulary Changes: {vocabulary_changes}\n"

        # Check for topic shifts using Llama
        topic_shifts = analyze_topic_shifts(context)
        response += f"Topic Shifts: {topic_shifts}\n"

    context_history.append(response)
    return response
```

In this version of the script, I've added a function to analyze topic shifts. This function generates a prompt asking the Llama model whether the topic has changed significantly in the user's input text, then sends this prompt to the model and returns its output.

Remember, this is a simplified example and a real implementation would likely be much more complex. You would need to decide how to interpret the outputs from the Llama model and how to use them to inform the AI's responses. As always, this tool should not replace professional help and any signs of psychosis should be addressed by a healthcare professional.
