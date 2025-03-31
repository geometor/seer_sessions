
Previous Code:
```python
import numpy as np
from typing import List, Dict, Tuple

"""
Transformation Rule Description:

1.  Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Locate the horizontal line of azure (8) pixels in the input grid. Copy this azure line to the exact same position in the output grid. Record the row index immediately above the azure line as the starting `stack_row`. If no azure line exists, the behavior is undefined by the examples, but we might assume stacking starts from the bottom row.
3.  Identify all distinct horizontal contiguous segments (lines) of pixels in the input grid that are *not* white (0) or azure (8). These are the "movable objects". For each object, record its color, its length (number of pixels), its original top row index, and its original start and end column indices.
4.  Create a list of these identified movable objects.
5.  Sort this list of objects based on the following criteria:
    *   Primary key: Sort by object length in descending order (longest objects first).
    *   Secondary key (for tie-breaking when lengths are equal): Sort by the original top row index in ascending order (objects that were originally higher in the input grid come first in case of a tie).
6.  Iterate through the sorted list of objects:
    *   For the current object, retrieve its color, start column index, and end column index.
    *   Place the pixels of this object into the output grid at the current `stack_row`, spanning from its start column index to its end column index.
    *   Decrement the `stack_row` by 1 (move up one row for the next object to be placed).
7.  The output grid now contains the transformed arrangement. Return the output grid.
"""

def find_movable_objects(input_grid: np.ndarray) -> List[Dict]:
    """
    Finds all horizontal contiguous lines of non-background (0) and non-base (8) colors.

    Args:
        input_grid: The input numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'length', 'row', 'col_start', 'col_end'.
    """
    objects = []
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if visited[r, c]:
                continue

            color = input_grid[r, c]
            # Ignore background (0) and base (8) colors
            if color == 0 or color == 8:
                visited[r, c] = True
                continue

            # Found the start of a potential horizontal object
            col_start = c
            col_end = c
            # Extend to the right as long as the color is the same
            while col_end + 1 < width and input_grid[r, col_end + 1] == color and not visited[r, col_end + 1]:
                col_end += 1

            # Mark all pixels of this object as visited
            visited[r, col_start:col_end + 1] = True

            # Calculate length and store object details
            length = col_end - col_start + 1
            objects.append({
                'color': color,
                'length': length,
                'row': r,
                'col_start': col_start,
                'col_end': col_end
            })

    return objects

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Rearranges horizontal colored lines (objects) above a fixed azure (8) base line.
    Objects are sorted primarily by length (descending) and secondarily by original
    row position (ascending - topmost first) before being stacked vertically
    above the base line, maintaining their original horizontal positions.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_np)

    # Find the azure base line (color 8)
    azure_row = -1
    for r in range(height - 1, -1, -1):
        if np.all(input_np[r, :] == 8):
             azure_row = r
             # Copy the azure line to the output
             output_grid[azure_row, :] = 8
             break
        # Optimization: if we see a mix of 8 and non-8, it's not the full base line
        elif 8 in input_np[r,:]:
            # Handle cases where 8 might be part of movable objects or partial lines
            # Check if the entire row is azure
             is_full_azure_row = True
             azure_indices = []
             for c_idx, val in enumerate(input_np[r,:]):
                 if val == 8:
                     azure_indices.append(c_idx)
                 else:
                     is_full_azure_row = False
                     # break # No need to break if we need indices later

             if is_full_azure_row:
                 azure_row = r
                 output_grid[azure_row, :] = 8
                 break
             # else: # if not a full row, treat the azure segments as potentially movable
             # This part is tricky based on provided examples. The examples only show
             # full azure base lines. Assuming the task implies a single, full-width
             # base line at the bottom if present. Let's find the *last* row containing any 8.
             if azure_row == -1 and len(azure_indices) > 0:
                 # Check if *all* 8s are in this bottom-most row containing 8s
                 all_8s_in_input = np.argwhere(input_np == 8)
                 max_row_with_8 = np.max(all_8s_in_input[:, 0]) if len(all_8s_in_input) > 0 else -1

                 if r == max_row_with_8 and is_full_azure_row: # It must be a full line at the bottom-most position of any 8
                     azure_row = r
                     output_grid[azure_row, :] = 8
                     break
                 # If not a full row or not the bottom-most row with 8s, treat 8s as movable unless
                 # specified otherwise. The current implementation of find_movable_objects
                 # excludes 8, aligning with the examples.

    # Determine the starting row for stacking objects
    # If an azure line was found, stack above it. Otherwise, stack from the bottom.
    stack_row = azure_row - 1 if azure_row != -1 else height - 1

    # Find all movable objects (horizontal lines not 0 or 8)
    movable_objects = find_movable_objects(input_np)

    # Sort the objects:
    # 1. By length (descending)
    # 2. By original row index (ascending - topmost first)
    sorted_objects = sorted(movable_objects, key=lambda obj: (-obj['length'], obj['row']))

    # Place the sorted objects onto the output grid
    for obj in sorted_objects:
        if stack_row < 0:
            # Should not happen if grid dimensions are sufficient, but safety check
            print(f"Warning: Not enough space to stack object: {obj}")
            continue

        # Place the object in the current stack_row at its original horizontal position
        output_grid[stack_row, obj['col_start']:obj['col_end'] + 1] = obj['color']

        # Move the stack_row up for the next object
        stack_row -= 1

    # Convert back to list of lists format for the expected output
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```
Expected Output:
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```
Transformed Output:
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 3 3 0
2 2 2 0
8 8 8 8
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.285714285714292

## Example 2:
Input:
```
0 2 2 0 0 0 0
0 0 0 0 3 0 0
1 1 1 0 0 0 0
0 0 0 0 0 0 0
0 5 5 5 5 5 5
0 0 0 0 0 0 0
6 6 6 6 6 0 0
0 0 0 4 4 4 4
0 0 0 0 0 0 0
8 8 8 8 8 8 8
```
Expected Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
0 0 0 0 0 2 2
0 0 0 0 1 1 1
0 0 0 4 4 4 4
0 0 6 6 6 6 6
0 5 5 5 5 5 5
8 8 8 8 8 8 8
```
Transformed Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 3 0 0
0 2 2 0 0 0 0
1 1 1 0 0 0 0
0 0 0 4 4 4 4
6 6 6 6 6 0 0
0 5 5 5 5 5 5
8 8 8 8 8 8 8
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 22.857142857142847

## Example 3:
Input:
```
2 2 0
0 4 0
8 8 8
```
Expected Output:
```
0 0 4
0 2 2
8 8 8
```
Transformed Output:
```
0 4 0
2 2 0
8 8 8
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 44.44444444444444
