
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:
Identify a contiguous horizontal span of non-white pixels in the input row. 
This span must consist of exactly two colors: one 'singleton' color appearing once, 
and one 'block' color appearing one or more times. The singleton pixel must be 
located at either the leftmost or rightmost position within this span. 
The transformation involves performing a circular shift (roll) on the sequence of pixels 
within the span. If the singleton was originally at the left end, roll the sequence 
left by one position. If the singleton was originally at the right end, roll the 
sequence right by one position. Place the rolled sequence back into the same span 
location in the output grid. Background pixels (color 0) remain unchanged.
"""

def find_span_and_singleton_pos(row):
    """
    Identifies the contiguous non-white span, its boundaries, and the singleton's position.

    Args:
        row (np.array): The 1D input row.

    Returns:
        tuple: (span_start, span_end, singleton_pos) or (None, None, None) if pattern not found.
               singleton_pos is 'left' or 'right'. Returns None if conditions (contiguity, 
               exactly one singleton at an end, exactly two colors) are not met.
    """
    # Find indices of all non-white pixels (colors != 0)
    non_white_indices = np.where(row != 0)[0]

    # Check if there are at least two non-white pixels needed for a singleton and a block
    if len(non_white_indices) < 2:
        return None, None, None

    # Determine the potential start and end of the contiguous span
    span_start = np.min(non_white_indices)
    span_end = np.max(non_white_indices)

    # Verify that the identified span is truly contiguous (no background pixels within)
    # The number of non-white pixels must equal the length of the span
    expected_len = span_end - span_start + 1
    if len(non_white_indices) != expected_len:
        # Implies gaps (background pixels) within the span
        return None, None, None

    # Extract the sequence of pixels within the span
    span_sequence = row[span_start : span_end + 1]

    # Count the occurrences of each color within the span
    color_counts = Counter(span_sequence)

    # Verify exactly two distinct non-white colors exist in the span
    if len(color_counts) != 2:
        return None, None, None
        
    # Identify the singleton color (the one with count 1)
    singleton_color = None
    block_color = None
    for color, count in color_counts.items():
        if count == 1:
            if singleton_color is not None: # Found more than one color with count 1
                 return None, None, None
            singleton_color = color
        else: # Must be the block color (count > 1)
             if block_color is not None: # Found more than one color with count > 1
                 return None, None, None
             block_color = color

    # Check if we successfully identified one singleton and one block color
    if singleton_color is None or block_color is None:
        return None, None, None

    # Find the index of the singleton *within the original row*
    # We know its color, find where it is located between span_start and span_end
    singleton_index_in_row = -1
    if row[span_start] == singleton_color:
        singleton_index_in_row = span_start
    elif row[span_end] == singleton_color:
        singleton_index_in_row = span_end
    else:
         # Singleton is not at either end of the span, pattern mismatch
         return None, None, None

    # Determine singleton position ('left' or 'right') based on its index in the row
    if singleton_index_in_row == span_start:
        singleton_pos = 'left'
    elif singleton_index_in_row == span_end:
        singleton_pos = 'right'
    else:
        # This case should technically be caught above, but double-check
        return None, None, None

    # If all checks passed, return the span boundaries and singleton position
    return span_start, span_end, singleton_pos


def transform(input_grid):
    """
    Applies the span rotation transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.
                                     Expected to be effectively 1D (1 row).

    Returns:
        list of lists: The transformed grid, or the original grid if the
                       specific pattern is not found.
    """
    # --- Input Validation and Initialization ---
    # Check if input is a list and not empty
    if not isinstance(input_grid, list) or not input_grid:
        print("Warning: Input grid is not a list or is empty.")
        return input_grid # Return original for invalid input format

    # Check if it contains at least one row
    if len(input_grid) < 1:
         print("Warning: Input grid has no rows.")
         return input_grid # Return original

    # This task specifically targets 1-row grids based on examples.
    # Handle multi-row inputs by returning original or raising error if needed.
    if len(input_grid) > 1:
        print("Warning: Input grid has more than one row. This function expects a single row. Returning original.")
        return input_grid

    # Check if the first row is a list
    if not isinstance(input_grid[0], list):
         print("Warning: First element of input grid is not a list.")
         return input_grid # Return original for malformed input

    # Convert the first (and only) row to a NumPy array for efficient processing
    input_row = np.array(input_grid[0])
    # Create a copy of the input row to modify for the output
    output_row = input_row.copy()

    # --- Find the Span and Singleton Position ---
    # Call the helper function to identify the relevant pattern components
    span_start, span_end, singleton_pos = find_span_and_singleton_pos(output_row)

    # If the expected pattern (contiguous span, 2 colors, singleton at end) isn't found,
    # the helper returns None. In this case, return the original grid unchanged.
    if span_start is None:
        # print("Pattern not found. Returning original grid.") # Optional debug message
        return input_grid

    # --- Extract and Rotate the Span ---
    # Extract the sequence of pixels within the identified span
    span_sequence = output_row[span_start : span_end + 1]

    # Perform circular shift (roll) based on the singleton's original position
    rotated_sequence = None
    if singleton_pos == 'left':
        # If singleton was on the left, roll the sequence LEFT by 1
        # Example: [S, B, B] -> [B, B, S]
        rotated_sequence = np.roll(span_sequence, -1)
    elif singleton_pos == 'right':
        # If singleton was on the right, roll the sequence RIGHT by 1
        # Example: [B, B, S] -> [S, B, B]
        rotated_sequence = np.roll(span_sequence, 1)
    # else: # This case is prevented by checks in find_span_and_singleton_pos
        # print("Error: Invalid singleton position detected after check.")
        # return input_grid # Return original on internal error


    # --- Update Output Grid ---
    # Place the rotated sequence back into the output row at the original span location
    if rotated_sequence is not None:
         output_row[span_start : span_end + 1] = rotated_sequence
    else:
         # Should not happen if singleton_pos is 'left' or 'right'
         print("Error: Rotation failed.")
         return input_grid # Return original if rotation calculation failed

    # --- Format and Return Output ---
    # Convert the modified numpy row back to a list
    output_list = output_row.tolist()
    # Wrap the list in another list to match the required output format [[]]
    output_grid = [output_list]

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 7 6 6 6 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 6 6 6 7 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 7 6 6 6 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.285714285714292

## Example 2:
Input:
```
0 0 0 8 1 1 1 1 1 1 0 0 0 0
```
Expected Output:
```
0 0 0 1 1 1 1 1 1 8 0 0 0 0
```
Transformed Output:
```
0 0 0 8 1 1 1 1 1 1 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.285714285714292

## Example 3:
Input:
```
7 6 6 6 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
6 6 6 7 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
7 6 6 6 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.285714285714292
