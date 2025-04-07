"""
This module defines a function to transform an input grid based on identifying the first vertical line marker.
The transformation crops the input grid horizontally, keeping all columns to the left of the first vertical line marker.
A vertical line marker is defined as a column where all cells have the same color, and this color is different 
from the color of the top-left cell (0, 0) of the input grid.
"""

import numpy as np

def is_vertical_line_marker(column_data, background_color_ref):
    """
    Checks if a given column data represents a vertical line marker.

    Args:
        column_data (np.array): 1D array representing the column pixels.
        background_color_ref (int): The color of the top-left pixel of the original grid.

    Returns:
        bool: True if the column is a vertical line marker, False otherwise.
    """
    # A column must have at least one pixel.
    if column_data.size == 0:
        return False
        
    # Get the color of the first pixel in the column.
    marker_color = column_data[0]
    
    # The marker color must be different from the reference background color.
    if marker_color == background_color_ref:
        return False
        
    # Check if all pixels in the column have the same marker_color.
    # np.all efficiently checks if all elements are True (column_data == marker_color).
    return np.all(column_data == marker_color)

def transform(input_grid):
    """
    Transforms the input grid by cropping it horizontally based on the first vertical line marker.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed (cropped) grid. Returns the original grid if no marker is found.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Handle edge case of empty or 1-pixel wide grid
    if width == 0:
        return np.array([[]] * height) # Return empty grid with correct height
    if width == 1:
         # If the single column is a marker, return empty grid. Otherwise, return the column.
         background_color_ref = input_np[0, 0]
         if is_vertical_line_marker(input_np[:, 0], background_color_ref):
             return np.array([[]] * height)
         else:
             return input_np # Or maybe empty? Examples suggest marker is always found before end.
                             # Let's stick to the primary logic for now. The loop below handles width=1 correctly.

    # Identify the background color reference from the top-left pixel
    background_color_ref = input_np[0, 0]
    
    # Initialize marker column index
    marker_column_index = -1
    
    # Iterate through columns to find the first vertical line marker
    for c in range(width):
        # Extract the current column
        column_data = input_np[:, c]
        
        # Check if this column is a vertical line marker
        if is_vertical_line_marker(column_data, background_color_ref):
            # Found the first marker column
            marker_column_index = c
            # Stop searching
            break
            
    # If a marker column was found
    if marker_column_index != -1:
        # Create the output grid by slicing the input grid
        # Select all rows (:) and columns from 0 up to (but not including) marker_column_index
        output_grid = input_np[:, 0:marker_column_index]
    else:
        # If no marker column was found (this shouldn't happen based on examples,
        # but as a fallback, return the original grid or handle as needed)
        # Returning the original grid seems safest if the pattern assumption fails.
        output_grid = input_np 
        # Alternatively, could return an empty grid: output_grid = np.array([[]]*height)
        
    return output_grid.tolist() # Return as list of lists as per ARC standard output format