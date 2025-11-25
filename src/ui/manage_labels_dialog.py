import customtkinter as ctk
import threading
from tkinter import colorchooser

class ManageLabelsDialog(ctk.CTkToplevel):
    def __init__(self, master, fetcher, project_id):
        super().__init__(master)
        self.fetcher = fetcher
        self.project_id = project_id
        
        self.title("Manage Labels")
        self.geometry("500x600")
        self.transient(master)
        self.after(100, self.grab_set)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create Label Form
        self.create_frame = ctk.CTkFrame(self)
        self.create_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.create_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.create_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Label Name")
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(self.create_frame, text="Color:").grid(row=1, column=0, padx=5, pady=5)
        
        # Color input frame
        self.color_frame = ctk.CTkFrame(self.create_frame, fg_color="transparent")
        self.color_frame.grid(row=1, column=1, sticky="ew")
        self.color_frame.grid_columnconfigure(0, weight=1)
        
        self.color_entry = ctk.CTkEntry(self.color_frame, placeholder_text="#FF0000")
        self.color_entry.grid(row=0, column=0, sticky="ew", padx=(5, 5), pady=5)
        self.color_entry.insert(0, "#428BCA")
        self.color_entry.bind("<KeyRelease>", self.update_preview)
        
        self.pick_btn = ctk.CTkButton(self.color_frame, text="Pick", width=50, command=self.pick_color)
        self.pick_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.preview_label = ctk.CTkLabel(self.create_frame, text="Preview", text_color="white", fg_color="#428BCA", corner_radius=5)
        self.preview_label.grid(row=1, column=2, padx=5, pady=5)
        
        self.create_btn = ctk.CTkButton(self.create_frame, text="Create Label", command=self.create_label)
        self.create_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.close_btn = ctk.CTkButton(self.create_frame, text="Close", fg_color="gray", command=self.destroy)
        self.close_btn.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        # List
        ctk.CTkLabel(self, text="Existing Labels", font=("Roboto", 14, "bold")).grid(row=1, column=0, sticky="w", padx=10)
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        threading.Thread(target=self._fetch_and_display, daemon=True).start()

    def _fetch_and_display(self):
        labels = self.fetcher.fetch_labels(self.project_id)
        self.after(0, lambda: self._display_labels(labels))

    def _display_labels(self, labels):
        for i, label in enumerate(labels):
            frame = ctk.CTkFrame(self.list_frame)
            frame.grid(row=i, column=0, sticky="ew", padx=2, pady=2)
            frame.grid_columnconfigure(0, weight=1)
            
            # Colored indicator
            try:
                lbl = ctk.CTkLabel(frame, text=label.name, text_color="white", fg_color=label.color, corner_radius=5)
            except:
                lbl = ctk.CTkLabel(frame, text=label.name) # Fallback if color invalid
            lbl.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            
            del_btn = ctk.CTkButton(frame, text="Delete", width=60, fg_color="#C42B1C", hover_color="#8E1F14", 
                                  command=lambda l=label: self.delete_label(l))
            del_btn.grid(row=0, column=1, padx=5, pady=5)

    def pick_color(self):
        color = colorchooser.askcolor(title="Choose Label Color")[1]
        if color:
            self.color_entry.delete(0, "end")
            self.color_entry.insert(0, color)
            self.update_preview()

    def update_preview(self, event=None):
        color = self.color_entry.get()
        if len(color) == 7 and color.startswith("#"):
            try:
                self.preview_label.configure(fg_color=color)
            except:
                pass

    def create_label(self):
        name = self.name_entry.get()
        color = self.color_entry.get()
        if not name: return
        
        success, msg = self.fetcher.create_label(self.project_id, name, color)
        if success:
            self.name_entry.delete(0, "end")
            self.refresh_list()
        else:
            print(f"Error creating label: {msg}")

    def delete_label(self, label):
        success, msg = self.fetcher.delete_label(self.project_id, label.name)
        if success:
            self.refresh_list()
        else:
            print(f"Error deleting label: {msg}")
