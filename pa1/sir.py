'''
Epidemic modelling

Jerry Shi

Functions for running a simple epidemiological simulation
'''

import random

import click

# This seed should be used for debugging purposes only!  Do not refer
# to it in your code.
TEST_SEED = 20170217

def count_ever_infected(city):
    '''
    Count the number of people infected or recovered

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
    Returns (int): count of the number of people who have been
      infected at some time.
    '''

    count = 0

    for p in city:
        if p != "S":
            count = count + 1

    return count


def has_an_infected_neighbor(city, position):
    '''
    Determine whether a person has an infected neighbor

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check

    Returns:
      True, if the person has an infected neighbor, False otherwise.
    '''

    # method to check if neighbor exists inspired by StackOverflow post at stackoverflow.com/questions/843277/how-do-i-check-of-a-variable-exists

    assert city[position] == "S"

    leftneighbor = position - 1

    rightneighbor = position + 1

    last = len(city) - 1



    if position == 0:
        if len(city) == 1:
    	    return False
        elif city[rightneighbor] != "S" and city[rightneighbor] != "R":
            return True
        else:
            return False

    elif position == last:
        if city[leftneighbor] != "S" and city[leftneighbor] != "R":
            return True
        else:
            return False

    else:
        if city[leftneighbor] != "S" and city[leftneighbor] != "R":
            return True
        elif city[rightneighbor] != "S" and city[rightneighbor] != "R":
            return True
        else:
            return False




def gets_infected_at_position(city, position, infection_rate):
    '''
    Determine whether the person at the specified position gets
    infected.

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check
      infection_rate (float): the chance of getting infected given an
        infected neighbor


    Returns (boolean):
      True, if the person would become infected, False otherwise.
    '''
    # This function should only be called when the person at position
    # is susceptible to infection.

    assert city[position] == "S"

    if has_an_infected_neighbor(city, position) == True:
        immune_level = random.random()
        if immune_level < infection_rate:
        	return True
        else:
            return False
    else:
        return False


def advance_person_at_position(city, position,
                               infection_rate, days_contagious):
    '''
    Compute the next state for the person at the specified position.

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check
      infection_rate (float): the chance of getting infected given an
        infected neighbor
      days_contagious (int): the number of a days a person is infected

    Returns: (string) disease state of the person after one day
    '''

    if city[position] == "R":
        return "R"
    elif city[position] == "S":
        if gets_infected_at_position(city, position, infection_rate) == True:
            return "I0"
        else:
        	return "S"
    else:
        disease_state = city[position].replace("I", "")
        disease_state = int(disease_state)
        if disease_state + 1 < days_contagious:
        	return "I" + str(disease_state + 1)
        else:
        	return "R"


def simulate_one_day(starting_city, infection_rate, days_contagious):
    '''
    Move the simulation forward a single day.

    Inputs:
      starting_city (list): the state of all people in the simulation at the
        start of the day
      infection_rate (float): the chance of getting infected given an
        infected neighbor
      days_contagious (int): the number of a days a person is infected
    Returns:
      new_city (list): disease state of the city after one day
    '''

    length = len(starting_city)
    resident = 0
    new_city = []
    while resident < length:
        new_status = advance_person_at_position(starting_city, resident, infection_rate, days_contagious)
        new_city.append(new_status)
        resident = resident + 1
    else:
        return new_city

def run_simulation(starting_city, random_seed, max_num_days,
                   infection_rate, days_contagious):
    '''
    Run the entire simulation for up to the specified maximum number
    of days.

    Inputs:
      starting_city (list): the state of all people in the city at the
        start of the simulation
      random_seed (int): the random seed to use for the simulation
      max_num_days (int): the maximum days of the simulation
      infection_rate (float): the chance of getting infected given an
        infected neighbor
      days_contagious (int): the number of a days a person is infected

    Returns tuple (list of strings, int): the final state of the city
      and the number of days actually simulated.
    '''

    assert max_num_days > 0

    random.seed(random_seed)
    
    new_city = simulate_one_day(starting_city, infection_rate, days_contagious)
    days_passed = 1

    if new_city == starting_city:
    	return (new_city, days_passed)
    else:
	    while days_passed < max_num_days:
	        possible_new_city = simulate_one_day(new_city, infection_rate, days_contagious)
	        if possible_new_city != new_city:
	            new_city = possible_new_city
	            days_passed = days_passed + 1
	        else:
	            return (new_city, days_passed + 1)
	    else:
	        return (new_city, days_passed)

def calc_avg_num_newly_infected(
        starting_city, random_seed, max_num_days,
        infection_rate, days_contagious, num_trials):
    '''
    Conduct N trials with the specified infection probability and
    calculate the number of people on average get infected over time.

    Inputs:
      starting_city (list): the state of all people in the city at the
        start of the simulation
      random_seed (int): the starting random seed. Use this value for
        the FIRST simulation, and then increment it once for each
        subsequent run.
      max_num_days (int): the maximum days of the simulation
      infection_rate (float): the chance of getting infected given an
        infected neighbor
      days_contagious (int): the number of a days a person is infected
      num_trials (int): the number of trials to run

    Returns (float): the average number of people infected over time
    '''
    assert max_num_days >= 0
    assert num_trials > 0

    total_infected = 0
    trials_conducted = 0

    while trials_conducted < num_trials:
    	(new_city, days_passed) = run_simulation(starting_city, random_seed, max_num_days, infection_rate, days_contagious)
    	total_infected = total_infected + count_ever_infected(new_city) - count_ever_infected(starting_city)
    	random_seed = random_seed + 1
    	trials_conducted = trials_conducted + 1

    average_infected = float(total_infected/trials_conducted)

    return average_infected


################ Do not change the code below this line #######################


@click.command()
@click.argument("city", type=str)
@click.option("--random_seed", default=None, type=int)
@click.option("--max-num-days", default=1, type=int)
@click.option("--infection-rate", default=0.5, type=float)
@click.option("--days-contagious", default=2, type=int)
@click.option("--num-trials", default=1, type=int)
@click.option("--task-type", default="single",
              type=click.Choice(['single', 'average']))
def cmd(city, random_seed, max_num_days, infection_rate,
        days_contagious, num_trials, task_type):
    '''
    Process the command-line arguments and do the work.
    '''

    # Convert the city string into a city list.
    city = [p.strip() for p in city.split(",")]
    emsg = ("Error: people in the city must be susceptible ('S'),"
            " recovered ('R'), or infected ('Ix', where *x* is an integer")
    for p in city:
        if p[0] == "I":
            try:
                _ = int(p[1])
            except ValueError:
                print(emsg)
                return -1
        elif p not in {"S", "R"}:
            print(emsg)
            return -1

    if task_type == "single":
        print("Running one simulation...")
        final_city, num_days_simulated = run_simulation(
            city, random_seed, max_num_days, infection_rate, days_contagious)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials...")
        avg_infected = calc_avg_num_newly_infected(
            city, random_seed, max_num_days, infection_rate,
            days_contagious, num_trials)
        msg = "Over {} trial(s), on average, {:3.1f} people were infected"
        print(msg.format(num_trials, avg_infected))

    return 0


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
