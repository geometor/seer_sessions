"""
1.  **Identify Orange Lines:** Find all vertical line segments of orange color in the input grid.
2.  **Combine Lines:** For each column, combine contiguous orange vertical line segments.  The combined length is the sum of the individual lengths plus the number of gaps between the segments.
3.  **Determine Output Dimensions:** The output grid's height is determined by the combined length of the orange vertical line segments. The width is the same as the input grid.
4.  **Create Blue Line:** In the output grid, create a vertical line of blue color. The length of this line is equal to the calculated combined length, and it is positioned at the same column index as the orange line segments in the input.
5. **Fill with Zeros:** All other cells in the output are zeros (white color)
"""

import numpy as np

def find_orange_lines(grid):
    """Finds all vertical orange (7) line segments in the grid."""
    rows, cols = grid.shape
    orange_lines = []
    for j in range(cols):
        i = 0
        while i < rows:
            if grid[i, j] == 7:
                start_row = i
                end_row = i
                while end_row + 1 < rows and grid[end_row + 1, j] == 7:
                    end_row += 1
                orange_lines.append((start_row, end_row, j))
                i = end_row + 1  # Skip the current line segment
            else:
                i += 1
    return orange_lines

def combine_lines(orange_lines, rows, cols):
    """Combines contiguous orange line segments and calculates combined length."""
    combined_lengths = {j: 0 for j in range(cols)}
    segments_per_column = {j: [] for j in range(cols)}

    for start_row, end_row, j in orange_lines:
      segments_per_column[j].append((start_row, end_row))

    for j in range(cols):
        segments = sorted(segments_per_column[j])
        if not segments:
            combined_lengths[j] = 0
            continue
        
        combined_length = 0
        gaps = 0

        #initial values
        combined_length += segments[0][1] - segments[0][0] + 1

        for i in range(1,len(segments)):
            combined_length += segments[i][1] - segments[i][0] + 1
            gaps += segments[i][0] - segments[i-1][1] - 1

        combined_lengths[j] = combined_length + gaps


    return combined_lengths

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    rows, cols = input_grid.shape
    orange_lines = find_orange_lines(input_grid)
    combined_lengths = combine_lines(orange_lines, rows, cols)

    # Determine output height and create output grid
    max_combined_length = 0
    for j in range(cols):
      if combined_lengths[j] > max_combined_length:
        max_combined_length = combined_lengths[j]

    
    output_grid = np.zeros((max_combined_length, cols), dtype=int)

    # Create blue lines in the output
    for start_row, end_row, col_index in orange_lines:
      
      output_grid[:combined_lengths[col_index], col_index] = 1


    return output_grid