import tkinter as tk
import time
import random

texts = [
    "PAdaptability is the ability to adjust and thrive in changing circumstances, and it is essential to navigating the complexities of life. Whether it's adapting to new technologies, social norms, or personal challenges, adaptability allows us to stay resilient and flexible in the face of change."
]

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test Pro")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e1e")

        self.text = random.choice(texts)
        self.start_time = None
        self.time_limit = 30
        self.running = False

        # Title
        tk.Label(root, text="Typing Speed Test", font=("Arial", 22, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=10)

        # Timer
        self.timer_label = tk.Label(root, text="Time: 30", font=("Arial", 14),
                                   fg="cyan", bg="#1e1e1e")
        self.timer_label.pack()

        # Text to type
        self.label_text = tk.Label(root, text=self.text, wraplength=750,
                                   font=("Arial", 14), fg="white", bg="#1e1e1e")
        self.label_text.pack(pady=10)

        # Input
        self.entry = tk.Text(root, height=5, width=90, font=("Arial", 12),
                             bg="#2d2d2d", fg="white", insertbackground="white")
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.live_update)

        # Stats
        self.stats_label = tk.Label(root, text="WPM: 0 | Accuracy: 0%",
                                    font=("Arial", 14),
                                    fg="lightgreen", bg="#1e1e1e")
        self.stats_label.pack(pady=10)

        # Buttons
        frame = tk.Frame(root, bg="#1e1e1e")
        frame.pack()

        tk.Button(frame, text="Start", command=self.start_test,
                  bg="#4CAF50", fg="white", width=10).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="Restart", command=self.reset_test,
                  bg="#f44336", fg="white", width=10).grid(row=0, column=1, padx=10)

    def start_test(self):
        if not self.running:
            self.running = True
            self.entry.delete("1.0", tk.END)
            self.start_time = time.time()
            self.countdown(self.time_limit)

    def reset_test(self):
        self.running = False
        self.text = random.choice(texts)
        self.label_text.config(text=self.text)
        self.entry.delete("1.0", tk.END)
        self.timer_label.config(text="Time: 30")
        self.stats_label.config(text="WPM: 0 | Accuracy: 0%")

    def countdown(self, time_left):
        if self.running:
            self.timer_label.config(text=f"Time: {time_left}")
            if time_left > 0:
                self.root.after(1000, self.countdown, time_left - 1)
            else:
                self.running = False
                self.calculate_final()

    def live_update(self, event=None):
        if not self.running:
            return

        typed = self.entry.get("1.0", tk.END).strip()
        elapsed = time.time() - self.start_time

        # WPM
        words = len(typed.split())
        wpm = (words / elapsed) * 60 if elapsed > 0 else 0

        # Accuracy
        correct = sum(1 for i in range(min(len(typed), len(self.text)))
                      if typed[i] == self.text[i])
        accuracy = (correct / len(self.text)) * 100

        self.stats_label.config(text=f"WPM: {int(wpm)} | Accuracy: {int(accuracy)}%")

        # Highlight mistakes
        self.entry.tag_remove("wrong", "1.0", tk.END)
        for i in range(len(typed)):
            if i < len(self.text) and typed[i] != self.text[i]:
                self.entry.tag_add("wrong", f"1.{i}", f"1.{i+1}")

        self.entry.tag_config("wrong", foreground="red")

    def calculate_final(self):
        typed = self.entry.get("1.0", tk.END).strip()
        total_time = self.time_limit

        words = len(typed.split())
        wpm = (words / total_time) * 60

        correct = sum(1 for i in range(min(len(typed), len(self.text)))
                      if typed[i] == self.text[i])
        accuracy = (correct / len(self.text)) * 100

        self.stats_label.config(
            text=f"Final WPM: {int(wpm)} | Accuracy: {int(accuracy)}%"
        )


root = tk.Tk()
app = TypingTest(root)
root.mainloop()
