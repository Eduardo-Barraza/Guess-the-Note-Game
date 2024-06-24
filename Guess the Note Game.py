import random
import time
from midiutil import MIDIFile
import pygame

# Define note sets for each difficulty level
MAJOR_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
SHARP_FLAT_NOTES = ['C#', 'D#', 'F#', 'G#', 'A#', 'Db', 'Eb', 'Gb', 'Ab', 'Bb']

EASY_LEVEL_TURNS = 15
MEDIUM_LEVEL_TURNS = 15
HARD_LEVEL_TURNS = 10

# Define a placeholder logo
logo = """ 
        GGGGGGGGGGGGG                                                                                      tttt         hhhhhhh                                           NNNNNNNN        NNNNNNNN                          tttt                              
     GGG::::::::::::G                                                                                   ttt:::t         h:::::h                                           N:::::::N       N::::::N                       ttt:::t                              
   GG:::::::::::::::G                                                                                   t:::::t         h:::::h                                           N::::::::N      N::::::N                       t:::::t                              
  G:::::GGGGGGGG::::G                                                                                   t:::::t         h:::::h                                           N:::::::::N     N::::::N                       t:::::t                              
 G:::::G       GGGGGGuuuuuu    uuuuuu      eeeeeeeeeeee        ssssssssss       ssssssssss        ttttttt:::::ttttttt    h::::h hhhhh           eeeeeeeeeeee              N::::::::::N    N::::::N   ooooooooooo   ttttttt:::::ttttttt        eeeeeeeeeeee    
G:::::G              u::::u    u::::u    ee::::::::::::ee    ss::::::::::s    ss::::::::::s       t:::::::::::::::::t    h::::hh:::::hhh      ee::::::::::::ee            N:::::::::::N   N::::::N oo:::::::::::oo t:::::::::::::::::t      ee::::::::::::ee  
G:::::G              u::::u    u::::u   e::::::eeeee:::::eess:::::::::::::s ss:::::::::::::s      t:::::::::::::::::t    h::::::::::::::hh   e::::::eeeee:::::ee          N:::::::N::::N  N::::::No:::::::::::::::ot:::::::::::::::::t     e::::::eeeee:::::ee
G:::::G    GGGGGGGGGGu::::u    u::::u  e::::::e     e:::::es::::::ssss:::::ss::::::ssss:::::s     tttttt:::::::tttttt    h:::::::hhh::::::h e::::::e     e:::::e          N::::::N N::::N N::::::No:::::ooooo:::::otttttt:::::::tttttt    e::::::e     e:::::e
G:::::G    G::::::::Gu::::u    u::::u  e:::::::eeeee::::::e s:::::s  ssssss  s:::::s  ssssss            t:::::t          h::::::h   h::::::he:::::::eeeee::::::e          N::::::N  N::::N:::::::No::::o     o::::o      t:::::t          e:::::::eeeee::::::e
G:::::G    GGGGG::::Gu::::u    u::::u  e:::::::::::::::::e    s::::::s         s::::::s                 t:::::t          h:::::h     h:::::he:::::::::::::::::e           N::::::N   N:::::::::::No::::o     o::::o      t:::::t          e:::::::::::::::::e 
G:::::G        G::::Gu::::u    u::::u  e::::::eeeeeeeeeee        s::::::s         s::::::s              t:::::t          h:::::h     h:::::he::::::eeeeeeeeeee            N::::::N    N::::::::::No::::o     o::::o      t:::::t          e::::::eeeeeeeeeee  
 G:::::G       G::::Gu:::::uuuu:::::u  e:::::::e           ssssss   s:::::s ssssss   s:::::s            t:::::t    tttttth:::::h     h:::::he:::::::e                     N::::::N     N:::::::::No::::o     o::::o      t:::::t    tttttte:::::::e           
  G:::::GGGGGGGG::::Gu:::::::::::::::uue::::::::e          s:::::ssss::::::ss:::::ssss::::::s           t::::::tttt:::::th:::::h     h:::::he::::::::e                    N::::::N      N::::::::No:::::ooooo:::::o      t::::::tttt:::::te::::::::e          
   GG:::::::::::::::G u:::::::::::::::u e::::::::eeeeeeee  s::::::::::::::s s::::::::::::::s            tt::::::::::::::th:::::h     h:::::h e::::::::eeeeeeee            N::::::N       N:::::::No:::::::::::::::o      tt::::::::::::::t e::::::::eeeeeeee  
     GGG::::::GGG:::G  uu::::::::uu:::u  ee:::::::::::::e   s:::::::::::ss   s:::::::::::ss               tt:::::::::::tth:::::h     h:::::h  ee:::::::::::::e            N::::::N        N::::::N oo:::::::::::oo         tt:::::::::::tt  ee:::::::::::::e  
        GGGGGG   GGGG    uuuuuuuu  uuuu    eeeeeeeeeeeeee    sssssssssss      sssssssssss                   ttttttttttt  hhhhhhh     hhhhhhh    eeeeeeeeeeeeee            NNNNNNNN         NNNNNNN   ooooooooooo             ttttttttttt      eeeeeeeeeeeeee  

 """

# Initialize pygame mixer for MIDI playback
pygame.init()
pygame.mixer.init()


# Function to play a note using MIDI
def play_note(note):
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time_position = 0
    duration = 1
    volume = 100

    note_to_midi = {
        'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63, 'E': 64,
        'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68, 'Ab': 68, 'A': 69,
        'A#': 70, 'Bb': 70, 'B': 71
    }

    midi_note = note_to_midi[note]

    midi.addTrackName(track, time_position, "Track")
    midi.addTempo(track, time_position, 120)
    midi.addProgramChange(track, channel, time_position, 1)
    midi.addNote(track, channel, midi_note, time_position, duration, volume)

    with open("note.mid", 'wb') as output_file:
        midi.writeFile(output_file)

    # Play the note using pygame
    pygame.mixer.music.load("note.mid")
    pygame.mixer.music.play()
    time.sleep(duration + 1)
    pygame.mixer.music.stop()


# Function to check user's guess against actual answer
def check_answer(guess, answer, turns):
    if guess == answer:
        print(f"You got it! The answer was {answer}.")
        return True
    else:
        print("Wrong guess.")
        return turns - 1


# Function to set difficulty
def set_difficulty():
    level = input("Choose a difficulty. Type 'easy', 'medium', or 'hard': ").lower()
    if level == "easy":
        return EASY_LEVEL_TURNS, MAJOR_NOTES
    elif level == "medium":
        return MEDIUM_LEVEL_TURNS, MAJOR_NOTES + SHARP_FLAT_NOTES
    elif level == "hard":
        return HARD_LEVEL_TURNS, MAJOR_NOTES + SHARP_FLAT_NOTES
    else:
        print("Invalid difficulty level. Setting to easy by default.")
        return EASY_LEVEL_TURNS, MAJOR_NOTES


# Game function
def game():
    print(logo)
    print("Welcome to the Note Guessing Game!")

    turns, notes = set_difficulty()
    answer = random.choice(notes)
    play_note(answer)

    guess = ""
    while guess != answer and turns > 0:
        print(f"You have {turns} attempts remaining to guess the note.")
        guess = input("Make a guess: ").capitalize()

        if guess not in notes:
            print("Invalid note. Try again.")
            continue

        turns = check_answer(guess, answer, turns)
        if turns == True:
            return
        elif turns == 0:
            print(f"You've run out of guesses, you lose. The correct answer was {answer}.")
            return
        else:
            print("Guess again.")
            play_note(answer)


if __name__ == "__main__":
    game()
