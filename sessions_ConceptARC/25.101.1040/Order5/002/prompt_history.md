
## train_1

**input:**
```
3 0 4 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
3 0 0 4 0 3 0 0 0 0 3 0 0 4 0 3 0 0 0 0 3
3 0 0 0 0 3 0 4 0 0 3 0 0 0 0 3 0 0 4 0 3
3 4 0 4 0 3 0 0 0 0 3 0 4 0 0 3 0 0 0 0 3
3 0 4 0 0 3 0 0 4 0 3 0 0 0 4 3 0 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
```


**output:**
```
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 4 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 4 0 3 0 0 4 0 3
3 0 0 4 0 3 0 4 0 0 3 0 0 0 0 3 0 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 4 0 0 3 4 0 4 0 3
3 0 0 0 0 3 0 0 4 0 3 0 0 0 4 3 0 4 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
```


## train_2

**input:**
```
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
3 4 0 4 0 3 4 0 0 0 3 4 0 0 4 3 0 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 4 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 4 3 0 0 0 0 3
3 0 4 0 0 3 0 4 0 0 3 0 4 0 0 3 0 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
```


**output:**
```
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 4 0 4 0 3 4 0 0 4 3
3 4 0 0 0 3 4 0 0 0 3 0 0 0 0 3 0 0 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 4 3
3 0 0 0 0 3 0 4 0 0 3 0 4 0 0 3 0 4 0 0 3
3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0 0 3
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Grid Structure:** The input and output grids maintain the same dimensions (6x21 in the examples).
2.  **Static Elements:** There are vertical lines of green pixels (color 3) at columns 0, 5, 10, 15, and 20. These lines act as separators and remain unchanged between the input and output. The background white pixels (color 0) also largely remain unchanged, except where yellow pixels are moved.
3.  **Dynamic Elements:** The yellow pixels (color 4) are the primary dynamic elements. They exist within the sections created by the green lines.
4.  **Sections:** The green lines divide the grid into four main operational sections:
    *   Section 1: Columns 1-4
    *   Section 2: Columns 6-9
    *   Section 3: Columns 11-14
    *   Section 4: Columns 16-19
5.  **Transformation:** The core transformation involves the yellow pixels in Section 1 and Section 4. The *entire pattern* of yellow pixels (maintaining relative positions) found in Section 1 is moved to Section 4, and the pattern of yellow pixels from Section 4 is moved to Section 1.
6.  **Pattern Anchoring:** When a pattern moves, its placement seems anchored by its top-leftmost pixel. The top-leftmost pixel of the pattern originally in Section 1 moves to the *same row* but starts at column 16 (the beginning of Section 4). Similarly, the top-leftmost pixel of the pattern originally in Section 4 moves to the *same row* but starts at column 1 (the beginning of Section 1).
7.  **Invariant Sections:** The patterns of yellow pixels within Section 2 and Section 3 remain unchanged in their positions between the input and output grids.

## Facts


```yaml
Grid:
  Properties:
    - Dimensions: Constant between input and output.
    - Background: Primarily white (0).
StaticObjects:
  - Type: SeparatorLines
    Properties:
      - Color: Green (3)
      - Shape: Vertical lines
      - Location: Columns 0, 5, 10, 15, 20
      - Role: Divide grid into sections; Remain unchanged.
Sections:
  - ID: 1
    Location: Columns 1-4
    Role: Contains dynamic patterns; Swaps content with Section 4.
  - ID: 2
    Location: Columns 6-9
    Role: Contains potentially dynamic patterns; Content remains unchanged.
  - ID: 3
    Location: Columns 11-14
    Role: Contains potentially dynamic patterns; Content remains unchanged.
  - ID: 4
    Location: Columns 16-19
    Role: Contains dynamic patterns; Swaps content with Section 1.
DynamicObjects:
  - Type: PixelPattern
    Properties:
      - Color: Yellow (4)
      - Shape: Collection of pixels within a section, maintaining relative positions.
      - Role: Represents the content to be moved.
Actions:
  - Name: IdentifyPatterns
    Target: Yellow pixels within Section 1 and Section 4.
    Details: Determine the set of yellow pixel coordinates and their relative arrangement for each section. Identify the top-leftmost pixel coordinate for each pattern.
  - Name: ClearTargetSections
    Target: Output grid Sections 1 and 4.
    Details: Set all pixels within columns 1-4 and 16-19 to white (0), preserving the green separators.
  - Name: SwapAndPlacePatterns
    Details:
      - Move the identified pattern from input Section 1 to output Section 4. The top-leftmost pixel of the pattern is placed at its original row, column 16. Other pixels are placed relative to this anchor.
      - Move the identified pattern from input Section 4 to output Section 1. The top-leftmost pixel of the pattern is placed at its original row, column 1. Other pixels are placed relative to this anchor.
Relationships:
  - Sections 1 and 4 are linked by a swap operation.
  - Sections 2 and 3 are independent of the swap operation.
  - Yellow pixel patterns maintain their internal relative structure during the swap.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Define the boundaries of the four operational sections based on the fixed green vertical lines: Section 1 (cols 1-4), Section 2 (cols 6-9), Section 3 (cols 11-14), Section 4 (cols 16-19).
3.  Identify all yellow pixels (color 4) located within Section 1 of the input grid. Record their coordinates. If any yellow pixels are found, find the minimum row (`min_row1`) and minimum column (`min_col1`) among them. Calculate the relative coordinates of all these yellow pixels with respect to (`min_row1`, `min_col1`).
4.  Identify all yellow pixels (color 4) located within Section 4 of the input grid. Record their coordinates. If any yellow pixels are found, find the minimum row (`min_row4`) and minimum column (`min_col4`) among them. Calculate the relative coordinates of all these yellow pixels with respect to (`min_row4`, `min_col4`).
5.  Clear all yellow pixels within Section 1 (columns 1-4) and Section 4 (columns 16-19) of the *output* grid by setting their color to white (0).
6.  Using the relative coordinates calculated in step 3 (from input Section 1), place the yellow pattern into Section 4 of the *output* grid. The anchor pixel (originally at `min_row1`, `min_col1`) should be placed at coordinate (`min_row1`, 16). Place all other pixels relative to this new anchor position.
7.  Using the relative coordinates calculated in step 4 (from input Section 4), place the yellow pattern into Section 1 of the *output* grid. The anchor pixel (originally at `min_row4`, `min_col4`) should be placed at coordinate (`min_row4`, 1). Place all other pixels relative to this new anchor position.
8.  The output grid, now containing the swapped patterns in Sections 1 and 4 and the unchanged content in Sections 2 and 3, is the final result.
```python
import copy

"""
The transformation identifies yellow pixel patterns within specific sections of the grid, 
defined by static vertical green lines. The grid is divided into four main 
operational sections: Section 1 (columns 1-4), Section 2 (columns 6-9), 
Section 3 (columns 11-14), and Section 4 (columns 16-19). 

The transformation rule is to swap the entire yellow pixel pattern found in 
Section 1 with the entire yellow pixel pattern found in Section 4. The patterns 
maintain their internal relative structure. The placement in the swapped section 
is anchored by the top-leftmost pixel of the original pattern. The top-leftmost 
pixel of the pattern from Section 1 moves to the same row but starts at the 
first column of Section 4 (column 16). Similarly, the top-leftmost pixel of the 
pattern from Section 4 moves to the same row but starts at the first column of 
Section 1 (column 1). The content (including yellow pixels) within Section 2 
and Section 3 remains unchanged.
"""

def find_yellow_pattern(grid: list[list[int]], start_col: int, end_col: int) -> tuple[int | None, list[tuple[int, int]]]:
    """
    Finds all yellow pixels within the specified column bounds.
    Calculates their coordinates relative to the top-leftmost yellow pixel found.

    Args:
        grid: The input grid.
        start_col: The starting column index (inclusive) of the section.
        end_col: The ending column index (inclusive) of the section.

    Returns:
        A tuple containing:
        - The row index of the top-leftmost yellow pixel (or None if no yellow pixels).
        - A list of relative coordinates (row_offset, col_offset) for all yellow pixels 
          relative to the top-leftmost pixel (or an empty list if none found).
    """
    coords = []
    min_row, min_col = float('inf'), float('inf')
    height = len(grid)
    
    for r in range(height):
        for c in range(start_col, end_col + 1):
            # Check bounds just in case, though columns should be valid
            if c < len(grid[0]) and grid[r][c] == 4: # 4 is yellow
                coords.append((r, c))
                if r < min_row:
                    min_row = r
                    min_col = c # Reset min_col when a new min_row is found
                elif r == min_row and c < min_col:
                    min_col = c # Update min_col if on the same min_row

    if not coords:
        return None, []

    # Calculate relative coordinates based on the found top-leftmost pixel
    relative_coords = [(r - min_row, c - min_col) for r, c in coords]
    
    return min_row, relative_coords

def clear_section(grid: list[list[int]], start_col: int, end_col: int):
    """
    Sets all pixels within the specified column bounds to white (0).

    Args:
        grid: The grid to modify (should be the output grid).
        start_col: The starting column index (inclusive).
        end_col: The ending column index (inclusive).
    """
    height = len(grid)
    width = len(grid[0])
    for r in range(height):
        for c in range(start_col, end_col + 1):
             if c < width: # Check bounds
                grid[r][c] = 0 # 0 is white

def place_pattern(grid: list[list[int]], anchor_row: int, target_start_col: int, relative_coords: list[tuple[int, int]]):
    """
    Places a pattern of yellow pixels onto the grid based on an anchor point and relative coordinates.

    Args:
        grid: The grid to modify (should be the output grid).
        anchor_row: The row index for the top-leftmost pixel of the pattern.
        target_start_col: The column index for the top-leftmost pixel of the pattern.
        relative_coords: A list of (row_offset, col_offset) tuples defining the pattern.
    """
    height = len(grid)
    width = len(grid[0])
    for rel_r, rel_c in relative_coords:
        target_row = anchor_row + rel_r
        target_col = target_start_col + rel_c
        # Check if the target coordinates are within the grid bounds
        if 0 <= target_row < height and 0 <= target_col < width:
            grid[target_row][target_col] = 4 # 4 is yellow

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by swapping the yellow pixel patterns between
    Section 1 (cols 1-4) and Section 4 (cols 16-19).

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        The 2D list representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Define section column boundaries (inclusive)
    sec1_start, sec1_end = 1, 4
    sec4_start, sec4_end = 16, 19

    # 1. Find the yellow pattern in Section 1 of the input grid
    anchor_row1, rel_coords1 = find_yellow_pattern(input_grid, sec1_start, sec1_end)

    # 2. Find the yellow pattern in Section 4 of the input grid
    anchor_row4, rel_coords4 = find_yellow_pattern(input_grid, sec4_start, sec4_end)

    # 3. Clear Section 1 and Section 4 in the output grid
    clear_section(output_grid, sec1_start, sec1_end)
    clear_section(output_grid, sec4_start, sec4_end)

    # 4. Place the pattern from original Section 1 into output Section 4
    if anchor_row1 is not None:
        place_pattern(output_grid, anchor_row1, sec4_start, rel_coords1)

    # 5. Place the pattern from original Section 4 into output Section 1
    if anchor_row4 is not None:
        place_pattern(output_grid, anchor_row4, sec1_start, rel_coords4)

    # Return the modified grid
    return output_grid
```
