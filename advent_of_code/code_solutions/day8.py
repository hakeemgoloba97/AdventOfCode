#! /usr/local/bin/python3.11

from collections import defaultdict
from typing import List, Set, Dict
import attr
import re
from pprint import pprint
from functools import total_ordering
from copy import copy

intructions_dict = {
    'R':1,
    'L':0
}
@attr.s(slots=True, auto_attribs=True)
class Solution:

    input_file: str

    def solution(self):
        network = dict()
        A_nodes = []
        # pos = 'AAA'
        with open(self.input_file, "r") as in_file:
            instructions = next(in_file).strip()
            next(in_file)
            for line in in_file:
                key, nodes = line.split("=")
                nodes = nodes.replace('(','("')
                nodes = nodes.replace(',','",')
                nodes = nodes.replace(', ',' ,"')
                nodes = nodes.replace(')','")')
                if key.strip().endswith('A'):
                    A_nodes.append(key.strip())
                network[key.strip()] = eval(nodes.strip())
            
            # while True:
            #     for inst in instructions:
            #         pos = network[pos][intructions_dict[inst]]
            #         steps+=1
            #         if pos == 'ZZZ':
            #             break
            #     if pos == 'ZZZ':
            #         break
            # print(steps)
            step_list = []
            for pos in A_nodes:
                steps = 0
                while True:
                    for inst in instructions:
                        pos = network[pos][intructions_dict[inst]]
                        steps+=1
                        if pos.endswith('Z'):
                            step_list.append(steps)
                            break
                    if pos.endswith('Z'):
                        break
            import math
            print(math.lcm(*step_list))
            
def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day8.txt")
    sln.solution()

if __name__ == "__main__":
    main()
                