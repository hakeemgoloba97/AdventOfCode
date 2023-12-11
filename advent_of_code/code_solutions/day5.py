#! /usr/local/bin/python3.11

from collections import defaultdict
from typing import List, Set, Dict, Tuple
import attr
import re

path = ["seed-to-soil","soil-to-fertilizer","fertilizer-to-water","water-to-light",
        "light-to-temperature","temperature-to-humidity","humidity-to-location"]

map_cache = {}
@attr.s(slots=True, auto_attribs=True)
class Map:
    mapper: Dict[str, List[Tuple[int,int,int]]] = defaultdict(list)
    map_name:str = ""

    def set_map_name(self, name):
        self.map_name = name

    def set_up(self,destination, source, number_range):
            self.mapper[self.map_name].append((destination,source,number_range))

    def find_map(self, val, dest, src, rang):
        for i in range(rang):
            map_cache[src+i] = dest+i
            if src+i == val:
                return True, dest+i
        return False, val
    
    def find_range(self, val, values):
        mapped = False
        for dest, src, rang in values:
            if val >= src:
                if not mapped and val <= src + rang:
                    if val not in map_cache:
                        mapped, val = self.find_map(val, dest, src, rang)
                    else:
                        val = map_cache[val]
                        mapped = True
        return val
    
    def walk_path(self, seed_number) -> str:
        from pprint import pprint
        val = seed_number
        for p in path:
            val = self.find_range(val, self.mapper[p])
        return val
    
@attr.s(slots=True, auto_attribs=True)
class Solution:
    input_file: str

    def solution(self):
        sol_list = []
        with open(self.input_file, "r") as in_file:
            seeds = next(in_file)
            seeds = seeds.split(":")[1]
            map_builder = Map()
            map_next = False
            for line in in_file:

                if line != "\n" and not map_next:
                    dest, source, num_range = line.split()
                    map_builder.set_up(int(dest.strip()), int(source.strip()), int(num_range.strip()))
                if map_next:
                    map_name = line.split()[0].strip()
                    map_builder.set_map_name(map_name)
                    map_next=False
                if line == "\n":
                    map_next = True
            for seed in seeds.split():
                sol_list.append(map_builder.walk_path(int(seed)))

    def solution_part_two(self):
        sol_list = []
        with open(self.input_file, "r") as in_file:
            seeds = next(in_file)
            seeds = seeds.split(":")[1]
            map_builder = Map()
            map_next = False
            for line in in_file:

                if line != "\n" and not map_next:
                    dest, source, num_range = line.split()
                    map_builder.set_up(int(dest.strip()), int(source.strip()), int(num_range.strip()))
                if map_next:
                    map_name = line.split()[0].strip()
                    map_builder.set_map_name(map_name)
                    map_next=False
                if line == "\n":
                    map_next = True
            
        seeds = list(map(int, seeds.split()))
        seeds = [seeds[i:i+2] for i in range(0,len(seeds),2)]
        seed_list = []
        for seed, seed_r in seeds:
            for i in range(seed_r):
                seed_list.append(seed+i)
        
        for seed in seed_list:
            sol_list.append(map_builder.walk_path(seed))
            print(sol_list)
        print(min(sol_list))
def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill
    sln: Solution = Solution(f"../input_files/day5.txt")
    sln.solution_part_two()

if __name__ == "__main__":
    main()