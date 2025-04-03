```python
import copy

"""
Swap the first and last pixels of a contiguous horizontal segment composed of a 
single 'marker' pixel followed by a sequence of identical pixels of a different color.

1.  Accept the input grid (expected 1xN).
2.  Create a deep copy for the output grid.
3.  Access the row.
4.  Find the index (`marker_idx`) and color (`marker_color`) of the first non-background pixel.
5.  If no marker found, return copy.
6.  Check the pixel immediately following the marker. If invalid (out of bounds, background, or same color as marker), return copy.
7.  Identify the sequence color (`sequence_color`) and find the end index (`sequence_end_idx`) of the contiguous sequence starting after the marker.
8.  If a valid sequence is found, swap the colors:
    a.  Place `sequence_color` at `marker_idx` in the output row.
    b.  Place `marker_color` at `sequence_end_idx` in the output row.
9.  Return the modified output grid.
"""

def find_pattern_indices(row):
    """
    Finds the indices of the marker pixel and the end of its adjacent sequence.

    Args:
        row (list): A list of integers representing a row of the grid.

    Returns:
        tuple: A tuple containing (marker_idx, sequence_end_idx), 
               or (None, None) if the pattern is not found.
    """
    marker_idx = -1
    marker_color = -1
    sequence_end_idx = -1
    
    # 1. Find the marker pixel (first non-zero)
    for i, pixel in enumerate(row):
        if pixel != 0:
            marker_idx = i
            marker_color = pixel
            break
            
    # If no marker found, pattern doesn't exist
    if marker_idx == -1:
        return None, None
        
    # 2. Check the pixel immediately following the marker
    seq_start_idx = marker_idx + 1
    if seq_start_idx >= len(row): # Check bounds
        return None, None
        
    sequence_color = row[seq_start_idx]
    
    # Check if the next pixel is background or same color as marker
    if sequence_color == 0 or sequence_color == marker_color:
        return None, None
        
    # 3. Find the end of the contiguous sequence
    sequence_end_idx = seq_start_idx # Initialize end index to the start of the sequence
    for i in range(seq_start_idx + 1, len(row)):
        if row[i] == sequence_color:
            sequence_end_idx = i
        else:
            # End of sequence (or end of row)
            break 
            
    # Pattern requires at least one sequence pixel, which is guaranteed by checks above
    return marker_idx, sequence_end_idx


def transform(input_grid):
    """
    Transforms the input grid by swapping the marker pixel color with the color 
    of the last pixel in its adjacent sequence.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid. 
                                       Expected to be 1xN based on examples.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Basic input validation
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        return input_grid # Return input as is if format is unexpected

    # Create a deep copy to modify
    output_grid = copy.deepcopy(input_grid)

    # Check if it's a single-row grid as expected from examples
    if len(output_grid) == 1:
        row = output_grid[0]
        
        # Find the indices defining the pattern
        marker_idx, sequence_end_idx = find_pattern_indices(row)
        
        # If the pattern was found, perform the swap
        if marker_idx is not None and sequence_end_idx is not None:
            # Store original colors before modifying the row
            marker_color = row[marker_idx]
            # Sequence color is the color of the pixel *after* the marker
            sequence_color = row[marker_idx + 1] 
            
            # Perform the swap in the output grid's row
            row[marker_idx] = sequence_color
            row[sequence_end_idx] = marker_color
            
    # Return the modified grid (or the original copy if no transformation occurred)
    return output_grid
```