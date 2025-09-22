import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, Text, Button
import threading
import time
import json
import os
import unicodedata
import difflib

DATA_FILE = "answers.json"

default_answers = {
    "đơn đồ thị vô hướng": "Đơn đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là tập các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là các cạnh.",
    "đa đồ thị vô hướng": "Đa đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là họ các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là tập các cạnh. e1 ∈ E, e2 ∈ E được gọi là cạnh bội nếu chúng cùng tương ứng với một cặp đỉnh.",
    "giả đồ thị vô hướng": "Giả đồ thị vô hướng G=<V,E> bao gồm V là tập đỉnh, E là họ các cặp không có thứ tự gồm hai phần tử (hai phần tử không nhất thiết phải khác nhau) trong V được gọi là các cạnh. Cạnh e được gọi là khuyên nếu có dạng e = (u,u).",
    "đơn đồ thị có hướng": "Đơn đồ thị có hướng G=<V,E> bao gồm V là tập các đỉnh, E là tập các cặp có thứ tự gồm hai phần tử của V gọi là các cung.",
    "đa đồ thị có hướng": "Đa đồ thị có hướng G=<V,E> bao gồm V là tập đỉnh, E là họ các cặp có thứ tự gồm hai phần tử khác nhau của V được gọi là các cung. Hai cung e1, e2 tương ứng với cùng một cặp đỉnh được gọi là cung lặp.",
    "đồ thị vô hướng": "Đơn đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là tập các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là các cạnh.",
    "đồ thị có hướng": "Đa đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là họ các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là tập các cạnh. e1 ∈ E, e2 ∈ E được gọi là cạnh bội nếu chúng cùng tương ứng với một cặp đỉnh.",
    "Bậc của đỉnh":"VHai đỉnh 𝑢 và 𝑣 của đồ thị vô hướng 𝐺 = <𝑉,𝐸 > được gọi là kề nhau nếu (𝑢,𝑣)là cạnh thuộc đồ thị 𝐺. Nếu 𝑒 = (𝑢,𝑣)là cạnh của đồ thị 𝐺 thì ta nói cạnh này liên thuộc với hai đỉnh 𝑢 và 𝑣, hoặc ta nói cạnh 𝑒 nối đỉnh 𝑢 với đỉnh 𝑣, đồng thời các đỉnh 𝑢 và 𝑣 sẽ được gọi là đỉnh đầu của cạnh (𝑢,𝑣).",
    "Định lý về tổng bậc các đỉnh":"Giả sử 𝐺 =< 𝑉,𝐸 > là đồ thị vô hướng với 𝑚cạnh, khi đó: Tổng deg𝑣 =2𝑚.",
    "Đường đi":" Đường đi độ dài 𝑛 từ đỉnh 𝑢 đến đỉnh 𝑣 trên đồ thị vô hướng 𝐺 =< 𝑉,𝐸 >là dãy x0, 𝑥1,.. . , 𝑥𝑛−1,𝑥𝑛, trong đó 𝑛 là số nguyên dương, 𝑥0 = 𝑢, 𝑥𝑛 = 𝑣,(𝑥𝑖,𝑥𝑖+1) ∈ 𝐸, 𝑖 = 0,1,2,...,𝑛 − 1.",
    "chu trình":" Đường đi có đỉnh đầu trùng với đỉnh cuối (𝑢 = 𝑣) ",
    "Liên thông":"Đồ thị vô hướng được gọi là liên thông  nếu luôn tìm được đường đi giữa hai đỉnh bất kỳ của nó",
    "Cạnh Cầu":" Cạnh 𝑒 ∈ 𝐸 được gọi là cầu nếu loại bỏ e làm tăng thành phần liên thông của đồ thị. Đỉnh 𝑢 ∈ 𝑉 được gọi là đỉnh trụ nếu loại bỏ 𝑢 cùng với các cạnh nối với 𝑢 làm tăng thành phần liên thông của đồ thị.",
    "Đỉnh trụ":" Là đỉnh trụ nếu loại bỏ 𝑢 cùng với các cạnh nối với 𝑢 làm tăng thành phần liên thông của đồ thị.",
    "Bán bậc của đỉnh":"Nếu 𝑒 =(𝑢,𝑣) là cung của đồ thị có hướng 𝐺 thì ta nói hai đỉnh 𝑢 và 𝑣 là kề nhau, và nói cung (𝑢,𝑣) nối đỉnh 𝑢 với đỉnh 𝑣, hoặc nói cung này đi ra khỏi đỉnh 𝑢 và đi vào đỉnh 𝑣. Đỉnh 𝑢 được gọi là đỉnh đầu, đỉnh 𝑣 được gọi là đỉnh cuối của cung (𝑢,𝑣).",
    " bán bậc ra":"Số cung của đồ thị đi ra khỏi 𝑣 và ký hiệu là 𝑑𝑒𝑔+(𝑣).",
    " bán bậc vào ":"là số cung của đồ thị đi vào 𝑣 và ký hiệu là 𝑑𝑒𝑔−(𝑣).",
    "liên thông mạnh":" nếu giữa hai đỉnh bất kỳ 𝑢 ∈ 𝑉,𝑣 ∈ 𝑉 đều  có đường đi từ 𝑢 đến 𝑣. ",
    "liên thông yếu":"nếu đồ thị vô hướng tương ứng với nó là liên thông.",
    "Định chiều được":" nếu ta có thể biến đổi các cạnh trong 𝐺 thành các cung tương ứng để nhận được một đồ thị có hướng liên thông mạnh. ",
    " Đồ thị đầy đủ":" 𝑛 đỉnh, ký hiệu là 𝐾𝑛, là đơn đồ thị vô  hướng mà giữa hai đỉnh bất kỳ của nó đều có cạnh nối",
    "Đồ thị vòng":"𝑛 đỉnh, ký hiệu là 𝐶𝑛 (𝑛 ≥ 3) là đơn đồ thị  vô hướng gồm các cạnh (1,2),(2,3),…,(𝑛 − 1,𝑛),(𝑛,1)",
    " Đồ thị bánh xe":"𝑛 đỉnh, ký hiệu là 𝑊𝑛 là đồ thị thu được bằng cách bổ sung một đỉnh nối với tất cả các đỉnh của đồ thị vòng 𝐶𝑛−1.",
    "Đồ thị hai phía":"tập đỉnh 𝑉 của nó có thể phân hoạch thành hai tập 𝑋 và 𝑌 sao cho mỗi cạnh của đồ thị chỉ có dạng (𝑥,𝑦), trong đó x ∈ 𝑋 và 𝑦 ∈ 𝑌."
}

# Load dữ liệu từ file hoặc tạo mớ,
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        custom_answers = json.load(f)
else:
    custom_answers = default_answers.copy()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_answers, f, ensure_ascii=False, indent=2)

# Biến toàn cục
training_mode = False
pending_question = ""
history = []
dark_mode = False
BG_COLOR = "#ffffff"
USER_COLOR = "#A3D8F4"
BOT_COLOR = "#FDE2E4"


# ------------------- Hàm lưu dữ liệu -------------------
def save_answers():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_answers, f, ensure_ascii=False, indent=2)


# ------------------- Cập nhật màu -------------------
def update_colors():
    global BG_COLOR, USER_COLOR, BOT_COLOR
    if dark_mode:
        BG_COLOR = "#2E2E2E"
        USER_COLOR = "#4A90E2"
        BOT_COLOR = "#FF6F61"
    else:
        BG_COLOR = "#ffffff"
        USER_COLOR = "#A3D8F4"
        BOT_COLOR = "#FDE2E4"
    root.configure(bg=BG_COLOR)
    chat_canvas.configure(bg=BG_COLOR)
    chat_frame.configure(bg=BG_COLOR)


# ------------------- Hiển thị tin nhắn -------------------
def add_message(msg, sender="bot"):
    bubble = Frame(chat_frame, bg=BG_COLOR)
    avatar = tk.Label(bubble, text="🤖" if sender == "bot" else "🧑", font=("Arial", 14), bg=BG_COLOR)
    avatar.pack(side="left" if sender == "bot" else "right", padx=5)
    color = BOT_COLOR if sender == "bot" else USER_COLOR
    lbl = tk.Label(
        bubble, text=msg, bg=color, fg="black",
        padx=12, pady=8, wraplength=400,
        font=("Segoe UI", 11), justify="left", bd=0, relief="flat"
    )
    lbl.pack(side="left" if sender == "bot" else "right", padx=5)
    bubble.pack(anchor="w" if sender == "bot" else "e", fill="x", pady=3, padx=10)
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)
    history.append(f"{'Bot' if sender == 'bot' else 'Bạn'}: {msg}")


# ------------------- Animation bot gõ -------------------
def bot_typing_animation(reply):
    bubble = Frame(chat_frame, bg=BG_COLOR)
    avatar = tk.Label(bubble, text="🤖", font=("Arial", 14), bg=BG_COLOR)
    avatar.pack(side="left", padx=5)
    lbl = tk.Label(
        bubble, text="", bg=BOT_COLOR, fg="black",
        padx=12, pady=8, wraplength=400,
        font=("Segoe UI", 11), justify="left", bd=0, relief="flat"
    )
    lbl.pack(side="left", padx=5)
    bubble.pack(anchor="w", fill="x", pady=3, padx=10)
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)
    displayed = ""
    for char in reply:
        displayed += char
        lbl.config(text=displayed)
        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1.0)
        time.sleep(0.02)


# ------------------- Chuẩn hóa text -------------------
def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


def normalize_text(text):
    text = remove_accents(text.lower())
    text = ' '.join(text.split())
    return text


# ------------------- Bot trả lời -------------------
def bot_reply(user_input):
    global training_mode, pending_question
    norm_input = normalize_text(user_input)
    found = False
    best_match = None
    highest_ratio = 0
    for k, v in custom_answers.items():
        norm_key = normalize_text(k)
        ratio = difflib.SequenceMatcher(None, norm_input, norm_key).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = v
    if highest_ratio > 0.6:
        bot_typing_animation(best_match)
        found = True
    if not found:
        training_mode = True
        pending_question = user_input.strip()
        bot_typing_animation(
            f"❓ Mình chưa biết trả lời thế nào cho '{user_input}'. Hãy nhập câu trả lời để mình học nhé!")


# ------------------- Gửi tin nhắn -------------------
def send_message(event=None):
    global training_mode, pending_question
    user_input = entry.get("1.0", tk.END).strip()
    if not user_input:
        return
    add_message(user_input, sender="user")
    entry.delete("1.0", tk.END)

    if training_mode:
        # Người dùng nhập câu trả lời cho câu hỏi chưa biết
        custom_answers[pending_question] = user_input
        save_answers()
        add_message("✅ Cảm ơn bạn! Mình đã học xong câu trả lời mới.", sender="bot")
        training_mode = False
        pending_question = ""
    else:
        threading.Thread(target=bot_reply, args=(user_input,), daemon=True).start()


# ------------------- Nhấn Enter -------------------
def on_enter(event):
    if event.state & 0x0001:
        return
    send_message()
    return "break"


# ------------------- Chế độ Dark/Light -------------------
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    update_colors()


# ------------------- Reset training -------------------
def reset_training():
    global custom_answers
    custom_answers = default_answers.copy()
    save_answers()
    add_message("♻️ Mình đã reset toàn bộ câu trả lời đã học, trở về trạng thái ban đầu.", sender="bot")


# ------------------- GUI -------------------
root = tk.Tk()
root.title("🤖 Chatbot Toán Rời Rạc 2")
root.geometry("650x700")
root.configure(bg=BG_COLOR)

chat_canvas = Canvas(root, bg=BG_COLOR, highlightthickness=0)
scrollbar = Scrollbar(root, orient="vertical", command=chat_canvas.yview)
chat_frame = Frame(chat_canvas, bg=BG_COLOR)

chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=scrollbar.set)

chat_canvas.pack(side="top", fill="both", expand=True, padx=5, pady=5)
scrollbar.pack(side="right", fill="y")

entry = Text(root, font=("Segoe UI", 12), height=3, wrap="word")
entry.pack(side="top", fill="x", padx=10, pady=(0, 5), ipady=5)

send_button = Button(root, text="Gửi", command=send_message,
                     bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), padx=20, pady=5)
send_button.pack(side="top", pady=(0, 5))

dark_button = Button(root, text="🌙/☀️", command=toggle_dark_mode,
                     bg="#555555", fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=3)
dark_button.place(x=10, y=650)

reset_button = Button(root, text="Reset Training", command=reset_training,
                      bg="#FF5722", fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=3)
reset_button.place(x=90, y=650)

entry.bind("<Return>", on_enter)

add_message("Chào bạn 👋! Mình là Chatbot – trợ lý thông minh giúp bạn học Toán Rời Rạc.", sender="bot")

root.mainloop()
