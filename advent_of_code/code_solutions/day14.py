#! /usr/local/bin/python3.11

from copy import copy
from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    x: int
    y: int
    val: str

    def __hash__(self) -> int:
        return hash((self.x,self.y,self.val))

@dataclass
class FieldMap:
    points: List[Point]
    row_length: int
    col_length: int
    last: str= ""

    def tilt_north(self, col_number):
        column_vals = []
        column_vals = [t for t in self.points if t.y == col_number] 
        self.points = [t for t in self.points if t.y != col_number]

        for _ in range(len(column_vals)):
            for idx, col_val in reversed(list(enumerate(column_vals))):
                if idx != 0 and col_val.val !='#':
                    if col_val.val == 'O' and column_vals[idx - 1].val == '.':
                        a, b = column_vals.index(col_val), column_vals.index(column_vals[idx - 1])
                        column_vals[a].x,column_vals[b].x = column_vals[b].x, column_vals[a].x
                        column_vals[a],column_vals[b] = column_vals[b], column_vals[a]

        self.points.extend(column_vals)
        self.last = "north"

    def tilt_west(self, row_number):
        row_vals = []
        row_vals = [t for t in self.points if t.x == row_number] 
        self.points = [t for t in self.points if t.x != row_number]

        for _ in range(len(row_vals)):
            for idx, row_val in list(enumerate(row_vals)):
                if idx != 0 and row_val.val !='#':
                    if row_val.val == 'O' and row_vals[idx - 1].val == '.':
                        a, b = row_vals.index(row_val), row_vals.index(row_vals[idx - 1])
                        row_vals[a].y,row_vals[b].y = row_vals[b].y, row_vals[a].y
                        row_vals[a],row_vals[b] = row_vals[b], row_vals[a]

        self.points.extend(row_vals)
        self.last = "west"

    def tilt_south(self, col_number):
        column_vals = []
        column_vals = [t for t in self.points if t.y == col_number] 
        self.points = [t for t in self.points if t.y != col_number]

        for _ in range(len(column_vals)):
            for idx, col_val in (list(enumerate(column_vals))):
                if idx+1 != len(column_vals) and col_val.val !='#':
                    if col_val.val == 'O' and column_vals[idx + 1].val == '.':
                        a, b = column_vals.index(col_val), column_vals.index(column_vals[idx + 1])
                        column_vals[a].x,column_vals[b].x = column_vals[b].x, column_vals[a].x
                        column_vals[a],column_vals[b] = column_vals[b], column_vals[a]

        self.points.extend(column_vals)
        self.last = "south"

    def tilt_east(self, row_number):
        row_vals = []
        row_vals = [t for t in self.points if t.x == row_number] 
        self.points = [t for t in self.points if t.x != row_number]

        for _ in range(len(row_vals)):
            for idx, row_val in reversed(list(enumerate(row_vals))):
                if idx+1 != len(row_vals) and row_val.val !='#':
                    if row_val.val == 'O' and row_vals[idx + 1].val == '.':
                        a, b = row_vals.index(row_val), row_vals.index(row_vals[idx + 1])
                        row_vals[a].y,row_vals[b].y = row_vals[b].y, row_vals[a].y
                        row_vals[a],row_vals[b] = row_vals[b], row_vals[a]

        self.points.extend(row_vals)
        self.last = "east"
    
    def get_row(self, row_number):
        row_vals = [t for t in self.points if t.x == row_number]
        return ''.join([row_val.val for row_val in row_vals])


    def __hash__(self) -> int:
        return hash(tuple(p.val for p in self.points))
    
    def __iter__(self):
        return iter(self.points)

def spin_cycle(things: FieldMap):
    for i in range(things.col_length):
        things.tilt_north(i)

    for i in range(things.row_length):
        things.tilt_west(i)

    for i in range(things.col_length):
        things.tilt_south(i)

    for i in range(things.row_length):
        things.tilt_east(i)

    return things

def check_total(things):
    total = 0

    for i in range(things.row_length):
        sentence = things.get_row(i)
        total+= (things.row_length - i) * sentence.count('O')
    return total



@dataclass
class Solution:
    input_file: str

    def solution(self):
        with open(self.input_file, encoding="utf8") as file:
            lines =  [line.strip() for line in  file.readlines()]
            contents = []
            for idx,line in enumerate(lines):
                for jdx in range(len(list(line))):
                    contents.append(Point(idx, jdx, line[jdx]))
            field_map = FieldMap(contents, len(lines), len(lines[0]))
            for i in range(field_map.col_length):
                field_map.tilt_north(i)

            return str(check_total(field_map))
def main():
    sln: Solution = Solution("../input_files/day14.txt")
    print(' '.join([sln.solution(), "20"]))

if __name__ == "__main__":
    main()
                