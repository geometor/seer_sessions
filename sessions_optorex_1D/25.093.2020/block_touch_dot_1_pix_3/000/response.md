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