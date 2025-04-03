import copy

"""
Transforms a 1xN input grid by identifying contiguous horizontal segments of 
blue (1) pixels in the single row. Each blue segment found, scanning from 
left to right, is recolored sequentially starting with magenta (6), then 
orange (7), and potentially subsequent colors if more segments exist. 
White (0) pixels remain unchanged. The input and output are 2D lists 
representing 1xN grids.
"""

def transform(input_grid):
    """
    Applies the sequential recoloring transformation to blue segments in a 1xN grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid, 
                                      expected to be 1xN.

    Returns:
        list[list[int]]: The transformed 2D output grid.
    """
    # Ensure input is a list of lists and not empty
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Return input unchanged or raise error if format is unexpected
        # ARC standard implies this will be a valid grid format.
        # Returning a copy might be safer than modifying in place if input was reused.
        return copy.deepcopy(input_grid) 
        
    # Grid dimensions (assuming 1xN based on examples)
    height = len(input_grid)
    if height != 1:
        # Handle case where grid is not 1xN if necessary
        # For this task, we assume it is 1xN
        print(f"Warning: Expected 1xN grid, got {height}x{len(input_grid[0])} grid. Processing first row only.")
        
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Extract the single row from input and output for easier access
    # Modifications to output_row will affect output_grid due to reference
    input_row = input_grid[0]
    output_row = output_grid[0] 

    # Initialize the color for the first blue segment
    current_color = 6 # Starts with magenta
    
    # Use an index to iterate through the row
    i = 0
    
    # Iterate through the row to find and process blue segments
    while i < width:
        # Check if the current pixel is blue (1)
        if input_row[i] == 1:
            # Found the start of a blue segment
            start_index = i
            
            # Find the end of the contiguous blue segment
            j = i
            while j < width and input_row[j] == 1:
                j += 1
            # end_index is exclusive (points to the element *after* the segment)
            end_index = j 
            
            # Change the pixels in the output row for this segment
            for k in range(start_index, end_index):
                output_row[k] = current_color
                
            # Increment the color for the next segment found
            current_color += 1
            
            # Move the main index past the processed segment to avoid re-checking its pixels
            i = end_index
        else:
            # If the pixel is not blue (it's white 0), just move to the next pixel
            i += 1
            
    # The modifications were made directly to output_row, which is part of output_grid
    return output_grid