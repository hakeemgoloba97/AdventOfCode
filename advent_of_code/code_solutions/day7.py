#! /usr/local/bin/python3.11

from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, ValuesView
from copy import copy
from functools import cmp_to_key

ORDERING: List[str] = ["HighCard", "OnePair", "TwoPair", "ThreeOfAKind" , "FullHouse", "FourOfAKind" , "FiveOfAKind"]

class Card:

    def __init__(self, card:str , part: str):
        self.card: str = card

        self.card_to_value: Dict[str, int] = {
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
        }
        if part == "part2":
            self.card_to_value['J'] = 1

    @property
    def value(self) -> int:
        return self.card_to_value[self.card]

    def __str__(self) -> str:
        return f"{self.card}"

@dataclass
class Hand:
    cards: List[Card] = field(default_factory=list)
    bid: int = field(default_factory=list)

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
        shape = None
        match sorted(list(dist),reverse=True):
            case [5]:
                shape = "FiveOfAKind"
            case [4,1]:
                shape = "FourOfAKind"
            case [3,2]:
                shape = "FullHouse"
            case [3,1,1]:
                shape = "ThreeOfAKind"
            case [2,2,1]:
                shape = "TwoPair"
            case [2,1,1,1]:
                shape = "OnePair"
            case [1,1,1,1,1]:
                shape = "HighCard"
        return shape

def cmp_items(a:Hand,b:Hand):
    for i in range(len(a.cards)):
        if a.cards[i].card == b.cards[i].card:
            continue
        if a.cards[i].value > b.cards[i].value:
            return 1
        else:
            return -1
    return 0

@dataclass
class Solution:
    input_file: str = field(default_factory=str)

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
                    card_list.append(Card(c,part))
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
    sln: Solution = Solution("../input_files/day7.txt")
    print(f"part1 = {sln.solution('part1')}")
    print(f"part2 = {sln.solution('part2')}")

if __name__ == "__main__":
    main()
                