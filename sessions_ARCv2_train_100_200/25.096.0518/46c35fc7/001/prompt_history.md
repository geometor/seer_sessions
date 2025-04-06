
## train_1

**input:**
```
9 6 5 7 7 7 7
8 7 1 7 7 7 7
0 8 9 7 7 7 7
7 7 7 7 7 7 7
7 7 7 1 8 4 7
7 7 7 4 7 6 7
7 7 7 6 2 4 7
```


**output:**
```
5 8 9 7 7 7 7
8 7 6 7 7 7 7
9 1 0 7 7 7 7
7 7 7 7 7 7 7
7 7 7 4 4 4 7
7 7 7 2 7 8 7
7 7 7 1 6 6 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 5 2 8 7 7
7 7 1 7 9 7 7
7 7 4 3 0 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 8 1 0 7 7
7 7 3 7 2 7 7
7 7 5 9 4 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7
7 7 7 6 5 5 7
7 7 7 5 7 6 7
7 7 7 1 5 1 7
8 8 8 7 7 7 7
9 7 9 7 7 7 7
0 0 0 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 5 5 1 7
7 7 7 5 7 5 7
7 7 7 6 6 1 7
8 9 0 7 7 7 7
0 7 8 7 7 7 7
8 9 0 7 7 7 7
```

Okay, I will analyze the provided examples to understand the transformation rule.

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) of single digits.
2.  **Grid Size:** The grids consistently have dimensions of 7x7 in all examples.
3.  **Background Value:** The digit '7' appears frequently and seems to act as a static background or padding. Cells containing '7' in the input remain '7' in the output.
4.  **Transformation Regions:** Changes between input and output occur within localized, contiguous 3x3 blocks where the digits are *not* '7'.
5.  **Transformation Type:** Within these 3x3 blocks, the digits are rearranged. Comparing the input and output blocks suggests a specific geometric transformation. Testing rotations and reflections reveals a pattern: a 90-degree clockwise rotation followed by swapping the corner elements along both the main diagonal and the anti-diagonal.

**YAML Fact Sheet:**


```yaml
task_description: Transform a 7x7 grid of digits based on local transformations within 3x3 subgrids.
elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - dimensions: 7x7
      - contains: cells
  - object: cell
    properties:
      - location: (row, column) coordinates
      - value: integer digit (0-9)
  - object: background_cell
    description: A cell whose value is 7.
    properties:
      - value: 7
      - behavior: Remains unchanged during transformation.
  - object: active_block
    description: A contiguous 3x3 subgrid composed entirely of non-background cells.
    properties:
      - dimensions: 3x3
      - location: defined by top-left corner coordinates within the main grid
      - contains: non-7 digits
    actions:
      - identify: Scan the grid to find these blocks.
      - transform: Apply a specific sequence of operations to the digits within the block.
relationships:
  - The output grid has the same dimensions as the input grid.
  - Background cells map directly from input to output at the same location.
  - Active blocks in the input are transformed and placed into the corresponding location in the output grid.
transformation_rule:
  - name: Rotate_and_Swap_Corners
  - steps:
    - 1: Identify all 3x3 subgrids in the input where none of the cells contain the digit 7.
    - 2: For each identified 3x3 block:
      - a: Perform a 90-degree clockwise rotation of the digits within the block.
      - b: Swap the digit at the top-left corner (0,0 relative to block) with the digit at the bottom-right corner (2,2 relative to block).
      - c: Swap the digit at the top-right corner (0,2 relative to block) with the digit at the bottom-left corner (2,0 relative to block).
    - 3: Construct the output grid by placing the transformed blocks into their original locations and copying all background (7) cells directly from the input.
```


**Natural Language Program:**

1.  Initialize an output grid of the same dimensions as the input grid (7x7), potentially filled with a placeholder value or copied from the input.
2.  Iterate through each cell of the input grid. If a cell contains the background digit '7', copy its value to the corresponding cell in the output grid.
3.  Identify all possible 3x3 subgrids within the input grid.
4.  For each 3x3 subgrid, check if all nine cells within it contain digits *other than* '7'.
5.  If a 3x3 subgrid consists entirely of non-'7' digits (an "active block"):
    a.  Extract the 3x3 block of digits from the input.
    b.  Perform a 90-degree clockwise rotation on this extracted block.
    c.  After rotation, swap the element at the block's relative coordinates (0, 0) with the element at (2, 2).
    d.  After the first swap, swap the element now at the block's relative coordinates (0, 2) with the element now at (2, 0).
    e.  Place the resulting transformed 3x3 block into the corresponding position in the output grid, overwriting any values previously copied (which should only have been '7's if the block detection logic is correct relative to step 2).
6.  Return the completed output grid.
