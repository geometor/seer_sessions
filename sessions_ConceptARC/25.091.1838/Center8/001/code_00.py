import numpy as np

"""
Identifies pairs of objects in the input grid: a single 'marker' pixel and a horizontal 'line segment' directly below it (on the next row).
For each pair found:
1. Calculates the horizontal midpoint of the line segment.
2. Removes the original marker pixel (sets it to white/0).
3. Draws a 3-pixel vertical line using the marker pixel's color. This vertical line is centered horizontally at the calculated midpoint of the original line segment and centered vertically on the row where the original line segment was located.
The process is applied independently to all such pairs found in the grid.
"""

def _find_segments(grid: np.ndarray) -> list:
    """
    Helper function to find all horizontal contiguous segments of the same non-background color.
    
    Args:
        grid: A numpy array representing the grid.
        
    Returns:
        A list of dictionaries, where each dictionary represents a segment and contains:
        'color', 'row', 'start' (column), 'end' (column), 'length'.
    """
    segments = []
    rows, cols = grid.shape
    # Keep track of visited pixels to avoid processing segments multiple times
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-background (not 0) and not yet visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                c_start = c
                c_end = c
                
                # Extend the segment to the right as long as the color matches and within bounds
                while c_end + 1 < cols and grid[r, c_end + 1] == color:
                    c_end += 1
                    
                # Mark all pixels in the found segment as visited
                for i in range(c_start, c_end + 1):
                    visited[r, i] = True
                    
                # Store segment information
                length = c_end - c_start + 1
                segments.append({
                    'color': color,
                    'row': r,
                    'start': c_start,
                    'end': c_end,
                    'length': length
                })
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: finds marker pixels above horizontal lines,
    removes the marker, and draws a 3-pixel vertical line of the marker's color
    at the line's midpoint, centered vertically on the line's original row.
    
    Args:
        input_grid: A numpy array representing the input grid.
        
    Returns:
        A numpy array representing the transformed output grid.
    """
    
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find all horizontal segments (includes single pixels and lines)
    segments = _find_segments(input_grid)

    # Separate segments into potential markers (length 1) and lines (length > 1)
    lines = [s for s in segments if s['length'] > 1]
    markers = [s for s in segments if s['length'] == 1]

    # Keep track of markers that have been processed to avoid using one marker
    # for multiple lines (though unlikely based on examples)
    processed_markers = set() # Stores (row, col) tuples of processed marker origins

    # Iterate through each identified horizontal line segment
    for line in lines:
        line_color = line['color']
        r_line = line['row']
        c_start = line['start']
        c_end = line['end']
        
        # Calculate the horizontal midpoint column of the line using integer division
        c_mid = c_start + (c_end - c_start) // 2
        
        # Determine the row where potential markers should reside (one row above the line)
        r_marker_expected = r_line - 1
        
        # Check if the expected marker row is valid (within grid bounds)
        if r_marker_expected < 0:
            continue # Cannot have a marker above the top row
            
        # Search for matching marker pixels in the row above the current line
        for marker in markers:
            # Define the position of the current marker candidate
            marker_pos = (marker['row'], marker['start']) # For markers, start==end==column

            # Check conditions for a valid marker-line pair:
            # 1. Marker is on the expected row (r_marker_expected)
            # 2. Marker color is different from the line color (ensures distinct objects)
            # 3. Marker has not already been processed (associated with another line)
            if marker['row'] == r_marker_expected and \
               marker['color'] != line_color and \
               marker_pos not in processed_markers:
                
                # We found a valid marker-line pair
                marker_color = marker['color']
                r_marker, c_marker = marker_pos
                
                # Mark this specific marker pixel as processed
                processed_markers.add(marker_pos)
                
                # --- Apply transformation rules to the output grid ---
                
                # 1. Erase the original marker pixel by setting it to background color (0)
                output_grid[r_marker, c_marker] = 0
                
                # 2. Draw the 3-pixel vertical line using the marker's color.
                #    The line is centered vertically on r_line and horizontally on c_mid.
                
                # Draw pixel above the line's original row (this is the marker's original row)
                # No need for lower bound check on row r_line-1 as we already checked r_marker_expected >= 0
                output_grid[r_line - 1, c_mid] = marker_color
                
                # Draw pixel on the line's original row
                output_grid[r_line, c_mid] = marker_color
                
                # Draw pixel below the line's original row, checking grid boundary
                r_below = r_line + 1
                if r_below < rows: 
                     output_grid[r_below, c_mid] = marker_color

                # In ARC tasks, it's typical that each marker corresponds to one line.
                # If structure allowed multiple markers above one line, this loop handles
                # it by applying the transformation for each marker found. The last
                # marker processed for this line would determine the final color at c_mid.
                
    # Return the modified grid after processing all lines
    return output_grid