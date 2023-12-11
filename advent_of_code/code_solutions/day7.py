#! /usr/local/bin/python3.11

from collections import defaultdict
from typing import List, Set, Dict, ValuesView
import attr
from copy import copy
from functools import cmp_to_key

ORDERING: List[str] = ["HighCard", "OnePair", "TwoPair", "ThreeOfAKind" , "FullHouse", "FourOfAKind" , "FiveOfAKind"]

@attr.s(slots=True, auto_attribs=True)
class Card:
    card: str
    card_to_value: Dict[str, int] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9":  9,
    "8":  8,
    "7":  7,
    "6":  6,
    "5":  5,
    "4":  4,
    "3":  3,
    "2":  2,
    "J":  1
    }

    @property
    def value(self) -> int:
        return self.card_to_value[self.card]

    def __str__(self) -> str:
        return f"{self.card}"

@attr.s(slots=True, auto_attribs=True)
class Hand:
    cards: List[Card]
    bid: int

    def __str__(self) -> str:
        return f"{''.join([c.card for c in self.cards])}"
    
    @property
    def count_cards(self) -> int:
        counts = defaultdict(int)
        for card in self.cards:
            counts[card.card] += 1
        return counts
    
    @property
    def card_dist(self) -> ValuesView:
        return self.count_cards.values()
            
    def get_hand_type(self, part:str) -> str:
        dist = self.card_dist

        if part == "part2":
            if 'J' in self.count_cards:
                card_count_copy = copy(self.count_cards)
                j_count = card_count_copy['J']
                if j_count < 5:
                    del card_count_copy['J']
                    card_count_copy[max(card_count_copy,key=card_count_copy.get)] += j_count
                    dist = card_count_copy.values()

        match sorted(list(dist),reverse=True):
            case [5]:
                return "FiveOfAKind"
            case [4,1]:
                return "FourOfAKind"
            case [3,2]:
                return "FullHouse"
            case [3,1,1]:
                return "ThreeOfAKind"
            case [2,2,1]:
                return "TwoPair"
            case [2,1,1,1]:
                return "OnePair"
            case [1,1,1,1,1]:
                return "HighCard"

def cmp_items(a:Hand,b:Hand):
    for i in range(len(a.cards)):
        if a.cards[i].card == b.cards[i].card:
            continue
        if a.cards[i].value > b.cards[i].value:
            return 1
        else:
            return -1
    return 0

@attr.s(slots=True, auto_attribs=True)
class Solution:

    input_file: str

    def solution(self, part):
        with open(self.input_file, "r") as in_file:
            ranks = defaultdict(list)
            sorter = cmp_to_key(cmp_items)
            fin_ranking = []
            table = []
            total = 0

            for line in in_file:
                cards, bid = line.split()
                card_list = []
                for c in list(cards):
                    card_list.append(Card(c))
                hand = Hand(card_list, int(bid))
                table.append(hand)
            
            for hand in table:
                ranks[hand.get_hand_type(part)].append(hand)
            
            for order in ORDERING:
                ranks[order].sort(key=sorter)
                if order in ranks:
                    for hand in ranks[order]:
                        fin_ranking.append(hand.bid)
            
            for i in range(1,len(fin_ranking)+1):
                total += fin_ranking[i-1] * i
            
            return(total)

def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day7.txt")
    print(f"part1 = {sln.solution('part1')}")
    print(f"part2 = {sln.solution('part2')}")

if __name__ == "__main__":
    main()
                