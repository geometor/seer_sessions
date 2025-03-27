import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the color of inner gray pixels to red.

    Iterates through each pixel of the input grid. If a pixel is gray (5), 
    it examines its 8 neighboring pixels (Moore neighborhood). If all 8 neighbors 
    are within the grid boundaries and are also gray (5), the corresponding 
    pixel in the output grid is set to red (2). Otherwise, the pixel retains its 
    original color from the input grid. Pixels that are not gray in the input 
    remain unchanged in the output.
    """

    # Convert input list of lists to a numpy array for easier index checking
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid. 
    # We will modify this copy.
    output_array = np.copy(input_array)
    
    # Get the dimensions (height, width) of the grid
    height, width = input_array.shape

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    # Offsets are in (row_change, column_change) format
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),  # Top row (left, middle, right)
        ( 0, -1),           ( 0, 1),  # Middle row (left, right)
        ( 1, -1), ( 1, 0), ( 1, 1)   # Bottom row (left, middle, right)
    ]

    # Iterate through each pixel (cell) in the input grid using its row (r) and column (c) index
    for r in range(height):
        for c in range(width):
            
            # Check if the current pixel in the input grid is gray (color code 5)
            if input_array[r, c] == 5:
                
                # Assume initially that this gray pixel is an "inner" pixel
                is_inner_pixel = True
                gray_neighbor_count = 0 # Count how many valid gray neighbors we find

                # Check each of the 8 neighbors
                for dr, dc in neighbor_offsets:
                    # Calculate the absolute coordinates of the neighbor
                    neighbor_r, neighbor_c = r + dr, c + dc

                    # Check if the neighbor's coordinates are within the grid bounds
                    if 0 <= neighbor_r < height and 0 <= neighbor_c < width:
                        # If the neighbor is within bounds, check if it is gray (5)
                        if input_array[neighbor_r, neighbor_c] == 5:
                            gray_neighbor_count += 1
                        else:
                            # If a neighbor is within bounds but *not* gray, 
                            # then the current pixel (r, c) is not an inner pixel.
                            is_inner_pixel = False
                            break # No need to check other neighbors
                    else:
                        # If a neighbor is outside the grid bounds, 
                        # then the current pixel (r, c) is not an inner pixel (it's on the border).
                        is_inner_pixel = False
                        break # No need to check other neighbors
                
                # After checking all neighbors (or breaking early):
                # If the pixel was determined to be an inner pixel 
                # (meaning the loop completed without breaking) AND 
                # exactly 8 valid gray neighbors were found:
                if is_inner_pixel and gray_neighbor_count == 8:
                    # Change the color of the corresponding pixel in the output grid to red (2)
                    output_array[r, c] = 2
            
            # If the input pixel was not gray (5), it keeps its original color in the output_array (due to the initial copy).
            # If the input pixel was gray (5) but was not an inner pixel, it also keeps its gray color in the output_array.

    # Convert the final numpy array back to a standard Python list of lists
    output_grid = output_array.tolist()

    return output_grid