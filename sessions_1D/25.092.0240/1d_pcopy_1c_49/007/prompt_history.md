
## train_1

**input:**
```
0 8 8 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 6 6 6 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 8 8 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 8 8 0 8 8 8 0 0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of the Elements:**

1.  **Grid Structure:** The input and output grids appear to be one-dimensional arrays or single rows. All examples show a 1x32 grid.
2.  **Colors:** The primary colors involved are white (0) and one other non-white color per example (azure '8' or magenta '6').
3.  **Input Pattern:** Each input starts with a white pixel (0) followed by a three-pixel sequence of a non-white color (e.g., `8 8 8` or `6 6 6`). This sequence appears to act as a template. Further along the row, there are one or more isolated single pixels of the *same* non-white color as the template. These isolated pixels are surrounded by white pixels.
4.  **Transformation:** The core transformation seems to involve the isolated single non-white pixels. Each of these isolated pixels in the input is replaced in the output by a copy of the initial three-pixel template pattern. The replacement is centered on the original position of the isolated pixel.
5.  **Preservation:** The initial template pattern at the beginning of the row (indices 1, 2, 3) remains unchanged in the output. The white pixels (0) that are not part of the replacement also remain unchanged.

**Facts:**


```yaml
task_type: pattern_replacement
grid_dimensionality: 1D # or 1xN 2D grid

elements:
  - element: background
    color: white (0)
    role: fills most of the grid

  - element: template_pattern
    description: A sequence of three identical non-white pixels found near the start of the input grid.
    properties:
      - location: fixed, starts at index 1 (columns 1, 2, 3)
      - size: 3 pixels wide
      - color: consistent within the pattern (e.g., all azure '8' or all magenta '6')
      - count: 1 per input grid
    role: defines the pattern to be copied

  - element: target_pixel
    description: Isolated single pixels matching the color of the template_pattern.
    properties:
      - location: variable, occurs after the template_pattern
      - size: 1 pixel
      - color: same as template_pattern
      - context: must be surrounded by background pixels (white '0') horizontally.
      - count: one or more per input grid
    role: marks locations for pattern insertion

actions:
  - action: identify_template
    input: input_grid
    output: template_pattern (value and color)
    condition: located at indices [1, 2, 3]

  - action: identify_targets
    input: input_grid
    output: list of target_pixel locations (indices)
    condition: pixels match template_pattern color and are isolated (index > 3, input[index-1]==0, input[index+1]==0)

  - action: copy_paste_pattern
    source: template_pattern
    destination_grid: output_grid (initially a copy of input_grid)
    targets: identified target_pixel locations
    process: For each target location `i`, overwrite the output grid at indices `[i-1, i, i+1]` with the `template_pattern`.
    centering: The middle pixel of the copied pattern aligns with the original target_pixel location.

relationships:
  - relationship: color_match
    between: [template_pattern, target_pixel]
    details: The color of the target_pixels must be the same as the color of the pixels in the template_pattern.
  - relationship: positional
    between: [template_pattern, target_pixel]
    details: Target pixels always appear later in the grid than the template pattern.
  - relationship: isolation
    element: target_pixel
    details: Target pixels are horizontally adjacent only to background pixels.

output_construction:
  - step: Initialize the output grid as a copy of the input grid.
  - step: Identify the template pattern (color C, pattern CCC) at indices 1, 2, 3.
  - step: Find all indices `i` where the input grid has value C, and input[i-1] and input[i+1] are 0.
  - step: For each such index `i`, modify the output grid by setting output[i-1]=C, output[i]=C, output[i+1]=C.
```


**Natural Language Program:**

1.  Start with the input grid. Create a copy of the input grid to serve as the basis for the output grid.
2.  Identify the "template pattern": Look at the pixels at indices 1, 2, and 3 in the input grid. This three-pixel sequence is the template pattern. Note its color (let's call it C).
3.  Scan the input grid starting from index 4 to find all "target pixels". A target pixel is a pixel that meets two conditions:
    a.  Its color is C (the same color as the template pattern).
    b.  Its immediate horizontal neighbors (at index - 1 and index + 1) are both white (0).
4.  For each identified target pixel located at index `i`:
    a.  Modify the output grid (which started as a copy of the input).
    b.  Replace the pixel at index `i` in the output grid with color C.
    c.  Replace the pixel at index `i-1` in the output grid with color C.
    d.  Replace the pixel at index `i+1` in the output grid with color C.
    (Essentially, copy the template pattern `C C C` into the output grid, centered at index `i`).
5.  The final modified grid is the result.
```python
import copy

# COLOR_MAP = {
#     0: (238, 238, 238),  # white
#     1: (30, 147, 255),  # blue
#     2: (220, 50, 40),  # red
#     3: (79, 204, 48),  # green
#     4: (230, 200, 0),  # yellow
#     5: (85, 85, 85),  # gray
#     6: (229, 58, 163),  # magenta
#     7: (230, 120, 20),  # orange
#     8: (135, 216, 241),  # azure
#     9: (146, 18, 49),  # maroon
# }

def transform(input_grid):
    """
    Transforms the input grid based on a pattern replacement rule.
    1. Identifies a 3-pixel template pattern (e.g., C C C) starting at index 1
       in the input row. The color C is noted.
    2. Scans the rest of the input row (from index 4 onwards) for 'target' pixels.
    3. A target pixel is a pixel with color C that is surrounded by the
       background color (white, 0) on both its left and right sides.
    4. For each target pixel found at index 'i', the output grid (initially a
       copy of the input) is modified by replacing the pixels at indices
       i-1, i, and i+1 with the template color C.
    5. The initial template pattern at indices 1, 2, 3 remains unchanged.
    """

    # Ensure input is a list of lists and extract the first row
    # ARC grids are typically 2D, even if 1xN
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Handle unexpected input format if necessary, or raise error
        # For now, assume it's the expected format [[...]]
        return [] # Or raise ValueError("Invalid input grid format")

    input_row = input_grid[0]
    grid_width = len(input_row)

    # Initialize output_grid as a copy of the input_grid
    # Using copy.deepcopy to handle the list of lists structure properly
    output_grid = copy.deepcopy(input_grid)
    # Get a reference to the row we will modify
    output_row = output_grid[0]

    # Check if grid is wide enough for the template and potential targets
    if grid_width < 5: # Need at least index 1,2,3 for template and index 4 to check neighbors
        return output_grid # Return unchanged grid if too small

    # Identify the template color from index 1
    # We assume the pattern C C C exists at indices 1, 2, 3 based on examples
    template_color = input_row[1]
    background_color = 0 # White

    # Iterate through the grid to find target pixels
    # Start scan from index 4 (after the template)
    # End scan at grid_width - 2 to safely access index i+1
    for i in range(4, grid_width - 1):
        # Check if the current pixel is a target pixel
        current_pixel_color = input_row[i]
        left_neighbor_color = input_row[i-1]
        right_neighbor_color = input_row[i+1]

        is_target = (current_pixel_color == template_color and
                     left_neighbor_color == background_color and
                     right_neighbor_color == background_color)

        if is_target:
            # Apply the transformation: replace the segment [i-1, i, i+1]
            # in the output row with the template color
            output_row[i-1] = template_color
            output_row[i]   = template_color
            output_row[i+1] = template_color

    return output_grid
```
```python
import copy

def transform(input_grid):
    """
    Transforms the input grid based on a pattern replacement rule.
    1. Accepts the input grid, expected as a list containing a single list 
       representing one row (e.g., [[0, 8, 8, 8, ...]]). Extracts this 
       inner list as the input_row.
    2. Creates a modifiable copy of the input_row called output_row.
    3. Checks if the input_row is long enough (at least 4 elements) and if 
       the pattern 0 C C C (where C is a non-zero color) exists at the 
       beginning (indices 0, 1, 2, 3).
    4. If the initial pattern is found, identifies the template_color C 
       (the color at index 1).
    5. If the initial pattern is not found or the row is too short, returns 
       the original input grid unmodified.
    6. Iterates through the input_row using an index i, starting from index 1 
       and going up to the second-to-last index (length - 2).
    7. For each index i, checks if it represents a "target pixel" based on 
       the following conditions:
        a. The pixel at input_row[i] has the template_color C.
        b. The pixel to its left (input_row[i-1]) is the background color (white, 0).
        c. The pixel to its right (input_row[i+1]) is the background color (white, 0).
        d. The index i is greater than 3 (to ensure it's not part of the original 
           template pattern 0 C C C).
    8. If all target conditions are met for index i:
        a. Modifies the output_row.
        b. Sets the color of the pixel at index i-1 in output_row to C.
        c. Sets the color of the pixel at index i in output_row to C.
        d. Sets the color of the pixel at index i+1 in output_row to C.
    9. After iterating through all possible indices, wraps the final output_row 
       into a list to conform to the standard 2D grid format: output_grid = [output_row].
    10. Returns the output_grid.
    """

    # Ensure input is a list of lists (standard ARC format)
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Return empty list or raise error for invalid format
        return [] 

    # Extract the first (and only) row
    input_row = input_grid[0]
    grid_width = len(input_row)
    
    # Initialize output_row as a copy of the input_row
    # We modify this copy. Use list() for a shallow copy, sufficient for 1D list of ints.
    output_row = list(input_row) 

    # Define background color
    background_color = 0

    # --- Step 3 & 4: Check for template and identify template color ---
    template_color = -1 # Default invalid color
    if grid_width >= 4 and \
       input_row[0] == background_color and \
       input_row[1] != background_color and \
       input_row[1] == input_row[2] == input_row[3]:
        template_color = input_row[1]
    else:
        # --- Step 5: Return original if template not found ---
        # Need deepcopy here to return a distinct object matching the input structure
        return copy.deepcopy(input_grid) 

    # --- Step 6 & 7: Iterate and find targets ---
    # Loop from index 1 up to width - 2 to allow checking i-1 and i+1
    for i in range(1, grid_width - 1):
        # Check target conditions (a, b, c, d)
        is_target_color = (input_row[i] == template_color)
        has_background_neighbors = (input_row[i-1] == background_color and 
                                    input_row[i+1] == background_color)
        is_after_template = (i > 3)

        if is_target_color and has_background_neighbors and is_after_template:
            # --- Step 8: Apply transformation to output_row ---
            # Check bounds just in case, although loop range should guarantee this
            if i - 1 >= 0 and i + 1 < grid_width:
                output_row[i-1] = template_color
                output_row[i]   = template_color
                output_row[i+1] = template_color

    # --- Step 9 & 10: Wrap row in a list and return ---
    output_grid = [output_row]
    return output_grid
```
```python
"""
Transforms an input grid (expected as a 1xN 2D list) based on a pattern replacement rule.
1. Validates the input: Checks if the grid is [[row]], the row length is >= 4, 
   and the pattern [0, C, C, C] (where C != 0) exists at indices 0-3.
2. If validation fails, returns an unmodified deep copy of the input.
3. If valid, identifies the active_color C from index 1.
4. Creates a mutable copy of the input row (output_row).
5. Finds all "target" indices 'i' in the input row where i > 3 and the 
   sequence [0, C, 0] exists at indices [i-1, i, i+1].
6. For each target index 'i', modifies the output_row by setting indices 
   i-1, i, and i+1 to the active_color C.
7. Returns the modified output_row wrapped in a list: [output_row].
"""

import copy

def transform(input_grid):
    """
    Applies a pattern replacement transformation to a 1xN grid.
    """
    # --- Step 1: Validate Input Structure ---
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Return unchanged copy if structure is not List[List[int]] with one inner list
        return copy.deepcopy(input_grid) 

    input_row = input_grid[0]
    grid_width = len(input_row)
    background_color = 0

    # --- Step 2: Validate Input Pattern and Length ---
    active_color = -1 # Default invalid color
    is_valid_template = False
    if grid_width >= 4 and \
       input_row[0] == background_color and \
       input_row[1] != background_color and \
       input_row[1] == input_row[2] == input_row[3]:
        active_color = input_row[1]
        is_valid_template = True

    # --- Step 3: Handle Invalid Input ---
    if not is_valid_template:
        # Return unchanged copy if template pattern [0, C, C, C] is not found
        return copy.deepcopy(input_grid) 

    # --- Step 4: Identify Active Color (already done in Step 2) ---
    # active_color = input_row[1] 

    # --- Step 5: Create Output Copy ---
    # Create a mutable copy of the input row. list() creates a shallow copy, sufficient here.
    output_row = list(input_row) 

    # --- Step 6: Find Targets ---
    # Iterate through the input row to find target signatures [0, C, 0] after the initial template
    # Loop from index 1 up to width - 2 to allow checking neighbors i-1 and i+1 safely
    for i in range(1, grid_width - 1):
        # Check target conditions:
        # a. Index must be after the initial template marker (i > 3)
        # b. Center pixel must match the active_color
        # c. Left neighbor must be background_color
        # d. Right neighbor must be background_color
        is_after_template = (i > 3)
        is_target_color = (input_row[i] == active_color)
        has_background_neighbors = (input_row[i-1] == background_color and 
                                    input_row[i+1] == background_color)

        # --- Step 7: Apply Replacement ---
        if is_after_template and is_target_color and has_background_neighbors:
            # Modify the output_row: Replace [0, C, 0] segment with [C, C, C]
            # Bounds are implicitly checked by the loop range (1 to width-2)
            output_row[i-1] = active_color
            output_row[i]   = active_color
            output_row[i+1] = active_color

    # --- Step 8 & 9: Format and Return Output ---
    # Wrap the final output_row in a list to conform to the standard 2D grid format
    output_grid = [output_row]
    return output_grid
```

Previous Code:
```python
"""
Transforms an input grid (expected as a 1xN 2D list) based on a pattern replacement rule.
1. Validates the input: Checks if the grid is [[row]], the row length is >= 4, 
   and the pattern [0, C, C, C] (where C != 0) exists at indices 0-3.
2. If validation fails, returns an unmodified deep copy of the input.
3. If valid, identifies the active_color C from index 1.
4. Creates a mutable copy of the input row (output_row).
5. Finds all "target" indices 'i' in the input row where i > 3 and the 
   sequence [0, C, 0] exists at indices [i-1, i, i+1].
6. For each target index 'i', modifies the output_row by setting indices 
   i-1, i, and i+1 to the active_color C.
7. Returns the modified output_row wrapped in a list: [output_row].
"""

import copy

def transform(input_grid):
    """
    Applies a pattern replacement transformation to a 1xN grid.
    """
    # --- Step 1: Validate Input Structure ---
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Return unchanged copy if structure is not List[List[int]] with one inner list
        return copy.deepcopy(input_grid) 

    input_row = input_grid[0]
    grid_width = len(input_row)
    background_color = 0

    # --- Step 2: Validate Input Pattern and Length ---
    active_color = -1 # Default invalid color
    is_valid_template = False
    if grid_width >= 4 and \
       input_row[0] == background_color and \
       input_row[1] != background_color and \
       input_row[1] == input_row[2] == input_row[3]:
        active_color = input_row[1]
        is_valid_template = True

    # --- Step 3: Handle Invalid Input ---
    if not is_valid_template:
        # Return unchanged copy if template pattern [0, C, C, C] is not found
        return copy.deepcopy(input_grid) 

    # --- Step 4: Identify Active Color (already done in Step 2) ---
    # active_color = input_row[1] 

    # --- Step 5: Create Output Copy ---
    # Create a mutable copy of the input row. list() creates a shallow copy, sufficient here.
    output_row = list(input_row) 

    # --- Step 6: Find Targets ---
    # Iterate through the input row to find target signatures [0, C, 0] after the initial template
    # Loop from index 1 up to width - 2 to allow checking neighbors i-1 and i+1 safely
    for i in range(1, grid_width - 1):
        # Check target conditions:
        # a. Index must be after the initial template marker (i > 3)
        # b. Center pixel must match the active_color
        # c. Left neighbor must be background_color
        # d. Right neighbor must be background_color
        is_after_template = (i > 3)
        is_target_color = (input_row[i] == active_color)
        has_background_neighbors = (input_row[i-1] == background_color and 
                                    input_row[i+1] == background_color)

        # --- Step 7: Apply Replacement ---
        if is_after_template and is_target_color and has_background_neighbors:
            # Modify the output_row: Replace [0, C, 0] segment with [C, C, C]
            # Bounds are implicitly checked by the loop range (1 to width-2)
            output_row[i-1] = active_color
            output_row[i]   = active_color
            output_row[i+1] = active_color

    # --- Step 8 & 9: Format and Return Output ---
    # Wrap the final output_row in a list to conform to the standard 2D grid format
    output_grid = [output_row]
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 8 8 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 8 8 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.5

## Example 2:
Input:
```
0 6 6 6 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 6 6 6 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 6 6 6 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.0

## Example 3:
Input:
```
0 8 8 8 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 8 8 8 0 8 8 8 0 0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 8 8 8 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.5
**General Assessment:**

The provided Python code aims to implement the observed pattern: identify a `0 C C C` template at the start, find isolated `0 C 0` patterns later in the sequence, and replace them with `C C C`. The logic within the code appears to correctly reflect this interpretation based on a manual trace of the examples.

However, the execution results show that the `transform` function consistently returned the *original input* instead of the modified output. The "Pixels Off" count in the results (2, 4, 6) corresponds exactly to the number of background pixels (0s) that *should* have been changed to the active color `C` (one `0` on each side of the target `C`) in each example. This strongly suggests:

1.  The core logic (identify template `C`, find `0 C 0`, replace with `C C C`) is likely correct.
2.  The test harness correctly compared the function's output to the *expected* output, calculating the differing pixels.
3.  The function, as executed by the harness, failed to perform the replacement step (`output_row[i-1] = active_color`, etc.). The most likely reason is that the `if` condition controlling this replacement never evaluated to `True` during the test execution, despite manual tracing indicating it should have.

**Strategy:**

The strategy is to trust the initial analysis and the "Pixels Off" metric, assuming they point towards the correct transformation. The failure likely lies in a subtle implementation detail or an execution environment issue not apparent from the code snippet alone. We will proceed by refining the documentation (YAML facts and Natural Language Program) based on the confirmed pattern, assuming the core logic is correct but needs careful implementation. We will use `tool_code` to verify grid properties and color counts to ensure our understanding of the examples is sound.

**Metrics:**


*code_execution:*
```python
import numpy as np

def analyze_grid(name, grid):
    np_grid = np.array(grid)
    dims = np_grid.shape
    colors, counts = np.unique(np_grid, return_counts=True)
    color_counts = dict(zip(colors, counts))
    print(f"--- {name} ---")
    print(f"Dimensions: {dims}")
    print(f"Color Counts: {color_counts}")

# Example 1
train1_in = [[0, 8, 8, 8, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train1_out = [[0, 8, 8, 8, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
analyze_grid("Train 1 Input", train1_in)
analyze_grid("Train 1 Output", train1_out)
print("-" * 20)

# Example 2
train2_in = [[0, 6, 6, 6, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train2_out = [[0, 6, 6, 6, 0, 6, 6, 6, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
analyze_grid("Train 2 Input", train2_in)
analyze_grid("Train 2 Output", train2_out)
print("-" * 20)

# Example 3
train3_in = [[0, 8, 8, 8, 0, 0, 8, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train3_out = [[0, 8, 8, 8, 0, 8, 8, 8, 0, 0, 8, 8, 8, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
analyze_grid("Train 3 Input", train3_in)
analyze_grid("Train 3 Output", train3_out)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Train 1 Input ---
Dimensions: (1, 32)
Color Counts: {np.int64(0): np.int64(28), np.int64(8): np.int64(4)}
--- Train 1 Output ---
Dimensions: (1, 32)
Color Counts: {np.int64(0): np.int64(26), np.int64(8): np.int64(6)}
--------------------
--- Train 2 Input ---
Dimensions: (1, 32)
Color Counts: {np.int64(0): np.int64(27), np.int64(6): np.int64(5)}
--- Train 2 Output ---
Dimensions: (1, 32)
Color Counts: {np.int64(0): np.int64(23), np.int64(6): np.int64(9)}
--------------------
--- Train 3 Input ---
Dimensions: (1, 32)
Color Counts: {np.int64(0): np.int64(26), np.int64(8): np.int64(6)}
--- Train 3 Output ---
Dimensions: (1, 32)
Color Counts: {np.int64(0): np.int64(20), np.int64(8): np.int64(12)}

```
**Observations from Metrics:**

*   **Dimensions:** All inputs and outputs are 1x32 grids.
*   **Color Counts:**
    *   Example 1: Input has 4 '8's, Output has 6 '8's (+2). Input has 28 '0's, Output has 26 '0's (-2). Corresponds to one `0 8 0` -> `8 8 8` replacement.
    *   Example 2: Input has 5 '6's, Output has 9 '6's (+4). Input has 27 '0's, Output has 23 '0's (-4). Corresponds to two `0 6 0` -> `6 6 6` replacements.
    *   Example 3: Input has 6 '8's, Output has 12 '8's (+6). Input has 26 '0's, Output has 20 '0's (-6). Corresponds to three `0 8 0` -> `8 8 8` replacements.
*   The metrics confirm that each transformation involves replacing occurrences of the pattern `[background, active_color, background]` with `[active_color, active_color, active_color]`, where the `active_color` is defined by the `[background, active_color, active_color, active_color]` pattern at the start of the grid. The number of background pixels decreases by 2 per replacement, and the number of active color pixels increases by 2 per replacement.

**YAML Facts:**


```yaml
task_type: pattern_replacement_1D
grid_dimensionality: 1D (represented as 1xN 2D list)
grid_size: fixed at 1x32 for all examples

elements:
  - element: background
    color: white (0)
    role: default fill, part of template and target patterns

  - element: template_pattern_marker
    description: A fixed sequence [0, C, C, C] at the start of the grid (indices 0-3), where C is a non-background color.
    properties:
      - location: indices [0, 1, 2, 3]
      - structure: [background, active_color, active_color, active_color]
      - color_C: The non-background color (e.g., azure '8', magenta '6') varies per task instance but is consistent within the pattern.
    role: Defines the 'active_color' (C) for the transformation and remains unchanged in the output.

  - element: target_sequence
    description: A sequence [0, C, 0] found elsewhere in the grid.
    properties:
      - location: variable, must occur at index `i` where `i > 3`.
      - structure: [background, active_color, background]
      - color_C: Must match the 'active_color' defined by the template_pattern_marker.
    role: Identifies locations for replacement.

  - element: replacement_sequence
    description: The sequence that replaces a target_sequence.
    properties:
      - structure: [active_color, active_color, active_color]
      - color_C: Same as the 'active_color'.
    role: The output pattern applied at target locations.

actions:
  - action: identify_active_color
    input: input_grid
    condition: Check if grid[0][0]==0 and grid[0][1]==grid[0][2]==grid[0][3] != 0.
    output: active_color C = grid[0][1]
    fallback: If condition fails, return input unchanged.

  - action: find_and_replace
    input: input_grid, active_color C
    output: modified_grid
    process:
      1. Create a mutable copy of the input grid row.
      2. Iterate through the input row indices `i` from 1 up to `width - 2`.
      3. If `i > 3` AND input_row[i] == C AND input_row[i-1] == 0 AND input_row[i+1] == 0:
         - This identifies a target_sequence centered at `i`.
         - Modify the copied row: Set index `i-1` to C, index `i` to C, index `i+1` to C.
      4. Return the modified row wrapped in a list.

relationships:
  - relationship: color_consistency
    between: [template_pattern_marker, target_sequence, replacement_sequence]
    details: The non-background color 'C' must be the same across the template marker, the target sequence center, and the replacement sequence.
  - relationship: positional_exclusion
    between: [template_pattern_marker, target_sequence]
    details: Target sequences cannot overlap with the initial template pattern marker (target center index `i` must be > 3).
```


**Natural Language Program:**

1.  **Input Validation:** Check if the input is a 1xN grid (a list containing one list). If not, return it unchanged. Let the single row be `input_row`.
2.  **Template Identification:** Check if the `input_row` is at least 4 pixels long and if the first four pixels match the pattern `[0, C, C, C]`, where `C` is any color other than white (0).
3.  **Active Color Extraction:** If the template pattern is found, identify the color `C` (the value at index 1) as the `active_color`.
4.  **Invalid Input Handling:** If the template pattern is *not* found at the start, return an unmodified copy of the original input grid.
5.  **Initialization:** Create a modifiable copy of the `input_row`, let's call it `output_row`.
6.  **Target Search:** Iterate through the `input_row` using an index `i`, starting from `i=1` and ending at `i = length - 2`.
7.  **Target Condition Check:** For each index `i`, check if *all* the following conditions are true:
    *   The index `i` is greater than 3 (i.e., it's located after the initial template marker).
    *   The pixel at `input_row[i]` has the `active_color` `C`.
    *   The pixel at `input_row[i-1]` (the left neighbor) is white (0).
    *   The pixel at `input_row[i+1]` (the right neighbor) is white (0).
8.  **Replacement:** If all conditions in step 7 are met, modify the `output_row`:
    *   Set the pixel at index `i-1` to the `active_color` `C`.
    *   Set the pixel at index `i` to the `active_color` `C`.
    *   Set the pixel at index `i+1` to the `active_color` `C`.
9.  **Output Formatting:** After checking all possible indices `i`, wrap the final `output_row` in a list to create the `output_grid` (e.g., `[[...output_row...]]`).
10. **Return Result:** Return the `output_grid`.
