```python
"""
Transforms an input grid by identifying horizontal lines of specific colors (2, 4, 6, 9) and inserting copies of
their pixels at different y-coordinates with x-coordinate shifts, depending on the color. Lines of other colors are ignored.
"""

import numpy as np

def find_horizontal_lines(grid):
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        start_c = -1
        current_color = 0
        for c in range(cols):
            if grid[r, c] != 0:
                if start_c == -1:
                    start_c = c
                    current_color = grid[r, c]
                elif grid[r, c] != current_color:
                    if c - start_c > 1:
                        lines.append({'color': current_color, 'y': r, 'x_start': start_c, 'x_end': c - 1})
                    start_c = c
                    current_color = grid[r, c]
            elif start_c != -1:
                if c - start_c > 1:
                    lines.append({'color': current_color, 'y': r, 'x_start': start_c, 'x_end': c - 1})
                start_c = -1
                current_color = 0
        if start_c != -1 and cols - start_c > 1:  # Check for line at the end of the row
            lines.append({'color': current_color, 'y': r, 'x_start': start_c, 'x_end': cols - 1})
    return lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # find horizontal lines
    lines = find_horizontal_lines(input_grid)

    # determine insertion color, x, and y coordinates and change output pixels
    for line in lines:
        if line['color'] == 9:
            # Insert gray(3) lines below
            for x in range(line['x_start'], min(line['x_end'] + 1, cols)): # Limit x to grid width.
              if line['y'] + 1 < rows:
                output_grid[line['y'] + 1, x] = 3

        elif line['color'] == 6:
            # Insert two magenta pixels above.
            x_shift = -2
            y_shift1 = -3
            y_shift2 = -4
            if line['x_start'] + x_shift >= 0:
                if line['y'] + y_shift1 >= 0 :
                    output_grid[line['y'] + y_shift1, line['x_start'] + x_shift] = 6
                if line['y'] + y_shift2 >= 0:
                    output_grid[line['y'] + y_shift2, line['x_start'] + x_shift] = 6
        elif line['color'] == 2:
             # Insert color 2 with y offset and x shift
            x_shift = -2
            if line['x_start'] + x_shift >= 0:
                if line['y'] -4  >= 0:
                  for x in range(line['x_start'], line['x_end'] +1):
                    if x + x_shift < cols:
                      output_grid[line['y']-4, x+x_shift] = 2
        elif line['color'] == 4:
            # Insert color 4 with y offset and x shift
            x_shift = 2

            insert_y = line['y']- 5
            insert_x = line['x_start'] + x_shift

            if insert_y >= 0 and insert_x < cols:
              output_grid[insert_y, insert_x]= 4


    # copy the original image to output
    for i in range(rows):
        for j in range(cols):
            if output_grid[i,j] == 0:
                output_grid[i,j] = input_grid[i,j]


    return output_grid
```