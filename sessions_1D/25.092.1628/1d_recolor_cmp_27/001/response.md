```python
import numpy as np

def find_horizontal_segments(row, target_color):
    """
    Finds all contiguous horizontal segments of a specific color in a 1D array (row).

    Args:
        row (np.array): The 1D array representing the grid row.
        target_color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              as (start_index, end_index).
    """
    segments = []
    width = len(row)
    j = 0
    while j < width:
        if row[j] == target_color:
            start_index = j
            # Find the end of the segment
            while j < width and row[j] == target_color:
                j += 1
            end_index = j - 1
            segments.append((start_index, end_index))
        else:
            j += 1
    return segments

def transform(input_grid):
    """
    Identifies the longest contiguous horizontal segment(s) of orange pixels (7)
    that are bordered on both the left and right by white pixels (0), and
    changes the color of these segment(s) to blue (1).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.
                                Assumed to be 1xN for this task based on examples.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Since the grid is 1xN, we operate on the first row
    row = input_grid[0]
    width = input_grid.shape[1]
    
    # 1. Identify all contiguous horizontal segments of orange (7)
    orange_segments = find_horizontal_segments(row, 7)
    
    bordered_segments = []
    # 2. Filter for segments bordered by white (0) on both sides
    for start, end in orange_segments:
        # Check left border
        is_left_bordered = (start > 0 and row[start - 1] == 0)
        # Check right border
        is_right_bordered = (end < width - 1 and row[end + 1] == 0)
        
        # 3. If bordered, record the segment and its length
        if is_left_bordered and is_right_bordered:
            length = end - start + 1
            bordered_segments.append({'start': start, 'end': end, 'length': length})
            
    # If no bordered segments were found, return the original grid
    if not bordered_segments:
        return output_grid
        
    # 4. Determine the maximum length among bordered segments
    max_length = 0
    for segment in bordered_segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            
    # 5. Change the color of the longest bordered segment(s) to blue (1)
    for segment in bordered_segments:
        if segment['length'] == max_length:
            start = segment['start']
            end = segment['end']
            # Modify the output grid in place
            output_grid[0, start:end + 1] = 1 # Change color to blue
            
    # 6. Return the modified grid
    return output_grid
```