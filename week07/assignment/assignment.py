"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Joseph Earl>
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

I chose to use pool sizes of 6, as that was what gave me the fastest time. This submission meets all the requirements for a category 4.

"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def log_results(results, result_list):
        result_list.append(results)

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        return f"{value} is prime"
    else:
        return f"{value} is not prime"



def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt", "r") as file:
        for line in file:
            if word == line.strip():
                return f"{word} Found"
            
        return f"{word} not found"

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return text.upper()

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    
    total = sum(range(start_value, end_value + 1))
    response = f"sum of {start_value} to {end_value} = {total}"
    return response

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        name = response.json().get('name', 'Unknown')
        return f"{url} has name {name}"
    except requests.RequestException:
        return f"{url} had an error receiving the information"


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pools = [mp.Pool(6) for _ in range(5)]
    # TODO you can change the following
    # TODO start and wait pools

    
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        print()
        print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            r1 = pools[0].apply_async(task_prime, (task['value'], ), callback= lambda res: log_results(res, result_primes))
        elif task_type == TYPE_WORD:
            r2 = pools[1].apply_async(task_word, (task['word'], ), callback= lambda res: log_results(res, result_words))
        elif task_type == TYPE_UPPER:
            r3 = pools[2].apply_async(task_upper, (task['text'], ), callback= lambda res: log_results(res, result_upper))
        elif task_type == TYPE_SUM:
            r4 = pools[3].apply_async(task_sum, (task['start'], task["end"]), callback= lambda res: log_results(res, result_sums))
        elif task_type == TYPE_NAME:
            r5 = pools[4].apply_async(task_name, (task['url'], ), callback= lambda res: log_results(res, result_names))

        else:
            log.write(f'Error: unknown task type {task_type}')


    for pool in pools:
        pool.close()

    for pool in pools:
        pool.join()



    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
