"""
Transforms a 1D grid (represented as a list of lists with one inner list) by identifying contiguous segments of non-background (non-zero) pixels. For each segment, it determines the most frequent color (majority color). It then constructs the output grid by replacing all pixels within each segment with that segment's majority color. Background (zero) pixels remain unchanged. The output format matches the input format (list of lists).
"""

import numpy as np
from collections import Counter

def find_non_background_segments(grid_1d):
    """
    Finds contiguous segments of non-zero pixels in a 1D numpy array.

    Args:
        grid_1d: A 1D numpy array representing the grid row.

    Returns:
        A list of tuples, where each tuple contains (start_index, end_index) 
        for a non-background segment. end_index is exclusive.
        Returns empty list if no non-background pixels are found.
    """
    segments = []
    in_segment = False
    start_index = -1
    # Iterate through the grid with index
    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and not in_segment:
            # Start of a new segment
            in_segment = True
            start_index = i
        elif pixel == 0 and in_segment:
            # End of the current segment (found a background pixel)
            in_segment = False
            segments.append((start_index, i)) 
            start_index = -1
            
    # Handle the case where a segment runs to the very end of the grid
    if in_segment:
        segments.append((start_index, len(grid_1d)))
        
    return segments

def get_majority_color(segment_pixels):
    """
    Determines the most frequent color in a numpy array of pixels. 
    Handles empty segments and uses Counter's default tie-breaking.

    Args:
        segment_pixels: A numpy array of pixel values from a segment.

    Returns:
        The integer value of the most frequent color. Returns None if segment is empty.
    """
    # Check if the segment is empty
    if not segment_pixels.size > 0:
        return None
    
    # Count occurrences of each color
    color_counts = Counter(segment_pixels)
    
    # Check if Counter is empty (shouldn't happen if segment_pixels wasn't empty)
    if not color_counts:
        return None
        
    # Find the most common color. most_common(1) returns list: [(color, count)]
    # In case of ties, most_common returns one of the tied elements arbitrarily.
    majority_color, _ = color_counts.most_common(1)[0]
    return majority_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid (expected to have one inner list).

    Returns:
        A list of lists representing the transformed grid, matching the input format.
    """
    
    # --- Input Handling and Initialization ---
    # Validate input format - expect list of lists
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        raise ValueError("Input grid must be a non-empty list of lists.")
        
    # Expecting a single row based on examples
    if len(input_grid) > 1:
         # For this specific problem, only handle single-row inputs.
         # A more general solution might loop through rows or handle 2D differently.
         print("Warning: Input grid has multiple rows, only processing the first row.")
         # Or raise ValueError("Input grid has multiple rows, expecting a single row for this task.")

    # Extract the first (and assumed only) row and convert to numpy array
    grid_1d_original = np.array(input_grid[0], dtype=int)
    
    # Initialize the output grid as a copy of the original 1D data
    output_grid_np = grid_1d_original.copy()

    # --- Core Transformation Logic ---
    # Step 1: Identify all non-background (non-zero) segments in the original grid
    segments = find_non_background_segments(grid_1d_original)

    # Step 2: Process each identified segment
    for start_idx, end_idx in segments:
        # Step 2a: Extract the pixels belonging to this segment from the *original* grid
        segment_pixels = grid_1d_original[start_idx:end_idx]
        
        # Step 2b: Determine the majority color for this segment
        majority_color = get_majority_color(segment_pixels)
        
        # Step 2c: If a majority color is found (i.e., segment was not empty)
        if majority_color is not None:
            # Step 2d: Replace all pixels in this segment's range *in the output grid*
            # with the determined majority color.
            output_grid_np[start_idx:end_idx] = majority_color
            
    # --- Output Formatting ---
    # Convert the final numpy array back to the required list of lists format
    output_grid_list_of_lists = [output_grid_np.tolist()]
    
    return output_grid_list_of_lists