#! /usr/local/bin/python3.11

from collections import defaultdict
from typing import List, Set, Dict
import attr
import re

@attr.s(slots=True, auto_attribs=True)
class Boat:
    time: int
    distance: int

    def calc_distance(self, time_remaining, speed):
        return time_remaining*speed

    def calc(self):
        success_count = 0
        for i in range((self.time//2)+1):
            hope = self.calc_distance(self.time - i, i)
            if hope <= self.distance:
                pass
                # print(f"{self.time}  {self.distance} hold:{i} travelled: {hope} speed: {i}")
            else: 
                break
        return len(range(i, self.time-i))+1
@attr.s(slots=True, auto_attribs=True)
class Solution:
    input_file: str

    def solution(self):
        time = []
        distance = []
        with open(self.input_file, "r") as in_file:
            time_string = next(in_file)
            distance_string = next(in_file)
            for val in time_string.split(":")[1].split():
                time.append(int(val.strip()))

            for val in distance_string.split(":")[1].split():
                distance.append(int(val.strip()))
            win = 1
            for i in range(len(distance)):
                b = Boat(time[i],distance[i])
                win*=b.calc()
            print(win)

    def solution_part_two(self):
        distance = []
        with open(self.input_file, "r") as in_file:
            time_string = next(in_file)
            distance_string = next(in_file)

            # for val in :
                # time.append(int(val.strip()))
            time = ''.join(time_string.split(":")[1].split())
            # for val in distance_string.split(":")[1].split():
            distance = ''.join(distance_string.split(":")[1].split())
            #     distance.append(int(val.strip()))
            # win = 1
            # for i in range(len(distance)):
            b = Boat(int(time),int(distance))
            print(b.calc())
def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day6.txt")
    sln.solution_part_two()

if __name__ == "__main__":
    main()
                