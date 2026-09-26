import tkinter as tk # Import the Tkinter library for the GUI
from tkinter import messagebox # Import the messagebox module from Tkinter, which provides predefined dialog boxes for displaying messages to the user.
import random # Import the random library for generating random values


# Define the red numbers on the roulette wheel as a set
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


# Initialize game dictionaries and variables
balances = {} # Initialize an empty dictionary that will store the players' balances
bets = {} # Initialize an empty dictionary that will store the current bets of each player
history = [] # Initialize an empty list that will store the history of roulette results
bot_labels = {}  # Initialize an empty dictionary that will contain GUI labels for displaying bot bets
balance_labels = {} # Initialize an empty dictionary that will contain GUI labels for displaying players' balances
results_labels = {} # Initialize an empty dictionary that will contain GUI labels for displaying each player's winnings or losses after every round

auto_play = None # Initialize the global variable as None; it will later become a BooleanVar (Tkinter variable)
                # used to connect to a checkbox that controls whether the game runs automatically

roulette_result_label = None # Initialize the global variable as None; it will later be used for the
                             # Label widget where the result of each roulette round will be displayed.

history_label = None # Initialize the global variable as None; it will later be used
                     # for the Label widget that displays the last 15 roulette results.

bet_type = None # Initialize the global variable as None; it will later become a Tkinter StringVar()
                # connected to the betting type selection buttons.
                # It is used to store the type of bet selected by the user (e.g. "color", "number", or "dozen").


value_menu = None # Initialize the global variable as None; it will later become a Tkinter OptionMenu widget
                  # that allows the user to select a value from a dropdown list, such as a color (red/black),
                  # a number (0-36), or a dozen (1-12, 13-24, 25-36) for the bet.

bet_value = None # Initialize the global variable as None; it will later become a Tkinter StringVar()
                 # connected to the OptionMenu.
                 # It is used to store the specific value selected by the user for the bet
                 # (e.g. "Red", "32", or "2nd Dozen (13-24)").

bet_amount = None # Initialize the global variable as None; it will later become a Tkinter StringVar()
                  # connected to the OptionMenu.
                  # It is used to store the amount that the user bets in each roulette round.


# Function for resetting and initializing the game
def reset_game():
    global balances, bets # Use global variables
    balances = {"Player": 300, "Bot 1": 300, "Bot 2": 300, "Bot 3": 300} # Set the initial balance for each player and bot
    bets.clear() # Clear the dictionary containing players and bets
    for player in balances:
        bets[player] = []  # Create an empty list of bets for each player
    history.clear() # Clear the results history list
    update_display() # Call the function that updates the GUI labels displaying the players' balances.
    update_result("") # Call the function that clears the roulette result at the beginning of a new game with an empty string
    update_history() # Call the function that clears the history
    reset_bots_display() # Call the function that clears the display of bot bets
    update_bet_options() # Call the function that synchronizes the OptionMenu contents with the current bet type
    reset_results_display() # Call the function that clears the results of each player at the beginning of a new game
    spin_button.config(state="normal", bg="#1e90ff")  # Enable the Spin Roulette button


# Function for updating the roulette result label in the GUI
def update_result(text):
    roulette_result_label.config(text=text)  # Display the roulette spin result


# Function for updating the history label
def update_history():
    # Unlock the Text widget so that it can be modified
    history_label.config(state="normal")
    history_label.delete("1.0", "end")  # Clear the contents of the Text widget

    # Get the last 15 results from the history in reverse order
    for result in reversed(history[-15:]): # Iterate through the last 15 results, from the most recent to the oldest
        parts = result.split(" ")  # Split the result string into a list of words using spaces
        number = parts[0] # Keep only the number to add it to the history
        
        if len(parts) > 1:  # Check whether the list contains more than one element
            color_text = parts[1].strip("()") # Store the color of the number; remove the parentheses from the second element
                                             # so that, for example, "(Red)" becomes "Red".
        else:
            color_text = "Black"  # Otherwise, assign "Black" to the variable
            
        # Select the text formatting color using the following check
        if color_text == "Κόκκινο":
            color = "red"
        elif color_text == "Πράσινο":
            color = "green"
        else:
            color = "black"

        # Define the tags used by the history_label Text widget
        # so that the numbers are displayed using their corresponding colors
        history_label.tag_config("red", foreground="red") # The foreground option defines the text color
        history_label.tag_config("green", foreground="green")
        history_label.tag_config("black", foreground="black")
    
        # Add the result to the widget using the corresponding color
        history_label.insert("end", f"{number}  ", (color,)) # Insert the number at the end of the widget and apply the color tag.
                                                            # The comma after color makes it a tuple instead of a string.
        
    
    # Lock the widget again so that it cannot be edited
    history_label.config(state="disabled")


# Function for updating the displayed balances of all players
def update_display():
    for player in balance_labels:  # Iterate through the balance_labels dictionary containing the GUI labels that display players' balances
        if player in balances: # Check whether the player has a balance in the balances dictionary and is therefore active in the game
            balance_labels[player].config(text=f"{balances[player]}€")  # Update the player's balance from the balances dictionary
        else:
            balance_labels[player].config(text="Out of game") # If the player is no longer in the balances dictionary, display "Out of game"


# Function for clearing the displayed bot bets
def reset_bots_display():
    for bot in bot_labels: # Iterate through the bot_labels dictionary containing the GUI labels used to display bot bets
        if bot in balances: # Check whether the bot has a balance and is therefore active in the game
            bot_labels[bot].config(text=f"{bot}: -") # Display "-" until the next bet is placed
        else:
            bot_labels[bot].config(text=f"{bot}: Out of game") # If the bot no longer has a balance, display "Out of game"


# Function for clearing the displayed winnings/losses when starting or resetting a game
def reset_results_display():
    for player in results_labels: # Iterate through the results_labels dictionary containing the labels for players' winnings/losses
        results_labels[player].config(text=f"{player}: -") # Display "-" for each player to clear the previous results


# Function for updating the user's betting options
def update_bet_options(*args): # *args means that the function can receive any number of arguments because it is connected to a Tkinter trace,
                              # which automatically passes arguments when the bet_type value changes
    options = {
        "color": ["Κόκκινο", "Μαύρο"],
        "number": list(range(37)),
        "dozen": ["1η 12άδα (1-12)", "2η 12άδα (13-24)", "3η 12άδα (25-36)"]
    }[bet_type.get()] # Return the current option based on the selected bet type connected to the selection buttons
    bet_value.set(options[0]) # Set the default value of bet_value to the first option of the selected category
    value_menu['menu'].delete(0, 'end') # The value_menu['menu'] refers to the OptionMenu's menu; clear it before adding the new options

    
    for option in options:   # Iterate through the options
        value_menu['menu'].add_command(label=option, command=tk._setit(bet_value, option)) # Add a new command to the dropdown menu for each option.
                                                                                           # The command is an internal Tkinter function that updates the StringVar
                                                                                           # bet_value with the selected option


# Function for displaying bot bets
def show_bot_bets():
    for bot in ["Bot 1", "Bot 2", "Bot 3"]: # Iterate through the list of bots
        if bot not in balances or balances[bot] <= 0: # Check whether the bot is not in balances or has a balance of 0 or less
            bot_labels[bot].config(text=f"{bot}: Out of game") # Display "Out of game" if the above condition is true
            continue # Skip this bot and move to the next one

        bet_type_bot = random.choice(["color", "number", "dozen"]) # Randomly select a betting type from the available options
        amount = 5 if bet_type_bot == "number" else random.choice([5, 10, 20]) # Bet 5 for a number bet; otherwise randomly select 5, 10, or 20
        amount = min(amount, balances[bot]) # Ensure that the selected amount does not exceed the bot's available balance

        if amount == 0:  # Check whether the betting amount is 0
            bot_labels[bot].config(text=f"{bot}: Not enough money to bet") # Update the bot label with a message indicating insufficient funds
            continue # Skip this bot and move to the next one

        # Select a betting value based on the randomly selected betting type
        if bet_type_bot == "color":
            value = random.choice(["Κόκκινο", "Μαύρο"])
        elif bet_type_bot == "dozen":
            value = random.choice(["1η 12άδα (1-12)", "2η 12άδα (13-24)", "3η 12άδα (25-36)"])
        else:
            value = random.randint(0, 36)

        balances[bot] -= amount # Subtract the bet amount from the bot's balance for the current round

        bets[bot].append({"type": bet_type_bot, "value": value, "amount": amount}) # Add a dictionary containing the bot's random betting choices
        bot_labels[bot].config(text=f"{bot}: {amount}€ στο/η {value} ({bet_type_bot})") # Update the bot label with the bet amount and selected value
        
    
# Function for placing the player's bet and starting a round
def place_bet():
    if "Player" in balances: # Check whether "Player" exists in the balances dictionary
        amount = int(bet_amount.get()) # Convert the amount selected by the player from bet_amount into an integer
        if amount > balances["Player"]: # Check whether the selected amount is available in the player's balance
            tk.messagebox.showerror("Σφάλμα", "Δεν έχετε αρκετά χρήματα για το ποντάρισμα σας!") # Display a pop-up error message indicating insufficient funds
            return # Terminate the function

        balances["Player"] -= amount # Subtract the bet amount from the player's available balance

        bets["Player"].append({"type": bet_type.get(), "value": bet_value.get(), "amount": amount}) # Add the player's bet information to the bets dictionary

    show_bot_bets() # Function that displays the bots' bets
    spin_roulette() # Function that starts the roulette spin
    update_display() # Function that updates the players' balances or indicates that they are out of the game


    
# Function for starting the roulette spin
def spin_roulette():
        
    number = random.randint(0, 36) # Assign a randomly selected number from 0 to 36 to the variable
    # Determine the color of the roulette number according to the randomly generated number
    color = "Κόκκινο" if number in RED_NUMBERS else "Μαύρο" if number != 0 else "Πράσινο"

    # Determine the dozen corresponding to the roulette number
    if 1 <= number <= 12: # 1-12
        dozen = "1η 12άδα (1-12)"
    elif 13 <= number <= 24: # 13-24
        dozen = "2η 12άδα (13-24)"
    elif 25 <= number <= 36: # 25-36
        dozen = "3η 12άδα (25-36)"
    else:
        dozen = None # If the roulette result is 0, dozen is set to None because 0 does not belong to any dozen

    result_text = f" {number} ({color})" # Create a string containing the number and its color
    if dozen: # Check whether the dozen variable contains a value
        result_text += f" - {dozen}" # If so, append the corresponding dozen to the result string
    update_result(result_text) # Call the function with result_text as the argument to display the roulette result

    history.append(f"{number} ({color})") # Add the result to the history list
    update_history() # Call the function to display the result in the history
    calculate_winnings(number, color, dozen) # Call the function to calculate the players' winnings
    update_display() # Call the function to display the players' balances or indicate that they are out of the game

    for player in bets: # Iterate through the bets dictionary
        bets[player] = [] # Clear the previous bets so that the next round can receive new bets
        
    # Check whether auto-play is enabled, more than one player remains in the game,
    # and the human player has been eliminated from the balances dictionary
    if auto_play.get() and len(balances) > 1 and "Player" not in balances: 
                                                                             
        root.after(2000, place_bet) # The root.after method calls place_bet after 2000 ms so that the bots can continue playing automatically


        
# Function for calculating winnings
def calculate_winnings(number, color, dozen):
    losers = [] # Create an empty list
    for player in list(balances): # Iterate through a copy of the list of keys in the balances dictionary
        total = 0  # Initialize the variable that stores the player's total winnings

        # Check whether the player has placed a bet
        if bets.get(player):
            bet_total = bets[player][0]["amount"] # Store the bet amount from the player's first bet
        else:
            bet_total = 0 # Set the bet amount to 0 if the player has no bet

        for bet in bets.get(player, []): # Iterate through the player's list of bets; return an empty list if there are no bets
            if bet["type"] == "number" and int(bet["value"]) == number: # Check whether the bet type is number and the selected number matches the roulette result
                total += bet["amount"] * 36 # Add the bet amount multiplied by 36 to total
            elif bet["type"] == "color" and bet["value"] == color: # Check whether the bet type is color and the selected color matches the roulette result
                total += bet["amount"] * 2 # Add the bet amount multiplied by 2 to total
            elif bet["type"] == "dozen" and bet["value"] == dozen: # Check whether the bet type is dozen and the selected dozen matches the roulette result
                total += bet["amount"] * 3 # Add the bet amount multiplied by 3 to total

        balances[player] += total # Add the winnings to the player's balance, if there are any

        if total > 0: # Check whether total winnings are greater than 0
            results_labels[player].config(text=f"{player}: κέρδισε {total}€", fg="green") # Update the player's result label with the amount won in green
        else:
            results_labels[player].config(text=f"{player}: έχασε {bet_total}€", fg="red") # Update the player's result label with the lost bet amount in red

        if balances[player] <= 0: # Check whether the player's balance is less than or equal to 0
            losers.append(player) # Add the player to the losers list
            if player == "Player": # Check whether the eliminated player is the human Player
                spin_button.config(state="disabled", bg="gray")  # Disable the Spin Roulette button


    for player in losers: # Iterate through the losers list
        results_labels[player].config(text=f"{player}: Εκτός παιχνιδιού!") # Update the result label to indicate that the player is out of the game
        del balances[player] # Remove the player from the balances dictionary

    
    if len(balances) == 1: # Check whether only one player remains in the balances dictionary
        winner = list(balances.keys())[0] # Convert the keys of balances to a list and retrieve the first (and only) value
        results_labels[winner].config(text=f"{winner}: Νικητής!") # Update the result label corresponding to the winner
        tk.messagebox.showinfo("Νικητής!", f"Ο {winner} είναι ο νικητής του παιχνιδιού!!!") # Display a pop-up announcing the winner
        spin_button.config(state="disabled", bg="gray")  # Disable the Spin Roulette button to prevent further spins

        root.quit()  # Terminate the game


# --- GUI Setup ---
root = tk.Tk() # Create the main application window
root.title("Project 55 (e-Roulette)") # Set the title displayed in the title bar
root.geometry("1200x1200") # Set the window size (width x height)
root.configure(bg="#2e2e2e") # Set a dark gray background for the entire window


# --- TOP FRAME ---
top_frame = tk.Frame(root, bg="#2e2e2e") # Create a frame at the top of the window
top_frame.pack(fill="x", pady=(5, 5)) # Place the frame horizontally across the window with 5-pixel vertical padding
tk.Button(top_frame, text="Επαναφορά Παιχνιδιού", command=reset_game, bg="#4e4e4e", fg="white").pack(side="right", padx=10) # Add a reset button that calls reset_game and is positioned on the right


# --- Bet Frame ---
bet_header = tk.Label(root, text="Ποντάρισμα", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white") # Display the "Bet" heading using bold, centered text
bet_header.pack(pady=(10, 5))

bet_frame = tk.LabelFrame(root, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white") # Create a frame for the betting controls with padding and a border
bet_frame.pack(padx=50, pady=(0, 10), fill="x")

bet_inner_frame = tk.Frame(bet_frame, bg="#3e3e3e") # Create an inner frame for better organization of the betting controls
bet_inner_frame.pack(expand=True)


# Variable for selecting the bet type (connected to the betting buttons)
bet_type = tk.StringVar(value="color") # Variable that stores the selected bet type ("color", "number", or "dozen").


# --- Bet type selection buttons (tk.Button, functioning as toggles through select_bet_type) ---
bet_buttons = {} # Dictionary used to store the betting buttons so that their appearance can be changed according to the selection


# Function that activates the selected button and deactivates the others
def select_bet_type(selected_type):
    # Change the bet_type variable
    bet_type.set(selected_type)
    # Update the displayed options
    update_bet_options()

    # Visually activate only the selected button (blue), while the others remain gray
    for bet, button in bet_buttons.items():
        if bet == selected_type:
            button.config(bg="#1e90ff", fg="white")  # Blue background, white text
        else:
            button.config(bg="#3e3e3e", fg="white")  # Gray background, white text


# Create the betting type selection buttons
bet_buttons["color"] = tk.Button(bet_inner_frame, text="Χρώμα", width=12, font=("Arial", 14, "bold"),
                                 command=lambda: select_bet_type("color"), bg="#1e90ff", fg="white")
bet_buttons["color"].grid(row=0, column=0, padx=10, pady=5) # Place the button in the grid layout, similarly to the number and dozen buttons

bet_buttons["number"] = tk.Button(bet_inner_frame, text="Αριθμός", width=12, font=("Arial", 14, "bold"),
                                   command=lambda: select_bet_type("number"), bg="#3e3e3e", fg="white")
bet_buttons["number"].grid(row=0, column=1, padx=10, pady=5)

bet_buttons["dozen"] = tk.Button(bet_inner_frame, text="12άδα", width=12, font=("Arial", 14, "bold"),
                                  command=lambda: select_bet_type("dozen"), bg="#3e3e3e", fg="white")
bet_buttons["dozen"].grid(row=0, column=2, padx=10, pady=5)


# OptionMenu value
bet_value = tk.StringVar() # Variable that stores the selected bet value (e.g. "Red", "Black", a number, or a dozen)
value_menu = tk.OptionMenu(bet_inner_frame, bet_value, "Κόκκινο", "Μαύρο") # Create the default color selection menu. The list changes according to bet_type through update_bet_options()
value_menu.config(bg="#3e3e3e", fg="white", font=("Arial", 12), width=15) # Format the OptionMenu
value_menu["menu"].config(bg="#3e3e3e", fg="white") # Format the dropdown menu
value_menu.grid(row=1, column=0, columnspan=3, pady=10) # Place the OptionMenu in the grid layout


# Amount selector
tk.Label(bet_inner_frame, text="ΠΟΣΟ:", bg="#3e3e3e", fg="white", font=("Arial", 12, "bold")).grid(row=2, column=0, pady=5) # Label for the betting amount
bet_amount = tk.StringVar(value="1") # Variable for storing the betting amount; default value is 1
# Create a dropdown menu with amounts from 1 to 20
amount_menu = tk.OptionMenu(bet_inner_frame, bet_amount, *[str(i) for i in range(1, 21)])
amount_menu.config(bg="#3e3e3e", fg="white", font=("Arial", 12), width=8) # Format the betting amount OptionMenu
amount_menu["menu"].config(bg="#3e3e3e", fg="white")
amount_menu.grid(row=2, column=1, pady=5)


# button_frame (used with sticky="ew" so that it can stretch horizontally)
button_frame = tk.Frame(bet_inner_frame, bg="#3e3e3e") # Create an inner frame for grouping the Spin and Auto Play buttons
button_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")


# Spin button
# The main "Spin" button, which calls place_bet() when pressed
spin_button = tk.Button(button_frame, text="Spin Roulette", command=place_bet, bg="#1e90ff", fg="white", font=("Arial", 12, "bold"))
spin_button.pack(anchor="center", pady=5)


# Auto Play checkbox
auto_play = tk.BooleanVar() # Variable indicating whether Auto Play is enabled (True/False)
auto_play_check = tk.Checkbutton(button_frame, text="Auto Play (μόνο Bots)", variable=auto_play, bg="#3e3e3e", fg="white", selectcolor="#1e90ff", font=("Arial", 12, "bold")) # Checkbox for enabling/disabling automatic bot play
auto_play_check.pack(anchor="center", pady=(5, 0))


# --- Balances + Bets ---
side_frame = tk.Frame(root, bg="#2e2e2e") # Create a horizontal frame containing two columns: player balances and round bets
side_frame.pack(padx=20, pady=(10, 10), fill="x")


# Balances Header
info_header = tk.Label(side_frame, text="Υπόλοιπα παικτών", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
info_header.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))


# Bets Header
bots_header = tk.Label(side_frame, text="Πονταρίσματα Γύρου Bots", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
bots_header.grid(row=0, column=1, sticky="ew", padx=5, pady=(0, 5))


# Balances Frame
# A LabelFrame used to display each player's balance
info_frame = tk.LabelFrame(side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
info_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))


# Display each player's name and balance next to it (e.g. 300€)
# The balance_labels dictionary is used to dynamically update the balances after each round
for i, player in enumerate(["Player", "Bot 1", "Bot 2", "Bot 3"]):
    tk.Label(info_frame, text=f"{player}:", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold")).grid(row=i, column=0, sticky="e", pady=3, padx=5)
    balance_labels[player] = tk.Label(info_frame, text="300€", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold"))
    balance_labels[player].grid(row=i, column=1, sticky="w", pady=3, padx=5)


# Bets Frame
# A second LabelFrame used to display what each bot bet during the current round
bots_frame = tk.LabelFrame(side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
bots_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0, 5))


# Initialize the betting rows for each bot. The content changes when "Spin" is pressed.
# The bot_labels dictionary allows us to quickly update what each bot has bet
for bot in ["Bot 1", "Bot 2", "Bot 3"]:
    bot_labels[bot] = tk.Label(bots_frame, text=f"{bot}: -", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold"), anchor="w", width=35)
    bot_labels[bot].pack(anchor="w", pady=3)


# Balance between frames
# Set equal column widths for Balances and Bets
side_frame.columnconfigure(0, weight=1, uniform="group_side")
side_frame.columnconfigure(1, weight=1, uniform="group_side")


# --- Results + Ball ---
# Create a horizontal frame that contains the players' results and the roulette ball result
results_side_frame = tk.Frame(root, bg="#2e2e2e")
results_side_frame.pack(padx=20, pady=(10, 10), fill="x")


# Headers
# Header for the players' results column
results_header = tk.Label(results_side_frame, text="Αποτελέσματα Γύρου", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
results_header.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))


# Header for the column displaying the roulette ball result
single_result_header = tk.Label(results_side_frame, text="Μπίλια", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
single_result_header.grid(row=0, column=1, sticky="ew", padx=5, pady=(0, 5))


# Results Frame
# Create a bordered frame for displaying the results of each player
results_frame = tk.LabelFrame(results_side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
results_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))


# Create a Label for each player to display the result of the round (e.g. whether they won or lost)
# The labels are stored in the results_labels dictionary for easy updating after each round
for player in ["Player", "Bot 1", "Bot 2", "Bot 3"]:
    results_labels[player] = tk.Label(results_frame, text=f"{player}: -", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold"), anchor="w", width=25)
    results_labels[player].pack(anchor="w", pady=3)


# Ball Frame
# Create a frame for displaying the number, color, and dozen corresponding to the roulette result
single_result_frame = tk.LabelFrame(results_side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
single_result_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0, 5))


# Label where the spin result is displayed
roulette_result_label = tk.Label(single_result_frame, text="", font=("Arial", 16, "bold"), bg="#3e3e3e", fg="white", anchor="center")
roulette_result_label.pack(expand=True, fill="both")


# Set equal column widths for Results and Ball
results_side_frame.columnconfigure(0, weight=1, uniform="group_results")
results_side_frame.columnconfigure(1, weight=1, uniform="group_results")


# --- HISTORY Header ---
# Header for the "Game History" section
history_header = tk.Label(root, text="Ιστορικό παιχνιδιού", font=("Arial", 14, "bold"), anchor="w", bg="#2e2e2e", fg="white")
history_header.pack(padx=20, pady=(10, 5), anchor="w")


# Text widget for the colored numerical history
history_frame = tk.Frame(root, bg="#2e2e2e")
history_frame.pack(padx=20, pady=(0, 10), anchor="w")


# Create a Text widget for displaying the history
history_label = tk.Text(history_frame, height=2, width=45, bg="#3e3e3e", fg="white", font=("Arial", 16, "bold"), padx=10, pady=10, relief="solid", borderwidth=2,)
history_label.pack()
history_label.config(state="disabled") # Set state to disabled so that the user cannot modify the history


# --- START ---
# Add a "trace" to the bet_type variable that calls update_bet_options whenever the bet type changes (e.g. from "color" to "number")
bet_type.trace("w", update_bet_options)
reset_game() # Call reset_game() to initialize the game and GUI elements (e.g. display the initial balances)
root.mainloop() # Start the Tkinter main loop, which keeps the window open and waits for user events
