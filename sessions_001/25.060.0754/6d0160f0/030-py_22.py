"""
1.  **Find Separators**: Identify all gray pixels (value 5) in the input grid. These act as horizontal and vertical separators.

2.  **Define All Segments**: Create a list of all rectangular segments defined by all combinations of adjacent horizontal and vertical separators.  A segment is defined by its top-left and bottom-right corner coordinates.

3.  **Iterate Through Segments**: For each segment in the list, from top to bottom and left to right:
    *   Find the unique, non-zero, non-gray colors within the segment, recording the location (row, column) of the *first* appearance of each color (scanning top to bottom, then left to right).

4.  **Iterate through horizontal separators** For each horizontal separator, find the associated segments.

5.  **Copy Colors**: For each color found in a source segment, copy the color to the row *immediately below* the horizontal separator line that defines the lower boundary of the segment.
    *   Maintain the *original column* of the color's first appearance within the source segment.
    *   *Do not* overwrite gray pixels (value 5) in the destination row. If the target cell is gray, skip the copy for that cell.

6.  **Preserve Separators:** All gray separator pixels from the input grid must be present in the output grid at their original positions.

7.  **Clear Remnants:** After copying colors, all pixels in each segment that don't contain the copied colors or the gray separators, should be set to white color(value=0).
"""

import numpy as np

def find_gray_separators(grid):
    """Finds the row and column indices of gray (5) pixels."""
    gray_pixels = np.where(grid == 5)
    return gray_pixels[0], gray_pixels[1]

def define_segments(gray_rows, gray_cols):
    """Defines all segments based on horizontal and vertical separators."""
    horizontal_separators = sorted(list(set(gray_rows)))
    vertical_separators = sorted(list(set(gray_cols)))
    segments = []
    for i in range(len(horizontal_separators)):
        for j in range(len(vertical_separators)):
          #get row start
          row_start = 0 if i == 0 else horizontal_separators[i-1] + 1
          #get row end
          row_end = horizontal_separators[i]
          #get col start
          col_start = 0 if j == 0 else vertical_separators[j-1] +1
          #get col end
          col_end = vertical_separators[j]
          segments.append(((row_start, col_start), (row_end, col_end)))
    return segments

def get_segment_colors(grid, row_start, row_end, col_start, col_end):
    """Extracts unique colors and their first occurrence in a segment."""
    segment_colors = {}
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            color = grid[r, c]
            if color != 0 and color != 5 and color not in segment_colors:
                segment_colors[color] = (r, c)  # Store first occurrence
    return segment_colors

def transform(input_grid):
    # Initialize output grid with zeros.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find gray separator positions.
    gray_rows, gray_cols = find_gray_separators(input_grid)

    # Preserve gray separators in the output grid.
    for r, c in zip(gray_rows, gray_cols):
        output_grid[r, c] = 5

    # Define all segments.
    segments = define_segments(gray_rows, gray_cols)
    horizontal_separators = sorted(list(set(gray_rows)))

    #create dictionary to hold segments by horizontal separator
    segments_by_h_sep = {}
    for h_sep in horizontal_separators:
      segments_by_h_sep[h_sep] = []

    #add segments
    for segment in segments:
      segments_by_h_sep[segment[1][0]].append(segment)

    # Iterate through horizontal separators and segments.
    for h_sep in horizontal_separators:
        dest_row = h_sep + 1
        if dest_row < rows: # Check if destination row is valid
            for segment in segments_by_h_sep[h_sep]:
              # Extract color information from each segment.
              row_start, col_start = segment[0]
              row_end, col_end = segment[1]              
              segment_colors = get_segment_colors(input_grid, row_start, row_end, col_start, col_end)

              # Copy colors to the destination row.
              for color, (orig_r, orig_c) in segment_colors.items():
                  if output_grid[dest_row, orig_c] == 0:  # Don't overwrite gray
                      output_grid[dest_row, orig_c] = color

    return output_grid