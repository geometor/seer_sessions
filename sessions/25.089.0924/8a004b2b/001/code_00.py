import numpy as np

"""
1. Identify all pixels with the color yellow (4) in the input grid.
2. Determine the minimum row (`min_row`), minimum column (`min_col`), maximum row (`max_row`), and maximum column (`max_col`) among the coordinates of these yellow pixels. This defines the bounding box.
3. Calculate the dimensions of the output grid: `height = max_row - min_row + 1`, `width = max_col - min_col + 1`.
4. Create a new grid (the output grid) of size `height` x `width`, initialized entirely with the background color white (0).
5. Iterate through the input grid for rows `r` from `min_row + 1` to `max_row - 1` and for columns `c` from `min_col + 1` to `max_col - 1`.
6. For each pixel at input grid coordinate (`r`, `c`), copy its color value to the output grid at coordinate (`r - min_row`, `c - min_col`).
7. Set the color of the four corner pixels in the output grid to yellow (4):
    * Output grid [0, 0] = 4
    * Output grid [0, `width` - 1] = 4
    * Output grid [`height` - 1, 0] = 4
    * Output grid [`height` - 1, `width` - 1] = 4
8. Return the completed output grid.
"""

def find_pixel_coordinates(grid, color_value):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    coordinates = np.argwhere(grid == color_value)
    # argwhere returns row, col pairs
    return coordinates

def transform(input_grid):
    """
    Extracts the content within a bounding box defined by yellow pixels (4) 
    from the input grid and places it into a new output grid, keeping the 
    yellow pixels at the corners of the output.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all pixels with the color yellow (4)
    yellow_coords = find_pixel_coordinates(input_np, 4)

    if yellow_coords.size == 0:
        # Handle case where no yellow pixels are found (return empty or original?)
        # Based on examples, yellow pixels are always present.
        # If this occurs, it might indicate an unexpected input format.
        # For now, let's return an empty grid of the same size or raise an error.
        # Returning input might be safer if the pattern doesn't match.
         return input_grid # Or raise ValueError("No yellow markers found")

    # 2. Determine the bounding box coordinates
    min_row = np.min(yellow_coords[:, 0])
    min_col = np.min(yellow_coords[:, 1])
    max_row = np.max(yellow_coords[:, 0])
    max_col = np.max(yellow_coords[:, 1])

    # 3. Calculate the dimensions of the output grid
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # 4. Create a new output grid initialized with white (0)
    output_np = np.zeros((height, width), dtype=int)

    # 5 & 6. Extract inner content and place it in the output grid
    # Ensure there is inner content to copy (check if box is larger than 1x1)
    if height > 1 and width > 1:
        inner_content = input_np[min_row + 1 : max_row, min_col + 1 : max_col]
        # Calculate the shape of the destination area in the output grid
        dest_rows, dest_cols = inner_content.shape
        # Place the content starting at [1, 1] in the output grid
        if dest_rows > 0 and dest_cols > 0:
             output_np[1 : 1 + dest_rows, 1 : 1 + dest_cols] = inner_content


    # 7. Set the four corner pixels in the output grid to yellow (4)
    output_np[0, 0] = 4
    output_np[0, width - 1] = 4
    output_np[height - 1, 0] = 4
    output_np[height - 1, width - 1] = 4
    
    # Convert numpy array back to list of lists for the required output format
    output_grid = output_np.tolist()

    # 8. Return the completed output grid
    return output_grid