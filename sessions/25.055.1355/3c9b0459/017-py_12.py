"""
1.  **Identify Objects:** Find all contiguous horizontal lines of non-zero pixels in the input grid.
2.  **Transformation:** For each horizontal line found:
    *   Create a vertical line of the same color.
    *   The vertical line's length equals the min(length of horizontal, height of the input).
    *   Position the vertical line in the center column of the output grid.
    *   The output grid has the same number of columns as the input.
    *   If the length of the horizontal line exceeds the height of the input, the vertical line height will equal the input's width.
3.  **Output:** Create an output grid where all other pixels (not part of the vertical lines) are set to 0 (background).
"""

import numpy as np

def get_horizontal_lines(grid):
    """Identifies contiguous horizontal lines of non-zero pixels."""
    lines = []
    for row_idx, row in enumerate(grid):
        current_line = []
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                if not current_line:
                    current_line.append((col_idx, pixel))
                elif pixel == current_line[-1][1]:
                    current_line.append((col_idx, pixel))
                else:
                    if len(current_line) > 0:
                        lines.append({
                            'row': row_idx,
                            'start_col': current_line[0][0],
                            'end_col': current_line[-1][0],
                            'color': current_line[0][1],
                            'length': len(current_line)
                        })
                    current_line = [(col_idx, pixel)]
            elif current_line:
                lines.append({
                    'row': row_idx,
                    'start_col': current_line[0][0],
                    'end_col': current_line[-1][0],
                    'color': current_line[0][1],
                    'length': len(current_line)
                })
                current_line = []

        if current_line:
            lines.append({
                'row': row_idx,
                'start_col': current_line[0][0],
                'end_col': current_line[-1][0],
                'color': current_line[0][1],
                'length': len(current_line)
            })
    return lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height, width), dtype=int)


    # Find horizontal lines
    horizontal_lines = get_horizontal_lines(input_grid)

    # change output pixels
    for line in horizontal_lines:
        color = line['color']
        line_length = line['length']
        center_col = width // 2
        vertical_length = min(line_length, height)

        # Handle the special case:
        if line_length > height:
            vertical_length = width

        start_row = (height - vertical_length) // 2  # Center vertically
        # Draw the vertical line
        for i in range(vertical_length):
            if 0 <= start_row + i < height: # boundary check added as requested
                output_grid[start_row + i, center_col] = color


    return output_grid.tolist()