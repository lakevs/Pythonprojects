import tkinter as tk
from tkinter import messagebox
import time
import random

sentences = [
    "This will be what you write, (Change it).",
    "This will be what you write, (Change it).",
    "This will be what you write, (Change it)."
]


class TypingSpeedTestApp:
    def __init__(self, root):
      
        self.root = root
        self.root.title("Typing Speed Test")
        self.sentence = random.choice(sentences)
        self.start_time = None
        self.end_time = None
        self.sentence_label = tk.Label(root, text=self.sentence, wraplength=400)
        self.sentence_label.pack(pady=20)
        self.typing_area = tk.Text(root, height=5, width=50)
        self.typing_area.pack(pady=20)
        self.typing_area.bind("<KeyPress>", self.start_timer4)
        self.submit_button = tk.Button(root, text="Submit", command=self.calculate_speed)
        self.submit_button.pack(pady=20)

    def start_timer4(self, event):
        if self.start_time is None:
            self.start_time = time.time()

    def calculate_speed(self):
        self.end_time = time.time()
        typed_text = self.typing_area.get("1.0", "end-1c")

        if not typed_text:
            messagebox.showerror("Error", "You didn't type anything!")
            return

        elapsed_time = self.end_time - self.start_time
        word_count = len(typed_text.split())
        words_per_minute = (word_count / elapsed_time) * 60

        accuracy = self.calculate_accuracy(self.sentence, typed_text)

        result_message = (
            f"Time taken: {elapsed_time:.2f} seconds\n"
            f"Words per minute: {words_per_minute:.2f}\n"
            f"Accuracy: {accuracy:.2f}%"
        )
        messagebox.showinfo("Results", result_message)
        self.reset_test()

    def calculate_accuracy(self, original, typed):
        original_words = original.split()
        typed_words = typed.split()

        correct_words = sum(1 for o, t in zip(original_words, typed_words) if o == t)
        total_words = max(len(original_words), len(typed_words))
        accuracy = (correct_words / total_words) * 100
        return accuracy

    def reset_test(self):
        self.start_time = None
        self.typing_area.delete("1.0", "end")
        self.sentence = random.choice(sentences)
        self.sentence_label.config(text=self.sentence)


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
