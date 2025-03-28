"""
Identify all pixels in the input grid that are not the background color white (0) and not the frame color red (2). These are the "content pixels". Find the minimum bounding box (smallest rectangle) that encloses all identified content pixels. Extract the subgrid from the input grid defined by this bounding box. This is the "source pattern". Create a new, larger grid ("scaled grid") whose height is twice the height of the source pattern and whose width is twice the width of the source pattern. Populate the scaled grid: For each pixel at (row, col) with color C in the source pattern, fill a 2x2 block of pixels in the scaled grid starting at (row * 2, col * 2) with the color C. Create the final output grid by adding a 1-pixel thick border of red (2) color around the entire scaled grid. The final output grid's dimensions will be (scaled_grid_height + 2) by (scaled_grid_width + 2).
"""

import numpy as np

def transform(input_grid):
    """
    Extracts a pattern of specific 'content' colors from the input,
    scales it up by 2x2, and adds a red border.
    """
    input_np = np.array(input_grid)
    background_color = 0
    frame_color = 2

    # 1. Identify content pixels (not background and not frame color)
    content_indices = np.where((input_np != background_color) & (input_np != frame_color))

    if len(content_indices[0]) == 0:
        # Handle case with no content pixels if necessary, though unlikely based on examples
        # Maybe return an empty grid or a default small grid?
        # For now, let's assume content pixels always exist.
        # Returning a 1x1 red grid as a placeholder.
         return np.array([[frame_color]], dtype=int)


    # 2. Find the minimum bounding box
    min_row = np.min(content_indices[0])
    max_row = np.max(content_indices[0])
    min_col = np.min(content_indices[1])
    max_col = np.max(content_indices[1])

    # 3. Extract the source pattern
    source_pattern = input_np[min_row:max_row+1, min_col:max_col+1]

    # 4. & 5. Create and populate the scaled grid (2x2 scaling)
    # We can use np.kron for efficient scaling. It repeats elements of an array.
    scale_factor = 2
    scaled_grid = np.kron(source_pattern, np.ones((scale_factor, scale_factor), dtype=source_pattern.dtype))

    # 6. Create the final output grid with a border
    scaled_height, scaled_width = scaled_grid.shape
    output_height = scaled_height + 2
    output_width = scaled_width + 2

    # Initialize output grid with the border color
    output_grid = np.full((output_height, output_width), frame_color, dtype=int)

    # Place the scaled grid inside the border
    output_grid[1:-1, 1:-1] = scaled_grid

    return output_grid.tolist() # Convert back to list of lists if required by ARC interface