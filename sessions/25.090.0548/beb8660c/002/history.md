
## train_1

**input:**
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```


## train_2

**input:**
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


**output:**
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


## train_3

**input:**
```
2 2 0
0 4 0
8 8 8
```


**output:**
```
0 0 4
0 2 2
8 8 8
```

Okay, let's analyze the task examples.

**Perception of Elements**

1.  **Grid Structure:** The input and output are grids of pixels, where each pixel has a color represented by an integer (0-9). White (0) acts as the background.
2.  **Azure Line (8):** In every example, there is a solid horizontal line composed of azure (8) pixels at the bottom row of the input grid. This line remains unchanged in the same position in the output grid. It functions as a fixed base or ground.
3.  **Colored Objects:** Above the azure line, the input grid contains various horizontal lines (segments) of different colors (blue, red, green, yellow, gray, magenta). These lines vary in length, color, and vertical/horizontal position. These are the objects that are transformed.
4.  **Transformation:** The core transformation involves rearranging the colored horizontal lines vertically. They appear to be collected, sorted, and then stacked compactly above the azure base line.
5.  **Sorting Mechanism:** Comparing the input and output arrangements, particularly in Example 2, reveals that the final vertical stacking order (from bottom to top, just above the azure line) corresponds to the objects sorted by their length in descending order. Longer lines are placed lower (closer to the azure base), and shorter lines are placed higher.
6.  **Tie-breaking:** In Example 1, two lines (red and green) have the same length (3). In the input, red is above green. In the output stack, red is placed first (lower) and green is placed directly above it. This suggests that for objects with the same length, their relative vertical order from the input is preserved during the sort (the one originally lower is placed lower in the stack).
7.  **Stacking:** The sorted objects are placed one by one, starting with the longest. The first (longest) object is placed in the row directly above the azure line. Each subsequent object is placed in the row directly above the previously placed object.
8.  **Horizontal Position:** Each object retains its original horizontal position (column indices) when placed in the output stack.
9.  **Background:** All space not occupied by the azure line or the rearranged colored objects becomes white (0).

**Facts**


```yaml
Task: Rearrange horizontal colored lines based on length.

Input_Features:
  - Grid: 2D array of integers (colors).
  - Objects:
      - Type: Horizontal contiguous lines of a single color.
      - Exclusions: White (0) background pixels are not objects. Azure (8) pixels form a special base object.
  - Base_Object:
      - Color: Azure (8).
      - Shape: Always a full-width horizontal line.
      - Position: Always occupies the bottom-most row.
      - Behavior: Fixed; remains unchanged in the output.
  - Movable_Objects:
      - Colors: Any color except White (0) and Azure (8).
      - Shape: Horizontal lines of varying lengths (>= 1 pixel).
      - Properties:
          - color: The integer value (1-7, 9).
          - length: The number of pixels in the line.
          - position: Original row and column indices in the input.

Transformation:
  - Action: Vertical rearrangement and stacking of Movable_Objects above the Base_Object.
  - Process:
      1. Identify all Movable_Objects and their properties (color, length, original position).
      2. Identify the Base_Object (Azure line) and its row index.
      3. Sort the Movable_Objects primarily by length in descending order.
      4. Use the original relative vertical order (topmost first) as a secondary sort key for objects with equal length (although examples suggest bottom-most first might be the tie-breaker - let's stick to the observed Ex1: Red was above Green, Red is placed first -> bottom-most first). Let's re-check Ex1: Input Red(row 2), Green(row 4). Output Red(row 5), Green(row 4). Red is lower. So, original *lower* object comes first in sort tiebreak.
      5. Create an output grid of the same dimensions as the input, initialized to White (0).
      6. Place the fixed Base_Object (Azure line) in the output grid at its original position.
      7. Initialize the 'current stacking row' to the row directly above the Base_Object.
      8. Iterate through the sorted Movable_Objects (longest first):
          a. Place the current object in the 'current stacking row', maintaining its original column indices.
          b. Decrement the 'current stacking row' by 1 for the next object.

Output_Features:
  - Grid: Same dimensions as input.
  - Base_Object: Azure line in the same bottom row position.
  - Stacked_Objects: The Movable_Objects from the input, stacked vertically above the Base_Object according to the length-sorted order, preserving original horizontal positions.
  - Background: Remaining grid cells are White (0).

Relationships:
  - The final vertical position of a Movable_Object depends on its length relative to other Movable_Objects.
  - The horizontal position of each Movable_Object is preserved from input to output.
  - All Movable_Objects are stacked contiguously above the fixed Base_Object.
```


**Natural Language Program**

1.  Initialize a new grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Locate the horizontal line of azure (8) pixels in the input grid. Copy this azure line to the exact same position in the new grid. Record the row index just above the azure line as the starting `stack_row`.
3.  Identify all distinct horizontal contiguous lines of pixels in the input grid that are *not* white (0) or azure (8). For each line, record its color, its length (number of pixels), its original column indices, and its original top row index.
4.  Create a list of these identified lines.
5.  Sort this list of lines based on the following criteria:
    *   Primary key: Sort by line length in descending order (longest lines first).
    *   Secondary key (for tie-breaking when lengths are equal): Sort by original top row index in descending order (lines that were originally lower in the input grid come first in case of a tie).
6.  Iterate through the sorted list of lines:
    *   For the current line, retrieve its color and original column indices.
    *   Place the pixels of this line into the new grid at the current `stack_row`, using its original column indices.
    *   Decrement the `stack_row` by 1 (move up one row for the next line).
7.  The new grid now contains the transformed output. Return the new grid.
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
