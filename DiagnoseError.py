import tkinter as tk

class SnippingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.8)
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(self.root, bg="gray", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # 🔑 Focus and key binding
        self.canvas.focus_set()
        self.root.bind_all("<Escape>", self.on_escape)

        self.start_x = None
        self.start_y = None
        self.rect = None

        print("SnippingTool initialized.")
        self.root.mainloop()

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', fill='blue'
        )

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        print("Mouse released.")
        self.root.destroy()

    def on_escape(self, event=None):
        print("Escape pressed — canceling.")
        self.root.destroy()

# Run it directly
if __name__ == "__main__":
    SnippingTool()