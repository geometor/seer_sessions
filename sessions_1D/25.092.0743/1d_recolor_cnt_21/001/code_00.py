"""
Identifies contiguous horizontal segments (runs) of yellow (4) pixels within each row of the input grid. 
Recolors these segments in the output grid based on their length:
- Length 1 yellow segments become green (3).
- Length 2 yellow segments become orange (7).
- Length 3 yellow segments become blue (1).
All other pixels, including the white (0) background, remain unchanged.
"""

import numpy as np

def find_segments(row_array, target_color):
    """
    Finds contiguous segments of a target color in a 1D numpy array.

    Args:
        row_array (np.array): A 1D numpy array representing a row.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, length) 
              of a found segment.
    """
    segments = []
    start_index = -1
    current_length = 0
    for i, pixel in enumerate(row_array):
        if pixel == target_color:
            if start_index == -1:
                start_index = i
            current_length += 1
        else:
            if start_index != -1:
                segments.append((start_index, current_length))
                start_index = -1
                current_length = 0
    # Check if the row ends with a segment
    if start_index != -1:
        segments.append((start_index, current_length))
    return segments

def transform(input_grid):
    """
    Transforms the input grid by recoloring yellow segments based on their length.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_array = np.copy(input_array)
    
    # Define the color mapping based on segment length
    length_to_color = {
        1: 3,  # green
        2: 7,  # orange
        3: 1,  # blue
    }
    
    target_color = 4 # yellow

    # Iterate through each row of the grid
    for r in range(input_array.shape[0]):
        row = input_array[r, :]
        
        # Find all yellow segments in the current row
        yellow_segments = find_segments(row, target_color)
        
        # Process each found yellow segment
        for start, length in yellow_segments:
            # Determine the new color based on the segment's length
            new_color = length_to_color.get(length)
            
            # If the length has a corresponding color in our mapping
            if new_color is not None:
                # Update the pixels in the output array for this segment
                output_array[r, start:start + length] = new_color
                
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    return output_grid