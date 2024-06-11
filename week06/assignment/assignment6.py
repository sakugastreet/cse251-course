"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Joseph Earl>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, to_bagger_conn, delay, marble_count, marbles_per_bag):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.to_bagger_conn = to_bagger_conn
        self.delay = delay
        self.marbles_per_bag = marbles_per_bag
        self.marble_count = marble_count

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        marbles_sent = 0
        for _ in range(self.marble_count):
            marble = random.choice(self.colors)
            self.to_bagger_conn.send(marble)
            marbles_sent += 1

            time.sleep(self.delay)
            if marbles_sent >= self.marbles_per_bag:
                self.to_bagger_conn.send(None)
                
                marbles_sent = 0
        self.to_bagger_conn.send(True)
            
            


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, from_creator_conn, to_assembler_conn, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.from_creater_conn = from_creator_conn
        self.to_assembler_conn = to_assembler_conn
        self.delay = delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag = Bag()
        while (True):
            marble = self.from_creater_conn.recv()
            if marble == None:
                self.to_assembler_conn.send(bag)
                bag.items = []
            elif marble == True:
                print("end of marbles")
                self.to_assembler_conn.send(None)
                break
            else:
                bag.add(marble)
                time.sleep(self.delay)
            



class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, from_bagger_conn, to_wrapper_conn, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.from_bagger_conn = from_bagger_conn
        self.to_wrapper_conn = to_wrapper_conn
        self.delay = delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while (True):
            bag = self.from_bagger_conn.recv()
            if bag == None:
                self.to_wrapper_conn.send(None)
                break

            gift = Gift(random.choice(self.marble_names), bag)
            self.to_wrapper_conn.send(gift)
            time.sleep(self.delay)




class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, to_wrapper_conn, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.to_wrapper_conn = to_wrapper_conn
        self.delay = delay

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        box = ""
        while (True):
            line = ""
            gift = self.to_wrapper_conn.recv()
            if gift == None:
                break

            line += f"Created - {datetime.now().time()}: Large marble: {gift.large_marble}, marbles: "
            for marble in gift.marbles.items:
                line += f"{marble}, "
            line = line[:-2]
            line += "\n"

            box += line
            
            
            
            
        with open(BOXES_FILENAME, "w") as file:
            file.write(box)


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    to_bagger_conn, from_creator_conn = mp.Pipe()
    to_assembler_conn, from_bagger_conn = mp.Pipe()
    to_wrapper_conn, from_assembler_conn = mp.Pipe()
    # TODO create variable to be used to count the number of gifts
    mp.Value("i", 0)
    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')
    
    # TODO Create the processes (ie., classes above)
    marc = Marble_Creator(to_bagger_conn, settings[CREATOR_DELAY], settings[MARBLE_COUNT], settings[NUMBER_OF_MARBLES_IN_A_BAG])
    bagg = Bagger(from_creator_conn, to_assembler_conn, settings[BAGGER_DELAY])
    asem = Assembler(from_bagger_conn, to_wrapper_conn, settings[ASSEMBLER_DELAY])
    kdot = Wrapper(from_assembler_conn, settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    # TODO add code here
    marc.start()
    bagg.start()
    asem.start()
    kdot.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    marc.join()
    bagg.join()
    asem.join()
    kdot.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.




if __name__ == '__main__':
    main()

