
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

## Perception

The input consists of a grid containing various horizontal bars (contiguous segments of a single color) placed on different rows, with a solid horizontal bar of azure (8) always present at the very bottom row. The background is white (0).

The transformation involves rearranging the colored bars located above the azure line. These bars effectively "fall" downwards towards the azure line. As they fall, they also shift horizontally to align with the right edge of the grid. They stack upon the azure line (or upon each other) in a specific order: the bar that was originally lowest (closest to the azure line) ends up at the bottom of the stack (directly above the azure line), the next lowest bar stacks on top of that, and so on, up to the bar that was originally highest, which ends up at the top of the stack. The azure line itself remains unchanged in its position. The final output grid has the same dimensions as the input grid, filled with white except for the unchanged azure line and the rearranged, right-aligned, stacked bars.

## Facts


```yaml
objects:
  - id: background
    type: grid_area
    color: white
  - id: floor
    type: horizontal_line
    color: azure
    location: bottom_row
    persistent: true # Remains unchanged in output
  - id: bars
    type: collection
    elements:
      type: horizontal_segment
      properties:
        color: non-white, non-azure
        location: various rows above the floor
        length: variable
        contiguity: horizontal

actions:
  - name: identify_bars
    input: input_grid
    target: bars above the floor
    output: list_of_bars (with color, length, original_row_index)
  - name: sort_bars
    input: list_of_bars
    criteria: original_row_index (descending - lowest first)
    output: sorted_list_of_bars
  - name: place_bars
    input: sorted_list_of_bars, grid_width, floor_row_index
    target: output_grid
    process: iterate through sorted bars, placing each one aligned to the right edge, stacking vertically upwards from the floor row.
  - name: copy_floor
    input: input_grid floor
    target: output_grid
    process: place the floor line in the same position in the output grid.

relationships:
  - type: spatial
    description: Bars are initially located above the floor.
  - type: order
    description: The final vertical stacking order of bars is the reverse of their initial vertical order.
  - type: alignment
    description: In the output, bars are aligned to the right edge of the grid.

grid_properties:
  - width: constant between input and output
  - height: constant between input and output
```


## Natural Language Program

1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with the white color (0).
2.  Identify the row index of the horizontal azure (8) line (the 'floor') in the input grid.
3.  Copy this azure line from the input grid to the exact same location in the output grid.
4.  Scan the input grid rows *above* the azure line to identify all distinct horizontal, contiguous segments (bars) of non-white, non-azure colors. For each bar found, record its color, its length (number of cells), and its original row index.
5.  Create a list of these identified bars.
6.  Sort this list of bars based on their original row index in *descending* order (i.e., the bar with the highest row index, which was originally lowest/closest to the floor, comes first).
7.  Determine the width of the grid.
8.  Set a variable `current_placement_row` to be the row index immediately above the azure line (`floor_row_index - 1`).
9.  Iterate through the sorted list of bars (from lowest original bar to highest):
    a.  Calculate the starting column index for the current bar to make it align with the right edge: `start_column = grid_width - bar_length`.
    b.  Place the current bar onto the output grid at row `current_placement_row`, spanning columns from `start_column` to `grid_width - 1`, using the bar's color.
    c.  Decrement `current_placement_row` by 1 to prepare for placing the next bar on top.
10. The resulting output grid contains the stacked, right-aligned bars above the unchanged azure floor.
```python
import numpy as np

"""
The transformation takes an input grid containing horizontal bars of various colors above a solid azure floor line at the bottom. 
It identifies these bars, sorts them by their original vertical position (lowest first), and then stacks them vertically upwards starting from the row just above the azure floor. 
Crucially, each bar is aligned to the right edge of the grid in the output. The azure floor remains in its original position. The rest of the grid is white.
"""

def find_bars(input_grid: np.ndarray, floor_row_index: int) -> list[tuple[int, int, int]]:
    """
    Finds all horizontal bars (contiguous segments of the same color, not white or azure) 
    above the floor line.

    Args:
        input_grid: The input grid as a numpy array.
        floor_row_index: The row index of the azure floor.

    Returns:
        A list of tuples, where each tuple represents a bar: (color, length, row_index).
    """
    bars = []
    height, width = input_grid.shape
    
    # Scan rows above the floor
    for r in range(floor_row_index):
        c = 0
        while c < width:
            color = input_grid[r, c]
            # Check if it's a bar color (not white 0 or azure 8)
            if color != 0 and color != 8:
                # Found the start of a potential bar
                start_c = c
                bar_color = color
                # Find the end of the bar
                while c < width and input_grid[r, c] == bar_color:
                    c += 1
                length = c - start_c
                bars.append((bar_color, length, r))
                # Continue scanning from the end of the found bar
            else:
                # Not a bar color, move to the next column
                c += 1
    return bars

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rearranges horizontal bars from the input grid by stacking them vertically 
    from bottom to top (based on original position), right-aligned, 
    above a fixed azure floor line.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_array = np.zeros_like(input_array)

    # Find the azure floor line (assuming it's solid and at the bottom)
    floor_row_index = -1
    for r in range(height - 1, -1, -1):
        if np.all(input_array[r, :] == 8):
            floor_row_index = r
            break
        # Handle cases where floor might not be solid, find first row containing 8
        elif 8 in input_array[r, :]: 
             # Check if it's the actual floor by seeing if it spans the width or is the lowest row with 8
             is_floor = True
             for c_check in range(width):
                 # Allow for white padding around the floor as seen in examples
                 if input_array[r, c_check] != 8 and input_array[r, c_check] != 0:
                     is_floor = False
                     break
             if is_floor and 8 in input_array[r,:]: # Ensure there's at least one 8
                floor_row_index = r
                break


    if floor_row_index == -1:
        # Fallback or error handling if no azure floor is found
        # For this specific problem, assume the floor always exists.
        # If it might not, we'd return the input or an empty grid, depending on requirements.
        # Let's assume it's the last row if no solid '8' row is found but 8 exists somewhere
        # For robustnes lets find the lowest row containing an 8
        for r in range(height - 1, -1, -1):
            if 8 in input_array[r,:]:
                floor_row_index = r
                break
        # If still -1, it means no 8 exists at all, which contradicts the problem description
        # For now, we proceed assuming floor_row_index is valid based on examples.


    # Copy the floor line to the output grid
    if floor_row_index != -1:
         output_array[floor_row_index, :] = input_array[floor_row_index, :]
    else:
         # If no floor was found even with fallbacks, maybe return input?
         # Based on problem, floor is guaranteed.
         pass 

    # Identify all bars above the floor
    bars = find_bars(input_array, floor_row_index if floor_row_index != -1 else height)

    # Sort bars by original row index (descending order - lowest bar first)
    # Bars with higher row index were lower on the screen
    sorted_bars = sorted(bars, key=lambda x: x[2], reverse=True)

    # Place the sorted bars onto the output grid, right-aligned, stacking upwards
    if floor_row_index != -1:
        current_placement_row = floor_row_index - 1
    else:
        # If no floor, stack from bottom
        current_placement_row = height - 1
        
    for bar_color, bar_length, _ in sorted_bars:
        if current_placement_row < 0:
            # Stop if we run out of space at the top
            break 
            
        # Calculate start column for right alignment
        start_col = width - bar_length
        end_col = width
        
        # Place the bar
        output_array[current_placement_row, start_col:end_col] = bar_color
        
        # Move placement row up for the next bar
        current_placement_row -= 1

    # Convert back to list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
```

Previous Code:
```python
import numpy as np

"""
The transformation takes an input grid containing horizontal bars of various colors above a solid azure floor line at the bottom. 
It identifies these bars, sorts them by their original vertical position (lowest first), and then stacks them vertically upwards starting from the row just above the azure floor. 
Crucially, each bar is aligned to the right edge of the grid in the output. The azure floor remains in its original position. The rest of the grid is white.
"""

def find_bars(input_grid: np.ndarray, floor_row_index: int) -> list[tuple[int, int, int]]:
    """
    Finds all horizontal bars (contiguous segments of the same color, not white or azure) 
    above the floor line.

    Args:
        input_grid: The input grid as a numpy array.
        floor_row_index: The row index of the azure floor.

    Returns:
        A list of tuples, where each tuple represents a bar: (color, length, row_index).
    """
    bars = []
    height, width = input_grid.shape
    
    # Scan rows above the floor
    for r in range(floor_row_index):
        c = 0
        while c < width:
            color = input_grid[r, c]
            # Check if it's a bar color (not white 0 or azure 8)
            if color != 0 and color != 8:
                # Found the start of a potential bar
                start_c = c
                bar_color = color
                # Find the end of the bar
                while c < width and input_grid[r, c] == bar_color:
                    c += 1
                length = c - start_c
                bars.append((bar_color, length, r))
                # Continue scanning from the end of the found bar
            else:
                # Not a bar color, move to the next column
                c += 1
    return bars

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rearranges horizontal bars from the input grid by stacking them vertically 
    from bottom to top (based on original position), right-aligned, 
    above a fixed azure floor line.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_array = np.zeros_like(input_array)

    # Find the azure floor line (assuming it's solid and at the bottom)
    floor_row_index = -1
    for r in range(height - 1, -1, -1):
        if np.all(input_array[r, :] == 8):
            floor_row_index = r
            break
        # Handle cases where floor might not be solid, find first row containing 8
        elif 8 in input_array[r, :]: 
             # Check if it's the actual floor by seeing if it spans the width or is the lowest row with 8
             is_floor = True
             for c_check in range(width):
                 # Allow for white padding around the floor as seen in examples
                 if input_array[r, c_check] != 8 and input_array[r, c_check] != 0:
                     is_floor = False
                     break
             if is_floor and 8 in input_array[r,:]: # Ensure there's at least one 8
                floor_row_index = r
                break


    if floor_row_index == -1:
        # Fallback or error handling if no azure floor is found
        # For this specific problem, assume the floor always exists.
        # If it might not, we'd return the input or an empty grid, depending on requirements.
        # Let's assume it's the last row if no solid '8' row is found but 8 exists somewhere
        # For robustnes lets find the lowest row containing an 8
        for r in range(height - 1, -1, -1):
            if 8 in input_array[r,:]:
                floor_row_index = r
                break
        # If still -1, it means no 8 exists at all, which contradicts the problem description
        # For now, we proceed assuming floor_row_index is valid based on examples.


    # Copy the floor line to the output grid
    if floor_row_index != -1:
         output_array[floor_row_index, :] = input_array[floor_row_index, :]
    else:
         # If no floor was found even with fallbacks, maybe return input?
         # Based on problem, floor is guaranteed.
         pass 

    # Identify all bars above the floor
    bars = find_bars(input_array, floor_row_index if floor_row_index != -1 else height)

    # Sort bars by original row index (descending order - lowest bar first)
    # Bars with higher row index were lower on the screen
    sorted_bars = sorted(bars, key=lambda x: x[2], reverse=True)

    # Place the sorted bars onto the output grid, right-aligned, stacking upwards
    if floor_row_index != -1:
        current_placement_row = floor_row_index - 1
    else:
        # If no floor, stack from bottom
        current_placement_row = height - 1
        
    for bar_color, bar_length, _ in sorted_bars:
        if current_placement_row < 0:
            # Stop if we run out of space at the top
            break 
            
        # Calculate start column for right alignment
        start_col = width - bar_length
        end_col = width
        
        # Place the bar
        output_array[current_placement_row, start_col:end_col] = bar_color
        
        # Move placement row up for the next bar
        current_placement_row -= 1

    # Convert back to list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
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
0 2 2 2
0 0 3 3
8 8 8 8
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 21.42857142857143

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
0 0 0 0 0 2 2
0 0 0 0 0 0 3
0 0 0 0 1 1 1
0 5 5 5 5 5 5
0 0 6 6 6 6 6
0 0 0 4 4 4 4
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
0 2 2
0 0 4
8 8 8
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 44.44444444444444
Okay, let's analyze the results and refine the understanding of the transformation.

**General Assessment**

The initial code correctly identified the core components (floor, bars) and the actions (stacking, right-alignment). However, it failed on all examples because the rule used to determine the *order* of stacking was incorrect. The previous assumption was that bars stacked based on their original vertical position (lowest first). The results show this is wrong.

Example 1 shows Red (row 2) below Green (row 4).
Example 3 shows Red (row 0) below Yellow (row 1).
Example 2 shows a complex order: Gray (row 4), Magenta (row 6), Yellow (row 7), Blue (row 2), Red (row 0), Green (row 1) from bottom to top.

This implies the sorting key is not simply the original row index. Comparing the bar lengths to the stacking order across all examples reveals a consistent pattern: bars are stacked primarily based on their length in *descending* order (longest bars at the bottom), and secondarily by their original row index in *ascending* order (if lengths are equal, the bar from the higher row goes first).

**Strategy for Resolution:**

1.  Verify the bar identification (color, length, original row) is correct for all examples.
2.  Confirm the new sorting hypothesis (length descending, then row ascending) matches the required stacking order in all examples.
3.  Update the YAML facts and Natural Language Program to reflect this corrected sorting rule.
4.  The subsequent coder phase will need to implement this new sorting logic.

**Metrics Gathering**


*code_execution:*
```python
import numpy as np

# Re-implement find_bars for isolated execution
def find_bars(input_grid: np.ndarray, floor_row_index: int) -> list[tuple[int, int, int, int]]:
    """
    Finds all horizontal bars (contiguous segments of the same color, not white or azure) 
    above the floor line.

    Args:
        input_grid: The input grid as a numpy array.
        floor_row_index: The row index of the azure floor.

    Returns:
        A list of tuples, where each tuple represents a bar: 
        (color, length, row_index, start_col_index). 
        Added start_col_index for potential future use, although not needed for sorting here.
    """
    bars = []
    height, width = input_grid.shape
    
    # Scan rows above the floor
    scan_limit_row = floor_row_index if floor_row_index != -1 else height
    for r in range(scan_limit_row):
        c = 0
        while c < width:
            color = input_grid[r, c]
            # Check if it's a bar color (not white 0 or azure 8)
            if color != 0 and color != 8:
                # Found the start of a potential bar
                start_c = c
                bar_color = color
                # Find the end of the bar
                while c < width and input_grid[r, c] == bar_color:
                    c += 1
                length = c - start_c
                bars.append((bar_color, length, r, start_c))
                # Continue scanning from the end of the found bar
            else:
                # Not a bar color, move to the next column
                c += 1
    return bars

# Define inputs
input_1 = np.array([
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [2, 2, 2, 0],
    [0, 0, 0, 0],
    [0, 3, 3, 0],
    [0, 0, 0, 0],
    [8, 8, 8, 8]
])

input_2 = np.array([
    [0, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 5, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 0, 0],
    [0, 0, 0, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 8, 8, 8, 8]
])

input_3 = np.array([
    [2, 2, 0],
    [0, 4, 0],
    [8, 8, 8]
])

# --- Analysis ---
results = {}

for i, input_grid in enumerate([input_1, input_2, input_3]):
    example_num = i + 1
    height, width = input_grid.shape
    floor_row_index = -1
    # Simplified floor finding for this known structure
    for r in range(height - 1, -1, -1):
        if 8 in input_grid[r, :]:
            floor_row_index = r
            break
            
    # Find bars
    bars_found = find_bars(input_grid, floor_row_index)
    
    # Sort bars: key = (-length, row_index)
    # -length for descending length, row_index for ascending row index (tie-breaker)
    sorted_bars = sorted(bars_found, key=lambda x: (-x[1], x[2]))
    
    # Store results
    results[f"Example {example_num}"] = {
        "floor_row": floor_row_index,
        "bars_found (color, length, row, col)": bars_found,
        "sorted_bars (color, length, row, col)": sorted_bars,
        "stacking_order_rows": [bar[2] for bar in sorted_bars]
    }

# Print results
for example, data in results.items():
    print(f"--- {example} ---")
    print(f"Floor Row Index: {data['floor_row']}")
    print("Bars Found (color, length, row, start_col):")
    for bar in data['bars_found (color, length, row, col)']:
        print(f"  {bar}")
    print("Sorted Bars for Stacking (color, length, row, start_col):")
    for bar in data['sorted_bars (color, length, row, col)']:
        print(f"  {bar}")
    print(f"Implied Stacking Order (Original Rows, Bottom to Top): {data['stacking_order_rows']}")
    print("-" * 20)

# Expected Stacking Order (Original Rows, Bottom to Top) from manual analysis of outputs
expected_order = {
    "Example 1": [2, 4, 0],
    "Example 2": [4, 6, 7, 2, 0, 1],
    "Example 3": [0, 1]
}

print("\n--- Verification ---")
match = True
for example, data in results.items():
    print(f"Comparing {example}:")
    print(f"  Calculated Order: {data['stacking_order_rows']}")
    print(f"  Expected Order:   {expected_order[example]}")
    if data['stacking_order_rows'] == expected_order[example]:
        print("  Order Matches!")
    else:
        print("  Order DOES NOT Match!")
        match = False
print(f"\nOverall Sorting Hypothesis Correct: {match}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 ---
Floor Row Index: 6
Bars Found (color, length, row, start_col):
  (np.int64(1), 1, 0, 3)
  (np.int64(2), 3, 2, 0)
  (np.int64(3), 2, 4, 1)
Sorted Bars for Stacking (color, length, row, start_col):
  (np.int64(2), 3, 2, 0)
  (np.int64(3), 2, 4, 1)
  (np.int64(1), 1, 0, 3)
Implied Stacking Order (Original Rows, Bottom to Top): [2, 4, 0]
--------------------
--- Example 2 ---
Floor Row Index: 9
Bars Found (color, length, row, start_col):
  (np.int64(2), 2, 0, 1)
  (np.int64(3), 1, 1, 4)
  (np.int64(1), 3, 2, 0)
  (np.int64(5), 6, 4, 1)
  (np.int64(6), 5, 6, 0)
  (np.int64(4), 4, 7, 3)
Sorted Bars for Stacking (color, length, row, start_col):
  (np.int64(5), 6, 4, 1)
  (np.int64(6), 5, 6, 0)
  (np.int64(4), 4, 7, 3)
  (np.int64(1), 3, 2, 0)
  (np.int64(2), 2, 0, 1)
  (np.int64(3), 1, 1, 4)
Implied Stacking Order (Original Rows, Bottom to Top): [4, 6, 7, 2, 0, 1]
--------------------
--- Example 3 ---
Floor Row Index: 2
Bars Found (color, length, row, start_col):
  (np.int64(2), 2, 0, 0)
  (np.int64(4), 1, 1, 1)
Sorted Bars for Stacking (color, length, row, start_col):
  (np.int64(2), 2, 0, 0)
  (np.int64(4), 1, 1, 1)
Implied Stacking Order (Original Rows, Bottom to Top): [0, 1]
--------------------

--- Verification ---
Comparing Example 1:
  Calculated Order: [2, 4, 0]
  Expected Order:   [2, 4, 0]
  Order Matches!
Comparing Example 2:
  Calculated Order: [4, 6, 7, 2, 0, 1]
  Expected Order:   [4, 6, 7, 2, 0, 1]
  Order Matches!
Comparing Example 3:
  Calculated Order: [0, 1]
  Expected Order:   [0, 1]
  Order Matches!

Overall Sorting Hypothesis Correct: True

```
**YAML Facts**


```yaml
objects:
  - id: background
    type: grid_area
    color: white
  - id: floor
    type: horizontal_line # Can contain white pixels but includes azure pixels
    color: azure
    location: lowest_row_containing_azure # The specific row containing azure (8) pixels, typically the bottom-most such row.
    persistent: true # Remains unchanged in output
  - id: bars
    type: collection
    elements:
      type: horizontal_segment
      properties:
        color: non-white, non-azure
        location: various rows above the floor
        length: number of contiguous pixels of the same color in the row
        original_row_index: the row index where the bar was located in the input
        contiguity: horizontal

actions:
  - name: identify_elements
    input: input_grid
    output:
      - floor_row_index: index of the lowest row containing azure (8)
      - list_of_bars: collection of tuples (color, length, original_row_index) for each bar above the floor
  - name: sort_bars
    input: list_of_bars
    criteria:
      - primary: length (descending - longest first)
      - secondary: original_row_index (ascending - highest row first in case of length tie)
    output: sorted_list_of_bars
  - name: create_output_grid
    input: input_grid_dimensions
    process: Initialize grid with white (0)
    output: output_grid
  - name: place_floor
    input: input_grid_floor_row, floor_row_index
    target: output_grid
    process: Copy the floor row content from input to the same row index in output.
  - name: place_bars
    input: sorted_list_of_bars, grid_width, floor_row_index
    target: output_grid
    process: Iterate through sorted bars. For each bar, calculate the starting column for right-alignment (`grid_width - bar_length`). Place the bar in the highest available row *below* the previously placed bar (or below the top of the grid if it's the first bar), starting from the row immediately above the floor (`floor_row_index - 1`) and moving upwards.
    output: output_grid with floor and stacked bars

relationships:
  - type: spatial
    description: Bars are initially located above the floor. In the output, they are stacked vertically immediately above the floor and aligned to the right edge.
  - type: order
    description: The final vertical stacking order (bottom to top) is determined by the bars' length (longest first) and then their original row index (highest original row first for ties).
  - type: alignment
    description: In the output, bars are aligned to the right edge of the grid.

grid_properties:
  - width: constant between input and output
  - height: constant between input and output
```


**Natural Language Program**

1.  Determine the dimensions (height, width) of the input grid.
2.  Initialize an output grid of the same dimensions, filled entirely with the white color (0).
3.  Identify the row index (`floor_row_index`) of the lowest row in the input grid that contains at least one azure (8) pixel.
4.  Copy the entire content of the row at `floor_row_index` from the input grid to the same row index in the output grid.
5.  Scan the rows of the input grid *above* the `floor_row_index` to identify all distinct horizontal, contiguous segments (bars) of non-white (0) and non-azure (8) colors. For each bar found, record its color, its length (number of cells), and its original row index.
6.  Create a list of these identified bars.
7.  Sort this list of bars using two criteria:
    a.  Primary Sort Key: Bar length, in *descending* order (longest bars first).
    b.  Secondary Sort Key (for ties in length): Original row index, in *ascending* order (bars from rows closer to the top of the grid come first).
8.  Set a variable `current_placement_row` to be the row index immediately above the floor (`floor_row_index - 1`).
9.  Iterate through the sorted list of bars:
    a.  If `current_placement_row` is less than 0, stop placing bars (grid is full).
    b.  Get the current bar's color and length (`bar_color`, `bar_length`).
    c.  Calculate the starting column index for the current bar to make it align with the right edge: `start_column = grid_width - bar_length`.
    d.  Place the current bar onto the output grid at row `current_placement_row`, spanning columns from `start_column` to `grid_width - 1`, using `bar_color`.
    e.  Decrement `current_placement_row` by 1 to prepare for placing the next bar in the row above.
10. The resulting output grid contains the floor line and the bars stacked above it, ordered by length (desc) and original position (asc for ties), and right-aligned.
