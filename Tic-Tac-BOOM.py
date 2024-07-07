import pygame
import tkinter as tk
from tkinter import PhotoImage
import random
import time
pygame.mixer.init()

window = tk.Tk()
window.title("Tic-Tac-BOOM")
icon_logo_image=PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Images\Logo.png")
window.iconphoto(False, icon_logo_image)

default_grid_color = "#F0F0F0"

sound_condition = 1
button_click = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\Coin_1.mp3")
end_game_sound = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\Exit_1.mp3")
bomb_planted_sound = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\SFX_Powerup_01.mp3")
bomb_touched_sound = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\8bit_bomb_explosion.mp3")
error_sound = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\Wrong_1.wav")
plyr1_click = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\SFX_Powerup_45.mp3")
plyr2_click = pygame.mixer.Sound(r"C:\Tic-Tac-BOOM Pack\Sound_Effects\SFX_Powerup_46.mp3")

music_condition = 1
menu_music = r"C:\Tic-Tac-BOOM Pack\Music Files\Insert Coin.mp3"
game_music = r"C:\Tic-Tac-BOOM Pack\Music Files\Raining Bits.mp3"
next_round_music = r"C:\Tic-Tac-BOOM Pack\Music Files\06-Continue.mp3"


pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)


def place_bomb():
    global bomb_count, bomb_row, bomb_column, bomb_touched, player, sound_condition
    if bomb_count == 0 and bomb_touched == 0 and not check_winner():
        bomb_row = random.randint(0, 2)
        bomb_column = random.randint(0, 2)
        while buttons[bomb_row][bomb_column]['text'] != " ":
            bomb_row = random.randint(0, 2)
            bomb_column = random.randint(0, 2)
        
        buttons[bomb_row][bomb_column]['text'] = "Bomb"
        buttons[bomb_row][bomb_column].config(fg=default_grid_color)
        bomb_count = 1 
        moves.append((bomb_row, bomb_column))
        
        player = players[1] if player == players[0] else players[0]
        label_turn.config(text=player+"'s turn")
        change_bg()

        # Reset timer when bomb is placed
        reset_timer()

        if sound_condition == 1:
            bomb_planted_sound.play()

        # Changes Bomb Button Visuals to indicate a bomb has been planted
        bomb_button.config(text = "Bomb Placed", width=15, fg="yellow",bg="black")
        if player == 'AI':
            ai_moves()
    
    else:
        if sound_condition == 1:
            error_sound.play()



def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != " ": 
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != " ":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != " ":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != " ":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True
    
    elif bomb_count == 0 and not empty_space():
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "TIE"

    else:
        return False
    



def end_game(result):
    global player_scores, bomb_count, bomb_row, bomb_column, bomb_touched, timer_id, sound_condition

    # Handle game result and update scoreboard
    if result == "TIE":
        for row in range(3):
            for column in range(3):
                if buttons[row][column]['text'] == " ":
                    buttons[row][column].config(bg="yellow")
        label_turn.config(text="TIE!", bg="yellow")
        
    else:
        if bomb_touched == 1:
            enemy = players[1] if player == players[0] else players[0]
            label_turn.config(text = player + " touched a bomb, " + (enemy) + " wins.",  bg = "black", fg = "yellow")
            time_label.config(text= "")
            player_scores[enemy] += 1  
            update_scoreboard()
        else:
            label_turn.config(text=player + " Wins", bg = "black",)
            player_scores[player] += 1 
            update_scoreboard()
            if player == players[0]:
                label_turn.config(bg="#00DEDE")  
            elif player == players[1]:
                label_turn.config(bg="red")


    # Check if there's an ongoing timer and cancel it
    if timer_id is not None:
        window.after_cancel(timer_id)
    
    reset_timer()  # Call reset_timer to restart the timer for the new game
    cancel_timer()  # Stop the timer when the game is over

    pygame.mixer.music.load(next_round_music)
    if music_condition == 1:
        pygame.mixer.music.play(-1, fade_ms = 1000)
    if sound_condition == 1:
            end_game_sound.play()



def update_scoreboard():
    scoreboard_label.config(text="Scoreboard:\n" + players[0] + ": " + str(player_scores[players[0]]) + "\n" + players[1] + ": " + str(player_scores[players[1]]))



def next_turn(row, column):
    global player, bomb_touched, time_left, sound_condition
    
    if check_winner() or bomb_touched == 1:
        if sound_condition == 1:
            error_sound.play() 
        return 
    
    else:
        if bomb_count == 1 and bomb_touched == 0:
            if buttons[row][column]['text'] == "Bomb":
                buttons[row][column].config(bg="black", fg="yellow")
                bomb_touched = 1
                end_game("loses")  # Call end_game() with "loses" argument
                return
            
        if buttons[row][column]['text'] == " ":
            if player == players[0]:
                buttons[row][column]['text'] = "X"
                buttons[row][column].config(bg="blue", fg="black") 
                if sound_condition == 1:
                    plyr1_click.play() 
            else:
                buttons[row][column]['text'] = "O"
                buttons[row][column].config(bg="red", fg="black")
                if sound_condition == 1:
                    plyr2_click.play()

            moves.append((row, column))
            
            time_left = time_limit  # Reset time_left to time_limit
            time_label.config(text=f"Time left: {time_left}")
            if check_winner():
                end_game(check_winner())
            else:
                reset_timer()
                switch_players()

        else:
            if sound_condition == 1:
                error_sound.play()

            

def switch_players():
    global player
    player = players[1] if player == players[0] else players[0]
    label_turn.config(text=player + "'s turn")
    change_bg()
    print("Switched players. Current player:", player)
    # Cancel the timer for the previous player
    cancel_timer()
    # Restart the timer for the new player
    start_timer()
    if player == "AI":
            ai_moves()




def reset_timer():
    global time_left
    time_left = time_limit
    time_label.config(text=f"Time left: {time_left}")
    print("Timer reset for", player)

    # Cancel the current timer and start a new one
    cancel_timer()
    start_timer()




def cancel_timer():
    global timer_id
    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None




def start_timer():
    global timer_id
    if timer_id is None:
        timer_id = window.after(1000, update_timer)




def update_timer():
    global time_left, timer_id, player
    time_left -= 1
    time_label.config(text=f"Time left: {time_left}")
    print("Timer updated. Time left:", time_left)
    if time_left == 0:
        error_sound.play()
        reset_timer()  # Reset the timer to the initial time limit
        switch_players()  # Switch players after resetting the timer
        


    elif time_left > 0:
        timer_id = window.after(1000, update_timer)
    else:
        cancel_timer()  # Stop the timer when time_left becomes negative or the game is over



def undo_move():
    global player, bomb_count, bomb_row, bomb_column, bomb_touched, time_left, sound_condition

    if check_winner() or bomb_touched == 1:
        if sound_condition == 1:
            error_sound.play()
        return
    
    elif moves:
        row, column = moves.pop()
        
        if sound_condition == 1:
            button_click.play()

        if bomb_count == 1:
            if (row, column) == (bomb_row, bomb_column):
                bomb_count = 0
                bomb_row = None
                bomb_column = None
            
        buttons[row][column]['text'] = " "
        buttons[row][column].config(bg=default_grid_color)  
        
        player = players[1] if player == players[0] else players[0]
        label_turn.config(text=player + "'s turn")
        
        change_bg()
        
        # Reset the timer to 5 seconds
        reset_timer()

        if player == 'AI':
            undo_move()
    else:
        if player == 'AI':
            ai_moves()



def empty_space():
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] == " ":
                return True
    return False



def ai_moves():
    global bomb_count, ai_symbol, human_symbol
    count = 0 
    choice = 0

    # If game is done, don't activate
    if check_winner() or bomb_touched == 1:
        return
        
    # If game is ongoing    
    else:
        # Try to find a winning move...
        # ...by horizontal
        for row in range(3):
            count = 0
            for column in range(3):
                if buttons[row][column]['text'] == ai_symbol:
                    count += 1
            if count == 2:
                for column in range(3):
                    if buttons[row][column]['text'] == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return

        #..by vertical
        for column in range(3):
            count = 0
            for row in range(3):
                if buttons[row][column]['text']  == ai_symbol:
                    count += 1
            if count == 2:
                for row in range(3):
                    if buttons [row][column]['text']  == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return

        #...by diagonal
        count = 0
        for row, column in zip(range(3), range(3)):
            if buttons[row][column]['text']  == ai_symbol:
                count += 1
        if count == 2:
                for row, column in zip(range(3), range(3)):
                    if buttons[row][column]['text']  == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return
                     
        count = 0
        for row, column in zip(range(3), range(2, -1, -1)):
            if buttons[row][column]['text']  == ai_symbol:
                count += 1
        if count == 2:
                for row, column in zip(range(3), range(2, -1, -1)):
                    if buttons[row][column]['text'] == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return
            
        #If none, prevent a winning move from enemy...
        #...by horizontal
        for row in range(3):
            count = 0
            for column in range(3):
                if buttons[row][column]['text'] == human_symbol:
                    count += 1
            if count == 2:
                for column in range(3):
                    if buttons[row][column]['text'] == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return

        #..by vertical
        for column in range(3):
            count = 0
            for row in range(3):
                if buttons[row][column]['text']  == human_symbol:
                    count += 1
            if count == 2:
                for row in range(3):
                    if buttons [row][column]['text']  == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return

        #...by diagonal
        count = 0
        for row, column in zip(range(3), range(3)):
            if buttons[row][column]['text']  == human_symbol:
                count += 1
        if count == 2:
                for row, column in zip(range(3), range(3)):
                    if buttons[row][column]['text']  == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return
                     
        count = 0
        for row, column in zip(range(3), range(2, -1, -1)):
            if buttons[row][column]['text']  == human_symbol:
                count += 1
        if count == 2:
                for row, column in zip(range(3), range(2, -1, -1)):
                    if buttons[row][column]['text'] == " " or buttons[row][column]['text'] == "Bomb":
                        next_turn(row, column)
                        return
                     
        
        #Otherwise, Do a random move
        choice = random.choice(range(1, 3))

        #if no bombs planted, and number is even, plant a bomb
        if bomb_count == 0 and choice % 2 == 0:
            place_bomb()
            return
        
        #else pick a random empty square
        else:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]['text'] == " " or buttons[r][c]['text'] == "Bomb"]
            if empty_cells:
                row, column = random.choice(empty_cells)
                next_turn(row, column)
       


def music_function():
    global music_condition, sound_condition

    if music_condition == 1:
        music_button.config(text = "Music: Off")
        music_condition = 0
        pygame.mixer.music.stop()
        if sound_condition == 1:
            button_click.play()
    
    else:
        music_button.config(text = "Music: On")
        music_condition = 1
        pygame.mixer.music.play(-1)
        if sound_condition == 1:
            button_click.play()



def sound_function():
    global sound_condition
    if sound_condition == 1:
        sound_button.config(text = "Sound: Off")
        sound_condition = 0
        button_click.play()

    else:
        sound_button.config(text = "Sound: On")
        sound_condition = 1


    


def change_bg():
    if player == players[0]:
        bg_image.config(image=plyr1bg_path)
        welcome_label.config(fg="#000000",bg="#00DEDE")
        label1.config(fg="#000000",bg="#00DEDE")
        label2.config(fg="#000000",bg="#00DEDE")
        start_button.config(fg="#000000",bg="#00DEDE")
        label_turn.config(bg="light blue", fg="black")
        reset_button.config(fg="#000000",bg="#00DEDE")
        undo_button.config(fg="#000000",bg="#00DEDE")
        if bomb_count == 0:
            bomb_button.config(fg="#000000",bg="#00DEDE", text="Place Bomb", font=('Press Start 2P', 15))
        scoreboard_label.config(bg="light blue")
        music_button.config(fg="#000000",bg="#00DEDE")
        sound_button.config(fg="#000000",bg="#00DEDE")

        
    elif player == players[1]: 
        bg_image.config(image=plyr2bg_path)
        welcome_label.config(fg="#F0F0F0",bg="#7A0000")
        label1.config(fg="#F0F0F0",bg="#7A0000")
        label2.config(fg="#F0F0F0",bg="#7A0000")
        start_button.config(fg="#F0F0F0",bg="#7A0000")
        label_turn.config(bg="red", fg="black")
        reset_button.config(fg="#F0F0F0",bg="#7A0000")
        undo_button.config(fg="#F0F0F0",bg="#7A0000")
        if bomb_count == 0:
                bomb_button.config(fg="#F0F0F0",bg="#7A0000", text="Place Bomb", font=('Press Start 2P', 15))
        scoreboard_label.config(bg="red")
        music_button.config(fg="#F0F0F0",bg="#7A0000")
        sound_button.config(fg="#F0F0F0",bg="#7A0000")



def new_game():
    global player, moves, bomb_count, bomb_touched, timer_id, time_limit, time_left, ai_symbol, human_symbol, game_music, music_condition, sound_condition

    player = random.choice(players)
    label_turn.config(text=player+"'s turn")

    label_turn.config(text="", fg="black")
    for row in range(3):
        for column in range(3):
            buttons[row][column]['text'] = " "
            buttons[row][column].config(bg=default_grid_color)
    moves = []
    
    bomb_count = 0
    bomb_touched = 0

    time_limit = 10  # Resetting time_limit to 5 seconds
    time_left = time_limit  # Resetting time_left to 5 seconds

    change_bg()

    # Cancel any ongoing timer updates and restart the timer
    if timer_id is not None:
        window.after_cancel(timer_id)
    timer_id = window.after(1000, update_timer)

    if players[0] == 'AI':
        ai_symbol = 'X'
        human_symbol = 'O'  
    elif players[1] == 'AI':
        ai_symbol = 'O'
        human_symbol = 'X'

    if player == 'AI':
        ai_moves() 

    pygame.mixer.music.load(game_music)
    if music_condition == 1:
        pygame.mixer.music.play(-1)

    if sound_condition == 1:
        button_click.play()


def start_game():
    global player, players, player_scores, moves, bomb_count, bomb_touched, ai_symbol, human_symbol, game_music, music_condition, sound

    player1 = entry1.get().strip()
    player2 = entry2.get().strip()

    if player1 == player2:
        label_turn.config(text="Player names need to be different!")
        if sound_condition == 1:
            error_sound.play()
        return
    
    if player1.lower() == "ai":
        player1 = player1.upper()

    elif player2.lower() == "ai":
        player2 = player2.upper()

    start_button.config(text="Reset")
    players = [player1, player2]
    player_scores = {player1: 0, player2: 0}
    
    player = random.choice(players)
    
    bomb_count = 0
    bomb_touched = 0

    for row in range(3):
        for column in range(3):
            buttons[row][column]['text'] = " "
            buttons[row][column].config(bg=default_grid_color)
    
    label_turn.config(text=player+"'s turn")
    change_bg()
    update_scoreboard()
    moves = []

    # Initializes needed values for AI
    if players[0] == 'AI':
        ai_symbol = 'X'
        human_symbol = 'O'  
    elif players[1] == 'AI':
        ai_symbol = 'O'
        human_symbol = 'X'  
    

    # Start the timer countdown
    update_timer()
    if player == 'AI':
        ai_moves()

    pygame.mixer.music.load(game_music)
    if music_condition == 1:
        pygame.mixer.music.play(-1)
    if sound_condition == 1:
        button_click.play()


image_path = PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Images\Main Menu.png")
plyr1bg_path = PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Images\Blue.png")
plyr2bg_path = PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Images\Red.png")

bg_image = tk.Label(window, image=image_path)
bg_image.place(relheight=1, relwidth=1)

welcome_label = tk.Label(window, text="Welcome to Tic-Tac-BOOM!!! Have Fun!", font=('Press Start 2P', 22), bg="#00DEDE") 
welcome_label.pack(side="top", padx=9, pady=10)

label1 = tk.Label(window, text="Enter Player 1 Name: ", font=('Press Start 2P', 18), bg="#00DEDE")
label1.pack(side="top", padx=9, pady=10)

entry1 = tk.Entry(window, font=('Pixelmix', 18))
entry1.pack(side="top", padx=9, pady=10)

label2 = tk.Label(window, text="Enter Player 2 Name: ", font=('Press Start 2P', 18), bg="#00DEDE")
label2.pack(side="top", padx=9, pady=10)

entry2 = tk.Entry(window, font=('Pixelmix', 18))
entry2.pack(side="top", padx=9, pady=10)

start_button = tk.Button(window, text="Start Game", font=('Press Start 2P', 15), command=start_game, width=10, bg="#00DEDE")
start_button.pack(side="top", padx=9, pady=10)

label_turn = tk.Label(window, text="", font=('Press Start 2P', 18), bg="light blue")
label_turn.pack(side="top", padx=9, pady=10)

reset_button = tk.Button(text="Restart", font=('Press Start 2P', 15), command=new_game, width=10, bg="#00DEDE")
reset_button.pack(side="top", padx=9, pady=10)

undo_button = tk.Button(text="Undo", font=('Press Start 2P', 15), command=undo_move, width=10, bg="#00DEDE")
undo_button.pack(side="top", padx=9, pady=10)

bomb_button = tk.Button(text="Place Bomb", font=('Press Start 2P', 15), command=place_bomb, width=10, bg="#00DEDE")
bomb_button.pack(side="top", padx=9, pady=10)

music_button = tk.Button(text = "Music: On", font=('Press Start 2P', 15), command= music_function , width=10, bg="#00DEDE")
music_button.place(relx = 0.75, rely = 0.53, anchor ='ne')

sound_button = tk.Button(text = "Sound: On", font=('Press Start 2P', 15), command= sound_function , width=10, bg="#00DEDE")
sound_button.place(relx = 0.75, rely = 0.6, anchor ='ne')


buttons = []
moves = [] 
frame = tk.Frame(window, bg=default_grid_color)
frame.pack(side="top", padx=9, pady=10)

for row in range(3):
    button_row = []  
    for column in range(3):
        button = tk.Button(frame, text=" ", font=('Pixelmix', 12), width=25, height=2, bg=default_grid_color, command=lambda row=row, column=column: next_turn(row, column))
        button.grid(row=row, column=column)
        button_row.append(button)  
    buttons.append(button_row) 


scoreboard_label = tk.Label(window, text="Scoreboard:", font=('Pixelmix', 11), bg="light blue", width=20)
scoreboard_label.pack(side="bottom", padx=9, pady=10) 

time_limit = 10
time_label = tk.Label(window, text="", font=('Press Start 2P', 12), bg=default_grid_color)
time_label.pack(side="top", padx=9, pady=10)  

player = None
players = []
player_scores = {}
bomb_count = 0
bomb_row = None
bomb_column = None
bomb_touched = 0
time_left = time_limit

window.mainloop()

    #Acknowledgements:
#   FONTS:
#       Pixelmix - Andrew Tyler[@andrewtyler.net]
#       Press Start 2P - Cody Boisclair [cody@zone38.net]
#   Images:
#       3157822 - "Designed by Freepik" <a href="http://www.freepik.com">Designed by Freepik</a>
#       3203855 - "Designed by Freepik" <a href="http://www.freepik.com">Designed by Freepik</a>
# the base concept and some design were inspired by Python Tic Tac Toe game tutorial  by Bro Code  https://www.youtube.com/watch?v=V9MbQ2Xl4CE&t=181s
#   Music:
#        Songs by megupets, for more go to megupets.com - https://opengameart.org/content/insert-coin
#                                                       - https://opengameart.org/content/raining-bits
#        Gundatsch - https://soundcloud.com/gundatsch   - https://opengameart.org/content/raining-bits
#       
#
#   Soundeffects:
#       @shades      - https://soundcloud.com/noshades  - https://opengameart.org/content/8-bit-sound-effect-pack-vol-001
#       Jesús Lastra                                    - https://opengameart.org/content/8-bit-powerup-1   




#Done/Documentation of changes from prior version: 
#changed condition of undo_move funct
#changed color of boxes and buttons
#replaced currents font to something more approriate
#changed color layout of program PER TURN
#fonts used
    #for board & user input = Pixelmix
    #for bold letters = Press Start 2P
#IMPORTED LOGO 
#gave credits to orignal creator of image and original creator of fonts
#changed layout of buttons




#2nd batch of changes
#changed syntax of place_bomb function
#changed bomb tracking system
#instead of checking the bomb position coordinates to see if player touched the bomb
#it will instead check if the button that the player touched has an invisible string which spells "bomb" [changes are located at next turn function]
#modified undo button so that it would also undo "place_bomb" move
#fix the condition for "tie" so it wont activate if a bomb has been placed.
#bomb_touched = used to stop stacking of losses of player accidentally double clicking a bomb in the same round, along with nullifying undo_move
#prevented a bug involving the two users having the same name[start_game function]

#3rd batch of changes 06/05/2024
#Changed the resetting of bomb_count / bomb_touched from the "end_game" function to "New_game"/ "start_game function"
#Made the file into a local drive, para di na need mag bago ng path names kada change ng laptop.
#binago yung changes na mangyayari sa label ng "player wins" if bomb_touched. imbis na pula ang bg, naging black. tas yung font naging yellow. [end_game function]

#finals updated 
#ai function 6/09/2024 -> 6/10/ 2024
#timer function 6/11/2024 -> 6/12/2024
#sound button function 6/24/2024 -> 6/26/2024
#music button function 6/26/2024/ -> 6/29/2024

