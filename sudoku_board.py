import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import random

class SudokuGame:
    # Encapsule all function
    def __init__(self, root):
        self.root = root
        self.GRID_SIZE, self.MINI_GRID_SIZE = 9, 3
        self.ANSWERS_GRID = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]  # Store original grid
        self.EDITABLE_GRID = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]  # Track editable states (0 = editable, 1 = read-only)
        self.is_revealed = False
        self.entries = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]  # Store Entry widgets
        self.hint_count , self.max_hint = 0, 0 
        self.font_size, self.button_size, self.progress_bar_size = 6, 1, 300 # Default
        self.progress_percentage = 0
        self.button_pad_y = 3
        self.num_to_remove = 0
        self.grid_gap = 4
        self.primary_color = "light blue"
        self.secondary_color = "light yellow"

    def resize_grid(self):
        # Resize grid based on GRID_SIZE
        self.ANSWERS_GRID = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)] # Reset answers grid
        self.EDITABLE_GRID = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)] 
        self.entries = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]  # Reset Entry widgets
        
    def validate_input(self, char):
    # Allow only numbers 1-16
        if (len(char) <= 2):
            if (char.isdigit() and 1 <= int(char) <= self.GRID_SIZE or char == ""):
                return True  # Also allow clearing the entry
        return False

    def create_grid(self, parent):
    # Create a Sudoku grid with border
        vcmd = (self.root.register(self.validate_input), "%P")  # Register validation function
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                # Alternate colors based on blocks
                entry_color = self.primary_color if (row // self.MINI_GRID_SIZE + col // self.MINI_GRID_SIZE) % 2 == 0 else self.secondary_color
                top_border = self.grid_gap if row % self.MINI_GRID_SIZE == 0 else 1 # Highlight
                left_border = self.grid_gap if col % self.MINI_GRID_SIZE == 0 else 1
                bottom_border = self.grid_gap if row == self.GRID_SIZE - 1 else 1
                right_border = self.grid_gap if col == self.GRID_SIZE - 1 else 1
                border = tk.Frame(parent, highlightbackground="black", highlightthickness=1)
                border.grid(row=row, column=col, padx=(left_border, right_border), pady=(top_border, bottom_border))
                entry = tk.Entry(border, bg=entry_color, width=3, justify="center", font=("Arial", self.font_size + 8), validate="key", validatecommand=vcmd)
                entry.pack(padx=1, pady=1)
                self.entries[row][col] = entry  # Store Entry widget
                for key, direction in [("<Up>", (-1, 0)), ("<Down>", (1, 0)), ("<Left>", (0, -1)), ("<Right>", (0, 1)),
                                    ("<w>", (-1, 0)), ("<s>", (1, 0)), ("<a>", (0, -1)), ("<d>", (0, 1)),
                                    ("<W>", (-1, 0)), ("<S>", (1, 0)), ("<A>", (0, -1)), ("<D>", (0, 1))]:
                                    # Change grid by using keyboard
                    entry.bind(key, lambda _, row=row, col=col, d=direction: self.move_grid(row + d[0], col + d[1])) 

    def recreate_grid(self):
        if (len(self.entries) != self.GRID_SIZE or len(self.entries[0])):
            for widget in self.top_frame.winfo_children():
                widget.destroy() # Clear existing entries
            self.entries = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]  # Reinitialize entries
            self.create_grid(self.top_frame)
        else: 
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    self.entries[row][col].config(state="normal", fg="black")
                    self.entries[row][col].delete(0, tk.END)
    
    def move_grid(self, row, col):
    # Move focus to a specific cell, ensuring the row and column stay within bounds
        if (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            self.entries[row][col].focus_set()

    def check_possible_num(self, num, row, col):
    # Check if the number can be placed in the (row, col) position
        for j in range(self.GRID_SIZE):
            if (self.entries[row][j].get() == str(num) or self.entries[j][col].get() == str(num)):
                return False
        start_row = (row // self.MINI_GRID_SIZE) * self.MINI_GRID_SIZE
        start_col = (col // self.MINI_GRID_SIZE) * self.MINI_GRID_SIZE
        for i in range(self.MINI_GRID_SIZE):
            for j in range(self.MINI_GRID_SIZE):
                if (self.entries[start_row + i][start_col + j].get() == str(num)):
                    return False
        return True 
    
    def is_empty(self, row, col):
    # Check if a given cell is empty
        return self.entries[row][col].get() == ""
    
    def find_empty_spot(self):
    # Find the first empty spot in the grid
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.is_empty(row, col):
                    return (row, col)
        return None  # No empty spots
    
    def fill_grid(self):
    # Recursive function to fill the grid using backtracking
        empty_spot = self.find_empty_spot()
        if not empty_spot:
            return True  # Grid is fully filled
        row, col = empty_spot
        possible_num = list(range(1, self.GRID_SIZE + 1))  # Possible numbers to fill
        random.shuffle(possible_num)  # Shuffle to add randomness
        for num in possible_num:
            if (self.check_possible_num(num, row, col)):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, num)
                self.ANSWERS_GRID[row][col] = num  # Store the number in the answers grid
                if (self.fill_grid()):  # Recursively fill the next spot
                    return True
                # If filling with this number doesn't work, backtrack
                self.entries[row][col].delete(0, tk.END)
                self.ANSWERS_GRID[row][col] = 0  # Clear the answer in case of backtrack
        return False  # Trigger backtracking

    def remove_numbers(self, remove_grid_count, mode): 
    # Remove numbers from grid
        print(f"{remove_grid_count} grids has been removed")
        self.num_to_remove = remove_grid_count # Remove numbers
        if (mode == "randommode"):
            self.max_hint = 3
        if (self.max_hint > 0):    
            self.game_buttons["hint_button"].config(state="normal") 
        self.hint_count = 0
        all_cells = [(i, j) for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE)]
        random.shuffle(all_cells)  # Shuffle to randomly pick cells to clear
        # Remove numbers from a random set of cells
        for i in range(self.num_to_remove):
            row, col = all_cells[i]
            self.entries[row][col].delete(0, tk.END)
        self.lock_initial_numbers()

    def lock_initial_numbers(self):
    # Lock the initially filled numbers and update the editable grid
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.entries[row][col].get() != "":
                    self.entries[row][col].config(state="readonly")  # Lock the entry
                    self.EDITABLE_GRID[row][col] = 1  # Mark as read-only
                else:
                    self.EDITABLE_GRID[row][col] = 0  # Mark as editable   

    def hint(self):
    # Show hint on the random empty grids
        if self.max_hint is not None:
            if (self.hint_count < self.max_hint):
                empty_grids = [(row, col) for row in range(self.GRID_SIZE) for col in range(self.GRID_SIZE) if self.is_empty(row, col)]
                if (empty_grids):
                    row, col = random.choice(empty_grids)
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, self.ANSWERS_GRID[row][col])
                    self.entries[row][col].config(state="readonly")
                    self.EDITABLE_GRID[row][col] = 1
                    self.hint_count += 1
                    self.update_progress()
                if (self.hint_count >= self.max_hint):
                    self.game_buttons["hint_button"].config(state="disabled")
            self.bind_entry_events() 

    def reset_grid(self):
    # Clear the grid for a new game
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                self.entries[row][col].config(state="normal", fg="black")  
                self.entries[row][col].delete(0, tk.END)
                self.ANSWERS_GRID[row][col] = 0
        self.progress_percentage = 0
        self.progress_label.config(text=f"Progress : {self.progress_percentage:.2f}%")
        self.progress_bar["value"] = self.progress_percentage  
        self.game_buttons["reveal_button"].config(text="Reveal", state="disable", command=self.reveal_grid)      
        self.game_buttons["load_button"].config(state="normal")  
        self.game_buttons["appearance"].config(state="normal")

    def is_grid_empty(self):
    # Check if all cells are empty
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.entries[(row, col)].get() != "":
                    return False
        return True

    def check_win(self):
    # Check if the current grid is a valid Sudoku solution
        valid_nums = set(str(i) for i in range(1, self.GRID_SIZE + 1))
        for row in range(self.GRID_SIZE):
            row_nums = set()
            col_nums = set()
            for col in range(self.GRID_SIZE):
                row_val = self.entries[row][col].get()
                col_val = self.entries[col][row].get()  
                if (row_val not in valid_nums or row_val in row_nums): 
                    return False  
                if (col_val not in valid_nums or col_val in col_nums):
                    return False  
                row_nums.add(row_val)
                col_nums.add(col_val)
        # Check 3x3 blocks
        for block_row in range(0, self.GRID_SIZE, self.MINI_GRID_SIZE):
            for block_col in range(0, self.GRID_SIZE, self.MINI_GRID_SIZE):
                block_nums = set()
                for i in range(self.MINI_GRID_SIZE):
                    for j in range(self.MINI_GRID_SIZE):
                        block_val = self.entries[block_row + i][block_col + j].get()
                        if block_val in block_nums or block_val not in valid_nums:
                            return False  # Duplicates in block
                        block_nums.add(block_val)
        return True 

    def check_completion(self):
    # Check if the puzzle is complete and display win message
        if (self.check_win()):
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    self.entries[row][col].config(fg="black")
            messagebox.showinfo("Victory", "You solved the puzzle!")
            self.progress_label.config(text=f"Progress : {100:.2f}%")
            self.game_buttons["reveal_button"].config(text="Clear", command=self.reset_grid)
            self.game_buttons["save_button"].config(state="disabled")
            # Clear grid

    def on_entry_change(self, event):
        # Get the row and column of the entry that triggered the event
        if (self.is_revealed):
            return
        grid_input = event.widget
        is_found = False
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if (self.entries[row][col] == grid_input):
                    is_found = True
                    break
            if (is_found):
                break      
        if (self.ANSWERS_GRID[row][col] != 0 and self.EDITABLE_GRID[row][col] == 0):
            # Check answer on each grid
            pass
            #if (grid_input.get().isdigit()):
                #if (grid_input.get() == str(self.ANSWERS_GRID[row][col])):
                    #grid_input.config(fg="green")  # Correct answer     
                #else:
                    #grid_input.config(fg="red")    # Incorrect answer
            #else:
                #grid_input.config(fg="black")  # Reset color if entry is empty or invalid
        self.update_progress()                   
        self.check_completion()

    def instruction(self): 
        # Show game instruction
        messagebox.showinfo("Instruction","How to play Sudoku\n"
        "1. Fill in the grid so that each row, column, and 3x3 block contains the numbers 1-9.\n"
        "2. You can only place numbers 1-9 in each empty cell\n"
        "3. You cannot edit cells that locked\n"
        "                                  Have fun!                                            ")

    def update_progress(self):
        correct_grids = 0
        total_grids = self.num_to_remove - self.hint_count
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if (self.entries[row][col].get() == str(self.ANSWERS_GRID[row][col]) and self.EDITABLE_GRID[row][col] == 0):
                    correct_grids += 1
        game_progress = correct_grids / total_grids
        if (total_grids > 0):
            progress_percentage = game_progress * 100  
            self.progress_bar["value"] = progress_percentage
        else:
            self.progress_bar["value"] = 100
        self.progress_label.config(text=f"Progress : {progress_percentage:.2f}%")

    def save_game(self): 
    # Save game data
        file_path = filedialog.asksaveasfilename(defaultextension=".dat",
                                                    filetypes=[("Data Files", "*.dat"),
                                                                ("Text Files", "*.txt"),
                                                                ("All Files", "*.*")])
        try:
            if (file_path):
                with open(file_path, "w") as f:
                    f.write(f"Grid Size : {self.GRID_SIZE}\n")
                    f.write(f"Mini Grid Size : {self.MINI_GRID_SIZE}\n")
                    f.write("Saved grid\n")
                    self.save_grid(f)
                    f.write("Editable\n")
                    self.save_editable_state(f)
                    f.write("Answer\n")
                    self.save_answers_grid(f)
                    f.write(f"Hints {self.hint_count}/{self.max_hint}\n")
                    f.write(f"Difficulty : {self.num_to_remove - self.hint_count}")                
                messagebox.showinfo("Save Game", "Game has been saved.")
            else:
                return    
        except Exception as e:
            messagebox.showerror("Save Game", f"An error occurred while saving: {e}")

    def save_grid(self, file):
        # Save progress
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                save_value = self.entries[row][col].get() or "0"
                file.write(save_value + " ")
            file.write("\n")

    def save_editable_state(self, file):
        # Save editable state
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                save_edit = str(self.EDITABLE_GRID[row][col]) 
                file.write(save_edit + " ")
            file.write("\n")    

    def save_answers_grid(self, file):
        # Save answers
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                save_value = str(self.ANSWERS_GRID[row][col])
                file.write(save_value + " ")
            file.write("\n")

    def load_game(self): 
    # Load game data 
        file_path = filedialog.askopenfilename(filetypes=[("Data Files", "*.dat"),
                                                        ("Text Files", "*.txt"), 
                                                        ("All Files", "*.*")])
        try:
            if (file_path):
                # If you confirm to load
                with open(file_path, "r") as f:
                    self.GRID_SIZE = int(f.readline().split(" : ")[1])
                    self.MINI_GRID_SIZE = int(f.readline().split(" : ")[1])# Read grid size
                    self.resize_grid()  # Resize grid based on loaded size
                    self.recreate_grid()  # Recreate grid widgets for new size
                    self.reset_grid()  # Clear the existing grid
                    f.readline()
                    self.load_grid(f)
                    f.readline()
                    self.load_edit_state(f)    
                    f.readline()
                    self.load_answers_grid(f)
                    self.bind_entry_events()
                    self.load_hint(f)
                    self.num_to_remove = int(f.readline().split(" : ")[1])
                    self.load_progress()
                messagebox.showinfo("Load Game", "Game successfully loaded.")
                self.game_buttons["save_button"].config(state="normal")
                self.game_buttons["load_button"].config(state="normal")
                self.game_buttons["reveal_button"].config(state="normal")
                self.game_buttons["appearance"].config(state="disabled")
                if (self.hint_count < self.max_hint):
                    self.game_buttons["hint_button"].config(state="normal") 
            else:
                return        
        except FileNotFoundError:
            messagebox.showwarning("Load Game", "No saved game found.")
        except Exception as e:
            messagebox.showerror("Load Game", f"An error occurred while loading: {e}")

    def load_grid(self, file):
        # Load saved grid
        for row in range(self.GRID_SIZE):
            line = file.readline().strip().split()
            for col in range(self.GRID_SIZE):
                value = line[col]
                self.entries[row][col].delete(0, tk.END) 
                if (value != "0"):
                    self.entries[row][col].insert(0, value)

    def load_edit_state(self, file):
        # Load editable state 
        for row in range(self.GRID_SIZE):
            line = file.readline().strip().split()
            for col in range(self.GRID_SIZE):
                editable_value = int(line[col])
                self.EDITABLE_GRID[row][col] = editable_value
                if (editable_value) == 1:  
                    self.entries[row][col].config(state="readonly")
                else:
                    self.entries[row][col].config(state="normal")

    def load_answers_grid(self, file):
        # Load answers
        for row in range(self.GRID_SIZE):
            line = file.readline().strip().split()
            for col in range(self.GRID_SIZE):
                self.ANSWERS_GRID[row][col] = int(line[col])   

    def load_hint(self, file):
        # Load and update hint and max hints
        hint_line = file.readline().strip().split()
        self.hint_count, self.max_hint = map(int, hint_line[1].split("/"))
        if (self.hint_count >= self.max_hint):
            self.game_buttons["reveal_button"].config(state="disabled")
    def load_progress(self):
        # Load game progress
        self.update_progress()
        
    def show_game_buttons(self, parent): 
    # Game button
        self.game_buttons = {}
        # Create game buttons (New game, Reveal answers, Save game, Load game)
        self.game_buttons['new_game_button'] = tk.Button(parent, text="New game", font=("Arial", self.font_size * 2), command=self.new_game_setting)
        self.game_buttons['reveal_button'] = tk.Button(parent, text="Reveal", font=("Arial", self.font_size * 2), command=self.reveal_grid, state="disabled")
        self.game_buttons['save_button'] = tk.Button(parent, text="Save game", font=("Arial", self.font_size * 2), command=self.save_game, state="disabled")
        self.game_buttons['load_button'] = tk.Button(parent, text="Load game", font=("Arial", self.font_size * 2), command=self.load_game)
        self.game_buttons['hint_button'] = tk.Button(parent, text="Hint", font=("Arial", self.font_size * 2), command=self.hint, state="disabled")
        self.game_buttons['instruction_button'] = tk.Button(parent, text="Instruction", font=("Arial", self.font_size * 2), command=self.instruction)
        self.game_buttons['appearance'] = tk.Button(parent, text="Appearance", font=("Arial", self.font_size * 2), command=self.change_appearence)
        self.game_buttons['exit_button'] = tk.Button(parent, text="Quit game", font=("Arial", self.font_size * 2), command=self.exit_game)
        self.game_buttons['new_game_button'].grid(row=1, column=0, padx=5, pady=10)
        self.game_buttons['load_button'].grid(row=1, column=1, padx=5, pady=10)
        self.game_buttons['save_button'].grid(row=1, column=2, padx=5, pady=10)
        self.game_buttons['hint_button'].grid(row=1, column=3, padx=5, pady=10)
        self.game_buttons['reveal_button'].grid(row=1, column=4, padx=5, pady=10)
        self.game_buttons['instruction_button'].grid(row=2, column=1, padx=5, pady=10)
        self.game_buttons['appearance'].grid(row=2, column=2, padx=5, pady=10)
        self.game_buttons['exit_button'].grid(row=2, column=3, padx=5, pady=10)

    def create_progress_bar(self, parent):
        # Create progress bar
        self.progress_label = tk.Label(parent, text=f"Progress : {self.progress_percentage:.2f}%", font=("Arial", self.font_size + 2))
        self.progress_bar = ttk.Progressbar(parent, orient="horizontal", length=self.progress_bar_size, mode="determinate")
        self.progress_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)    
        self.progress_bar.grid(row=0, column=2, columnspan=3, padx=5, pady=10)

    def reveal_grid(self):
        if (messagebox.askyesno("Reveal", "Are you sure to reveal and end the game?")):
            # Reveal correct answer
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    self.entries[row][col].config(state="normal")  # Make editable
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, self.ANSWERS_GRID[row][col])  # Insert the original number
                    self.entries[row][col].config(state="readonly")
                    self.entries[row][col].config(fg="black")  # Lock after revealing
            self.progress_bar["value"] = 0        
            self.progress_label.config(text=f"Progress : -.--%")
            self.game_buttons["reveal_button"].config(state="disabled") # Disable "Reveal" button
            self.game_buttons["save_button"].config(state="disabled") # Disable "Save game" button  
            self.game_buttons["hint_button"].config(state="disabled") # Disable "Load game" button
            self.is_revealed = True
        else:
            return

    def bind_entry_events(self):
    # Bind key release event to each entry widget to check for completion
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if (not self.entries[row][col].bind("<KeyRelease>")):
                    self.entries[row][col].bind("<KeyRelease>", self.on_entry_change)       

    def random_mode(self):
    # Random mode (Reset grid then generate new Sudoku)
        self.is_revealed = False
        self.resize_grid()
        self.recreate_grid() # Recreate the grid
        self.reset_grid()
        self.fill_grid() 
        # Save the fully solved grid before removing any numbers
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                self.ANSWERS_GRID[row][col] = int(self.entries[row][col].get())  # Save the number in the answers grid
        self.bind_entry_events()
        self.game_buttons["new_game_button"].config(state="normal") 
        self.game_buttons["reveal_button"].config(state="normal")  
        self.game_buttons["save_button"].config(state="normal")
        self.game_buttons["appearance"].config(state="disabled")

    def custom_mode(self):
    # Custom mode (Input a hint and a number of grids to be removed)
        custom_mode_window = tk.Toplevel()
        custom_mode_window.geometry("350x250")
        custom_mode_window.resizable(False, False)
        custom_mode_window.title("Custom Mode")
        custom_mode_window.protocol("WM_DELETE_WINDOW", lambda: [self.close_window(), custom_mode_window.destroy()])
        def entry_check(char):
            if ((char.isdigit() or char == "") and (len(char) <= 3)):
                return True   
            return False
        def get_remove_number():
            try:
                remove_grid_count = int(custom_mode_entry.get())
                self.max_hint = int(hint_entry.get())
                if (0 < remove_grid_count < self.GRID_SIZE * self.GRID_SIZE):
                    if (self.max_hint < remove_grid_count):
                        self.random_mode()
                        self.remove_numbers(remove_grid_count, "custommode")
                        custom_mode_window.destroy()
                    else:
                        messagebox.showwarning("Error", f"Please enter hints lower than {remove_grid_count}")
                else:
                    messagebox.showwarning("Error", f"Please enter the number between 1 and {self.GRID_SIZE * self.GRID_SIZE - 1}")
            except ValueError:
                messagebox.showwarning("Error", "Invaild input!")         
        vcmd = (custom_mode_window.register(entry_check), "%P")        
        custom_mode_label = tk.Label(custom_mode_window, text="Enter a number of grids to be removed ", font=("Arial", self.font_size * 2))
        custom_mode_entry = tk.Entry(custom_mode_window, font=("Arial", self.font_size * 2), width= 4, justify="center" ,validate="key", validatecommand=vcmd)
        hint_label = tk.Label(custom_mode_window, text="Enter a number of hints ", font=("Arial", self.font_size * 2))
        hint_entry = tk.Entry(custom_mode_window, font=("Arial", self.font_size * 2), width= 4, justify="center" ,validate="key", validatecommand=vcmd)
        confirm_button = tk.Button(custom_mode_window, text="Start Game", font=("Arial", self.font_size * 2), command=get_remove_number)
        custom_mode_label.pack(pady=self.button_pad_y * 2)
        custom_mode_entry.pack(pady=self.button_pad_y * 2)
        hint_label.pack(pady=self.button_pad_y * 2)
        hint_entry.pack(pady=self.button_pad_y * 2)
        confirm_button.pack(pady=self.button_pad_y * 2)

    def difficulty_select(self):
        if (self.GRID_SIZE == 4 or self.GRID_SIZE == 9 or self.GRID_SIZE == 16 or self.GRID_SIZE == 25): 
            removed_grid_limit = (self.GRID_SIZE ** 2) - 1 
            easy_mode_range = (removed_grid_limit * (25 / 100), removed_grid_limit * (35 / 100) - 1)
            medium_mode_range = ((easy_mode_range[1] + 1), removed_grid_limit * (45 / 100) - 1)
            hard_mode_range = ((medium_mode_range[1] + 1), removed_grid_limit * (60 / 100) - 1)
            extreme_mode_range = ((hard_mode_range[1] + 1), removed_grid_limit * (80 / 100))
            random_mode_range = (easy_mode_range[0], extreme_mode_range[1])
            difficulty_name = [(f"Easy removes {easy_mode_range} grids.", easy_mode_range),
                               (f"Medium removes {medium_mode_range} grids", medium_mode_range),
                               (f"Hard {hard_mode_range} grids", hard_mode_range),
                               (f"Extreme {extreme_mode_range} grids", extreme_mode_range),
                               (f"Random", random_mode_range)]
        else:
            messagebox.showwarning("Error", "Please select a valid grid size before choosing difficulty.")
            return
        difficulty_select_window = tk.Toplevel()
        difficulty_select_window.geometry("550x450")
        difficulty_select_window.resizable(False, False)
        difficulty_select_window.title("Choose difficulty")
        difficulty_select_window.protocol("WM_DELETE_WINDOW", lambda: [self.close_window(), difficulty_select_window.destroy()])
        difficulty_select_label= tk.Label(difficulty_select_window, text="Choose difficulty", font=("Arial", self.font_size + 8))
        difficulty_select_label.grid(row=0, column=0, columnspan=2, padx=30, pady=20)
        for i, (label, difficulty_range) in enumerate(difficulty_name):
            difficulty_button = tk.Button(difficulty_select_window, text=label, font=("Arial", self.font_size * 2), command=lambda range = difficulty_range:[self.random_mode(),
                                                                                                self.remove_numbers(random.randint(int(range[0]), int(range[1])), "randommode"),
                                                                                                difficulty_select_window.destroy()])
            difficulty_button.grid(row=(1 + i // 2), column=(i % 2), padx=30, pady=10)

    def close_window(self):
        # Rewind New games
        self.game_buttons["new_game_button"].config(state="normal")

    def exit_game(self):
    # Exit game
        is_quit = messagebox.askyesno("Quit", "Are you sure to quit?\nYour game progress will not be saved.")
        if (is_quit):
            self.root.destroy()
        else:
            return

    def new_game_setting(self):
    # Choose to remove random or custom numbers to be removed
        self.game_buttons["new_game_button"].config(state="disabled")
        grid_size_selection = tk.Toplevel()
        grid_size_selection.geometry("350x250")
        grid_size_selection.resizable(False, False)
        grid_size_selection.title("Grid Size Selection")
        grid_size_selection_label = tk.Label(grid_size_selection, text="Choose grid size", font=("Arial", self.font_size + 8))
        grid_size_buttons = [tk.Button(grid_size_selection, text="4x4", font=("Arial", self.font_size * 2), command=lambda:[setattr(self, "GRID_SIZE", 4), setattr(self, "MINI_GRID_SIZE", 2), grid_size_selection.destroy(), mode_selection()]),
                             tk.Button(grid_size_selection, text="9x9", font=("Arial", self.font_size * 2), command=lambda:[setattr(self, "GRID_SIZE", 9), setattr(self, "MINI_GRID_SIZE", 3), grid_size_selection.destroy(), mode_selection()]),
                             tk.Button(grid_size_selection, text="16x16", font=("Arial", self.font_size * 2), command=lambda:[setattr(self, "GRID_SIZE", 16), setattr(self, "MINI_GRID_SIZE", 4), grid_size_selection.destroy(), mode_selection()]),
                             tk.Button(grid_size_selection, text="25x25", font=("Arial", self.font_size * 2), command=lambda:[setattr(self, "GRID_SIZE", 25), setattr(self, "MINI_GRID_SIZE", 5), grid_size_selection.destroy(), mode_selection()])]
        grid_size_selection_label.pack(pady=self.button_pad_y * 2)
        for button in grid_size_buttons:
            button.pack(pady=self.button_pad_y)
        grid_size_selection.protocol("WM_DELETE_WINDOW", lambda: [self.close_window(), grid_size_selection.destroy()])
        def mode_selection():
            grid_size_selection.destroy()
            new_game_setting = tk.Toplevel()
            new_game_setting.geometry("350x250")
            new_game_setting.resizable(False, False)
            new_game_setting.title("New Game")
            mode_selection = tk.Label(new_game_setting, text="Choose mode", font=("Arial", self.font_size + 8))
            random_mode_button = tk.Button(new_game_setting, text="Random", font=("Arial", self.font_size *2), command=lambda:[self.difficulty_select(), new_game_setting.destroy()])
            random_mode_label = tk.Label(new_game_setting, text="Will select difficulty", font=("Arial", self.font_size * 2))
            custom_mode_button = tk.Button(new_game_setting, text="Custom", font=("Arial", self.font_size * 2), command=lambda:[self.custom_mode(), new_game_setting.destroy()])
            custom_mode_label = tk.Label(new_game_setting, text="Will remove a certain number of grids", font=("Arial", self.font_size * 2))
            mode_selection.pack(pady=self.button_pad_y)
            random_mode_button.pack(pady=self.button_pad_y)
            random_mode_label.pack(pady=self.button_pad_y)
            custom_mode_button.pack(pady=self.button_pad_y)
            custom_mode_label.pack(pady=self.button_pad_y)
            new_game_setting.protocol("WM_DELETE_WINDOW", lambda: [new_game_setting.destroy(), self.close_window()])

    def change_appearence(self):
        change_appearence_window = tk.Toplevel()
        change_appearence_window.geometry("500x400")
        change_appearence_window.resizable(False, False)
        change_appearence_window.title("Change Appearance")
        color_label = tk.Label(change_appearence_window, text="Choose Color", font=("Arial", self.font_size * 2))
        colors = ["light blue", "light yellow", "white", "gray", "light green", "light pink"]
        color_listbox = tk.Listbox(change_appearence_window, font=("Arial", self.font_size * 2), selectmode="multiple", height=len(colors))
        for color in colors:
            color_listbox.insert(tk.END, color)
        def apply_colors():
            try:
                color_selection = color_listbox.curselection()
                if (len(color_selection) == 2):
                    self.primary_color = color_listbox.get(color_selection[0])
                    self.secondary_color = color_listbox.get(color_selection[1])
                    self.recreate_grid()
                    change_appearence_window.destroy()
                else:
                    messagebox.showwarning("Selection Error", "Please select both a primary and secondary color.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        color_label.pack(pady=self.button_pad_y)
        color_listbox.pack(pady=self.button_pad_y)
        apply_button = tk.Button(change_appearence_window, text="Apply", font=("Arial", self.font_size * 2), command=apply_colors)
        apply_button.pack(pady=self.button_pad_y)
        change_appearence_window.protocol("WM_DELETE_WINDOW", lambda: [self.close_window(), change_appearence_window.destroy()])

