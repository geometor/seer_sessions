# 25.045.0759 • 1-3aa6fb7a • 004 example_2 - CODE

---

**input**
```
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x764D50412110>

**output**
```
0 0 0 0 0 0 0
0 8 1 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x764D50412140>

*text:*
**Natural Language Program:**

Identify all contiguous vertical blocks of azure color (8). Order these blocks from left to right based on their column index. For the leftmost block, locate the topmost cell of color azure. Change the color of the cell immediately to its right to blue (1). For the next block (if any), locate the bottommost cell of color azure. Change the color of the cell at the same position to blue (1).

**Step-by-step transformation:**

1. **Identify vertical blocks of azure (8):**
   - Block 1: Column 1, Rows 1-2 (coordinates: (1,1), (2,1))
   - Block 2: Column 4, Rows 3-4 (coordinates: (3,4), (4,4))

2. **Order blocks by column index:**
   - Block 1 (column 1) is first.
   - Block 2 (column 4) is second.

3. **Process the first block (Block 1):**
   - Find the topmost azure cell: (1,1)
   - Change the color of the cell to its right (1, 2) to blue (1).

4. **Process the second block (Block 2):**
   - Find the bottommost azure cell: (4,4)
   - Change the color of the cell at the same position (4, 4) to blue (1).

This step-by-step transformation matches the observed change from input to output.

*text:*
```python
"""
Identify all contiguous vertical blocks of azure color (8). Order these blocks from left to right based on their column index. For the leftmost block, locate the topmost cell of color azure. Change the color of the cell immediately to its right to blue (1). For the next block (if any), locate the bottommost cell of color azure. Change the color of the cell at the same position to blue (1).
"""

import collections

def transform(input_grid):
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    output_grid = [row[:] for row in input_grid] # Create a copy to avoid modifying input

    vertical_blocks = collections.defaultdict(list)
    for j in range(cols):
        start_row = -1
        for i in range(rows):
            if input_grid[i][j] == 8:
                if start_row == -1:
                    start_row = i
            else:
                if start_row != -1:
                    vertical_blocks[j].extend(range(start_row, i))
                    start_row = -1
        if start_row != -1:
            vertical_blocks[j].extend(range(start_row, rows))

    ordered_blocks_cols = sorted(vertical_blocks.keys())
    blocks_info = []
    for col_index in ordered_blocks_cols:
        blocks_info.append((col_index, sorted(list(set(vertical_blocks[col_index]))))) # remove duplicates and sort rows

    if not blocks_info:
        return output_grid

    # Process the first block (leftmost)
    first_block_col, first_block_rows = blocks_info[0]
    topmost_row = first_block_rows[0]
    if first_block_col + 1 < cols:
        output_grid[topmost_row][first_block_col + 1] = 1

    if len(blocks_info) > 1:
        # Process the second block
        second_block_col, second_block_rows = blocks_info[1]
        bottommost_row = second_block_rows[-1]
        output_grid[bottommost_row][second_block_col] = 1

    return output_grid


if __name__ == '__main__':

    input = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0],
        [0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    expected_output = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 1, 0, 0, 0, 0],
        [0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 1, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    output = transform(input)

    if output == expected_output:
        print("SUCCESS!\n")
    else:
        print("FAILED!\n")
        print("Expected Output:", expected_output)
        print("Transformed Output:", output)

    print()
    assert output == expected_output, "Transformed output does not match expected output."
```

**input**
```
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 8 1 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 1 8 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x764D504113C0>

**output**
```
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 8 1 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 1 8 0 0
0 0 0 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x764D50412530>

*text:*
**Natural Language Program:**

Identify all contiguous vertical blocks of azure color (8). Order these blocks from left to right based on their column index. For the leftmost block, locate the topmost cell of color azure. Change the color of the cell immediately to its right to blue (1). For the next blocks (if any), locate the bottommost cell of color azure. Change the color of the cell at the same position to blue (1).

**Step-by-step transformation:**

1. **Identify vertical blocks of azure (8):**
   - Block 1: Column 4, Rows 0-1 (coordinates: (0,4), (1,4))
   - Block 2: Column 2, Rows 2-3 (coordinates: (2,2), (3,2))
   - Block 3: Column 4, Rows 5-6 (coordinates: (5,4), (6,4))

2. **Order blocks by column index:**
   - Block 2 (column 2) is first.
   - Block 1 (column 4) is second.
   - Block 3 (column 4) is third.
   - Actually, blocks 1 and 3 are in the same column, so we need to consider the order of blocks based on their starting column index. If columns are the same, then order does not matter for the rule as described. Let's re-examine.  Order blocks from left to right, so based on their column index only.
   - Block 2 (column 2) is first.
   - Block 1 (column 4) is second.
   - Block 3 (column 4) is third.

3. **Process the first block (Block 2, column 2):**
   - Find the topmost azure cell: (2,2)
   - Change the color of the cell to its right (2, 3) to blue (1).

4. **Process the second block (Block 1, column 4):**
   - Find the bottommost azure cell: (1,4)
   - Change the color of the cell at the same position (1, 4) to blue (1).

5. **Process the third block (Block 3, column 4):**
   - Find the bottommost azure cell: (6,4)
   - Change the color of the cell at the same position (6, 4) to blue (1).

This step-by-step transformation matches the observed change from input to output.
**Instructions**

- Generate a complete Python module to be run in your code_execution to
  represent the natural language program 
- Follow the template below
- If your code fails to achieve a match - analyze the expected and generated
  outputs and try to run the code again 

**Transform Template:**

```python
"""
{ natural language description of the transformation rule }
"""

{ allowed imports that support the transform }

def transform(input):
    # initialize output

    # change output pixels 

    return output


if __name__ == '__main__':

    input = [
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 0, 8, 0],
        [0, 0, 8, 1, 0, 0, 0],
        [0, 0, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 1, 8, 0, 0]
    ]

    expected_output = [
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 1, 8, 0],
        [0, 0, 8, 1, 0, 0, 0],
        [0, 0, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 8, 0, 0],
        [0, 0, 0, 8, 8, 0, 0]
    ]

    output = transform(input)

    if output == expected_output:
        print("SUCCESS!\n")
    else:
        print("FAILED!\n")
        print("Expected Output:", expected_output)
        print("Transformed Output:", output)

    print()
    assert output == expected_output, "Transformed output does not match expected output."

```
