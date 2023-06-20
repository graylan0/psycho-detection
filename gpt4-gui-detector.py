import openai

# Set the API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Define a matrix of data
data_matrix = [
    ["delusions", "Does the text show signs of delusions?"],
    ["hallucinations", "Does the text show signs of hallucinations?"],
    ["disorganized speech", "Does the text show signs of disorganized speech?"],
    ["disorganized behavior", "Does the text show signs of disorganized behavior?"],
    ["negative symptoms", "Does the text show signs of negative symptoms?"]
]

def analyze_text(text, prompt):
    # Use the GPT-4 API to analyze the text
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=f"{text}\n\n{prompt}",
        temperature=0.5,
        max_tokens=60
    )

    # Get the model's answer
    answer = response.choices[0].text.strip()

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
