
## train_1

**input:**
```
0 0 0 0 6
0 4 4 4 0
0 4 4 4 0
0 4 4 4 0
2 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 4 4 6 0
0 4 4 4 0
0 2 4 4 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 7
0 8 8 8 0
0 8 8 8 0
0 0 0 0 7
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 8 8 7 0
0 8 8 7 0
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 5 5 5 0
0 5 5 5 0
0 5 5 5 0
4 0 0 0 2
```


**output:**
```
0 0 0 0 0
0 5 5 5 0
0 5 5 5 0
0 4 5 2 0
0 0 0 0 0
```

Okay, analyzing the provided examples.

**Perception of Elements:**

*   The task operates on a 2D grid of single-digit integers.
*   The input grid contains background zeros (`0`).
*   There is typically a central or significant block of a single, repeated non-zero digit (e.g., `4`s, `8`s, `5`s). Let's call this the "target block".
*   There are one or more other non-zero digits located elsewhere in the grid, often near the edges or corners, separated from the target block by zeros. Let's call these "mover digits".
*   The transformation involves moving the "mover digits" diagonally towards the "target block".
*   The mover digit stops and replaces the first digit of the target block it encounters along its diagonal path.
*   The original position of the mover digit is replaced with a zero.
*   All other digits (zeros and the un-replaced parts of the target block) remain unchanged.

**YAML Facts:**


```yaml
task_elements:
  - object: grid
    properties:
      - type: 2D array
      - content: single-digit integers (0-9)
      - size: fixed (e.g., 5x5 in examples)
  - object: cell
    properties:
      - location: (row, column)
      - value: integer (0-9)
  - object: target_block
    properties:
      - type: group of adjacent cells
      - value: identical non-zero integer (e.g., 4, 8, 5)
      - location: typically central or contiguous
  - object: mover_digit
    properties:
      - type: cell
      - value: non-zero integer, different from target_block value
      - location: typically separated from target_block by zeros, often near edges/corners
actions:
  - action: identify
    actor: system
    target: mover_digits
    condition: non-zero cells not part of the largest contiguous block of identical non-zero numbers.
  - action: identify
    actor: system
    target: target_block
    condition: the largest contiguous block of identical non-zero numbers.
  - action: determine_path
    actor: mover_digit
    parameters:
      - direction: diagonal towards the nearest cell of the target_block
  - action: move
    actor: mover_digit
    result:
      - moves along the determined path until it encounters the first cell belonging to the target_block.
  - action: update_grid
    actor: system
    steps:
      - copy input grid to output grid.
      - for each mover_digit:
        - find the destination cell (first target_block cell on its diagonal path).
        - set the value of the destination cell in the output grid to the mover_digit's value.
        - set the value of the mover_digit's original cell in the output grid to 0.
relationships:
  - type: spatial
    entities: [mover_digit, target_block]
    description: mover_digit moves diagonally towards the target_block.
  - type: replacement
    entities: [mover_digit, target_block_cell]
    description: mover_digit value replaces the value of the first target_block cell encountered on its path.
  - type: state_change
    entities: [mover_digit_original_cell]
    description: original cell of the mover_digit becomes 0.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the primary "target block" within the input grid, which is the largest contiguous group of identical non-zero numbers.
3.  Identify all "mover digits" in the input grid. These are non-zero numbers that are *not* part of the identified target block.
4.  For each identified mover digit:
    a.  Determine its starting position (row, col).
    b.  Determine the diagonal direction towards the nearest cell belonging to the target block. (e.g., if the mover is top-right relative to the block, move down-left; if bottom-left, move up-right; etc.).
    c.  Trace this diagonal path one step at a time from the mover's starting position.
    d.  Find the first cell along this path whose value in the *input* grid belongs to the target block. This is the destination cell.
    e.  Update the output grid: Set the value of the destination cell to the value of the mover digit.
    f.  Update the output grid: Set the value of the mover digit's original cell (starting position) to 0.
5.  Return the final updated output grid.
