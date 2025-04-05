
## train_1

**input:**
```
0 2 0 0 9 9 9 9 9 9 9 0
```


**output:**
```
0 2 0 9 9 9 9 9 9 9 0 0
```


## train_2

**input:**
```
0 0 1 1 0 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 2 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 2 0 0 0 0 0 6 0 0 0
```


**output:**
```
0 0 2 0 0 0 0 6 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 2 0 0 1 1
```


**output:**
```
0 0 0 0 0 0 0 2 0 1 1 0
```


## train_5

**input:**
```
0 9 9 9 9 9 9 0 0 0 2 0
```


**output:**
```
0 0 9 9 9 9 9 9 0 0 2 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 1 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 1 0 2
```


## train_7

**input:**
```
9 0 0 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 9 0 0 0 0 0 0 2 0 0 0
```

Okay, let's break down the task.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are single strings representing sequences of 12 digits.
2.  **Digits:** The sequences contain digits from 0 to 9.
3.  **Special Digit '2':** The digit '2' appears exactly once in every input and output sequence. Its position seems crucial.
4.  **Zeroes ('0'):** The digit '0' appears multiple times and seems to act as a background or empty space.
5.  **Other Non-Zero Digits (1, 6, 9):** These digits appear, sometimes contiguously, forming blocks.
6.  **Transformation:** The core transformation involves shifting a contiguous block of non-zero digits (excluding '2') either one step left or one step right. The digit '2' remains stationary. A '0' swaps position with the shifting block.
7.  **Shift Direction:** The direction of the shift depends on the block's position relative to the '2'. Blocks to the left of '2' shift right; blocks to the right of '2' shift left.
8.  **Zero Swap:** When a block shifts, it swaps places with an adjacent '0'. If shifting right, it swaps with the '0' immediately to its right. If shifting left, it swaps with the '0' immediately to its left.

**YAML Facts:**


```yaml
Task: Shift a block relative to a fixed point '2'.

Objects:
  - name: Sequence
    type: List[int]
    length: 12
    elements: Digits 0-9
  - name: Pivot
    type: Digit
    value: 2
    property: Stationary position
  - name: Block
    type: Contiguous Subsequence
    elements: Digits 1, 3, 4, 5, 6, 7, 8, 9 (non-zero, non-pivot)
    property: Mobile
  - name: Space
    type: Digit
    value: 0
    property: Swappable with Block

Relationships:
  - type: Relative Position
    object1: Block
    object2: Pivot
    states: [Left Of, Right Of]
  - type: Adjacency
    object1: Block
    object2: Space
    states: [Space follows Block, Space precedes Block]

Actions:
  - name: Identify Pivot Position
    input: Sequence
    output: index_pivot
  - name: Identify Blocks
    input: Sequence
    output: List[Block_info(start_index, end_index, content)]
  - name: Determine Shift Direction
    input: Block_info, index_pivot
    output: Direction (Left, Right, None)
    condition: |
      if block.end_index < index_pivot: return Right
      if block.start_index > index_pivot: return Left
      else: return None
  - name: Perform Shift and Swap
    input: Sequence, Block_info, Direction
    output: Modified Sequence
    condition: |
      Requires an adjacent '0' in the direction opposite the shift.
      - If Direction is Right and Sequence[block.end_index + 1] == 0:
          Swap Block(start:end) with Space(end+1). Block moves to start+1:end+1, Space moves to start.
      - If Direction is Left and Sequence[block.start_index - 1] == 0:
          Swap Block(start:end) with Space(start-1). Block moves to start-1:end-1, Space moves to end.
    assumption: Only one block shifts per task instance based on examples.
```


**Natural Language Program:**

1.  Convert the input string into a list of integers.
2.  Find the index of the digit '2' (the pivot).
3.  Search the list for the first contiguous block of non-zero digits that are not '2'. Record its start and end indices. *Assumption based on examples: there will be exactly one such block that needs to move.*
4.  Compare the block's position to the pivot's index:
    a.  If the block's end index is less than the pivot's index (block is to the left):
        i.  Check if the element immediately to the right of the block (at index `end + 1`) is '0'.
        ii. If it is '0', perform a swap: Move the block one position to the right (occupying indices `start + 1` to `end + 1`) and move the '0' from `end + 1` to the original `start` index.
    b.  If the block's start index is greater than the pivot's index (block is to the right):
        i.  Check if the element immediately to the left of the block (at index `start - 1`) is '0'.
        ii. If it is '0', perform a swap: Move the block one position to the left (occupying indices `start - 1` to `end - 1`) and move the '0' from `start - 1` to the original `end` index.
5.  Convert the modified list of integers back into the output string format (digits separated by spaces).
```python
import re

"""
The transformation rule identifies a single, stationary pivot digit '2' within a sequence of 12 digits. 
It then locates the first contiguous block of non-zero digits (excluding the pivot '2').
If this block is located entirely to the left of the pivot '2', and there is a '0' immediately to the right of the block, the block is shifted one position to the right, swapping places with that '0'.
If the block is located entirely to the right of the pivot '2', and there is a '0' immediately to the left of the block, the block is shifted one position to the left, swapping places with that '0'.
The pivot '2' and any other '0's remain in their positions unless directly involved in the swap.
The output is the modified sequence of digits, formatted as a space-separated string.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts the space-separated input string into a list of integers."""
    return [int(d) for d in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_pivot_index(grid: list[int]) -> int:
    """Finds the index of the pivot digit '2'."""
    try:
        return grid.index(2)
    except ValueError:
        # Should not happen based on problem description, but good practice
        return -1 

def find_movable_block(grid: list[int], pivot_index: int) -> tuple[int | None, int | None]:
    """
    Finds the start and end indices of the first contiguous block of 
    non-zero digits (excluding the pivot '2').
    Returns (None, None) if no such block is found.
    """
    start_index = None
    for i, digit in enumerate(grid):
        if digit != 0 and i != pivot_index:
            # Found the start of a potential block
            start_index = i
            # Find the end of this block
            end_index = i
            for j in range(i + 1, len(grid)):
                if grid[j] == 0 or j == pivot_index:
                    break # Block ends here
                end_index = j
            return start_index, end_index
        
    return None, None # No block found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    
    1. Parses the input string into a list of integers.
    2. Finds the index of the pivot '2'.
    3. Finds the contiguous block of non-zero, non-'2' digits.
    4. Determines if the block is left or right of the pivot.
    5. Checks for an adjacent '0' in the appropriate direction for swapping.
    6. Performs the shift and swap if conditions are met.
    7. Formats the resulting list back into a string.
    """
    # 1. Parse input
    grid = parse_input(input_str)
    output_grid = list(grid) # Work on a copy

    # 2. Find pivot
    pivot_index = find_pivot_index(grid)
    if pivot_index == -1:
        # Handle error case if '2' is not found (though examples imply it's always there)
        return input_str 

    # 3. Find the block to move
    start_index, end_index = find_movable_block(grid, pivot_index)

    # 4. Determine direction and perform shift/swap if possible
    if start_index is not None and end_index is not None:
        block_content = grid[start_index : end_index + 1]
        
        # 4a. Block is to the left of the pivot
        if end_index < pivot_index:
            # Check if a swap to the right is possible
            swap_pos = end_index + 1
            if swap_pos < len(grid) and grid[swap_pos] == 0:
                # Perform right shift: place 0 at start, block at start+1
                output_grid[start_index] = 0
                output_grid[start_index + 1 : end_index + 2] = block_content
                
        # 4b. Block is to the right of the pivot
        elif start_index > pivot_index:
            # Check if a swap to the left is possible
            swap_pos = start_index - 1
            if swap_pos >= 0 and grid[swap_pos] == 0:
                 # Perform left shift: place 0 at end, block at start-1
                 output_grid[end_index] = 0
                 output_grid[start_index - 1 : end_index] = block_content

    # 7. Format output
    return format_output(output_grid)

```
