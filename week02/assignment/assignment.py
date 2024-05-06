"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):

    def __init__(self, url):
        threading.Thread.__init__(self)
        inc_call_count()
        self.url = url
        self.data = {}

    def run(self):
        response = requests.get(self.url)
        
        if response.status_code == 200:
            self.data = response.json
        else:
            self.data = {'RESPONSE = ', response.status_code}

# TODO Add any functions you need here
def inc_call_count():
    global call_count
    call_count += 1

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    log.write("-----------------------------------------")

    # TODO Retrieve Top API urls
    t1 = Request_thread(fr"{TOP_API_URL}")
    t1.start()
    t1.join()

    thread_list = []

    # TODO Retireve Details on film 6
    t2 = Request_thread(fr"{t1.data()["films"]}6")
    t2.start()
    t2.join()

    log.write(f"Title   : {t2.data()['title']}")
    log.write(f"Director: {t2.data()['director']}")
    log.write(f"Producer: {t2.data()['producer']}")
    log.write(f"Released: {t2.data()['release_date']}")
    log.write_blank_line()


    for item in t2.data():
        if type(t2.data()[item]) == list:
            # creating a list to hold all the things in that category
            category = []
            names = []
            for url in t2.data()[item]:
                cat_name = item.capitalize()
                new_thread = Request_thread(url)
                category.append(new_thread)
                new_thread.start()

            for thread in category:
                thread.join()
                names.append(thread.data()["name"])

            names.sort()
            log.write(f"{cat_name}: {category.__len__()}")
            final_string = ""
            for name in names:
                final_string += name + ", "
            
            log.write(final_string)
            log.write_blank_line()



    

        


    # TODO Display results

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
