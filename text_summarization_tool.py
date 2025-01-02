
from transformers import pipeline
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Summarization Function
def summarize_text(text, max_length=150, min_length=40):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

# GUI Functions
def load_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, file.read())

def perform_summarization():
    text = input_text.get(1.0, tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please provide some input text!")
        return

    max_len = int(max_length_var.get())
    min_len = int(min_length_var.get())
    
    if min_len >= max_len:
        messagebox.showerror("Error", "Minimum length should be less than maximum length!")
        return

    summary = summarize_text(text, max_length=max_len, min_length=min_len)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, summary)

# GUI Setup
root = tk.Tk()
root.title("Text Summarization Tool")

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Input Text:").pack(anchor=tk.W)
input_text = scrolledtext.ScrolledText(input_frame, width=60, height=15, wrap=tk.WORD)
input_text.pack(padx=5, pady=5)

file_button = tk.Button(input_frame, text="Load Text File", command=load_text_file)
file_button.pack(pady=5)

# Settings Frame
settings_frame = tk.Frame(root)
settings_frame.pack(pady=10)

tk.Label(settings_frame, text="Max Length:").grid(row=0, column=0, padx=5, pady=5)
max_length_var = tk.StringVar(value="150")
max_length_entry = tk.Entry(settings_frame, textvariable=max_length_var, width=5)
max_length_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(settings_frame, text="Min Length:").grid(row=0, column=2, padx=5, pady=5)
min_length_var = tk.StringVar(value="40")
min_length_entry = tk.Entry(settings_frame, textvariable=min_length_var, width=5)
min_length_entry.grid(row=0, column=3, padx=5, pady=5)

# Output Frame
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

tk.Label(output_frame, text="Summary Output:").pack(anchor=tk.W)
output_text = scrolledtext.ScrolledText(output_frame, width=60, height=15, wrap=tk.WORD)
output_text.pack(padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

summarize_button = tk.Button(button_frame, text="Summarize", command=perform_summarization)
summarize_button.pack(side=tk.LEFT, padx=10)

# Run the Application
root.mainloop()
