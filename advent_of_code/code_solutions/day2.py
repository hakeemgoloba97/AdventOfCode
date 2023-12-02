#! /usr/local/bin/python3.11

##############################################################################################################################################
# You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number 
# (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag 
# (like 3 red, 5 green, 4 blue).
#
# For example, the record of a few games might look like this:
#
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# In game 1, three sets of cubes are revealed from the bag (and then put back again). 
# The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; 
# the third set is only 2 green cubes.
#
# The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 
# 13 green cubes, and 14 blue cubes?
#
# In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. 
# However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, 
# game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. 
#
# If you add up the IDs of the games that would have been possible, you get 8.
##############################################################################################################################################



from typing import List
import attr
import os 

RED, GREEN, BLUE = 12,13,14
@attr.s(slots=True, auto_attribs=True)
class Bag:
    red: int
    green: int
    blue: int

    def remove_ball(self, number, colour):
        match colour:
            case "red":
                self.red -= number
            case "green":
                self.green -= number
            case "blue":
                self.blue -= number
            case _:
                print("wow")
    
    def check_valid(self):
        return all(x >= 0 for x in [self.red,self.blue,self.green])

            
    def min_tracker(self, number, colour):
        match colour:
            case "red":
                self.red = max(self.red, number)
            case "green":
                self.green = max(self.green, number)
            case "blue":
                self.blue = max(self.blue, number)
    
    def reset(self):
        self.red, self.green, self.blue = RED, GREEN, BLUE

    def cube_square(self):
        return self.blue*self.red*self.green
    
    def __str__(self) -> str:
        return f"{self.red=} {self.green=} {self.blue=}"
    
@attr.s(slots=True, auto_attribs=True)
class Solution:
    input_file: str

    def handle_moves(self, bag: Bag, moves: str):
        rounds: List[str] = moves.strip().split(";")
        for round in rounds:
            each_move = round.strip().split(",")
            for move in each_move:
                number, colour = move.strip().split(" ")
                bag.remove_ball(int(number.strip()),colour.strip())
            if bag.check_valid():
                bag.reset()
            else:
                return False
        return True
    
    def solution(self) -> int:
        final_sum = 0
        with open(self.input_file, "r") as in_file:
            for line in in_file:
                game, moves = line.split(":")
                _, id = game.split(" ")
                if not self.handle_moves(Bag(12,13,14), moves):
                    continue
                final_sum += int(id.strip()) 
        return final_sum
    
    def handle_moves_part_two(self, bag: Bag, moves: str):
        rounds: List[str] = moves.strip().split(";")
        for round in rounds:
            each_move = round.strip().split(",")
            for move in each_move:
                number, colour = move.strip().split(" ")
                bag.min_tracker(int(number.strip()),colour.strip())
    
    def solution_part_two(self) -> int:
        final_sum = 0
        with open(self.input_file, "r") as in_file:
            for line in in_file:
                _, moves = line.split(":")
                bag = Bag(0,0,0)
                self.handle_moves_part_two(bag, moves)
                final_sum += bag.cube_square()
        return final_sum
    
def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day2.txt")
    print(f"Solution 1: {sln.solution()}")
    print(f"Solution 2: {sln.solution_part_two()}")

if __name__ == "__main__":
    main()
                