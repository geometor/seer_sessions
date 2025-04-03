"""
Transforms the input grid by identifying the single non-white color, finding all
contiguous horizontal segments (runs) of that color within the grid (assumed to be 
effectively 1D or easily flattenable), selecting the segment with the maximum 
length, and creating an output grid of the same dimensions containing only that 
longest segment, with all other cells set to the background color (white, 0).
If multiple segments share the maximum length, the behavior isn't explicitly 
defined by the examples, but this implementation will keep the first one encountered
among the longest.
"""

import numpy as np
import itertools

def find_segments(flat_grid, target_color):
    """
    Finds all contiguous segments of a target color in a 1D numpy array.

    Args:
        flat_grid (np.ndarray): The 1D input grid (numpy array of integers).
        target_color (int): The color to find segments of.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              (start_index, end_index, length). Returns an empty list
              if no segments are found or target_color is 0.
    """
    if target_color == 0:
        return []

    segments = []
    start_index = None
    for i, pixel in enumerate(flat_grid):
        if pixel == target_color:
            # If we found the target color and are not currently in a segment, start one
            if start_index is None:
                start_index = i
        elif start_index is not None:
            # If we encounter a different color and were in a segment, the segment ends here
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = None # Reset for the next potential segment

    # After the loop, check if a segment was ongoing and extends to the end of the grid
    if start_index is not None:
        end_index = len(flat_grid) - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only the longest contiguous segment
    of the non-background color.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid. 
                                  Expected to be effectively 1D (e.g., shape 1xN or Nx1).

    Returns:
        np.ndarray: A 2D NumPy array representing the transformed output grid,
                    containing only the longest segment of the non-white color.
    """
    # Store original shape and flatten the grid for easier 1D processing
    original_shape = input_grid.shape
    flat_input = input_grid.flatten()
    
    # Initialize the flattened output grid with background color (0)
    flat_output = np.zeros_like(flat_input)

    # Identify the non-white color
    non_white_colors = np.unique(flat_input[flat_input != 0])
    
    # If the grid is all white or empty, return the all-white output grid reshaped
    if len(non_white_colors) == 0:
        return flat_output.reshape(original_shape)
        
    # Assume only one non-white color based on examples
    non_white_color = non_white_colors[0]

    # Find all segments of the non-white color in the flattened input
    segments = find_segments(flat_input, non_white_color)

    # If no segments are found, return the all-white output grid reshaped
    if not segments:
        return flat_output.reshape(original_shape)

    # Find the longest segment(s)
    max_length = 0
    for _, _, length in segments:
        if length > max_length:
            max_length = length
            
    # Get all segments that have the maximum length
    longest_segments = [seg for seg in segments if seg[2] == max_length]
    
    # Select the first longest segment found (based on start index)
    # Sort by start index just to be deterministic if order wasn't guaranteed
    longest_segments.sort(key=lambda x: x[0])
    chosen_segment = longest_segments[0] 

    # Copy the chosen longest segment to the flattened output grid
    start, end, _ = chosen_segment
    flat_output[start : end + 1] = non_white_color

    # Reshape the flat output back to the original grid shape and return
    output_grid = flat_output.reshape(original_shape)
    return output_grid