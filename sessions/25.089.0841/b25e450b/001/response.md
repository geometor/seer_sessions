```python
import numpy as np

def transform(input_grid):
    """
    Transforms a grid based on the following rules applied to each pixel:
    1. Examine the 8 neighbors (Moore neighborhood) of the current pixel.
    2. Check if at least one neighbor is gray (5) AND at least one neighbor is orange (7).
    3. If this condition is true:
        a. If the current pixel is white (0), change it to orange (7) in the output grid.
        b. If the current pixel is NOT white (0), change it to white (0) in the output grid.
    4. If the condition is false, the pixel's color remains unchanged in the output grid.
    """

    # Convert input list of lists to a numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            has_gray_neighbor = False
            has_orange_neighbor = False

            # Iterate through the 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the center pixel itself
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_array[nr, nc]
                        # Check for gray neighbor
                        if neighbor_color == 5:
                            has_gray_neighbor = True
                        # Check for orange neighbor
                        if neighbor_color == 7:
                            has_orange_neighbor = True
            
            # Apply transformation rules if both gray and orange neighbors are found
            if has_gray_neighbor and has_orange_neighbor:
                current_pixel_color = input_array[r, c]
                # If the current pixel is white (0), change it to orange (7)
                if current_pixel_color == 0:
                    output_array[r, c] = 7
                # If the current pixel is not white (non-0), change it to white (0)
                else:
                    output_array[r, c] = 0
            # Otherwise (condition false), the pixel in output_array retains its original value (already copied)

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
```