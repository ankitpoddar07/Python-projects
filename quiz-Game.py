import tkinter as tk
from tkinter import messagebox

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "Who wrote 'Hamlet'?",
        "options": ["Charles Dickens", "Mark Twain", "William Shakespeare", "Jane Austen"],
        "answer": "William Shakespeare"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": "Pacific Ocean"
    },
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(root, text="", font=("Helvetica", 16), wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=("Helvetica", 14), width=20, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        self.next_button = tk.Button(root, text="Next", font=("Helvetica", 14), command=self.next_question, state="disabled")
        self.next_button.pack(pady=10)

        self.load_question()

    def load_question(self):
        question_data = questions[self.current_question]
        self.question_label.config(text=f"Q{self.current_question + 1}: {question_data['question']}")
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, state="normal")
        self.next_button.config(state="disabled")

    def check_answer(self, selected_index):
        question_data = questions[self.current_question]
        selected_option = question_data["options"][selected_index]
        if selected_option == question_data["answer"]:
            self.score += 1
            messagebox.showinfo("Correct!", "✅ That's the right answer!")
        else:
            messagebox.showerror("Wrong!", f"❌ The correct answer was: {question_data['answer']}")
        self.score_label.config(text=f"Score: {self.score}")
        for btn in self.option_buttons:
            btn.config(state="disabled")
        self.next_button.config(state="normal")

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(questions):
            self.load_question()
        else:
            messagebox.showinfo("Quiz Complete", f"🎉 You've completed the quiz! Your final score is {self.score}/{len(questions)}")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()