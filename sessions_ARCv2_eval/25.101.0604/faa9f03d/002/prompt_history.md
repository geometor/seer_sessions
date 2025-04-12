
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 3 0 0
1 1 1 1 0 0 0 0 0 3 0 0
0 0 0 1 0 0 0 0 0 3 0 0
2 3 3 3 2 0 0 0 0 3 0 0
0 0 0 1 3 0 0 0 0 3 0 0
0 0 0 1 3 1 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 2 3 3 3 0 2 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 0 0
1 1 1 1 0 0 0 0 0 3 0 0
0 0 0 1 0 0 0 0 0 3 0 0
3 3 3 1 3 0 0 0 0 3 0 0
0 0 0 1 3 0 0 0 0 3 0 0
0 0 0 1 1 1 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 3 3 1 3 3 3 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 7 0
7 7 7 7 0 0 0 0 0 0 7 0
3 3 3 3 3 0 3 3 3 4 7 0
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 7 7 7 7 0 3 0 0 0
0 0 0 0 0 0 7 0 3 0 7 0
0 0 7 7 7 7 7 0 3 0 7 0
0 0 7 0 0 0 0 0 3 0 7 0
3 3 0 3 3 3 3 3 3 0 7 0
0 0 7 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 7 0
7 7 7 7 0 0 0 0 0 0 7 0
0 0 0 7 0 0 0 0 3 3 3 3
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 7 7 7 7 0 3 0 7 0
0 0 0 0 0 0 7 0 3 0 7 0
0 0 7 7 7 7 7 0 3 0 7 0
0 0 7 0 0 0 0 0 3 0 7 0
3 3 3 3 3 3 3 3 3 0 7 0
0 0 7 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 1 0 0 0 0 1 0 0 0 6 0
0 1 0 0 0 0 1 0 0 0 6 0
6 1 6 6 6 6 0 6 0 6 6 0
0 1 0 0 0 0 1 0 0 0 4 0
0 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 1 0 0 0 0 1 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0 0 0
6 1 6 6 6 6 1 6 6 6 6 0
0 1 0 0 0 0 1 0 0 0 6 0
0 1 0 0 0 0 1 0 0 0 6 0
0 1 1 1 1 1 1 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
```

Okay, I will analyze the provided examples to understand the transformation task.

## Perception of Elements

Based on the examples, particularly `train_1`, the task seems to involve modifying horizontal patterns within a grid.

1.  **Grid Structure:** The input and output are consistently 12x12 grids of colored cells (represented by integers).
2.  **Colors:** Different colors (0, 1, 2, 3, 4, 6, 7) appear, but specific transformations seem tied to particular colors acting as boundaries or fill patterns.
3.  **Key Transformations (Train 1):**
    *   **Red Boundaries (Color 2):** Pairs of color `2` on the same row define a segment. These boundaries are changed to color `3`. The content between them is filled with color `3`, except for one specific cell which is changed to color `1`. The position of this `1` appears dependent on whether a `0` was initially present within the segment.
    *   **Blue Propagation (Color 1):** Color `1` seems to fill gaps (horizontally) between existing `1`s. Any cell (including `0` or other colors like `3`) located immediately between two `1`s in the same row is changed to `1`.
4.  **Other Examples:** Trains 2 and 3 introduce other colors and potentially different rules (vertical propagation, row copying, specific column fills, horizontal fills with other colors like 3 and 6). However, the rules derived from Train 1 seem self-contained and consistently applied there. The task might focus specifically on the interactions observed with colors 1, 2, and 3 as seen in Train 1, or the examples might represent different modes or types of transformations applicable under different conditions not fully revealed. Given the instruction to find *the* transformation rule, I will focus on the clear rules from Train 1, assuming they represent the core task logic.
5.  **Process:** The transformation appears to happen in distinct steps: first handling the red boundaries, then propagating the blue color.

## YAML Facts Documentation

```yaml
Grid:
  type: object
  properties:
    size: 12x12
    cells: list of lists of integers (colors)

Colors:
  - 0: Black (Background/Empty)
  - 1: Blue
  - 2: Red (Boundary marker)
  - 3: Green (Fill color)
  - (Other colors 4, 6, 7 appear in other examples but their role in the primary transformation derived from train_1 is secondary or undefined)

Objects:
  - Horizontal Segment: A sequence of cells in a single row.
    properties:
      - boundary_left: Cell defining the start (e.g., color 2, or grid edge/0)
      - boundary_right: Cell defining the end (e.g., color 2, or grid edge/0)
      - content: Sequence of cells between boundaries
      - contains_zero: boolean indicating if any cell within the content was originally 0

Actions:
  - Find Red Boundary Pairs: Identify pairs of cells with color 2 on the same row.
  - Fill Segment: Change the color of cells within a segment to a specified color (e.g., 3).
  - Modify Boundaries: Change the color of boundary cells (e.g., 2 -> 3).
  - Place Marker: Change a specific cell within a filled segment to a different color (e.g., 1).
  - Propagate Color Horizontally: Change cells between two cells of the same color (e.g., 1) to that color.

Relationships/Rules:
  - Rule_Red_Boundary:
    - trigger: Pair of color 2 cells (c1, c2) on a row `r`.
    - action_1: Change cells (r, c1) and (r, c2) to color 3.
    - action_2: Fill cells (r, c) for c1 < c < c2 with color 3.
    - action_3: Determine marker position:
      - if original segment content (c1 < c < c2) contained 0: marker_pos = c1 + 2
      - else: marker_pos = c2 - 1
    - action_4: Change cell (r, marker_pos) to color 1.
  - Rule_Blue_Propagation:
    - trigger: A cell (r, c) is not color 1, but its horizontal neighbors (r, c-1) and (r, c+1) are both color 1.
    - action: Change cell (r, c) to color 1.
    - condition: Apply iteratively/repeatedly until no more changes occur in the row.
  - Order: Rule_Red_Boundary is applied first across the grid, then Rule_Blue_Propagation is applied.
```

## Natural Language Program

1.  **Initialization:** Create a working copy of the input grid.
2.  **Red Boundary Transformation Pass:**
    *   For each row `r` from top to bottom in the grid:
        *   Find all pairs of column indices `(c1, c2)` such that `c1 < c2`, the input grid at `(r, c1)` is `2`, and the input grid at `(r, c2)` is `2`. Process these pairs (if multiple pairs exist, assume they don't overlap based on examples).
        *   For each found pair `(c1, c2)`:
            *   Determine if any cell in the input grid at `(r, c)` for `c` between `c1 + 1` and `c2 - 1` (inclusive) has the color `0`. Store this boolean result (e.g., `found_zero`).
            *   In the working grid copy, change the color of cells `(r, c1)` and `(r, c2)` to `3`.
            *   In the working grid copy, change the color of all cells `(r, c)` for `c` between `c1 + 1` and `c2 - 1` (inclusive) to `3`.
            *   If `found_zero` is true, change the color of the cell at `(r, c1 + 2)` in the working grid copy to `1`.
            *   If `found_zero` is false, change the color of the cell at `(r, c2 - 1)` in the working grid copy to `1`.
3.  **Blue Propagation Pass:**
    *   For each row `r` from top to bottom in the working grid copy:
        *   Repeatedly scan the row until no changes are made in a full scan:
            *   Set a flag `change_made_in_scan` to false.
            *   For each column `c` from `1` to `width - 2`:
                *   If the cell `(r, c)` is *not* color `1`, AND the cell `(r, c-1)` is color `1`, AND the cell `(r, c+1)` is color `1`:
                    *   Change the color of cell `(r, c)` to `1`.
                    *   Set `change_made_in_scan` to true.
            *   If `change_made_in_scan` is false after scanning the entire row, exit the repetition for this row.
4.  **Final Output:** Return the modified working grid copy.
```python
import copy

"""
Transforms an input grid based on two primary rules applied sequentially:

1.  **Red Boundary Transformation:** Identifies horizontal segments defined by pairs of '2's (red) on the same row in the original input. 
    - The boundary '2's are changed to '3's (green).
    - The cells between the boundaries are filled with '3's.
    - A single '1' (blue) is placed within the segment. Its position depends on whether a '0' (black) was originally present between the boundaries:
        - If a '0' was present, the '1' is placed at column `c1 + 2` (where `c1` is the left boundary column).
        - If no '0' was present, the '1' is placed at column `c2 - 1` (where `c2` is the right boundary column).
    This transformation uses the original input grid to determine the segments and the presence of '0's, but applies changes to a working copy.

2.  **Blue Propagation:** Iteratively fills horizontal gaps between '1's. 
    - If a cell is not '1', but its immediate left and right neighbors in the same row are '1', the cell is changed to '1'.
    - This process repeats for each row until no more cells can be changed in that row.
    This transformation operates on the grid resulting from the Red Boundary Transformation pass.
"""

def find_red_boundaries(row_data: list[int]) -> list[tuple[int, int]]:
    """Finds pairs of indices corresponding to the color 2 in a row."""
    indices = [i for i, color in enumerate(row_data) if color == 2]
    pairs = []
    # Simple pairing assuming non-overlapping boundaries as seen in examples
    for i in range(0, len(indices), 2):
        if i + 1 < len(indices):
            pairs.append((indices[i], indices[i+1]))
    return pairs

def check_zero_in_segment(row_data: list[int], c1: int, c2: int) -> bool:
    """Checks if the color 0 exists in the row segment between c1+1 and c2-1."""
    if c1 + 1 >= c2: # Check if segment is empty or just boundaries
        return False
    return 0 in row_data[c1 + 1 : c2]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the red boundary transformation and blue propagation rules to the input grid.
    """
    # Initialize output_grid as a deep copy of the input to modify
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # --- 1. Red Boundary Transformation Pass ---
    # This pass uses the original input_grid for checks but modifies output_grid
    for r in range(height):
        original_row = input_grid[r]
        # Find pairs of '2's in the original row
        boundary_pairs = find_red_boundaries(original_row)

        for c1, c2 in boundary_pairs:
            # Check for '0' within the segment in the original row
            found_zero = check_zero_in_segment(original_row, c1, c2)

            # Modify the output_grid
            # Change boundaries to 3
            if 0 <= r < height and 0 <= c1 < width:
                 output_grid[r][c1] = 3
            if 0 <= r < height and 0 <= c2 < width:
                 output_grid[r][c2] = 3

            # Fill segment between boundaries with 3
            for c in range(c1 + 1, c2):
                 if 0 <= r < height and 0 <= c < width:
                     output_grid[r][c] = 3

            # Place '1' based on zero check
            if found_zero:
                marker_pos = c1 + 2
            else:
                marker_pos = c2 - 1

            if 0 <= r < height and 0 <= marker_pos < width:
                # Ensure marker is within the segment bounds before placing
                if c1 < marker_pos < c2:
                    output_grid[r][marker_pos] = 1
                # Handle edge case where segment is too small for marker placement logic (e.g., c1+2 >= c2)
                # The logic derived seems to assume segments are wide enough. If not, the original fill remains.


    # --- 2. Blue Propagation Pass ---
    # This pass operates entirely on the (potentially modified) output_grid
    for r in range(height):
        while True: # Keep iterating on the row until no changes are made
            change_made_in_scan = False
            # Create a temporary row copy to avoid propagation within the same scan
            row_copy = list(output_grid[r])
            for c in range(1, width - 1):
                # Check if cell is not blue, but neighbors are blue
                if row_copy[c] != 1 and row_copy[c-1] == 1 and row_copy[c+1] == 1:
                    # Check if the cell in the actual grid is still not blue before changing
                    # This handles cases where a cell might have been changed by the red boundary pass
                    if output_grid[r][c] != 1:
                        output_grid[r][c] = 1
                        change_made_in_scan = True
            
            if not change_made_in_scan:
                break # No changes in this scan, move to the next row

    return output_grid
```
