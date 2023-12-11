#! /usr/local/bin/python3.11

from collections import defaultdict
from typing import List, Set, Dict
import attr
import re
from pprint import pprint
from functools import total_ordering
from copy import copy

@attr.s(slots=True, auto_attribs=True)
class Solution:

    input_file: str

    def calculate_history(self, sequence):
        seq = next_seq = sequence
        total_seq = [sequence]
        while True:
            vibes = []
            for i in range(len(total_seq[-1])-1):
                vibes.append(total_seq[-1][i] - total_seq[-1][i+1])
            if set(vibes) != set([0]):
                total_seq.append(vibes)
            else:
                break
        diff = None
        last_val = 0
        for idx in range(len(total_seq)):
            last_val += total_seq[len(total_seq)-1 -idx][0]
        return last_val
        # last_val = 0
        # for idx in range(len(total_seq)):
        #     last_val += total_seq[len(total_seq)-1 -idx][-1]
        # return last_val

    def solution(self):
        with open(self.input_file, "r") as in_file:
            hists = [] 
            for line in in_file:
                sequence = list(map(int,line.split()))
                hists.append(self.calculate_history(sequence))
            print(sum(hists))

            
def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day9.txt")
    sln.solution()

if __name__ == "__main__":
    main()
                