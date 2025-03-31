
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
**Metrics Analysis:**

*   The `find_movable_objects` function correctly identifies the objects.
*   The sorting logic `key=lambda obj: (-obj['length'], obj['row'])` correctly implements: primary sort by length descending (`-obj['length']`), secondary sort by original row ascending (`obj['row']`).
*   The sequence of objects in the `code_output` matches the expected stacking order (bottom-up) derived from the expected outputs.
*   The key mistake was assuming the horizontal position (`col_start`, `col_end`) was preserved. It should be calculated based on right-alignment.

**Recap of Tie-breaking:**
My initial analysis of Example 1 tie-breaking was slightly confused. Let's re-verify:
Ex 1: Red (len 3, row 2), Green (len 2, row 4). No tie needed. Sorted: Red, Green.
My previous note said: "In Example 1, two lines (red and green) have the same length (3)." - This was WRONG. Red is length 3, Green is length 2.
Let's imagine a tie: If Red was length 2 (row 2) and Green was length 2 (row 4). Sorting key `(-length, row)` would give `(-2, 2)` for Red and `(-2, 4)` for Green. Sorting these tuples gives `(-2, 2)` first, then `(-2, 4)`. So Red (row 2) would be placed first (lower), then Green (row 4). This matches the "original row ascending" tie-breaker rule (`obj['row']`).

**Final Confirmation of Rules:**
1.  Find base (azure line, row `r_base`).
2.  Find movable objects (non-0, non-8 horizontal lines), note color, length, original row (`r_orig`), original columns.
3.  Sort objects by length descending, then by `r_orig` ascending.
4.  Initialize output grid (all 0s).
5.  Copy base line to output at `r_base`.
6.  Set `stack_row = r_base - 1`.
7.  For each sorted object:
    *   Calculate `new_col_start = grid_width - object_length`.
    *   Calculate `new_col_end = grid_width - 1`.
    *   Place object color in `output_grid[stack_row, new_col_start:new_col_end + 1]`.
    *   Decrement `stack_row`.
8.  Return output grid.

This seems consistent with all examples now.**General Assessment**

The previous attempt correctly identified the core task: sorting horizontal colored lines (objects) by length and stacking them. The sorting order (length descending, original row ascending for ties) was also correctly identified based on the code execution metrics. The key error was in determining the *horizontal placement* of the objects in the output stack. The initial assumption that original column indices were preserved was incorrect. Analysis of the failed examples shows that the objects are instead **right-aligned** within the grid width when placed in the output stack.

**Strategy for Resolution**

1.  Modify the logic for placing objects in the output grid. Instead of using the original `col_start` and `col_end`, calculate the new starting column based on the object's length and the grid's width to achieve right-alignment.
2.  Update the Facts and Natural Language Program to reflect this right-alignment rule accurately.

**Metrics**


*code_execution:*
```python
import numpy as np

def find_movable_objects(input_grid: np.ndarray) -> list:
    objects = []
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    for r in range(height):
        for c in range(width):
            if visited[r, c]: continue
            color = input_grid[r, c]
            if color == 0 or color == 8: # Ignore background and base
                visited[r, c] = True
                continue
            col_start = c
            col_end = c
            # Extend horizontally
            while col_end + 1 < width and input_grid[r, col_end + 1] == color and not visited[r, col_end + 1]:
                col_end += 1
            visited[r, col_start:col_end + 1] = True
            length = col_end - col_start + 1
            objects.append({'color': int(color), 'length': int(length), 'row': int(r), 'col_start': int(col_start), 'col_end': int(col_end)})
    return objects

def analyze_example(input_grid_list: list, output_grid_list: list, example_name: str):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    height, width = input_grid.shape

    print(f"\n--- Analysis: {example_name} ---")
    print(f"Grid Dimensions: {height}x{width}")

    # Find base line
    azure_row_in = -1
    for r in range(height - 1, -1, -1):
        if np.all(input_grid[r, :] == 8):
            azure_row_in = r
            break
    print(f"Input Azure Base Row: {azure_row_in}")

    azure_row_out = -1
    for r in range(height - 1, -1, -1):
        if np.all(output_grid[r, :] == 8):
            azure_row_out = r
            break
    print(f"Output Azure Base Row: {azure_row_out}")

    # Find and sort movable objects from input
    movable_objects_in = find_movable_objects(input_grid)
    sorted_objects = sorted(movable_objects_in, key=lambda obj: (-obj['length'], obj['row']))
    print("\nInput Movable Objects (Sorted by [-Length, Row]):")
    for i, obj in enumerate(sorted_objects):
        print(f"  {i+1}. {obj}")

    # Find movable objects in output and their positions
    movable_objects_out = find_movable_objects(output_grid)
    # Create a mapping for easy lookup based on color and length (assuming unique for simplicity in examples)
    # A more robust approach would match based on sorted order if colors/lengths repeat
    output_object_map = {(obj['color'], obj['length']): obj for obj in movable_objects_out}

    print("\nOutput Object Placement (Right-Alignment Check):")
    stack_row = azure_row_out - 1 if azure_row_out != -1 else height - 1
    placement_correct = True
    for i, obj in enumerate(sorted_objects):
        expected_row = stack_row - i
        expected_col_start = width - obj['length']
        expected_col_end = width - 1

        output_obj_key = (obj['color'], obj['length'])
        if output_obj_key in output_object_map:
            output_obj = output_object_map[output_obj_key]
            print(f"  Object {i+1} (Color: {obj['color']}, Len: {obj['length']}):")
            print(f"    Input Pos: Row={obj['row']}, Cols={obj['col_start']}-{obj['col_end']}")
            print(f"    Expected Output Pos: Row={expected_row}, Cols={expected_col_start}-{expected_col_end} (Right-aligned)")
            print(f"    Actual Output Pos:   Row={output_obj['row']}, Cols={output_obj['col_start']}-{output_obj['col_end']}")
            if not (output_obj['row'] == expected_row and output_obj['col_start'] == expected_col_start and output_obj['col_end'] == expected_col_end):
                placement_correct = False
                print("    MISMATCH!")
        else:
            print(f"  Object {i+1} (Color: {obj['color']}, Len: {obj['length']}): Not found in output grid!")
            placement_correct = False

    print(f"\nRight-Alignment Placement Consistent: {placement_correct}")


# Example 1 Data
grid1_in = [[0,0,0,1],[0,0,0,0],[2,2,2,0],[0,0,0,0],[0,3,3,0],[0,0,0,0],[8,8,8,8]]
grid1_out = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,3,3],[0,2,2,2],[8,8,8,8]]
analyze_example(grid1_in, grid1_out, "Example 1")

# Example 2 Data
grid2_in = [[0,2,2,0,0,0,0],[0,0,0,0,3,0,0],[1,1,1,0,0,0,0],[0,0,0,0,0,0,0],[0,5,5,5,5,5,5],[0,0,0,0,0,0,0],[6,6,6,6,6,0,0],[0,0,0,4,4,4,4],[0,0,0,0,0,0,0],[8,8,8,8,8,8,8]]
grid2_out = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,3],[0,0,0,0,0,2,2],[0,0,0,0,1,1,1],[0,0,0,4,4,4,4],[0,0,6,6,6,6,6],[0,5,5,5,5,5,5],[8,8,8,8,8,8,8]]
analyze_example(grid2_in, grid2_out, "Example 2")

# Example 3 Data
grid3_in = [[2,2,0],[0,4,0],[8,8,8]]
grid3_out = [[0,0,4],[0,2,2],[8,8,8]]
analyze_example(grid3_in, grid3_out, "Example 3")
```

*code_execution_result:*
outcome: OUTCOME_OK
```

--- Analysis: Example 1 ---
Grid Dimensions: 7x4
Input Azure Base Row: 6
Output Azure Base Row: 6

Input Movable Objects (Sorted by [-Length, Row]):
  1. {'color': 2, 'length': 3, 'row': 2, 'col_start': 0, 'col_end': 2}
  2. {'color': 3, 'length': 2, 'row': 4, 'col_start': 1, 'col_end': 2}
  3. {'color': 1, 'length': 1, 'row': 0, 'col_start': 3, 'col_end': 3}

Output Object Placement (Right-Alignment Check):
  Object 1 (Color: 2, Len: 3):
    Input Pos: Row=2, Cols=0-2
    Expected Output Pos: Row=5, Cols=1-3 (Right-aligned)
    Actual Output Pos:   Row=5, Cols=1-3
  Object 2 (Color: 3, Len: 2):
    Input Pos: Row=4, Cols=1-2
    Expected Output Pos: Row=4, Cols=2-3 (Right-aligned)
    Actual Output Pos:   Row=4, Cols=2-3
  Object 3 (Color: 1, Len: 1):
    Input Pos: Row=0, Cols=3-3
    Expected Output Pos: Row=3, Cols=3-3 (Right-aligned)
    Actual Output Pos:   Row=3, Cols=3-3

Right-Alignment Placement Consistent: True

--- Analysis: Example 2 ---
Grid Dimensions: 10x7
Input Azure Base Row: 9
Output Azure Base Row: 9

Input Movable Objects (Sorted by [-Length, Row]):
  1. {'color': 5, 'length': 6, 'row': 4, 'col_start': 1, 'col_end': 6}
  2. {'color': 6, 'length': 5, 'row': 6, 'col_start': 0, 'col_end': 4}
  3. {'color': 4, 'length': 4, 'row': 7, 'col_start': 3, 'col_end': 6}
  4. {'color': 1, 'length': 3, 'row': 2, 'col_start': 0, 'col_end': 2}
  5. {'color': 2, 'length': 2, 'row': 0, 'col_start': 1, 'col_end': 2}
  6. {'color': 3, 'length': 1, 'row': 1, 'col_start': 4, 'col_end': 4}

Output Object Placement (Right-Alignment Check):
  Object 1 (Color: 5, Len: 6):
    Input Pos: Row=4, Cols=1-6
    Expected Output Pos: Row=8, Cols=1-6 (Right-aligned)
    Actual Output Pos:   Row=8, Cols=1-6
  Object 2 (Color: 6, Len: 5):
    Input Pos: Row=6, Cols=0-4
    Expected Output Pos: Row=7, Cols=2-6 (Right-aligned)
    Actual Output Pos:   Row=7, Cols=2-6
  Object 3 (Color: 4, Len: 4):
    Input Pos: Row=7, Cols=3-6
    Expected Output Pos: Row=6, Cols=3-6 (Right-aligned)
    Actual Output Pos:   Row=6, Cols=3-6
  Object 4 (Color: 1, Len: 3):
    Input Pos: Row=2, Cols=0-2
    Expected Output Pos: Row=5, Cols=4-6 (Right-aligned)
    Actual Output Pos:   Row=5, Cols=4-6
  Object 5 (Color: 2, Len: 2):
    Input Pos: Row=0, Cols=1-2
    Expected Output Pos: Row=4, Cols=5-6 (Right-aligned)
    Actual Output Pos:   Row=4, Cols=5-6
  Object 6 (Color: 3, Len: 1):
    Input Pos: Row=1, Cols=4-4
    Expected Output Pos: Row=3, Cols=6-6 (Right-aligned)
    Actual Output Pos:   Row=3, Cols=6-6

Right-Alignment Placement Consistent: True

--- Analysis: Example 3 ---
Grid Dimensions: 3x3
Input Azure Base Row: 2
Output Azure Base Row: 2

Input Movable Objects (Sorted by [-Length, Row]):
  1. {'color': 2, 'length': 2, 'row': 0, 'col_start': 0, 'col_end': 1}
  2. {'color': 4, 'length': 1, 'row': 1, 'col_start': 1, 'col_end': 1}

Output Object Placement (Right-Alignment Check):
  Object 1 (Color: 2, Len: 2):
    Input Pos: Row=0, Cols=0-1
    Expected Output Pos: Row=1, Cols=1-2 (Right-aligned)
    Actual Output Pos:   Row=1, Cols=1-2
  Object 2 (Color: 4, Len: 1):
    Input Pos: Row=1, Cols=1-1
    Expected Output Pos: Row=0, Cols=2-2 (Right-aligned)
    Actual Output Pos:   Row=0, Cols=2-2

Right-Alignment Placement Consistent: True

```
**Facts**


```yaml
Task: Rearrange horizontal colored lines by length, stacking them right-aligned above a fixed base.

Input_Features:
  - Grid: 2D array of integers (colors) with width W and height H.
  - Background_Color: White (0).
  - Base_Object:
      - Identifier: A horizontal line of Azure (8) pixels, typically full width.
      - Position: Usually occupies the bottom-most row (row H-1).
      - Behavior: Fixed; remains unchanged in the output at its original position. If absent, the effective base for stacking is the bottom edge of the grid.
  - Movable_Objects:
      - Identifier: Horizontal contiguous lines of a single color.
      - Exclusions: White (0) background pixels and Azure (8) base pixels.
      - Properties:
          - color: The integer value (1-7, 9).
          - length: The number of pixels (width) of the line.
          - original_row: Row index in the input grid.
          - original_col_start: Starting column index in the input grid.
          - original_col_end: Ending column index in the input grid.

Transformation:
  - Action: Collect, sort, and stack Movable_Objects vertically above the Base_Object (or grid bottom), applying right-alignment.
  - Process:
      1. Identify the Base_Object (Azure line) and its row index (`base_row`). If no base object exists, `base_row` is conceptually H.
      2. Identify all Movable_Objects and their properties (color, length, original_row, original_col_start, original_col_end).
      3. Sort the Movable_Objects:
          - Primary key: By `length` in descending order.
          - Secondary key: By `original_row` in ascending order (topmost first in case of length tie).
      4. Create an output grid of the same dimensions (W x H) as the input, initialized to White (0).
      5. If a Base_Object exists, copy it to the output grid at `base_row`.
      6. Initialize the `current_stack_row` to `base_row - 1`.
      7. Iterate through the sorted Movable_Objects:
          a. Calculate the target horizontal position for right-alignment:
             - `target_col_start = W - length`
             - `target_col_end = W - 1`
          b. Place the current object's `color` into the output grid at `current_stack_row`, spanning columns from `target_col_start` to `target_col_end`.
          c. Decrement `current_stack_row` by 1.

Output_Features:
  - Grid: Same dimensions (W x H) as input.
  - Base_Object: Azure line (if present in input) in the same bottom row position.
  - Stacked_Objects: The Movable_Objects from the input, stacked vertically above the Base_Object (or bottom edge).
      - Vertical Order: Determined by the sort (longest first, then topmost original position).
      - Horizontal Position: Each object is right-aligned within the grid width.
  - Background: Remaining grid cells are White (0).

Relationships:
  - The final vertical position of a Movable_Object depends on its length and original row relative to other Movable_Objects.
  - The final horizontal position depends *only* on the object's length and the grid width (right-aligned). Original horizontal position is ignored for placement.
  - All Movable_Objects are stacked contiguously above the fixed Base_Object or grid bottom.
```


**Natural Language Program**

1.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Search the input grid, starting from the bottom row and moving upwards, to find the first row composed entirely of azure (8) pixels. If found, copy this azure line to the exact same row in the output grid and record its row index as `base_row`. If no such line is found, set `base_row` to be the total height of the grid (effectively placing the base just below the last row).
3.  Identify all distinct horizontal, contiguous lines of pixels in the input grid that are *not* white (0) and *not* azure (8). For each such line (object), record its color, its length (number of pixels), and its original row index in the input grid.
4.  Create a list of these identified objects.
5.  Sort this list of objects based on two criteria:
    *   Primary criterion: Sort by object length in descending order (longest objects first).
    *   Secondary criterion (for ties in length): Sort by the original row index in ascending order (objects that were originally higher in the input grid come first).
6.  Determine the width of the grid.
7.  Initialize a `current_stack_row` variable to `base_row - 1`.
8.  Iterate through the sorted list of objects:
    *   For the current object, retrieve its color and length.
    *   Calculate the starting column for placing the object in the output grid: `start_column = grid_width - object_length`.
    *   Place the object's color into the output grid at the `current_stack_row`, filling the cells from `start_column` up to the last column (inclusive).
    *   Decrement the `current_stack_row` by 1 (to move up one row for the next object).
9.  Return the completed output grid.
