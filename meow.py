#!/usr/bin/env python3
"""Do You Love Me? - a playful prank app (tkinter, no dependencies)."""

import random
import tkinter as tk

FONT = "DejaVu Sans"
BG = "#ffe4ec"
PINK = "#e91e63"
DARK = "#880e4f"

REJECTIONS = [
    "Wrong answer. Try again 😤",
    "Nope, that button is broken 🙃",
    "Are you sure? Think harder 🥺",
    "I'll pretend I didn't see that 😌",
    "Come on... you can do better 💔",
    "Still no? Bold of you 😏",
    "This window is persistent, just like my love 💘",
]


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        # Screen scale factor (1.0 = 96 DPI). Used for all sizes and fonts.
        self.s = max(1.0, self.root.winfo_fpixels("1i") / 96)
        self.win = None
        self.attempts = 0
        self.root.bind_all("<Escape>", lambda e: self.quit())
        self.show_love()
        self.root.mainloop()

    # ---------- helpers ----------
    def px(self, n):
        return int(n * self.s)

    def font(self, pt, style=""):
        """Font in pixels, so it always matches the pixel-based layout."""
        return (FONT, -int(pt * 96 / 72 * self.s), style) if style else \
               (FONT, -int(pt * 96 / 72 * self.s))

    def quit(self):
        self.root.destroy()

    def new_window(self, title, bg=BG):
        if self.win is not None:
            self.win.destroy()
        win = tk.Toplevel(self.root)
        win.title(title)
        win.resizable(False, False)
        win.configure(bg=bg)
        self.win = win
        return win

    def show(self, win, jitter=False):
        """Size window to its content, center it, and bring it to front."""
        win.update_idletasks()
        w, h = win.winfo_reqwidth(), win.winfo_reqheight()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        if jitter:
            x += random.randint(-250, 250)
            y += random.randint(-150, 150)
        x = min(max(0, x), max(0, win.winfo_screenwidth() - w))
        y = min(max(0, y), max(0, win.winfo_screenheight() - h))
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.lift()
        win.attributes("-topmost", True)
        win.after(300, lambda: win.attributes("-topmost", False))
        win.focus_force()

    def make_button(self, parent, text, bg, hover):
        return tk.Button(
            parent, text=text, font=self.font(15, "bold"), bg=bg, fg="white",
            activebackground=hover, activeforeground="white",
            relief="flat", bd=0, padx=self.px(22), pady=self.px(8),
            cursor="hand2",
        )

    def build_question(self, win, emoji, question, subtitle):
        wrap = self.px(460)
        tk.Label(win, text=emoji, font=self.font(40), bg=BG).pack(
            padx=self.px(30), pady=(self.px(20), 0))
        tk.Label(win, text=question, font=self.font(22, "bold"), fg=PINK,
                 bg=BG, wraplength=wrap, justify="center").pack(
            padx=self.px(30), pady=(self.px(4), 0))
        tk.Label(win, text=subtitle, font=self.font(12, "italic"), fg=DARK,
                 bg=BG, wraplength=wrap, justify="center").pack(
            padx=self.px(30), pady=(self.px(6), self.px(8)))
        arena = tk.Frame(win, bg=BG, width=self.px(460), height=self.px(110))
        arena.pack(padx=self.px(30), pady=(0, self.px(24)))
        arena.pack_propagate(False)
        return arena

    # ---------- window 1: Do you love me? ----------
    def show_love(self):
        win = self.new_window("A Very Important Question")
        subtitle = ("Be honest... 👀" if self.attempts == 0
                    else REJECTIONS[(self.attempts - 1) % len(REJECTIONS)])
        arena = self.build_question(win, "💘", "Do you love me Niama? ❤️", subtitle)

        yes = self.make_button(arena, "Yes 💖", "#4caf50", "#388e3c")
        no = self.make_button(arena, "No 💔", "#f44336", "#d32f2f")
        yes.place(relx=0.25, rely=0.5, anchor="center")
        no.place(relx=0.75, rely=0.5, anchor="center")

        yes.config(command=self.show_date)
        no.config(command=self.rejected)          # clickable, but rejected
        win.protocol("WM_DELETE_WINDOW", self.rejected)  # X = rejected too
        self.show(win, jitter=self.attempts > 0)

    def rejected(self):
        self.attempts += 1
        self.show_love()  # closes this window, opens a fresh one

    # ---------- window 2: date request ----------
    def show_date(self):
        win = self.new_window("One More Thing...")
        arena = self.build_question(
            win, "🌹", "Will you go on a date with me?", "Say yes. Please. 🥺")

        yes = self.make_button(arena, "Yes 😍", "#4caf50", "#388e3c")
        no = self.make_button(arena, "No 😢", "#f44336", "#d32f2f")
        yes.place(relx=0.25, rely=0.5, anchor="center")
        no.place(relx=0.75, rely=0.5, anchor="center")
        yes.config(command=self.show_thanks)
        win.protocol("WM_DELETE_WINDOW", self.show_date)

        def dodge(event=None):
            win.update_idletasks()
            aw, ah = arena.winfo_width(), arena.winfo_height()
            bw, bh = no.winfo_reqwidth(), no.winfo_reqheight()
            yx, yy = yes.winfo_x(), yes.winfo_y()
            yw, yh = yes.winfo_reqwidth(), yes.winfo_reqheight()
            cx, cy = no.winfo_x(), no.winfo_y()
            x, y = cx, cy
            for _ in range(100):
                x = random.randint(0, max(0, aw - bw))
                y = random.randint(0, max(0, ah - bh))
                overlaps = (x < yx + yw + 10 and x + bw > yx - 10 and
                            y < yy + yh + 10 and y + bh > yy - 10)
                far_enough = abs(x - cx) + abs(y - cy) > self.px(120)
                if far_enough and not overlaps:
                    break
            no.place(relx=0, rely=0, anchor="nw", x=x, y=y)

        no.bind("<Enter>", dodge)
        no.bind("<Button-1>", lambda e: (dodge(), "break")[1])  # never clickable
        no.config(command=dodge)
        self.show(win)

    # ---------- window 3: thanks + falling hearts ----------
    def show_thanks(self):
        win = self.new_window("It's a Date! 💕", bg="#fff0f5")
        win.protocol("WM_DELETE_WINDOW", self.quit)
        w, h = self.px(560), self.px(400)

        canvas = tk.Canvas(win, width=w, height=h, bg="#fff0f5",
                           highlightthickness=0)
        canvas.pack()

        hearts = []
        for _ in range(28):
            item = canvas.create_text(
                random.randint(0, w), random.randint(-h, 0),
                text=random.choice(["❤️", "💕", "💖", "🌹", "✨"]),
                font=self.font(random.randint(12, 24)),
            )
            hearts.append((item, random.uniform(1.5, 4.5) * self.s))

        canvas.create_text(w // 2, int(h * .27), text="🌹", font=self.font(46))
        canvas.create_text(w // 2, int(h * .50), text="Thanks babe!",
                           font=self.font(28, "bold"), fill=PINK)
        canvas.create_text(w // 2, int(h * .64),
                           text="Can't wait for our date! 🌹✨",
                           font=self.font(16), fill=DARK)

        close = self.make_button(canvas, "Close 💋", PINK, "#c2185b")
        close.config(command=self.quit, font=self.font(12, "bold"))
        canvas.create_window(w // 2, int(h * .83), window=close)

        def fall():
            if not canvas.winfo_exists():
                return
            for item, speed in hearts:
                canvas.move(item, 0, speed)
                if canvas.coords(item)[1] > h + 30:
                    canvas.coords(item, random.randint(0, w), -30)
            canvas.after(33, fall)

        fall()
        self.show(win)


if __name__ == "__main__":
    App()
