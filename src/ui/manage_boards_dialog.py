import customtkinter as ctk
import threading

class ManageBoardsDialog(ctk.CTkToplevel):
    def __init__(self, master, fetcher, project_id):
        super().__init__(master)
        self.fetcher = fetcher
        self.project_id = project_id
        
        self.title("Manage Boards")
        self.geometry("400x500")
        self.transient(master)
        self.after(100, self.grab_set)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create Board Form
        self.create_frame = ctk.CTkFrame(self)
        self.create_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.create_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.create_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Board Name")
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        self.create_btn = ctk.CTkButton(self.create_frame, text="Create Board", command=self.create_board)
        self.create_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.close_btn = ctk.CTkButton(self.create_frame, text="Close", fg_color="gray", command=self.destroy)
        self.close_btn.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # List
        ctk.CTkLabel(self, text="Existing Boards", font=("Roboto", 14, "bold")).grid(row=1, column=0, sticky="w", padx=10)
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        threading.Thread(target=self._fetch_and_display, daemon=True).start()

    def _fetch_and_display(self):
        boards = self.fetcher.fetch_boards(self.project_id)
        self.after(0, lambda: self._display_boards(boards))

    def _display_boards(self, boards):
        for i, board in enumerate(boards):
            frame = ctk.CTkFrame(self.list_frame)
            frame.grid(row=i, column=0, sticky="ew", padx=2, pady=2)
            frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(frame, text=board.name).grid(row=0, column=0, sticky="w", padx=5, pady=5)
            
            del_btn = ctk.CTkButton(frame, text="Delete", width=60, fg_color="#C42B1C", hover_color="#8E1F14", 
                                  command=lambda b=board: self.delete_board(b))
            del_btn.grid(row=0, column=1, padx=5, pady=5)

    def create_board(self):
        name = self.name_entry.get()
        if not name: return
        
        success, msg = self.fetcher.create_board(self.project_id, name)
        if success:
            self.name_entry.delete(0, "end")
            self.refresh_list()
        else:
            print(f"Error creating board: {msg}")

    def delete_board(self, board):
        success, msg = self.fetcher.delete_board(self.project_id, board.id)
        if success:
            self.refresh_list()
        else:
            print(f"Error deleting board: {msg}")
