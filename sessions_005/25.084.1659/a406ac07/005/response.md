```python
import numpy as np

"""
Transforms the input grid by drawing colored rectangles based on matching color 
segments found in the last row and last column, while preserving these borders.

1.  **Initialization:** Create an output grid of the same dimensions as the input, filled with the background color (0, white).
2.  **Border Preservation (Initial):** Copy the last row and the last column from the input grid onto the output grid.
3.  **Identify Row Segments:** Scan the last row of the input grid (excluding the last pixel). Identify contiguous horizontal segments of non-background colors. Record each segment's color (Cr), starting column index (Sr), and length (Lr).
4.  **Identify Column Segments:** Scan the last column of the input grid (excluding the last pixel). Identify contiguous vertical segments of non-background colors. Record each segment's color (Cc), starting row index (Sc), and length (Lc).
5.  **Match Segments and Draw Rectangles:**
    a.  For each row segment (Cr, Sr, Lr):
    b.  Find the unique column segment (Cc, Sc, Lc) where Cc equals Cr.
    c.  Define the rectangle's parameters:
        i.  Color: C = Cr
        ii. Top row: row_start = Sc
        iii.Bottom row (exclusive): row_end = Sc + Lc
        iv. Left column: col_start = Sr
        v.  Right column (exclusive): col_end = Sr + Lr
    d.  Fill the area output_grid[row_start : row_end, col_start : col_end] with color C, ensuring drawing stays within the bounds defined by height-1 and width-1.
6.  **Border Preservation (Final):** Re-copy the last row and last column from the input grid onto the output grid to restore any overwritten border pixels.
7.  **Return:** Return the final output grid.
"""

def get_segments(line):
    """
    Finds contiguous segments of non-zero colors in a 1D array.

    Args:
        line (np.ndarray): A 1D numpy array of integers (colors).

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and has keys 'color' (int), 'start' (int), and 'length' (int).
    """
    segments = []
    current_color = 0
    start_index = -1
    # Ensure iteration works even if line is empty
    line_length = len(line) if line is not None else 0
    
    for i in range(line_length):
        color = int(line[i]) # Convert numpy int to standard int
        
        # Check if the current segment ends
        if color == 0 or color != current_color:
            # If a non-background segment just ended, record it
            if current_color != 0:
                segments.append({'color': current_color, 'start': start_index, 'length': i - start_index})

            # Reset or start a new segment
            if color != 0:
                current_color = color
                start_index = i
            else: # color is 0 (background)
                current_color = 0
                start_index = -1
        # Continue the current segment (color != 0 and color == current_color)
        # No action needed here, segment length increases implicitly

    # After the loop, check if the last segment needs to be recorded
    if current_color != 0:
        segments.append({'color': current_color, 'start': start_index, 'length': line_length - start_index})
        
    return segments

def transform(input_grid):
    """
    Transforms the input grid based on border segment matching.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Initialization: Create output_grid with background color (0)
    output_grid = np.zeros_like(input_np)
    
    # 2. Border Preservation (Initial): Copy last row and column
    # Check if dimensions are valid before copying
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
        
    # Handle edge cases: If grid is too small for drawing area, return borders only
    if height <= 1 or width <= 1:
        return output_grid.tolist()

    # 3. Identify Row Segments (excluding last pixel)
    last_row_data = input_np[height - 1, :width - 1]
    row_segments = get_segments(last_row_data)
    
    # 4. Identify Column Segments (excluding last pixel)
    last_col_data = input_np[:height - 1, width - 1]
    col_segments = get_segments(last_col_data)

    # --- Create a lookup map for column segments by color for efficiency ---
    col_segment_map = {seg['color']: seg for seg in col_segments}

    # 5. Match Segments and Draw Rectangles
    for row_seg in row_segments:
        row_color = row_seg['color']
        
        # Find the matching column segment by color
        if row_color in col_segment_map:
            col_seg = col_segment_map[row_color]
            
            # Define rectangle parameters
            color_to_draw = row_color
            row_start = col_seg['start']
            row_end = col_seg['start'] + col_seg['length']
            col_start = row_seg['start']
            col_end = row_seg['start'] + row_seg['length']
            
            # Clip drawing bounds to stay within the inner grid area (not overwrite borders)
            row_end_clipped = min(row_end, height - 1)
            col_end_clipped = min(col_end, width - 1)
            
            # Ensure the clipped area is valid before drawing
            if row_start < row_end_clipped and col_start < col_end_clipped:
                 output_grid[row_start : row_end_clipped, col_start : col_end_clipped] = color_to_draw

    # 6. Border Preservation (Final): Re-copy borders to ensure they weren't overwritten
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
            
    # 7. Return: Convert back to list of lists
    return output_grid.tolist()
```