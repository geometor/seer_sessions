import numpy as np

"""
Identify a contiguous horizontal segment of a non-white (0), non-blue (1) color ('Fill Segment'). Record its color ('fill color') and the column index of its rightmost pixel ('end column').
Find the column index of the single blue (1) pixel ('boundary column').
Change the color of the pixels between the original end of the Fill Segment and the Boundary Marker to the 'fill color'. Specifically, modify pixels from column 'end column + 1' up to (but not including) 'boundary column'.
Leave all other pixels unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                   Assumed to have exactly one row.

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    
    # As per examples, grids are 1xN. Access the single row.
    if grid.shape[0] != 1:
        # Handle unexpected input shape, maybe return input as is or raise error
        # For now, assume correct shape based on examples
        return input_grid 
        
    row = output_grid[0]
    height, width = grid.shape # height will be 1

    fill_color = -1
    segment_end_index = -1
    blue_index = -1

    # 1. & 2. Scan to find the fill segment end and the blue boundary marker
    in_segment = False
    current_segment_color = -1
    for i in range(width):
        pixel_color = row[i]
        
        # Find the blue boundary marker
        if pixel_color == 1:
            blue_index = i
            # We assume only one blue pixel based on examples. 
            # Stop looking for blue once found, but continue scan for segment end if needed.

        # Detect the start of a non-white, non-blue segment
        if not in_segment and pixel_color != 0 and pixel_color != 1:
            in_segment = True
            current_segment_color = pixel_color
            fill_color = current_segment_color # Store the color of the first segment found

        # Detect the end of the current segment
        if in_segment and pixel_color != current_segment_color:
            segment_end_index = i - 1 # The previous pixel was the end
            in_segment = False 
            # Since we only care about the first segment, we can potentially break early
            # if we have also found the blue pixel. However, the blue pixel could be later.
            # Let's just record the end index of the *first* segment encountered.
            # If another segment starts, we ignore it.

        # If we are in a segment and reach the end of the row
        if in_segment and i == width - 1:
             segment_end_index = i


    # 3. & 4. Perform the fill operation if segment and boundary are valid
    # Ensure we found both, and the boundary is after the segment end
    if fill_color != -1 and segment_end_index != -1 and blue_index != -1 and blue_index > segment_end_index:
        # Iterate from the column immediately after the segment end up to (not including) the blue index
        for col in range(segment_end_index + 1, blue_index):
            # 5. Change pixel color to the fill color
            row[col] = fill_color
            
    # 6. Return the modified grid (as list of lists)
    return output_grid.tolist()