"""
Scales the content within the bounding box of the non-white object(s) in the input grid by a factor of 2x2 to produce the output grid.

1. Find all non-white pixels in the input grid.
2. Determine the minimal bounding box enclosing these pixels.
3. Create an output grid with dimensions twice the height and width of the bounding box.
4. Iterate through each pixel within the input grid's bounding box.
5. For each input pixel at relative coordinates (r, c) within the bounding box, copy its color to the 2x2 block starting at (r*2, c*2) in the output grid.
"""

import numpy as np

def find_bounding_box(grid):
    """
    Finds the minimal bounding box containing all non-zero pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (min_row, min_col, height, width) of the bounding box.
               Returns None if no non-zero pixels are found.
    """
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return None  # Or handle as appropriate, maybe return (0, 0, 0, 0) or raise error

    min_row = np.min(non_zero_coords[:, 0])
    max_row = np.max(non_zero_coords[:, 0])
    min_col = np.min(non_zero_coords[:, 1])
    max_col = np.max(non_zero_coords[:, 1])

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return min_row, min_col, height, width

def transform(input_grid):
    """
    Transforms the input grid by scaling the content of the non-white object's bounding box by 2x2.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid as a list of lists.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. & 2. Find the bounding box of non-white pixels
    bbox = find_bounding_box(input_array)

    # Handle case where no non-white pixels are found (though examples suggest this won't happen)
    if bbox is None:
        # Returning an empty grid or the original grid might be options depending on requirements.
        # Based on the problem description, we expect an object.
        # Let's return an empty 0x0 grid for now, or maybe raise an error.
        return [] 

    min_row, min_col, height, width = bbox

    # 3. Calculate output dimensions and initialize output grid
    output_height = height * 2
    output_width = width * 2
    output_array = np.zeros((output_height, output_width), dtype=int)

    # 4. & 5. Iterate through the bounding box in the input grid and scale to output grid
    for r in range(height):
        for c in range(width):
            # Get the color from the input grid within the bounding box
            color = input_array[min_row + r, min_col + c]

            # Calculate the top-left corner for the 2x2 block in the output grid
            out_r_start = r * 2
            out_c_start = c * 2

            # Fill the 2x2 block in the output grid
            output_array[out_r_start:out_r_start + 2, out_c_start:out_c_start + 2] = color

    # Convert back to list of lists format if required by the environment
    output_grid = output_array.tolist()
    return output_grid