"""
Fill white rows below a gray separator using a repeating color sequence from the first row.

1. Identify the sequence of colors present in the first row (pattern_sequence).
2. Identify rows below the second row (separator row) that are entirely white (target_rows).
3. Create the output grid, initially a copy of the input grid.
4. Iterate through each target_row.
5. For each target_row, determine the fill color by cycling through the pattern_sequence based on the row's position relative to the start of the target rows.
6. Fill the entire target_row in the output grid with the determined color.
7. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills white rows below a gray separator using a repeating color sequence 
    from the first row.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.
        
    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_arr = np.array(input_grid, dtype=int)
    output_arr = input_arr.copy()
    
    # Check if the grid is tall enough to have pattern, separator, and fill area
    if input_arr.shape[0] < 3:
        # If not tall enough, return the input as is (or handle as an error case if needed)
        # Based on examples, there's always at least 3 rows if transformation happens.
        return output_grid.tolist() 

    # 1. Identify the sequence of colors from the first row
    pattern_sequence = input_arr[0, :]
    pattern_len = len(pattern_sequence)
    
    # Define grid dimensions
    height, width = input_arr.shape

    # 3. Create the output grid (already done via output_arr = input_arr.copy())

    # 4. Iterate through rows starting from the third row (index 2)
    pattern_index = 0
    for r in range(2, height):
        # 2. Identify rows below the separator that are entirely white
        # Check if the current row consists entirely of white pixels (0)
        # Note: Based on the examples, we only fill rows that *were* white.
        # The logic implies filling starts from row 2 regardless of initial content,
        # but the description focuses on *white* rows. Let's stick to the pattern repetition logic.
        
        # 5. Determine the fill color by cycling through the pattern_sequence
        # The color for row 'r' is determined by the pattern_sequence element 
        # at index corresponding to (r-2) modulo pattern_len.
        # However, the pattern is applied *per row*, using one color from the sequence *per row*.
        # The index depends on which element of the sequence we need *for this row*.
        
        # Correct logic: The Nth row to be filled (starting from row index 2) gets the (N % pattern_len)-th color from the sequence.
        # N = r - 2
        color_index_in_sequence = (r - 2) % pattern_len 
        fill_color = pattern_sequence[color_index_in_sequence]
        
        # 6. Fill the entire target_row in the output grid with the determined color.
        # Check if the row in the *input* was white before filling. 
        # While the description says "fill white rows", the examples show filling *all* rows below row 1,
        # using the pattern. Let's follow the example behavior.
        output_arr[r, :] = fill_color
        
    # Convert back to list of lists for the expected output format
    return output_arr.tolist()