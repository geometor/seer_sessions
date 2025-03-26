```python
import numpy as np

def transform(input_grid):
    """
    Downsamples a 6x6 input grid to a 3x3 output grid.
    The value of each pixel in the output grid is determined by finding the 
    non-white pixel within the corresponding 2x2 block in the input grid.
    If a 2x2 block contains only white pixels (0), the corresponding output pixel is white (0).
    It assumes each 2x2 block in the input contains at most one non-white pixel.
    """
    
    # Convert input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Get dimensions of the input grid
    input_height, input_width = input_array.shape
    
    # Calculate dimensions of the output grid (half the input dimensions)
    output_height = input_height // 2
    output_width = input_width // 2
    
    # Initialize the output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through the input grid using 2x2 blocks
    for r_out in range(output_height):
        for c_out in range(output_width):
            # Define the top-left corner of the 2x2 block in the input grid
            r_in_start = r_out * 2
            c_in_start = c_out * 2
            
            # Extract the 2x2 block
            block = input_array[r_in_start:r_in_start+2, c_in_start:c_in_start+2]
            
            # Find the value for the output pixel
            output_value = 0 # Default to white (0)
            # Iterate through the pixels in the 2x2 block
            for r_block in range(2):
                for c_block in range(2):
                    pixel_value = block[r_block, c_block]
                    # If a non-white pixel is found, use its value and stop searching this block
                    if pixel_value != 0:
                        output_value = pixel_value
                        break # Assumes at most one non-white pixel per block
                if output_value != 0:
                    break # Exit outer loop as well if non-white pixel found

            # Assign the determined value to the corresponding pixel in the output grid
            output_grid[r_out, c_out] = output_value
            
    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()

```