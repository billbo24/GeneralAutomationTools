

#%%

import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import pyautogui
from PIL import Image, ImageTk
import mss

# Call this before launching the canvas window
def get_save_path(path=''):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    if path == '':
        folder = simpledialog.askstring("Folder Path", "Enter the folder path to save the screenshot:")
        if not folder:
            messagebox.showinfo("Cancelled", "No folder entered. Exiting.")
            return None, None
    
    else:
        folder = path

    filename = simpledialog.askstring("Filename", "Enter the filename (without extension):")
    if not filename:
        messagebox.showinfo("Cancelled", "No filename entered. Exiting.")
        return None, None

    save_path = os.path.join(folder, filename + ".png")
    return save_path, root


class SnippingTool:
    def __init__(self,save_path):
        self.save_path = save_path

        # Take a screenshot first
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            self.screenshot = Image.frombytes(
                "RGB", (monitor["width"], monitor["height"]),
                sct.grab(monitor).rgb
            )

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.8)  # Transparent overlay
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)


        self.start_x = None
        self.start_y = None
        self.rect = None


        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # 🔑 Focus and key binding
        self.canvas.focus_set()
        self.root.bind_all("<Escape>", self.on_escape)

        self.root.mainloop()

    def on_escape(self, event=None):
        print("Screenshot cancelled.")
        self.root.destroy()

    def on_mouse_down(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_up(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.root.config(cursor='none')

        self.root.destroy()

        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))

        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        screenshot.save(self.save_path)
        print(f"Screenshot saved as {self.save_path}")



def take_screenshot_and_save(path=''):
    save_path, dialog_root = get_save_path(path)
    if not save_path:
        return None  # or return or skip, depending on your logic

    # Don't forget to destroy the hidden dialog root if you used one
    dialog_root.destroy()

    #instantiate the snipping tool
    tool = SnippingTool(save_path)


    return None

#SnippingTool('C:\\Users\\wfloyd\\OneDrive - The Kleingers Group\\Documents\\GeneralAutomationTools\\UnanetTest')
#take_screenshot_and_save(path='C:\\Users\\wfloyd\\OneDrive - The Kleingers Group\\Documents\\GeneralAutomationTools\\UnanetTest')
# %%


