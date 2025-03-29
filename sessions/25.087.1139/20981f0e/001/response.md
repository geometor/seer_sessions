```python
import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies red marker pixels (value 2). For each red marker pixel at position (r, c),
    it checks the 3x3 region in the input grid whose top-left corner is at (r+1, c+1).
    If any blue pixel (value 1) is found within this 3x3 region,
    a solid 2x2 blue square is drawn in the output grid with its top-left corner at (r+2, c+2).
    Red pixels and the background (value 0) are preserved from the input grid.
    """

    # Convert input_grid to a NumPy array if it isn't already
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # Initialize output grid with the same dimensions and background color (0)
    # Then copy the red pixels from the input
    output_grid = np.zeros_like(input_grid_np)
    red_pixels = np.where(input_grid_np == 2)
    output_grid[red_pixels] = 2

    # Find the locations of all red marker pixels
    red_marker_coords = np.argwhere(input_grid_np == 2)

    # Iterate through each red marker pixel
    for r, c in red_marker_coords:
        # Define the bounds for the 3x3 detection area
        detect_r_start = r + 1
        detect_r_end = r + 4  # Exclusive index for slicing
        detect_c_start = c + 1
        detect_c_end = c + 4  # Exclusive index for slicing

        # Ensure detection area is within grid bounds
        detect_r_start = max(0, detect_r_start)
        detect_r_end = min(height, detect_r_end)
        detect_c_start = max(0, detect_c_start)
        detect_c_end = min(width, detect_c_end)

        # Extract the detection area slice
        detection_area = input_grid_np[detect_r_start:detect_r_end, detect_c_start:detect_c_end]

        # Check if any blue pixel (1) exists in the detection area
        if np.any(detection_area == 1):
            # Define the bounds for the 2x2 output square area
            output_r_start = r + 2
            output_r_end = r + 4 # Exclusive index for slicing
            output_c_start = c + 2
            output_c_end = c + 4 # Exclusive index for slicing

            # Ensure output area is within grid bounds before drawing
            if output_r_start < height and output_c_start < width:
                # Calculate the actual end indices, clamped to grid dimensions
                actual_output_r_end = min(height, output_r_end)
                actual_output_c_end = min(width, output_c_end)

                # Draw the 2x2 blue square (or the portion within bounds)
                output_grid[output_r_start:actual_output_r_end, output_c_start:actual_output_c_end] = 1

    return output_grid.tolist() # Convert back to list of lists if necessary for the environment
```