import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Initialize the GPT-Neo model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')
model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M').to(device)

# Define a matrix of data
data_matrix = [
    ["delusions", "Does the text show signs of delusions?"],
    ["hallucinations", "Does the text show signs of hallucinations?"],
    ["disorganized speech", "Does the text show signs of disorganized speech?"],
    ["disorganized behavior", "Does the text show signs of disorganized behavior?"],
    ["negative symptoms", "Does the text show signs of negative symptoms?"]
]

def analyze_text(text, prompt):
    # Encode the prompt
    encoded_prompt = tokenizer.encode(prompt + text, return_tensors='pt')

    # Generate the response using the GPT-Neo model
    output = model.generate(encoded_prompt, max_length=60, do_sample=True)
    answer = tokenizer.decode(output[0])

    return answer

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')
    return data

def main():
    # Read the text file
    file_path = "path_to_your_file.txt"
    text = read_file(file_path)

    # Iterate over the data matrix and analyze the text for each prompt
    for data in data_matrix:
        symptom, prompt = data
        answer = analyze_text(text, prompt)
        print(f"{symptom}: {answer}")

if __name__ == "__main__":
    main()
