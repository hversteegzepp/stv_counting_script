import csv
from fractions import Fraction
from dataclasses import dataclass

# for fully blank ballots, omit entry in CSV input file
# for partially filled out ballots, only add the given preferences in order

num_seats: int = 3  # number of fillable seats


@dataclass
class WeightedBallot:
    preferences: list
    weight: Fraction


with open('votes.csv', 'r') as votes_file:
    csv_reader = csv.reader(votes_file)
    # combined list of ballot votes + current round weights
    # remove empty preference spots
    ballot_list = [
        WeightedBallot(preferences=[preference for preference in ballot if preference], weight=Fraction(1))
        for ballot in csv_reader
    ]

# collect all candidate names which appear on at least one ballot
remaining_candidates = set()
for ballot in ballot_list:
    remaining_candidates.update(ballot.preferences)

# keep track of which candidates have been elected or eliminated
elected_candidates = set()
eliminated_candidates = set()

while num_seats > len(elected_candidates):
    # determine number of non-blank ballots still participating and corresponding quotum
    num_ballots: int = len(ballot_list)
    quotum: Fraction = Fraction(num_ballots, num_seats + 1)

    # dict with candidate names as keys and total round vote count as values
    round_results = {candidate: Fraction(0) for candidate in remaining_candidates}
    for ballot in ballot_list:
        round_results[ballot.preferences[0]] += ballot.weight

    max_votes = max(round_results.values())
    min_votes = min(round_results.values())
    if max_votes >= quotum:
        # one or more candidates are electable
        candidates_to_elect = [candidate for candidate, votes in round_results.items() if votes == max_votes]
        if len(candidates_to_elect) <= (num_seats - len(elected_candidates)):
            pass  # all elected
        else:
            # one elected at random
            rand_user_input = int(input(f'Enter random integer from 1 to {len(candidates_to_elect)}: '))
            candidates_to_elect = [list(candidates_to_elect)[rand_user_input - 1]]
        elected_candidates.update(candidates_to_elect)
        # update ballot weights
        for ballot in ballot_list:
            # ballots with elected candidate as current top preference have their weight reduced
            if ballot.preferences[0] in candidates_to_elect:
                votes_for_candidate = round_results[ballot.preferences[0]]
                ballot.weight = ballot.weight * Fraction((votes_for_candidate - quotum), votes_for_candidate)
    else:
        # one candidate must be eliminated
        candidates_to_eliminate = [candidate for candidate, votes in round_results.items() if votes == min_votes]
        if len(candidates_to_eliminate) == 1:
            # one eliminated
            eliminated_candidates.add(candidates_to_eliminate[0])
        else:
            # one eliminated at random
            rand_user_input = int(input(f'Enter random integer from 1 to {len(candidates_to_eliminate)}: '))
            eliminated_candidates.add(list(candidates_to_eliminate)[rand_user_input - 1])
        # ballot weights stay the same

    # remove names of all elected and eliminated candidates so far from ballots and remaining candidates set
    for candidate_to_remove in elected_candidates | eliminated_candidates:
        for ballot in ballot_list:
            ballot.preferences = [candidate for candidate in ballot.preferences if candidate != candidate_to_remove]
        if candidate_to_remove in remaining_candidates:
            remaining_candidates.remove(candidate_to_remove)

    # remove ballots and corresponding weights with no remaining preferences (blank votes from now on)
    # non-blank votes with a weight of zero are kept, as they are still count towards determining the quotom
    ballot_list = [ballot for ballot in ballot_list if ballot.preferences]

    print('eliminated: ' + ', '.join(eliminated_candidates))
    print('elected   : ' + ', '.join(elected_candidates))
