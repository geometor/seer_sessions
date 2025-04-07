
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 4 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 1 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 8 1 1 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 4 0 1 1 1 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 1 8 1 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 8 8 1 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 1 1 8 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 8 1 1 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, I will analyze the provided examples to understand the transformation rule.

## Perception

1.  **Grid Structure:** The input and output are 2D grids of integers (pixels). The dominant value is 0, representing the background.
2.  **Key Colors/Objects:**
    *   **Color 0:** Background.
    *   **Colors 1 and 8:** These colors form a single, connected 3x3 block in each input grid. This block appears to be the primary object undergoing transformation.
    *   **Color 4:** These appear as isolated points in the input. They seem to act as signals or triggers influencing the transformation.
3.  **Transformation Core:** The central action involves modifying the 3x3 block of 1s and 8s and relocating one of the '4's based on its position relative to the block.
4.  **Input Variations:** The position and internal pattern of the 3x3 block vary, as do the number and positions of the '4's.
5.  **Output Structure:** The output grid retains the background. The 3x3 block (potentially altered) remains in its original position. Only one '4' remains, moved to a new position determined by the input configuration. All other '4's from the input are removed.
6.  **Conditional Logic:** The specific transformation applied to the 3x3 block and the rule for moving the '4' appear to depend on the vertical distance between the 3x3 block and the "determining" '4' (the topmost, leftmost one).
    *   If the determining '4' is 1 row above the block, one set of rules applies (Rule A).
    *   If the determining '4' is 2 rows above the block, a different set of rules applies (Rule B).

## Facts


```yaml
elements:
  - object: grid
    description: A 2D array of integers representing pixels.
  - object: pixel
    properties:
      - color: An integer value (0, 1, 4, 8 observed).
      - position: (row, column) coordinates.
  - object: background
    description: Pixels with color 0.
  - object: main_block
    description: A connected 3x3 component composed entirely of pixels with colors 1 and 8. There is exactly one such block in each input.
    properties:
      - top_left_corner: (row, column) of the top-left pixel of the block.
      - pattern: The specific 3x3 array of 1s and 8s.
  - object: signal_pixels
    description: Pixels with color 4. They appear isolated.
    properties:
      - position: (row, column) coordinates.

relationships:
  - relation: relative_position
    object1: determining_signal_pixel
    object2: main_block
    description: The row and column difference between the determining signal pixel (topmost, then leftmost '4') and the top-left corner of the main_block. This relative position dictates the transformation rules applied.

actions:
  - action: identify_main_block
    input: input_grid
    output: main_block object (pattern and position)
  - action: identify_signal_pixels
    input: input_grid
    output: list of signal_pixel objects (positions)
  - action: select_determining_signal
    input: list of signal_pixels
    output: one signal_pixel object (the one with the minimum row index, breaking ties with the minimum column index)
  - action: determine_rule_set
    input: relative_position (determining_signal to main_block)
    output: rule_identifier ('Rule A' or 'Rule B')
    logic: |
      If relative_row = -1, use Rule A.
      If relative_row = -2, use Rule B.
  - action: transform_main_block
    input: main_block pattern, rule_identifier
    output: transformed_main_block pattern
    logic: |
      Applies a specific, fixed 3x3 transformation based on the rule_identifier (T_A or T_B, derived from examples). The transformation swaps an equal number of 1s and 8s within the block. The block remains in its original position in the grid.
      - T_A (Rule A): Observed in examples 1 and 3.
      - T_B (Rule B): Observed in examples 2 and 4.
  - action: move_determining_signal
    input: determining_signal position, rule_identifier
    output: new_signal_position
    logic: |
      Calculates the output position for the determining signal pixel based on the rule_identifier.
      - Rule A: new_position = (input_row + 4, input_col)
      - Rule B: new_position = (input_row + 1, input_col + 1)
  - action: construct_output_grid
    input: input_grid_dimensions, transformed_main_block (pattern and position), new_signal_position
    output: output_grid
    logic: |
      Create a new grid filled with 0s.
      Place the transformed_main_block pattern at its original position.
      Place a '4' at the new_signal_position.
```


## Natural Language Program

1.  **Identify Objects:**
    a.  Scan the input grid to find the 3x3 connected component consisting solely of pixels with values 1 and 8. Record its pattern and the coordinates of its top-left corner. This is the `main_block`.
    b.  Scan the input grid to find all pixels with value 4. Record their coordinates. These are the `signal_pixels`.
2.  **Select Key Signal:**
    a.  From the list of `signal_pixels`, find the one with the minimum row index.
    b.  If there are multiple signal pixels with the same minimum row index, select the one among them with the minimum column index. This is the `determining_signal`.
3.  **Determine Transformation Rules:**
    a.  Calculate the relative row offset between the `determining_signal` and the `main_block` ( `determining_signal.row - main_block.top_left_row`).
    b.  If the relative row offset is -1, select **Rule Set A**.
    c.  If the relative row offset is -2, select **Rule Set B**.
4.  **Apply Transformations:**
    a.  **Transform Block:** Apply the specific 3x3 pattern transformation corresponding to the selected Rule Set (`T_A` for Rule Set A, `T_B` for Rule Set B, as observed in the training examples) to the `main_block`'s pattern. The block's position in the grid does not change.
    b.  **Move Signal:** Calculate the new position for the `determining_signal` based on the selected Rule Set:
        *   If Rule Set A: `new_signal_position = (determining_signal.row + 4, determining_signal.col)`
        *   If Rule Set B: `new_signal_position = (determining_signal.row + 1, determining_signal.col + 1)`
5.  **Construct Output:**
    a.  Create a new grid of the same dimensions as the input grid, initialized with 0s.
    b.  Place the transformed `main_block` pattern onto the new grid at its original top-left corner coordinates.
    c.  Place a pixel with value 4 at the calculated `new_signal_position` in the new grid.
    d.  The resulting grid is the output.
```python
"""
Identifies a 3x3 block composed of colors 1 and 8, and multiple signal pixels of color 4.
It selects the topmost, then leftmost signal pixel (determining_signal).
Based on the vertical distance between the determining_signal and the 3x3 block,
it applies one of two transformation rules:

Rule A (determining_signal is 1 row above the block):
- Swaps elements (0,1) <-> (2,0) and (0,2) <-> (1,2) within the 3x3 block pattern.
- Moves the determining_signal pixel 4 rows down from its original position.

Rule B (determining_signal is 2 rows above the block):
- Swaps elements (0,1) <-> (2,0), (0,2) <-> (2,2), and (1,0) <-> (1,2) within the 3x3 block pattern.
- Moves the determining_signal pixel 1 row down and 1 column right from its original position.

The output grid contains the transformed 3x3 block at its original location and
only the determining_signal pixel moved to its new location. All other signal
pixels are removed. The background remains color 0.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def find_main_block(grid: np.ndarray) -> Optional[Tuple[Tuple[int, int], np.ndarray]]:
    """
    Finds the 3x3 block composed solely of 1s and 8s.
    Returns the top-left corner coordinates and the 3x3 block pattern.
    """
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            block = grid[r:r+3, c:c+3]
            # Check if all elements are either 1 or 8
            if np.all(np.isin(block, [1, 8])):
                 # Check if at least one 1 and one 8 exist to ensure it's the target block
                 if np.any(block == 1) and np.any(block == 8):
                    return ((r, c), block)
    return None

def find_determining_signal(signal_pixels: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """
    Finds the topmost, then leftmost signal pixel (color 4).
    """
    if not signal_pixels:
        return None
    # Sort by row (primary key), then column (secondary key)
    signal_pixels.sort(key=lambda x: (x[0], x[1]))
    return signal_pixels[0]

def apply_block_transform(block_pattern: np.ndarray, rule_type: str) -> np.ndarray:
    """Applies the specified transformation rule to the 3x3 block pattern."""
    transformed_block = block_pattern.copy()
    if rule_type == 'A':
        # Swap (0,1) <-> (2,0)
        transformed_block[0, 1], transformed_block[2, 0] = transformed_block[2, 0], transformed_block[0, 1]
        # Swap (0,2) <-> (1,2)
        transformed_block[0, 2], transformed_block[1, 2] = transformed_block[1, 2], transformed_block[0, 2]
    elif rule_type == 'B':
        # Swap (0,1) <-> (2,0)
        transformed_block[0, 1], transformed_block[2, 0] = transformed_block[2, 0], transformed_block[0, 1]
        # Swap (0,2) <-> (2,2)
        transformed_block[0, 2], transformed_block[2, 2] = transformed_block[2, 2], transformed_block[0, 2]
        # Swap (1,0) <-> (1,2)
        transformed_block[1, 0], transformed_block[1, 2] = transformed_block[1, 2], transformed_block[1, 0]
    return transformed_block

def calculate_new_signal_position(signal_pos: Tuple[int, int], rule_type: str) -> Tuple[int, int]:
    """Calculates the new position for the determining signal pixel."""
    r, c = signal_pos
    if rule_type == 'A':
        return (r + 4, c)
    elif rule_type == 'B':
        return (r + 1, c + 1)
    else: # Should not happen with valid rules
        return signal_pos


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation based on the relative position of the
    topmost, leftmost signal pixel (4) to the 3x3 block (1s and 8s).
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # Initialize output grid with zeros
    output_grid = np.zeros_like(grid_np)

    # 1. Identify Objects
    signal_pixels = find_pixels(grid_np, 4)
    block_info = find_main_block(grid_np)

    # Check if necessary components are found
    if not signal_pixels or block_info is None:
        # Return empty or original grid if components missing?
        # Based on examples, components always exist. Return empty for safety.
        print("Warning: Could not find required components (signal pixels or main block).")
        return output_grid.tolist()

    (block_pos, block_pattern) = block_info
    block_r, block_c = block_pos

    # 2. Select Key Signal
    determining_signal_pos = find_determining_signal(signal_pixels)
    if determining_signal_pos is None: # Should not happen if signal_pixels is not empty
         print("Warning: Could not determine key signal pixel.")
         return output_grid.tolist()
    signal_r, signal_c = determining_signal_pos

    # 3. Determine Transformation Rules
    relative_row = signal_r - block_r
    rule_type = None
    if relative_row == -1:
        rule_type = 'A'
    elif relative_row == -2:
        rule_type = 'B'
    else:
        # Handle unexpected relative positions if necessary
        print(f"Warning: Unexpected relative row {relative_row}. No rule defined.")
        # For now, maybe just copy the block and place the signal? Or return empty?
        # Let's proceed assuming rules A or B cover all cases in the test set.
        # If no rule applies, we will place the original block and the moved signal according to some default or just skip.
        # Returning empty grid for now if rule is not found.
        return output_grid.tolist()


    # 4. Apply Transformations
    # Transform Block
    transformed_block_pattern = apply_block_transform(block_pattern, rule_type)

    # Move Signal
    new_signal_pos = calculate_new_signal_position(determining_signal_pos, rule_type)
    new_signal_r, new_signal_c = new_signal_pos

    # 5. Construct Output
    # Place the transformed block
    if 0 <= block_r < rows - 2 and 0 <= block_c < cols - 2:
         output_grid[block_r:block_r+3, block_c:block_c+3] = transformed_block_pattern
    else:
        print(f"Warning: Block position {block_pos} is invalid for grid size {rows}x{cols}.")


    # Place the moved determining signal pixel (color 4)
    if 0 <= new_signal_r < rows and 0 <= new_signal_c < cols:
        output_grid[new_signal_r, new_signal_c] = 4
    else:
        # Handle cases where the new signal position is outside the grid
        print(f"Warning: New signal position {new_signal_pos} is outside the grid boundaries ({rows}x{cols}).")


    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
