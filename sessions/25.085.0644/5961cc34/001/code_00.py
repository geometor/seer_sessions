import numpy as np

"""
Transforms an input grid based on the positions of blue (1), green (3), and yellow (4) pixels.
1. Initialize the output grid with the same dimensions as the input grid, filled with the background color (azure, 8).
2. Identify all pixels in the input grid that are blue (1) or green (3).
3. Determine the minimum bounding box (top-left and bottom-right coordinates) that encloses all identified blue and green pixels. If no blue or green pixels exist, skip this step and step 4.
4. Fill the area within this bounding box in the output grid with red (2) pixels.
5. Locate the single yellow (4) pixel in the input grid.
6. Identify the column index of this yellow pixel.
7. Fill the entire column corresponding to this index in the output grid, from the top row to the bottom row, with red (2) pixels. This overrides any pixels previously placed in this column by step 4.
"""

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    background_color = 8
    fill_color = 2
    shape_colors = [1, 3] # blue, green
    marker_color = 4 # yellow

    # 1. Initialize output_grid with background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 2. Identify all blue (1) or green (3) pixels
    shape_pixels_coords = np.argwhere(np.isin(input_grid_np, shape_colors))

    # 3. Determine the minimum bounding box for shape pixels
    if shape_pixels_coords.size > 0:
        min_row = np.min(shape_pixels_coords[:, 0])
        max_row = np.max(shape_pixels_coords[:, 0])
        min_col = np.min(shape_pixels_coords[:, 1])
        max_col = np.max(shape_pixels_coords[:, 1])

        # 4. Fill the area within the bounding box with red (2)
        output_grid[min_row:max_row+1, min_col:max_col+1] = fill_color

    # 5. Locate the single yellow (4) pixel
    marker_pixel_coords = np.argwhere(input_grid_np == marker_color)

    # 6. Identify the column index of the yellow pixel
    if marker_pixel_coords.size > 0:
        # Assuming there's only one yellow pixel as per observation
        marker_col = marker_pixel_coords[0, 1]

        # 7. Fill the entire column with red (2)
        output_grid[:, marker_col] = fill_color

    return output_grid.tolist() # Return as list of lists