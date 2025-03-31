import numpy as np

"""
Transforms the input grid based on the following rule:
1. Identify horizontal line segments of a single color 'C' that are interrupted by exactly one white (0) pixel gap.
2. The total horizontal span of the colored segments plus the single gap must be at least 3 pixels.
3. For each identified segment and gap:
    a. Fill the single white gap pixel with the line color 'C'.
    b. Draw a vertical ray upwards from the position directly above the filled gap, using the same color 'C'.
    c. This upward ray continues until it reaches the top edge (row 0) of the grid.
    d. The ray overwrites any existing pixel values (white or colored) in its path.
4. Pixels not part of a filled gap or an upward ray path remain unchanged from the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Keep track of gaps that have already been processed as part of a line
    processed_gaps = set()

    # Iterate through each cell to check if it's a potential gap
    for r in range(height):
        # A gap must have a left and right neighbor within the grid bounds
        for c in range(1, width - 1):

            # Condition 1: Is the current cell a white pixel (potential gap)?
            if input_grid[r, c] == 0:
                
                # Condition 2: Are the immediate left and right neighbors non-white and the same color?
                left_pixel_color = input_grid[r, c - 1]
                right_pixel_color = input_grid[r, c + 1]

                if left_pixel_color != 0 and left_pixel_color == right_pixel_color:
                    line_color = left_pixel_color
                    gap_col = c

                    # Avoid reprocessing if this gap was part of an already identified line
                    if (r, gap_col) in processed_gaps:
                        continue

                    # --- Verify the full segment properties ---

                    # Find the leftmost extent of the line segment
                    start_c = c - 1
                    while start_c > 0 and input_grid[r, start_c - 1] == line_color:
                        start_c -= 1

                    # Find the rightmost extent of the line segment
                    end_c = c + 1
                    while end_c < width - 1 and input_grid[r, end_c + 1] == line_color:
                        end_c += 1
                        
                    # Calculate total span (colored parts + gap)
                    span = end_c - start_c + 1

                    # Condition 3: Is the total span at least 3?
                    if span < 3:
                        continue # Line segment too short

                    # Condition 4: Is there exactly one gap (at the expected position) within this span?
                    gap_count = 0
                    found_gap_col = -1
                    valid_segment = True
                    for scan_c in range(start_c, end_c + 1):
                        pixel = input_grid[r, scan_c]
                        if pixel == 0:
                            gap_count += 1
                            found_gap_col = scan_c
                        elif pixel != line_color:
                            valid_segment = False # Found an unexpected color
                            break
                    
                    # Check if conditions met: exactly one gap, it's at the column 'c' we started with, and no other colors interfered
                    if not valid_segment or gap_count != 1 or found_gap_col != gap_col:
                        continue # Invalid segment structure

                    # --- All conditions met, perform the transformation ---

                    # Mark this gap as processed
                    processed_gaps.add((r, gap_col))

                    # 1. Fill the gap in the output grid
                    output_grid[r, gap_col] = line_color

                    # 2. Draw the vertical ray upwards, overwriting existing pixels
                    # Start from the row directly above the gap
                    for ray_r in range(r - 1, -1, -1): # Iterate from r-1 down to 0
                         output_grid[ray_r, gap_col] = line_color

    return output_grid