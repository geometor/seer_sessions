import copy
import sys

# Increase recursion depth for deep copy, just in case
# sys.setrecursionlimit(2000) # Usually not needed unless grids are huge

"""
Transforms the input grid based on the following rules:

1. Initialization: Create an output grid initially identical to the input grid.

2. Background and Leftward Propagation: Iterate through the input grid.
   - If a cell `(r, c)` in the input contains 0:
     - Check the cell immediately to its right `(r, c+1)`.
     - If the right cell exists (within bounds) and is non-zero, set the output cell `output_grid[r][c]` to the value of the right cell `input_grid[r][c+1]`.
     - Otherwise (right cell is 0 or out of bounds), set the output cell `output_grid[r][c]` to 5.
   - If a cell `(r, c)` in the input is non-zero, its value is initially kept in the output grid (this happens implicitly by copying).

3. Rightmost Segment Modification: Iterate through each row of the grid.
   - Identify all contiguous horizontal segments of non-zero numbers based on the *input* grid.
   - For each segment found in a row `r`, determine the column index `c_rightmost` of its rightmost cell.
   - Set the corresponding cell `output_grid[r][c_rightmost]` to 5.

4. Return the final modified output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # 1. Initialization: Create an output grid initially identical to the input grid.
    # Use deepcopy to avoid modifying the original input list if it's passed elsewhere
    try:
        output_grid = copy.deepcopy(input_grid)
    except RecursionError:
        # Fallback for extremely large grids if deepcopy hits recursion limits
        output_grid = [row[:] for row in input_grid]


    # 2. Background and Leftward Propagation
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:
                # Check cell to the right
                if c + 1 < cols and input_grid[r][c + 1] != 0:
                    # Propagate color from the right
                    output_grid[r][c] = input_grid[r][c + 1]
                else:
                    # Set to background color 5
                    output_grid[r][c] = 5
            # else: non-zero cells retain their original value from the copy initially

    # 3. Rightmost Segment Modification
    for r in range(rows):
        c = 0
        while c < cols:
            # Find the start of a non-zero segment in the *input* grid
            if input_grid[r][c] != 0:
                start_c = c
                # Find the end of this segment
                while c + 1 < cols and input_grid[r][c + 1] == input_grid[r][start_c]:
                     # Make sure it's the same non-zero color, although examples don't show mixed colors in a segment
                     # Let's assume segments are mono-colored based on examples
                     # Correction: The examples imply connectivity defines the segment, not just value.
                     # But rule seems simpler: contiguous non-zero values. Let's stick to that first.
                     # Re-evaluating: The rule is simpler than components. It's just horizontal runs.
                     # If input[r][c+1] is also non-zero (any non-zero), it's part of the segment.
                     # Let's refine: Find contiguous runs of *any* non-zero numbers.
                     if input_grid[r][c+1] != 0:
                         c += 1
                     else:
                         break # End of segment because next is zero
                
                # The loop finishes with c at the last column index of the segment
                rightmost_c = c
                # Modify the rightmost cell of this segment in the *output* grid
                output_grid[r][rightmost_c] = 5
                # Continue searching after this segment
                c += 1 # Move to the next potential start
            else:
                # Current cell is 0, move to the next column
                c += 1

    # 4. Return the final modified output grid
    return output_grid
