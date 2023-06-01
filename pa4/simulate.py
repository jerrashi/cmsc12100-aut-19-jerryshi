'''
Polling places

YOUR NAME(s) HERE

Main file for polling place simulation
'''

import sys
import random
import queue
import click
import util



### YOUR Voter class GOES HERE.


class Precinct(object):

    def __init__(self, name, hours_open, max_num_voters,
                 arrival_rate, voting_duration_rate):
        '''
        Constructor for the Precint class

        Input:
            name: (str) Name of the precinct
            hours_open: (int) Hours the precinct will remain open
            max_num_voters: (int) number of voters in the precinct
            arrival_rate: (float) rate at which voters arrive
            voting_duration_rate: (float) lambda for voting duration
        '''

        # YOUR CODE HERE

        # REPLACE "pass" with your constructor implementation
        pass


    def simulate(self, seed, num_booths):
        '''
        Simulate a day of voting

        Input:
            seed: (int) Random seed to use in the simulation
            num_booths: (int) Number of booths to use in the simulation

        Output:
            List of voters who voted in the precinct
        '''

        # REPLACE [] with appropriate return value
        return []


### YOUR VotingBooths class GOES HERE.


def find_avg_wait_time(precinct, num_booths, ntrials, initial_seed=0):
    '''
    Simulates a precinct multiple times with a given number of booths
    For each simulation, computes the average waiting time of the voters,
    and returns the median of those average waiting times.

    Input:
        precinct: (dictionary) A precinct dictionary
        num_booths: (int) The number of booths to simulate the precinct with
        ntrials: (int) The number of trials to run
        initial_seed: (int) initial seed for random number generator

    Output:
        The median of the average waiting times returned by simulating
        the precinct 'ntrials' times.
    '''

    # YOUR CODE HERE.

    # REPLACE 0.0 with the waiting time this function computes
    return 0.0


def find_number_of_booths(precinct, target_wait_time, max_num_booths,
                          ntrials, seed=0):
    '''
    Finds the number of booths a precinct needs to guarantee a bounded
    (average) waiting time.

    Input:
        precinct: (dictionary) A precinct dictionary
        target_wait_time: (float) The desired (maximum) waiting time
        max_num_booths: (int) The maximum number of booths this
                        precinct can support
        ntrials: (int) The number of trials to run when computing
                 the average waiting time
        seed: (int) A random seed

    Output:
        A tuple (num_booths, waiting_time) where:
        - num_booths: (int) The smallest number of booths that ensures
                      the average waiting time is below target_waiting_time
        - waiting_time: (float) The actual average waiting time with that
                        number of booths

        If the target waiting time is infeasible, returns (0, None)
    '''

    # YOUR CODE HERE

    # REPLACE (0,0) with a tuple containing the optimal number of booths
    # and the average waiting time for that number of booths
    return (0, 0)


# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, len-as-condition, too-many-locals
# pylint: disable-msg= missing-docstring, too-many-branches
# pylint: disable-msg= line-too-long
@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--max-num-booths', type=int)
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, max_num_booths, target_wait_time, print_voters):
    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = {}
        for p in precincts:
            precinct = Precinct(p["name"], p["hours_open"], p["num_voters"],
                                p["voter_distribution"]["arrival_rate"],
                                p["voter_distribution"]["voting_duration_rate"])
            voters[p["name"]] = precinct.simulate(seed, p["num_booths"])
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    sys.exit(-1)
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        if max_num_booths is None:
            max_num_booths = precinct["num_voters"]

        nb, avg_wt = find_number_of_booths(precinct, target_wait_time, max_num_booths, 20, seed)

        if nb == 0:
            msg = "The target wait time ({:.2f}) is infeasible"
            msg += " in precint '{}' with {} or less booths"
            print(msg.format(target_wait_time, precinct["name"], max_num_booths))
        else:
            msg = "Precinct '{}' can achieve average waiting time"
            msg += " of {:.2f} with {} booths"
            print(msg.format(precinct["name"], avg_wt, nb))


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
