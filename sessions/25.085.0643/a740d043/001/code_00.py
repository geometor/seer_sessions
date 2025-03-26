import numpy as np

"""
Identify all pixels in the input grid that are not blue (color 1). Determine the
bounding box enclosing these non-blue pixels. Create a new output grid with the
dimensions of the bounding box, initially filled with white (color 0). Copy the
non-blue pixels from the input grid into the output grid, maintaining their relative
positions within the bounding box.
"""

def transform(input_grid):
    """
    Extracts non-background objects (pixels not equal to 1) from the input grid,
    places them within their bounding box onto a new grid filled with color 0,
    preserving relative positions.

    Args:
        input_grid (list of lists): The input grid representing the puzzle state.

    Returns:
        list of lists: The transformed grid containing only the non-background
                     objects within their bounding box on a white background.
    """
    input_array = np.array(input_grid, dtype=int)
    background_color = 1
    output_fill_color = 0

    # Find coordinates of non-background pixels
    non_background_coords = np.argwhere(input_array != background_color)

    # Handle case where there are no non-background pixels (return empty grid or specific format if needed)
    if non_background_coords.size == 0:
        # Based on examples, this case might not occur or might need specific handling.
        # Returning a 1x1 white grid as a placeholder, adjust if needed based on task spec.
        return [[output_fill_color]] 

    # Determine the bounding box
    min_row = non_background_coords[:, 0].min()
    max_row = non_background_coords[:, 0].max()
    min_col = non_background_coords[:, 1].min()
    max_col = non_background_coords[:, 1].max()

    # Calculate output grid dimensions
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # Create the output grid initialized with the fill color
    output_array = np.full((height, width), output_fill_color, dtype=int)

    # Transfer non-background pixels to the output grid
    for r, c in non_background_coords:
        # Calculate the corresponding position in the output grid
        output_r = r - min_row
        output_c = c - min_col
        # Copy the color from the input grid
        output_array[output_r, output_c] = input_array[r, c]

    # Convert back to list of lists format for the ARC standard
    output_grid = output_array.tolist()

    return output_grid