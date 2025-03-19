import numpy as np

def analyze_grids(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows, cols = input_grid.shape
    analysis = []

    for j in range(cols):
        for i in range(rows):
            if input_grid[i, j] == 4:  # Found yellow
                yellow_info = {
                    'column': j,
                    'yellow_coordinates': (i, j),
                    'yellow_color': 4,
                    'left_neighbor': [],
                    'right_neighbor': []
                }

                # Check left neighbor
                if j > 0:
                    for row_index in range(rows):
                      yellow_info['left_neighbor'].append(input_grid[row_index,j-1])
                # Check right neighbor
                if j < cols - 1:
                    for row_index in range(rows):
                        yellow_info['right_neighbor'].append(input_grid[row_index,j+1])

                analysis.append(yellow_info)

    return analysis
