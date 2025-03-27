import numpy as np

"""
The transformation operates independently on each column of the input grid. 
For each column, identify the set of unique colors present in that column. 
Based on this set of colors, apply a specific color substitution rule to every pixel 
within that column. 

The substitution rules derived from the examples are:
- If column contains only white (0): white remains white.
- If column contains only yellow (4): yellow remains yellow.
- If column contains only gray (5): gray remains gray.
- If column contains red (2) and yellow (4): red remains red, yellow becomes magenta (6).
- If column contains yellow (4) and magenta (6): yellow becomes gray (5), magenta remains magenta.
- If column contains yellow (4) and gray (5): yellow becomes red (2), gray remains gray.
- If column contains white (0) and yellow (4): white becomes green (3), yellow remains yellow.
- If column contains white (0) and green (3): white becomes maroon (9), green remains green.
- If column contains white (0) and maroon (9): white becomes yellow (4), maroon remains maroon.

If a column's color set does not match any of these specific rules, or if a pixel's 
color within a column is not explicitly mentioned in the rule for that column's color set, 
the pixel retains its original color.
"""

def transform(input_grid):
    """
    Transforms the input grid column by column based on the unique colors present in each column.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier column access
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize the output grid as a copy of the input grid. Modifications will be made in place.
    output_array = np.copy(input_array)

    # Iterate through each column index
    for c in range(cols):
        # Extract the current column
        column = input_array[:, c]
        
        # Find the set of unique colors in this column and sort them for consistent comparison
        unique_colors = tuple(sorted(list(np.unique(column))))

        # Define the transformation map for the current column based on its unique colors
        transform_map = {}
        if unique_colors == (0,): 
            transform_map = {0: 0}
        elif unique_colors == (4,): 
            transform_map = {4: 4}
        elif unique_colors == (5,): 
            transform_map = {5: 5}
        elif unique_colors == (2, 4): 
            transform_map = {2: 2, 4: 6} # Red remains Red, Yellow becomes Magenta
        elif unique_colors == (4, 6): 
            transform_map = {4: 5, 6: 6} # Yellow becomes Gray, Magenta remains Magenta
        elif unique_colors == (4, 5): 
            transform_map = {4: 2, 5: 5} # Yellow becomes Red, Gray remains Gray
        elif unique_colors == (0, 4): 
            transform_map = {0: 3, 4: 4} # White becomes Green, Yellow remains Yellow
        elif unique_colors == (0, 3): 
            transform_map = {0: 9, 3: 3} # White becomes Maroon, Green remains Green
        elif unique_colors == (0, 9): 
            transform_map = {0: 4, 9: 9} # White becomes Yellow, Maroon remains Maroon
        else:
            # If no specific rule matches the unique color set, use an identity map (no change)
            transform_map = {color: color for color in unique_colors}

        # Apply the determined transformation to each cell in the current column
        for r in range(rows):
            input_color = input_array[r, c]
            # Update the output array using the transformation map.
            # Use .get() with the original color as default in case a color isn't in the map 
            # (though this shouldn't happen if unique_colors includes all colors in the column).
            output_array[r, c] = transform_map.get(input_color, input_color)

    # Convert the output NumPy array back to a list of lists before returning
    return output_array.tolist()