#! /usr/local/bin/python3.11

##################################################################################################################################
# The newly-improved calibration document consists of lines of text; each line originally contained a specific                   #
# calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining            #
# the first digit and the last digit (in that order) to form a single two-digit number.                                          #
#                                                                                                                                #
# For example:                                                                                                                   #
#                                                                                                                                #
# 1abc2                                                                                                                          #
# pqr3stu8vwx                                                                                                                    #
# a1b2c3d4e5f                                                                                                                    #
# treb7uchet                                                                                                                     #
# In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.        #
#                                                                                                                                #
##################################################################################################################################


from typing import Dict, Iterable
import attr
import re

@attr.s(slots=True, frozen=True, auto_attribs=True)
class Solution:
    input_file: str
    search_regex: re.Pattern
    #Couldn't figure it out so I hardcoded things that were tripping up my solution
    word_to_digit: Dict[str,str] = {
        "oneight":"18",
        "twone":"21",
        "eightwo":"82",
        "nineight":"98",
        "eighthree":"83",
        "threeight":"38",
        "sevenine":"79",
        "one":"1",
        "two":"2",
        "three":"3",
        "four":"4",
        "five":"5",
        "six":"6",
        "seven":"7",
        "eight":"8",
        "nine":"9",
        "ten":"10",
    }

    def convert_words(self, line):
        for k,v in self.word_to_digit.items():
            line = re.sub(k,v, line, flags=re.IGNORECASE)
        return line
    
    def solution(self) -> Iterable[int]:
        with open(self.input_file, "r") as in_file:
            for line in in_file:
                # migh be bad for really long liens in files 
                results = [val for val in list(line) if val.isdigit()]
                #Assume every line will have at least 2 digits based on problem
                res = ''.join([results[0],results[-1]])
                # using generator in case we get insanely large file
                yield int(res)

    def solution_part_two(self) -> Iterable[int]:
        with open(self.input_file, "r") as in_file:
            for line in in_file:
                line = self.convert_words(line)
                # migh be bad for really long liens in files
                results = [val for val in list(line) if val.isdigit()]
                #Assume every line will have at least 2 digits based on problem
                res = ''.join([results[0],results[-1]])
                # using generator in case we get insanely large file
                yield int(res)

def main():
    # Nothing special in solution use regex to extract all digits then sum them up
    # sacraficng speed for memeory efficiency in case of huge input files.. (yield) maybe overkill

    sln: Solution = Solution("../input_files/day1.txt", re.compile(r"\d+"))
    final_sum: int = 0
    for value in sln.solution():
        final_sum += value
        print(f"Solution 1: {final_sum}")
    final_sum = 0
    for value in sln.solution_part_two():
        final_sum += value
        print(f"Solution 2: {final_sum}")

if __name__ == "__main__":
    main()