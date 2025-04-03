import numpy as np
from typing import List, Tuple

"""
Identify the non-white foreground color present in the 1D input grid.
Scan the input grid horizontally to locate all contiguous segments composed 
solely of the foreground color.
Calculate the length of each identified segment.
Find the segment with the greatest length. If there are multiple segments of 
the same maximum length, select the first one encountered.
Create a new grid with the same dimensions as the input grid, initializing 
all cells to the background color (white, 0).
Copy the pixels belonging to the identified longest foreground segment from 
their original positions in the input grid to the corresponding positions 
in the new output grid.
The resulting grid is the final output.
"""

def find_foreground_color(grid_1d: np.ndarray) -> int:
    """
    Finds the first non-zero color in the 1D grid.
    Assumes there is exactly one foreground color besides 0.
    """
    for pixel in grid_1d:
        if pixel != 0:
            return int(pixel)
    # Should not happen based on task description, but return default if empty/all zero
    return 0 

def find_contiguous_segments(grid_1d: np.ndarray, target_color: int) -> List[Tuple[int, int, int]]:
    """
    Finds all contiguous segments of the target_color in the 1D grid.
    Returns a list of tuples: (start_index, end_index_exclusive, length).
    """
    segments = []
    start_index = -1
    for i, pixel in enumerate(grid_1d):
        if pixel == target_color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment
            end_index = i
            length = end_index - start_index
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset for the next segment
            
    # Handle segment that extends to the end of the grid
    if start_index != -1:
        end_index = len(grid_1d)
        length = end_index - start_index
        segments.append((start_index, end_index, length))
        
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only the longest contiguous 
    horizontal segment of the foreground color.
    """
    # Ensure input is treated as a 1D array (single row)
    if input_grid.ndim > 1:
         # Assuming it's always 1 row based on examples
        grid_1d = input_grid.flatten()
    else:
        grid_1d = input_grid 
        
    grid_width = len(grid_1d)
    
    # 1. Identify the foreground color
    foreground_color = find_foreground_color(grid_1d)
    
    # If no foreground color found (e.g., all white grid), return input or empty
    if foreground_color == 0:
        return np.zeros_like(input_grid) # Return all background

    # 2. Find all contiguous horizontal segments of the foreground color
    segments = find_contiguous_segments(grid_1d, foreground_color)
    
    # 3. Find the segment with the maximum length
    longest_segment = None
    max_length = 0
    if segments:
        # Sort segments primarily by length (descending), then by start index (ascending)
        # This handles ties by selecting the first longest segment.
        segments.sort(key=lambda x: (-x[2], x[0]))
        longest_segment = segments[0]
        # Alternatively, iterate to find max:
        # for seg in segments:
        #     if seg[2] > max_length:
        #         max_length = seg[2]
        #         longest_segment = seg
        #     # Tie-breaking: keep the first one found with max_length
    
    # 4. Create output grid filled with background color (0)
    output_grid_1d = np.zeros(grid_width, dtype=int)
    
    # 5. Copy the longest segment to the output grid at its original position
    if longest_segment:
        start, end, _ = longest_segment
        output_grid_1d[start:end] = foreground_color
        
    # Reshape the output to match the original input shape (especially if it was 1xN)
    output_grid = output_grid_1d.reshape(input_grid.shape)

    return output_grid
