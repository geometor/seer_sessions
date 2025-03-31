import numpy as np

def transform(input_grid):
    """
    Tiles the input grid in a 2x2 arrangement to create the output grid.
    The output grid's dimensions are twice the input grid's dimensions.
    The input grid is copied into each of the four quadrants of the output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    input_height, input_width = input_array.shape
    
    # Calculate the dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2
    
    # Initialize the output grid with zeros (or any placeholder, it will be overwritten)
    # Use the same data type as the input
    output_array = np.zeros((output_height, output_width), dtype=input_array.dtype)
    
    # Copy the input grid into the top-left quadrant
    output_array[0:input_height, 0:input_width] = input_array
    
    # Copy the input grid into the top-right quadrant
    output_array[0:input_height, input_width:output_width] = input_array
    
    # Copy the input grid into the bottom-left quadrant
    output_array[input_height:output_height, 0:input_width] = input_array
    
    # Copy the input grid into the bottom-right quadrant
    output_array[input_height:output_height, input_width:output_width] = input_array
    
    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
