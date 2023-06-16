import json
import tkinter as tk
from llama_cpp import Llama
import requests

# Assuming llm1 generates code, llm2 debugs code, llm3 searches the web, and llm4 asks GPT-4 for advice
llm1 = Llama(model_path="path_to_model_1")
llm2 = Llama(model_path="path_to_model_2")
llm3 = Llama(model_path="path_to_model_3")
llm4 = Llama(model_path="path_to_model_4")

# Initialize the task structure
task_structure = {
    "task": "",
    "code": "",
    "debugged_code": "",
    "test_result": "",
    "new_code": "",
    "search_results": "",
    "advice": ""
}

# GUI setup
root = tk.Tk()
entry = tk.Entry(root)
entry.pack()
text = tk.Text(root)
text.pack()

def generate_code(llm, prompt, max_tokens=200):
    output = llm(prompt, max_tokens=max_tokens)
    return output['choices'][0]['text']

def debug_code(llm, code, max_tokens=200):
    output = llm(code, max_tokens=max_tokens)
    return output['choices'][0]['text']

def test_code(code):
    try:
        # Execute the code
        exec(code)
        return "Code executed successfully"
    except Exception as e:
        # If there's an error, return it
        return str(e)

def ask_advice(llm, error, max_tokens=200):
    prompt = f"I encountered an error when running some code: {error}. Can you help me fix it?"
    output = llm(prompt, max_tokens=max_tokens)
    return output['choices'][0]['text']

def search_web(llm, query, max_tokens=200):
    prompt = f"Search the web for: {query}"
    output = llm(prompt, max_tokens=max_tokens)
    return output['choices'][0]['text']

def execute_task():
    # Get the task from the user input
    task = entry.get()

    # Generate some code
    code = generate_code(llm1, task)

    # Debug the code
    debugged_code = debug_code(llm2, code)

    # Test the code
    test_result = test_code(debugged_code)

    # If there's an error, ask GPT-4 for advice
    if "error" in test_result:
        advice = ask_advice(llm4, test_result)
    else:
        advice = "No errors found"

    # Feed the test result back into the model as a new prompt
    new_prompt = f"The result of the code execution was: {test_result}"
    new_code = generate_code(llm1, new_prompt)

    # Search the web for documentation related to the task
    search_results = search_web(llm3, task + " documentation")

    # Update the task structure
    task_structure["task"] = task
    task_structure["code"] = code
    task_structure["debugged_code"] = debugged_code
    task_structure["test_result"] = test_result
    task_structure["new_code"] = new_code
    task_structure["search_results"] = search_results
    task_structure["advice"] = advice

    # Display the task structure in the GUI
    text.insert(tk.END, json.dumps(task_structure, indent=4))
