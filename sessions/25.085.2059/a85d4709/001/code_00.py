"""
Transforms an input grid based on the column position of a gray pixel (5) in each row.

For each row in the input grid:
1. Find the column index of the gray pixel (value 5).
2. Determine an output color based on this column index:
   - If the gray pixel is in column 0, the output color is red (2).
   - If the gray pixel is in column 1, the output color is yellow (4).
   - If the gray pixel is in column 2, the output color is green (3).
3. Fill the entire corresponding row in the output grid with the determined output color.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize the output grid with the same dimensions, filled with zeros initially
    output_array = np.zeros((rows, cols), dtype=int)

    # Define the mapping from column index to output color
    color_map = {
        0: 2,  # Column 0 -> Red (2)
        1: 4,  # Column 1 -> Yellow (4)
        2: 3   # Column 2 -> Green (3)
    }

    # Iterate through each row of the input grid
    for i in range(rows):
        # Find the column index (j) where the value is gray (5) in the current row (i)
        # np.where returns a tuple of arrays; we need the first element of the first array
        gray_pixel_indices = np.where(input_array[i] == 5)[0]

        # Check if exactly one gray pixel was found in the row (as per assumption)
        if len(gray_pixel_indices) == 1:
            j = gray_pixel_indices[0]

            # Determine the output color using the map, default to 0 if index not in map (though unlikely based on examples)
            output_color = color_map.get(j, 0) 

            # Fill the corresponding row in the output grid with the determined color
            output_array[i, :] = output_color
        else:
            # Handle cases where the assumption of one gray pixel per row is violated
            # For now, we can leave the row as zeros or raise an error.
            # Based on the prompt, we assume exactly one gray pixel exists.
            # If no gray pixel is found, the output row remains 0. If multiple are found, it takes the first one.
            # A more robust implementation might require clarification on handling these cases.
            print(f"Warning: Row {i} does not contain exactly one gray pixel (5). Found indices: {gray_pixel_indices}")


    # Convert the output numpy array back to a list of lists for the expected format
    output_grid = output_array.tolist()

    return output_grid