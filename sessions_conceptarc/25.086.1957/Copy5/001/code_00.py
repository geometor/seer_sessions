import numpy as np

"""
Identify blue pixels (color 1) in the input grid.
The number of blue pixels (N) determines the repetition count.
The alignment of blue pixels (all in one row or all in one column) determines the repetition direction ('horizontal' or 'vertical').
The minimum row/column index of the blue pixels determines the boundary for the pattern unit.
Extract the pattern unit:
- If alignment is horizontal, the unit is the columns from the start up to the first blue pixel column.
- If alignment is vertical, the unit is the rows from the start up to the first blue pixel row.
Create a separator:
- A column of white pixels (0) if horizontal.
- A row of white pixels (0) if vertical.
Construct the output by concatenating the pattern unit and separator N times, followed by a final pattern unit. The total number of pattern units is N+1.
"""

def transform(input_grid):
    """
    Repeats a section of the input grid based on the count, alignment, and 
    position of blue pixels (color 1), inserting white (color 0) separators.
    """
    input_arr = np.array(input_grid, dtype=int)
    height, width = input_arr.shape

    # 1. Identify all pixels in the input grid with the color blue (1).
    blue_coords = np.argwhere(input_arr == 1)

    # 2. Count the number of blue pixels found; let this count be N.
    N = len(blue_coords)

    # If N is 0, return the input grid (based on assumption, not explicitly shown in examples)
    if N == 0:
        # Although not specified, this is a likely base case.
        # Example 3 shows blue pixels are removed, so maybe return input without blue?
        # Let's stick to the pattern: N=0 means repeat 0+1 = 1 time with 0 separators.
        # Need to decide if blue pixels are removed in this case. Given example 3, it seems
        # the part *containing* blue is never part of the unit. Let's return the original grid for now.
        # Revisit if test cases fail.
         return input_grid # Tentative decision

    # 3. Determine if all blue pixels lie in the same row or the same column.
    rows, cols = blue_coords[:, 0], blue_coords[:, 1]
    
    direction = None
    r_min = -1
    c_min = -1

    if np.all(rows == rows[0]): # All blue pixels in the same row
        direction = 'horizontal'
        c_min = np.min(cols)
    elif np.all(cols == cols[0]): # All blue pixels in the same column
        direction = 'vertical'
        r_min = np.min(rows)
    else:
        # This case is not covered by the examples, raise an error or handle appropriately.
        # For now, assume it won't happen based on provided examples.
        raise ValueError("Blue pixels are not aligned in a single row or column.")

    # 4. Extract the pattern_unit from the input grid:
    pattern_unit = None
    if direction == 'horizontal':
        if c_min == 0: # If blue is in the first column, the unit is empty? This seems unlikely.
                       # Let's assume c_min will always be > 0 if direction is horizontal.
                       # Based on examples, pattern is *before* the blue pixels.
            pattern_unit = input_arr[:, :c_min]
        else:
             pattern_unit = input_arr[:, :c_min]
        
    elif direction == 'vertical':
        if r_min == 0: # Similar edge case check for rows.
             pattern_unit = input_arr[:r_min, :] # This would be empty
        else:
             pattern_unit = input_arr[:r_min, :]

    if pattern_unit is None or pattern_unit.size == 0:
         # Handle cases where the pattern unit might be empty based on blue pixel position.
         # Example 1: blue at (0,4), c_min=4, unit = input[:, :4] -> Correct
         # Example 2: blue at (0,3), (0,4), c_min=3, unit = input[:, :3] -> Correct
         # Example 3: blue at (3,0), (4,0), (5,0), r_min=3, unit = input[:3, :] -> Correct
         # Seems the logic holds, but add a check just in case.
         raise ValueError("Pattern unit could not be determined or is empty.")


    # 5. Create a separator:
    separator = None
    if direction == 'horizontal':
        unit_height, _ = pattern_unit.shape
        separator = np.zeros((unit_height, 1), dtype=int) # White column
    elif direction == 'vertical':
        _, unit_width = pattern_unit.shape
        separator = np.zeros((1, unit_width), dtype=int) # White row

    # 6. Construct the output grid by repeatedly concatenating
    output_parts = []
    
    # Append the first pattern_unit
    output_parts.append(pattern_unit)
    
    # Repeat N times: Append the separator, then append the pattern_unit.
    for _ in range(N):
        output_parts.append(separator)
        output_parts.append(pattern_unit)

    # Concatenate along the correct axis
    if direction == 'horizontal':
        output_grid = np.concatenate(output_parts, axis=1)
    else: # direction == 'vertical'
        output_grid = np.concatenate(output_parts, axis=0)

    return output_grid.tolist() # Return as list of lists per ARC standard
