# STV Voting Script

A Python script for counting votes in an election where the Single Transferable Vote (STV) principle is used.
Partial or fully blank votes are supported, votes with the same preference number for multiple candidates are not.
In any given round, the quotum of (weighted) votes which must be equaled or exceeded to get elected in a given round, is equal to the number of remaining non-blank votes in that round divided by one more than the total number of seats available.
Leftover votes after election/elimination are carried over fully using exact fractions.
Ties are resolved with manual user input.

# Requirements

Only a compatible version of Python must be installed to be able to run the script.
No other python packages are required, hence a system-wide Python environment can be used.

The script has only been tested with [Python 3.12.0](https://www.python.org/downloads/release/python-3120/) on Windows, which is thus the recommended setup.
Later Python versions will likely also work, but have not been tested.
Some earlier versions may also work.

Make sure Python is accessible with the `python` command system-wide by adding it to the `PATH` environment variable in Windows.

# Input File

The input file should be a plain text CSV file, with the names of candidates as the first row / header, for example:

    "Candidate 1","Candidate 2","Candidate 3","Candidate 4"

Each subsequent row should contain the preference order number for each of the candidates as a string (an empty choice/blank vote is allowed for any candidate and any preference number), for example:

    "3","1","","4"

The file `example_votes.csv` is provided as a valid example.

# Usage

To run the script and generate the list of elected candidates, run the following command in the same directory as the script:

    python stv_counting_script.py --seats=<number of seats available> --file=<path to voting results file>

The number of seats that are available / up for election can range from 1 to the number of candidates.

If a tie occurs during the counting process (for either elimination or election), the script will ask for a manual random number input to determine the outcome.
This is done to allow for reproduction of the results by recording the random input used.
Making sure this number is fair/unbiased is left to the user, for example by generating it with a die roll or coin toss.

This feature can be tried with the `example_votes.csv` file, which is set up such that a tie occurs if 1 or 3 seats are available:

    python stv_counting_script.py --seats=3 --file=example_votes.csv
