#! /usr/local/bin/python3.11

from collections import defaultdict
from typing import List, Set, Dict
import attr
import re

@attr.s(auto_attribs=True, slots=True)
class Hand:
    card_number: int
    hand: Set[int]
    winning: Set[int]
    points: int = 0

    @property
    def winning_count(self):
        return len(self.hand.intersection(self.winning))
    
    def calc_points(self) -> int:
        if self.winning_count > 0:
            self.points = 1
            for _ in self.hand.intersection(self.winning):
                self.points *= 2
        
            return self.points//2
        else:
            return 0
    
    def __str__(self) -> str:
        return f"{self.hand=} {self.winning=}"

@attr.s(auto_attribs=True, slots=True)
class MegaHand:
    hands: List[Hand]
    track_copies: Dict[str, int] = defaultdict(int)

    def calc_points_part_2(self) -> int:
        from pprint import pprint
        for hand in self.hands:
            self.track_copies[hand.card_number]+=1
            applied_copy = set()
            for i in range(1,hand.winning_count+1):
                self.track_copies[hand.card_number+i]+=1
                applied_copy.add(hand.card_number+i)
            self.apply_copies(self.track_copies[hand.card_number]-1, applied_copy)

    def apply_copies(self, copy_count, apply_to):
        for idx in apply_to:
            for _ in range(copy_count):
                self.track_copies[idx]+=1

    def clean_up(self, last_val):
        sol = 0
        for k, v in self.track_copies.items():
            if k < last_val:
                sol+= v
        return sol
    

@attr.s(slots=True, auto_attribs=True)
class Solution:
    input_file: str
    
    def solution_part_two(self):
        from pprint import pprint
        sol = None
        megahand = []
        with open(self.input_file, "r") as in_file:
            for line in in_file:
                card_number,full_hand= line.split(":")
                hand, winning = full_hand.split("|")
                card_number = int(card_number.split()[1].strip())
                sol = Hand(card_number,set(hand.strip().split()), set(winning.strip().split()))
                megahand.append(sol)
                last_val = card_number
        mh = MegaHand(megahand)
        mh.calc_points_part_2()
        print(mh.clean_up(last_val+1))
                    
    def solution(self):
        val = 0
        with open(self.input_file, "r") as in_file:
            for line in in_file:
                hand, winning = line.split(":")[1].strip().split("| ")
                sol = Hand(set(map(hand.strip().split(),int)), set(map(winning.strip().split(),int)))
                val += sol.calc_points()
        return val
    
def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day4.txt")
    sln.solution_part_two()

if __name__ == "__main__":
    main()
                