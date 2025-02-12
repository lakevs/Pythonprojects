import tkinter as tk
from tkinter import colorchooser, simpledialog
from PIL import Image, ImageDraw, ImageTk
from collections import deque

class VirtualWhiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Whiteboard")

        self.canvas = tk.Canvas(root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.history = deque(maxlen=20)  # History for undo functionality

        self.color = "black"
        self.brush_size = 5
        self.eraser_on = False

        self.setup_menu()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.root.bind("<Control-z>", self.undo)

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        brush_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Brush", menu=brush_menu)
        brush_menu.add_command(label="Brush Size", command=self.select_brush_size)
        brush_menu.add_command(label="Brush Color", command=self.select_color)
        brush_menu.add_command(label="Toggle Eraser", command=self.toggle_eraser)

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        paint_color = "white" if self.eraser_on else self.color
        self.canvas.create_oval(x1, y1, x2, y2, fill=paint_color, outline=paint_color)
        self.draw.ellipse([x1, y1, x2, y2], fill=paint_color, outline=paint_color)
        self.history.append(self.image.copy())  # Save current state for undo

    def save_image(self):
        filename = "virtual_whiteboard.png"
        self.image.save(filename)
        print(f"Image saved as {filename}")

    def select_brush_size(self):
        size = simpledialog.askinteger("Brush size", "Enter brush size:", minvalue=1, maxvalue=50)
        if size:
            self.brush_size = size

    def select_color(self):
        color = colorchooser.askcolor(color=self.color)[1]
        if color:
            self.color = color
            self.eraser_on = False  # Ensure eraser is off when selecting a color

    def toggle_eraser(self):
        self.eraser_on = not self.eraser_on

    def undo(self, event=None):
        if self.history:
            self.history.pop()  # Remove the current state
            if self.history:
                self.image = self.history.pop()  # Restore the last state
                self.draw = ImageDraw.Draw(self.image)
                self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualWhiteboard(root)
    root.mainloop()
