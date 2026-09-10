import tkinter as tk # Εισαγωγή της βιβλιοθήκης Tkinter για GUI
from tkinter import messagebox #Εισαγωγή του module messagebox από τη βιβλιοθήκη Tkinter, το οποίο παρέχει διάφορα προκαθορισμένα παράθυρα διαλόγου για εμφάνιση μηνυμάτων προς τον χρήστη.
import random # Εισαγωγή της βιβλιοθήκης random για τυχαίους αριθμούς

# Εισαγωγή των κόκκινων αριθμών στη ρουλέτα σε σύνολο
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

# Αρχικοποίηση λεξικών και μεταβλητών παιχνιδιού
balances = {} # Αρχικοποίηση κενού λεξικού όπου θα κρατά τα υπόλοιπα των παικτών 
bets = {} # Αρχικοποίηση κενού λεξικού όπου θα κρατά τα τρέχοντα πονταρίσματα κάθε παίκτη
history = [] # Αρχικοποίηση κενής λίστας όπου θα κρατά το ιστορικό των αποτελεσμάτων
bot_labels = {}  # Αρχικοποίηση κενού λεξικού όπου θα  περιέχει τις ετικέτες(labels) του GUI για εμφάνιση πονταρισμάτων bots
balance_labels = {} # Αρχικοποίηση κενού λεξικού όπου θα περιέχει τις ετικετες (labels) του GUI που εμφανίζουν τα υπόλοιπα των παικτών
results_labels = {} # Αρχικοποίηση κενού λεξικού όπου θα περιέχει τις ετικετες (labels) του GUI για να δείχνει τα αποτελέσματα (κέρδη ή απώλειες) κάθε παίκτη μετά από κάθε γύρο

auto_play = None # Αρχικοποίηση global μεταβλητής με τιμή None που αργότερα θα γίνει BooleanVar (μεταβλητή Tkinter)
                    #για σύνδεση με checkbox όπου θα ελέγχει αν το παιχνίδι θα εκτελείται αυτόματα

roulette_result_label = None # Αρχικοποίηση global μεταβλητής με τιμή None που αργότερα θα χρησιμοποιηθεί για το
                    #widget ετικέτας (Label) στο οποίο θα εμφανίζεται το αποτέλεσμα κάθε γύρου της ρουλέτας.

history_label = None # Αρχικοποίηση global μεταβλητής που αρχικά δεν έχει τιμή (None) και αργότερα θα χρησιμοποιηθεί
                     #για το widget ετικέτας (Label)που θα εμφανίζει το ιστορικό των 10 τελευταίων αποτελεσμάτων της ρουλέτας.

bet_type = None # Αρχικοποίηση global μεταβλητής που αρχικά δεν έχει τιμή (None) και αργότερα θα γίνει μεταβλητή TKinter τύπου  StringVar() και συνδεεται με Radiobutton
                    #Xρησιμοποιείται για να παρακολουθεί τον τύπο του ποντάρισματος που επιλέγει ο χρήστης (π.χ. "color", "number" ή "dozen").


value_menu = None # Αρχικοποίηση  global μεταβλητής που αρχικά δεν έχει τιμή (None) και αργότερα θα γίνει ένα OptionMenu widget του Tkinter
                    #όπου θα επιτρέπει στον χρήστη να επιλέξει μια τιμή από μια πτυσσόμενη λίστα όπως το χρώμα (κόκκινο/μαύρο), τον αριθμό (0-36) ή την 12άδα (1-12, 13-24, 25-36) για το πονταρίσμα.

bet_value = None # Αρχικοποίηση global μεταβλητής που αρχικά δεν έχει τιμή (None) και αργότερα θα γίνει μεταβλητή TKinter τύπου StringVar()και συνδεεται με optionmenu
                    # Xρησιμοποιείται για να αποθηκεύει την συγκεκριμένη τιμή που επιλέγει ο χρήστης για το πονταρίσμα (π.χ. "Κόκκινο", "32", ή "2η 12άδα (13-24)").
                    
bet_amount = None # Αρχικοποίηση global μεταβλητής που αρχικά δεν έχει τιμή (None) και αργότερα θα γίνει μεταβλητή TKinter τύπου  StringVar() και συνδεεται με optionmenu
                   # Xρησιμοποιείται για να αποθηκεύει το ποσό που ποντάρει ο χρήστης σε κάθε γύρο της ρουλέτας.


# Συνάρτηση για επαναφορά και αρχικοποίηση του παιχνιδιού
def reset_game():
    global balances, bets, history # Χρήση global μεταβλητών
    balances = {"Player": 300, "Bot 1": 300, "Bot 2": 300, "Bot 3": 300} # Ορισμός αρχικού υπολοίπου για κάθε παίκτη και bot
    bets.clear() # Καθαρισμός λεξικου με παικτες και πονταρισμάτα
    for player in balances:
        bets[player] = []  # Δημιουργία κενής λίστας στοιχημάτων για κάθε παίκτη
    history.clear() # Καθαρισμός λίστας με ιστορικό αποτελεσματων
    update_display() # Κλήση συνάρτησης όπου ενημερώνει τα widgets ετικετών (Labels) στο παράθυρο του παιχνιδιού.
    update_result("") # Κλήση συνάρτησης όπου καθαρίζει το αποτέλεσμα της ρουλέτας στην αρχή ενός νέου παιχνιδιού με κενο string
    update_history()# Κλήση συνάρτησης όπου καθαρίζει το ιστορικό
    reset_bots_display()# Κλήση συνάρτησης για καθαρισμό προβολής των στοιχημάτων των bots
    update_bet_options() # Κλήση συνάρτησης για να συγχρονίσει το περιεχόμενο του OptionMenu με τον τρέχοντα τύπο πονταρίσματος (bet_type), κάθε φορά που το παιχνίδι επαναφέρεται
    reset_results_display() # Κλήση συνάρτησης όπου καθαρίζει τα αποτέλεσματα του καθε παικτη στην αρχή ενός νέου παιχνιδιού
    spin_button.config(state="normal", bg="#1e90ff")  # ενεργοποιω το widget spin roulette
    

# Συνάρτηση για ενημέρωση του label του αποτελέσματος περιστροφης της ρουλετας στο GUI
def update_result(text):
    roulette_result_label.config(text=text)  # Εμφάνιση αποτελέσματος περιστροφής ρουλέτας

    
# Συνάρτηση για ενημέρωση της label του ιστορικού
def update_history():
    # Ξεκλειδώνουμε το text widget για να γίνει επεξεργάσιμο
    history_label.config(state="normal")
    history_label.delete("1.0", "end")  # Καθαρίζουμε το περιεχόμενο του label

    # Παίρνουμε τα τελευταία 15 αποτελέσματα από το ιστορικό (αντιστραμμένα)
    for result in reversed(history[-15:]): #Διατρέχει από τη λίστα history τα τελευταία 15 αποτελέσματα από το πιο πρόσφατο στο πιο παλιό
        parts = result.split(" ")  #Σπάμε το string του αποτελέσματος σε λίστα λέξεων με βάση τα κενά
        number = parts[0] #Κρατάμε μόνο τον αριθμό για να το προσθέσουμε στο ιστορικό
        
        if len(parts) > 1:  # Έλεγχος αν το μήκος της λίστας parts είναι >1
            color_text = parts[1].strip("()")# Ορίζω μεταβληρη με το χρώμα του νούμερου. Αφαιρούμε τις παρενθεσεις απο το δευτερο στοιχειο που ειναι το χρωμα αν η λίστα parts έχει 2ο στοιχειο 
                                            # έτσι ώστε το π.χ το (κοκκινο) να φαινεται 'κοκκινο', ενώ αν δεν έχει ορίζετε ως 'μαύρο'
        else:
            color_text = "Μαύρο"  #Διαφορετικά ορίζω τη μεταβλητή να έχει τη τιμή μαύρο
                
        # Επιλέγουμε χρώμα μορφοποίησης για το κείμενο με τον παρακάτω έλεγχο
        if color_text == "Κόκκινο":
            color = "red"
        elif color_text == "Πράσινο":
            color = "green"
        else:
            color = "black"

        # Ορίζουμε το στυλ της ετικέτας history_label
        # Ετσι ωστε να εμφανιζει τους αριθμούς με τα χρώματα τους
        history_label.tag_config("red", foreground="red") # το foreground οριζει το χρώμα του κειμένου
        history_label.tag_config("green", foreground="green")
        history_label.tag_config("black", foreground="black")
    
        # Προσθέτουμε το αποτέλεσμα στο widget με το αντίστοιχο χρώμα
        history_label.insert("end", f"{number}  ", (color,)) #Εισαγω στο τελος του label το νούμερο, και βαζω tag για χρωματισμο του νούμερου. Το ','στο τέλος του color είναι γιατι θελω να το πάρει ως tuple και οχι ως string
        
    
    # Ξανακλειδώνουμε το widget για να μην είναι επεξεργασιμο
    history_label.config(state="disabled")


#Συνάρτηση για ενημέρωση της εμφάνισης υπολοίπων όλων των παικτών
def update_display():
    for player in balance_labels:  #Διατρέχει το dict balance_labels όπου περιέχει τις ετικετες (labels) του GUI που εμφανίζουν τα υπόλοιπα των παικτών
        if player in balances: # Ελέγχει αν ο παίκτης έχει χρηματικό απόθεμα στο dict balances οπότε και είναι ενεργός στο παιχνίδι
            balance_labels[player].config(text=f"{balances[player]}€")  # Ενημέρωση υπολοίπου του παίκτη απο το dict balances
        else:
            balance_labels[player].config(text="Εκτός παιχνιδιού") #Σε περίπτωση που ο παίκτης δεν έχει χρηματικό απόθεμα στο dict balnces, τότε εμφανίζεται το μύνημα "Εκτός παιχνιδιού"
            

# Συνάρτηση για καθαρισμό της εμφάνισης στοιχημάτων των bots
def reset_bots_display():
    for bot in bot_labels: #Διατρέχει το dict bot_labels όπου περιέχει τις ετικέτες(labels) του GUI για εμφάνιση πονταρισμάτων bots
        if bot in balances: # Ελέγχει αν το bot έχει χρηματικό απόθεμα στο dict balances οπότε και είναι ενεργός στο παιχνίδι
            bot_labels[bot].config(text=f"{bot}: -") #Εμφανίζει στο label του bot_labels στιγμιαία "-" μέχρι το επόμενο ποντάρισμα
        else:
            bot_labels[bot].config(text=f"{bot}: Εκτός παιχνιδιού") #Σε περίπτωση που το bot δεν έχει χρηματικό απόθεμα τότε εμφανίζεται το μύνημα "Εκτός παιχνιδιού"


# Συνάρτηση για καθαρισμό της εμφάνισης των κερδών/ζημίων σε νέο παιχνίδι ή επαναφορά 
def reset_results_display():
    for player in results_labels:#Διατρέχει το dict results_labels όπου περιέχει τις ετικετες (labels) με τα κέρδη / ζημίες των παικτών μετά από κάθε γύρο
        results_labels[player].config(text=f"{player}: -") #Εμφανίζει στο label του κάθε παικτη "-" όπου καθαρίζει τα αποτελέσματα των παικτών


# Συνάρτηση για ενημέρωση επιλογών πονταρίσματος απο τον χρήστη
def update_bet_options(*args): #το *args σημαινει ότι η συνάρτη παιρνει οποιοδήποτε αριθμό ορισμάτων γιατι συνδέεται με τη trace tkinter που περνά αυτόματα ορίσματα
                            #όταν αλλάξει η τιμή bet_type καλείτι αυτοματα μέσω της μεθόδου trace
    options = {
        "color": ["Κόκκινο", "Μαύρο"],
        "number": list(range(37)),
        "dozen": ["1η 12άδα (1-12)", "2η 12άδα (13-24)", "3η 12άδα (25-36)"]
    }[bet_type.get()] #επιστρεφει τη τρεχουσα επιλογή του χρήστη στη μεταβλητή bet_type (σύνδεση με radiobutton)
    bet_value.set(options[0]) #θετουμε την προεπιλεγμένη τιμή της μεταβλητής bet_value να είναι η 1η τιμη του επιλεγμένου κλειδιού
    value_menu['menu'].delete(0, 'end') #Το value_menu['menu'] αναφέρεται στο "μενού" του OptionMenu, όπου καθαρίζει πλήρως το μενου πριν προσθέσει νεες επιλογές

    
    for option in options:   #Διατρεχω το dict options  
        value_menu['menu'].add_command(label=option, command=tk._setit(bet_value, option)) #προσθετω μια νέα εντολή στο dropdown menu με τις τιμες που έχουν τα values του
        #κάθε κλειδιου ενώ το command..ειναι μία εσωτ συναρτηση της tkinter που ενημερώνει τη stringVar bet_value να πάρει τη τιμή option που ο χρήστης έχει τοποθετήσει στο μενού

# Συνάρτηση εμφάνισης πονταρισμάτων bots
def show_bot_bets():
    for bot in ["Bot 1", "Bot 2", "Bot 3"]: #επανάληψη που διατρέχει λίστα με Bots
        if bot not in balances or balances[bot] <= 0: #έλεγχος αν το balances του καθε Bot είναι <=0 ή αν υπάρχει στη λίστα το Bot 
            bot_labels[bot].config(text=f"{bot}: Εκτός παιχνιδιού") #στο text του label αναγράφει 'εκτος παιχνιδιού' αν επαληθευθει ο παραπάνω έλεγχος
            continue #Αν ένα bot δεν πληρει τον παραπάνω έλεγχο το προσπερνά και παει στο επόμενο

        bet_type_bot = random.choice(["color", "number", "dozen"]) #Αποδίδει τυχαια τιμή σε μεταβλητή ανάμεσα στα ["color", "number", "dozen"]
        amount = 5 if bet_type_bot == "number" else random.choice([5, 10, 20]) #Αν επιλεγει number τότε αποδιδει τιμή 5 σε μεταβλητη αλλιώς παίρνει 1 τυχαια ανάμεσα στο 5,10 και 15
        amount = min(amount, balances[bot]) #εξασφαλίζει ότι η τιμη που θα πάρει θα εξυπηρετεί το υπόλοιπο

        if amount == 0:  #έλεγχος αν το amount ειναι 0
            bot_labels[bot].config(text=f"{bot}: Δεν έχει αρκετά για ποντάρισμα") # Το bot_label του bot ενημερώνεται με το μύνημα "Δεν έχει αρκετά για ποντάρισμα"
            continue #Αν ένα bot δεν πληρει τον παραπάνω έλεγχο το προσπερνά και παει στο επόμενο

        #Έλεγχος και αποδοση τιμης σε μεταβλητη ανάλογα με τη παραπάνω τυχαια επιλογη πονταρισματος
        if bet_type_bot == "color":
            value = random.choice(["Κόκκινο", "Μαύρο"])
        elif bet_type_bot == "dozen":
            value = random.choice(["1η 12άδα (1-12)", "2η 12άδα (13-24)", "3η 12άδα (25-36)"])
        else:
            value = random.randint(0, 36)

        balances[bot] -= amount #αφαίρεση του ποσού πονταρισματος από το balance του bot σε κάθε ποντάρισμα

        bets[bot].append({"type": bet_type_bot, "value": value, "amount": amount}) #Προσθήκη λεξικού στη λίστα των bots με τις τυχαιες επιλογες 
        bot_labels[bot].config(text=f"{bot}: {amount}€ στο/η {value} ({bet_type_bot})") #Ενημέρωση του label bot_labels με το ποσό και το ποντάρισμα του bot
        
    
# Συνάρτηση πονταρίσματος παίκτη και έναρξης γύρου
def place_bet():
    if "Player" in balances: #ελεγχος αν υπαρχει ο "Player" στο dict balances
        amount = int(bet_amount.get()) # απόδοση σε μεταβλητη η τιμή που θα επιλέξει ο παικτης απο το bet_amount μέσω τη μεθόδου .get()
        if amount > balances["Player"]: # Έλεγχος αν το ποσό που επέλεξε ο παικτης είναι διαθέσιμο στο υπόλοιπο του παίκτη
            tk.messagebox.showerror("Σφάλμα", "Δεν έχετε αρκετά χρήματα για το ποντάρισμα σας!") #Ριχνει pop up μύνημα ότι δεν εχει διαθεσιμο υπόλοιπο για αυτο το ποντάρισμα μεσω του messagebox
            return #τερματίζει η συνάρτηση

        balances["Player"] -= amount #αφαιρείται το ποσο πονταρισματος από το διαθέσιμο υπολοίπο του παικτη

        bets["Player"].append({"type": bet_type.get(), "value": bet_value.get(), "amount": amount}) #προσθηκη στο λεξικό bets τα στοιχεια πονταρισματος του παίκτη

    show_bot_bets() # Συναρτηση που εμφανίζει τα πονταρισματα των Bots
    spin_roulette() # Συνάρτηση για έναρξη περιστροφής ρουλέτας
    update_display()# Συναρτηση που ανανεωνει τα υπόλοιπα των παίκτών ή τους ενημερωνει ότι είναι εκτος παιχνιδιου
    
    

# Συνάρτηση έναρξης περιστροφής ρουλέτας
def spin_roulette():
        
    number = random.randint(0, 36) #αποδοση τιμης σε μεταβλητη τυχαια επιλογη αριθμού απο 0-36
    #Έλεγχος και αποδοση τιμης σε μεταβλητη του χρωματος των αριθμων της ρουλετα σύμφωνα με τη τυχαια τιμή του number
    color = "Κόκκινο" if number in RED_NUMBERS else "Μαύρο" if number != 0 else "Πράσινο"

    # Έλεγχος αριθμών που αντιστοιχουν σε 12αδες
    if 1 <= number <= 12: #1-12
        dozen = "1η 12άδα (1-12)"
    elif 13 <= number <= 24: #13-24
        dozen = "2η 12άδα (13-24)"
    elif 25 <= number <= 36: #25-36
        dozen = "3η 12άδα (25-36)"
    else:
        dozen = None #Αν η ρουλέτα βγάλει το 0 τότε η μεταβλητή dozen παίρνει τη τιμή 0

    result_text = f" {number} ({color})" #Δημιουργει ενα string με τον αριθμό και το χρωμα
    if dozen: #ελεγχος αν η μεταβλητη dozen έχει κάποια τιμή (παντα εκτος αν ο αριθμος ειναι 0) 
        result_text += f" - {dozen}" #Αν ισχυει προσθετει στο παραπανω string τη 12-αδα
    update_result(result_text) #Καλει τη συναρτηση και παιρνει ως ορισμα το αποτελεσμα result text για την εμφανιση του αποτελέσματος της περιστροφης

    history.append(f"{number} ({color})") #Προσθετει το αποτελεσμα στη λιστα του ιστορικου
    update_history() #Καλεί τη συνάρτηση για να εμφανισει το αποτέλεσμα στο ιστορικο
    calculate_winnings(number, color, dozen) # Καλει τη συνάρτηση για να υπολόγίσει τα κέρδη των παικτων 
    update_display() #Καλει τη συνάρτηση για να να εμφανισει το υπολοιπο των παικτων ή αν δεν έχουν υπολοιπο να εμφανίσει μύνημα "Εκτός παιχνιδιού"

    for player in bets: #Διατρεχει το λεξικο bets με τα στοιχήματα των παικτων
        bets[player] = [] #Καθαρίζει τα παλια πονταρίσματα, έτσι ώστε να πάρει τα πονταρίσματα του επόμενου γύρου
        
    #Έλεγχος αν το autoplay για τα bots είναι true και αν είναι τουλαχιστον 2 bots είναι στο παιχνιδι και ο παίκτης έχει βγει από αυτο (δεν είναι στο balances)
    if auto_play.get() and len(balances) > 1 and "Player" not in balances: 
                                                                             
        root.after(2000, place_bet) # Η μεθοδος root.after εκτελεί τη συναρτηση place bet καθε 2000 ms οπου τα bots παιζουν αυτόματα

        
# Συνάρτηση υπολογισμού κερδών
def calculate_winnings(number, color, dozen):
    losers = [] # Δημιουργια κενής λίστας
    for player in list(balances): #Διατρεχει το dict balances δημιουργώντας αντίγραφο της λίστας των κλειδιών
        total = 0  #Απόδοση τιμης σε μεταβλητη για συνολικα κέρδη παίκτη 

        #Έλεγχος αν ο παίκτης έχει ποντάρει (παιρνει τιμη με τη μεθοδο .get()) 
        if bets.get(player):
            bet_total = bets[player][0]["amount"] #Αποδιδει σε μεταβλητη το ποσο πονταρισματος απο τη λίστα με λεξικά bets[player]
        else:
            bet_total = 0 #Απόδιδει τιμη 0 αν ο παίκτης είναι εκτός λιστας balances

        for bet in bets.get(player, []): #Διατρέχει τη λίστα πονταρισμάτων (αν δεν έχει πονταρισμα επιστρεφει κενη λιστα)
            if bet["type"] == "number" and int(bet["value"]) == number: #ελεγχος αν ο τυπος πονταρισματος ειναι number και ο αριθμός που πόνταρε ο παικτης είναι ίδιος με τον αριθμό της ρουλετας
                total += bet["amount"] * 36 #Προσθετει το ποσο που πονταρε ο παικτης * 36 στη μεταβλητη total 
            elif bet["type"] == "color" and bet["value"] == color: #ελεγχος αν ο τυπος πονταρισματος ειναι color και  το χρωμα που πόνταρε ο παικτης είναι ίδιο με το χρωμα του αριθμού της ρουλετας
                total += bet["amount"] * 2 #Προσθετει το ποσο που πονταρε ο παικτης * 2 στη μεταβλητη total 
            elif bet["type"] == "dozen" and bet["value"] == dozen: #ελεγχος αν ο τυπος πονταρισματος ειναι dozen και η 12αδα που πόνταρε ο παικτης είναι η σωστή με αυτή που έβγαλε η ρουλετα
                total += bet["amount"] * 3 #Προσθετει το ποσο που πονταρε ο παικτης * 3 στη μεταβλητη total 
 
        balances[player] += total #Προσθέτει στο balance του παίκτη το κερδος εφοσον υπάρχει

        if total > 0: #έλεγχος αν η μεταβλητη total είναι > 0
            results_labels[player].config(text=f"{player}: κέρδισε {total}€", fg="green") #ενημερωνει το label results_label του παίκτη με μύνημα που αναγραφει το ποσο που κέρδισε σε πρασινη γραμματοσειρα
        else:
            results_labels[player].config(text=f"{player}: έχασε {bet_total}€", fg="red") #ενημερωνει το label results_label του παίκτη με μύνημα που αναγραφει το ποσο πονταρισματος που έχασε σε κοκκινη γραμματοσειρα

        if balances[player] <= 0: #έλεγχος αν ο παικτης εχει υπόλοιπο <=0
            losers.append(player) # Τότε προσθετει τον παικτη σε λιστα losers
            if player == "Player": #ελεγχος αν ο ηττημενος είναι ο Player 
                spin_button.config(state="disabled", bg="gray")  # Απενεργοποίηση το widget spin button


    for player in losers: #Διατρέχει τη λίστα losers
        results_labels[player].config(text=f"{player}: Εκτός παιχνιδιού!") #ενημερωνει το label results_labels με μύνημα οτι ο παικτης είναι εκτός παιχνιδιου
        del balances[player] #Διαγραφει τον παικτη από το λεξικο balances

    
    if len(balances) == 1: #ελεγχος αν παραμεινει μονο ενας παικτης στο balances
        winner = list(balances.keys())[0] #Επιστρεφει όλα τα κλειδια του balances σε λίστα(μονο 1, αφου πέρασε τον έλεγχο) και αποδισει τη πρωτη τιμη της λίστας στη μεταβλητη winner
        results_labels[winner].config(text=f"{winner}: Νικητής!") # ενημερωνει το label results_labels που αντιστοιχει στον νικητη εμφανίζοντας μύνημα 'Νικητης'
        tk.messagebox.showinfo("Νικητής!", f"Ο {winner} είναι ο νικητής του παιχνιδιού!!!") #Εμφάνιση pop up ότι υπάρχει νικητης και ειναι ο winner
        spin_button.config(state="disabled", bg="gray")  # Απενεργοποίηση του widget spin roulette για αποφυγή συνεχιση παιχνιδιου πατώντας για νεα περιστροφη

        root.quit()  #Τερματισμός παιχνιδιού

# --- GUI Setup ---
root = tk.Tk() # Δημιουργεί το κύριο παράθυρο της εφαρμογής
root.title("Project 55 (e-Roulette)") #Ορίζει τον τίτλο του παραθύρου που εμφανίζεται στην μπάρα τίτλου.
root.geometry("1200x1200") #Καθορίζει το μέγεθος του παραθύρου (πλάτος x ύψος).
root.configure(bg="#2e2e2e") #Ορίζει σκούρο γκρι φόντο για όλο το παράθυρο

# --- TOP FRAME ---
top_frame = tk.Frame(root, bg="#2e2e2e") #Δημιουργεί ένα frame στην κορυφή του παραθύρου
top_frame.pack(fill="x", pady=(5, 5)) #Τοποθετεί το frame οριζόντια (γεμίζει όλο το πλάτος), με κατακόρυφο περιθώριο 5 pixels.
tk.Button(top_frame, text="Επαναφορά Παιχνιδιού", command=reset_game, bg="#4e4e4e", fg="white").pack(side="right", padx=10) #Προσθέτει κουμπί επαναφοράς παιχνιδιού (καλεί reset_game), με σκούρα εμφάνιση που τοποθετείται δεξιά

# --- Bet Frame ---
bet_header = tk.Label(root, text="Ποντάρισμα", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")#Εμφανίζει την επικεφαλίδα "Ποντάρισμα" με bold γράμματα και κεντραρισμένη εμφάνιση
bet_header.pack(pady=(10, 5))

bet_frame = tk.LabelFrame(root, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white") #Πλαίσιο για τα κουμπιά επιλογών πονταρίσματος, με περιθώρια και πλαίσιο
bet_frame.pack(padx=50, pady=(0, 10), fill="x")

bet_inner_frame = tk.Frame(bet_frame, bg="#3e3e3e") #Εσωτερικό frame για καλύτερη οργάνωση των κουμπιών πονταρίσματος.
bet_inner_frame.pack(expand=True)

# Μεταβλητή επιλογής τύπου πονταρίσματος (συνδέεται με τα κουμπιά επιλογής πονταρίσματος)
bet_type = tk.StringVar(value="color") #Μεταβλητή που κρατά τον επιλεγμένο τύπο πονταρίσματος ("color", "number", "dozen").

# --- Κουμπιά επιλογής τύπου πονταρίσματος (tk.Button, λειτουργούν σαν toggle μέσω select_bet_type) ---
bet_buttons = {} # Λεξικό για αποθήκευση των κουμπιών πονταρίσματος, ώστε να αλλάζουμε εμφάνιση (χρώμα) ανάλογα με την επιλογή.

# Συνάρτηση που ενεργοποιεί το button και απενεργοποιεί τα άλλα
def select_bet_type(selected_type):
    # Αλλάζουμε τη μεταβλητή bet_type
    bet_type.set(selected_type)
    # Ενημέρωση εμφανιζόμενων επιλογών
    update_bet_options()

    # Ενεργοποιεί οπτικά μόνο το επιλεγμένο κουμπί (μπλε χρώμα), ενώ τα υπόλοιπα παραμένουν γκρι
    for bet, button in bet_buttons.items():
        if bet == selected_type:
            button.config(bg="#1e90ff", fg="white")  # Μπλε φόντο, λευκό κείμενο
        else:
            button.config(bg="#3e3e3e", fg="white")  # Γκρι φόντο, λευκό κείμενο

# Δημιουργία κουμπιών για επιλογη πονταρισματος
bet_buttons["color"] = tk.Button(bet_inner_frame, text="Χρώμα", width=12, font=("Arial", 14, "bold"),
                                 command=lambda: select_bet_type("color"), bg="#1e90ff", fg="white")
bet_buttons["color"].grid(row=0, column=0, padx=10, pady=5) #Τοποθετεί το κουμπί στο grid layout ομοίως και για αριθμό,12άδα.

bet_buttons["number"] = tk.Button(bet_inner_frame, text="Αριθμός", width=12, font=("Arial", 14, "bold"),
                                  command=lambda: select_bet_type("number"), bg="#3e3e3e", fg="white")
bet_buttons["number"].grid(row=0, column=1, padx=10, pady=5)

bet_buttons["dozen"] = tk.Button(bet_inner_frame, text="12άδα", width=12, font=("Arial", 14, "bold"),
                                 command=lambda: select_bet_type("dozen"), bg="#3e3e3e", fg="white")
bet_buttons["dozen"].grid(row=0, column=2, padx=10, pady=5)

# OptionMenu value
bet_value = tk.StringVar() #Μεταβλητή που αποθηκεύει την τιμή του πονταρίσματος (π.χ. "Κόκκινο", "Μαύρο", αριθμός, ή 12άδα).
value_menu = tk.OptionMenu(bet_inner_frame, bet_value, "Κόκκινο", "Μαύρο") #Δημιουργεί default μενού επιλογής για χρώμα. (Η λίστα αλλάζει με βάση το bet_type μέσω της update_bet_options().)
value_menu.config(bg="#3e3e3e", fg="white", font=("Arial", 12), width=15) #Μορφοποίηση Option Menu
value_menu["menu"].config(bg="#3e3e3e", fg="white")#Μορφοποίηση Dropdown Menu
value_menu.grid(row=1, column=0, columnspan=3, pady=10)#Τοποθετεί το OptionMenu στο grid layout

# Amount selector
tk.Label(bet_inner_frame, text="ΠΟΣΟ:", bg="#3e3e3e", fg="white", font=("Arial", 12, "bold")).grid(row=2, column=0, pady=5) #Ετικέτα για το ποσό
bet_amount = tk.StringVar(value="1") #Μεταβλητή για αποθήκευση ποσού πονταρίσματος (π.χ. 1€, 2€, ..., 20€) default επιλογή το 1
#Δημιουργεί dropdown με ποσά από 1 έως 20 )
amount_menu = tk.OptionMenu(bet_inner_frame, bet_amount, *[str(i) for i in range(1, 21)])
amount_menu.config(bg="#3e3e3e", fg="white", font=("Arial", 12), width=8) # Μορφοποίηση του OptionMenu ποσού (κουμπί και dropdown) και τοποθέτηση με grid
amount_menu["menu"].config(bg="#3e3e3e", fg="white")
amount_menu.grid(row=2, column=1, pady=5)

# button_frame (θα το βάλουμε με sticky="ew" για να είναι stretch)
button_frame = tk.Frame(bet_inner_frame, bg="#3e3e3e") #Δημιουργεί ένα εσωτερικό frame για για την ομαδοποίηση των κουμπιών (Spin και Auto Play)
button_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

# Spin button
# Το βασικό κουμπί "Spin", καλεί τη συνάρτηση place_bet() όταν πατηθεί
spin_button = tk.Button(button_frame, text="Spin Roulette", command=place_bet, bg="#1e90ff", fg="white", font=("Arial", 12, "bold"))
spin_button.pack(anchor="center", pady=5)

# Auto Play checkbox
auto_play = tk.BooleanVar()# Μεταβλητή που δείχνει αν είναι ενεργοποιημένο το auto play (True/False).
auto_play_check = tk.Checkbutton(button_frame, text="Auto Play (μόνο Bots)", variable=auto_play, bg="#3e3e3e", fg="white", selectcolor="#1e90ff", font=("Arial", 12, "bold")) #Checkbox για ενεργοποίηση/απενεργοποίηση της αυτόματης λειτουργίας bots.
auto_play_check.pack(anchor="center", pady=(5, 0))

# --- Υπόλοιπα + Πονταρίσματα ---
side_frame = tk.Frame(root, bg="#2e2e2e") #Δημιουργεί ένα οριζόντιο πλαίσιο που περιλαμβάνει δύο στήλες: Υπόλοιπα παικτών και Πονταρίσματα γύρου
side_frame.pack(padx=20, pady=(10, 10), fill="x")

# Υπόλοιπα Header
info_header = tk.Label(side_frame, text="Υπόλοιπα παικτών", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
info_header.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))

# Πονταρίσματα Header
bots_header = tk.Label(side_frame, text="Πονταρίσματα Γύρου Bots", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
bots_header.grid(row=0, column=1, sticky="ew", padx=5, pady=(0, 5))

# Υπόλοιπα Frame
# Ένα LabelFrame για εμφάνιση του υπολοίπου κάθε παίκτη
info_frame = tk.LabelFrame(side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
info_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

#Εμφανίζει για κάθε παίκτη την ετικέτα με το όνομά του και δίπλα το υπόλοιπο (π.χ. 300€)
#Χρησιμοποιείται λεξικό balance_labels για να μπορούμε να ενημερώνουμε δυναμικά τα υπόλοιπα μετά από κάθε γύρο
for i, player in enumerate(["Player", "Bot 1", "Bot 2", "Bot 3"]):
    tk.Label(info_frame, text=f"{player}:", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold")).grid(row=i, column=0, sticky="e", pady=3, padx=5)
    balance_labels[player] = tk.Label(info_frame, text="300€", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold"))
    balance_labels[player].grid(row=i, column=1, sticky="w", pady=3, padx=5)

# Πονταρίσματα Frame
# Δεύτερο LabelFrame για την εμφάνιση του τι πόνταρε κάθε bot στον τρέχοντα γύρο.
bots_frame = tk.LabelFrame(side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
bots_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0, 5))

# Αρχικοποιεί τις γραμμές πονταρίσματος για κάθε bot. Το περιεχόμενο αλλάζει όταν πατηθεί το "Spin".
#Το bot_labels είναι λεξικό που επιτρέπει να ενημερώνουμε γρήγορα το τι πόνταρε κάθε bot.
for bot in ["Bot 1", "Bot 2", "Bot 3"]:
    bot_labels[bot] = tk.Label(bots_frame, text=f"{bot}: -", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold"), anchor="w", width=35)
    bot_labels[bot].pack(anchor="w", pady=3)

# Ισορροπία πλαισίων
# Ορισμός ίδιου πλάτους για στήλες: Υπόλοιπα και Πονταρίσματα
side_frame.columnconfigure(0, weight=1, uniform="group_side")
side_frame.columnconfigure(1, weight=1, uniform="group_side")

# --- Αποτελέσματα + Μπίλια ---
# Δημιουργεί ένα οριζόντιο πλαίσιο που θα περιλαμβάνει τα αποτελέσματα των παικτών και την ένδειξη της μπίλιας
results_side_frame = tk.Frame(root, bg="#2e2e2e")
results_side_frame.pack(padx=20, pady=(10, 10), fill="x")

# Headers
#Επικεφαλίδα για τη στήλη αποτελεσμάτων παικτών
results_header = tk.Label(results_side_frame, text="Αποτελέσματα Γύρου", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
results_header.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))

#Επικεφαλίδα για τη στήλη που δείχνει το αποτέλεσμα της μπίλιας
single_result_header = tk.Label(results_side_frame, text="Μπίλια", font=("Arial", 14, "bold"), anchor="center", bg="#2e2e2e", fg="white")
single_result_header.grid(row=0, column=1, sticky="ew", padx=5, pady=(0, 5))

# Αποτελέσματα Frame
# Δημιουργεί ένα πλαίσιο με περίγραμμα για τα αποτελέσματα κάθε παίκτη.
results_frame = tk.LabelFrame(results_side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
results_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

#Για κάθε παίκτη δημιουργείται ένα Label που θα εμφανίζει το αποτέλεσμα του γύρου (π.χ., αν κέρδισε ή όχι).
# Τα labels αποθηκεύονται σε λεξικό results_labels για εύκολη ενημέρωση μετά από κάθε γύρο
for player in ["Player", "Bot 1", "Bot 2", "Bot 3"]:
    results_labels[player] = tk.Label(results_frame, text=f"{player}: -", bg="#3e3e3e", fg="white", font=("Arial", 13, "bold"), anchor="w", width=25)
    results_labels[player].pack(anchor="w", pady=3)

# Μπίλια Frame
# Δημιουργεί ένα πλαίσιο για την εμφάνιση του αριθμού,χρώματος και 12άδας που έκατσε η μπίλια
single_result_frame = tk.LabelFrame(results_side_frame, padx=15, pady=15, relief="solid", borderwidth=2, bg="#3e3e3e", fg="white")
single_result_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=(0, 5))

# Label όπου εμφανίζεται το αποτέλεσμα του spin
roulette_result_label = tk.Label(single_result_frame, text="", font=("Arial", 16, "bold"), bg="#3e3e3e", fg="white", anchor="center")
roulette_result_label.pack(expand=True, fill="both")

# Ορισμός ίδιου πλάτους για στήλες: Αποτελέσματα και Μπίλια
results_side_frame.columnconfigure(0, weight=1, uniform="group_results")
results_side_frame.columnconfigure(1, weight=1, uniform="group_results")

# --- ΙΣΤΟΡΙΚΟ Header ---
# Επικεφαλίδα για το "Ιστορικό παιχνιδιού"
history_header = tk.Label(root, text="Ιστορικό παιχνιδιού", font=("Arial", 14, "bold"), anchor="w", bg="#2e2e2e", fg="white")
history_header.pack(padx=20, pady=(10, 5), anchor="w")

# Text widget για έγχρωμα αριθμημένα ιστορικά
history_frame = tk.Frame(root, bg="#2e2e2e")
history_frame.pack(padx=20, pady=(0, 10), anchor="w")

#Δημιουργεί ένα Text widget για την εμφάνιση του ιστορικού
history_label = tk.Text(history_frame, height=2, width=45, bg="#3e3e3e", fg="white", font=("Arial", 16, "bold"), padx=10, pady=10, relief="solid", borderwidth=2,)
history_label.pack()
history_label.config(state="disabled") # (state="disabled") ώστε ο χρήστης να μην μπορεί να αλλάξει το ιστορικό

# --- START ---
# Προσθέτει έναν "παρατηρητή" στη μεταβλητή bet_type που καλεί τη συνάρτηση update_bet_options κάθε φορά που αλλάζει το ποντάρισμα (π.χ. από "color" σε "number").
bet_type.trace("w", update_bet_options)
reset_game() #Καλεί τη συνάρτηση reset_game() για να αρχικοποιήσει το παιχνίδι και τα στοιχεία του GUI (π.χ. να εμφανίσει τα αρχικά υπόλοιπα)
root.mainloop() # Ξεκινά το βασικό loop του Tkinter (root.mainloop()), το οποίο κρατά το παράθυρο ανοιχτό και περιμένει γεγονότα από τον χρήστη
