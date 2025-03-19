import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        grid_height, grid_width = input_grid.shape

        # Find the rotated subgrid by comparing input and output
        diff = input_grid != output_grid
        rows, cols = np.where(diff)

        if len(rows) == 0:  # No changes
            results.append({
                'example_index': i,
                'rotated': False,
                'subgrid_top_left': None,
                'subgrid_colors': None,
                'surrounding_colors': None,
                'grid_size': (grid_height, grid_width)
            })
            continue

        #assume 2x2 subgrid
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)

        #check if the rotation assumption valid
        if (max_row - min_row != 1) or (max_col - min_col != 1):
             results.append({
                'example_index': i,
                'rotated': False,
                 'rotation_assumption_failed': True,
                'subgrid_top_left': None,
                'subgrid_colors': None,
                'surrounding_colors': None,
                 'grid_size': (grid_height, grid_width)
            })
             continue

        top_left_row, top_left_col = min_row, min_col
        subgrid_colors = input_grid[top_left_row:top_left_row+2, top_left_col:top_left_col+2].tolist()


        # Get surrounding colors
        surrounding_colors = {}

        #check edges
        if top_left_row > 0:
            surrounding_colors['top'] = input_grid[top_left_row - 1, top_left_col:top_left_col+2].tolist()
        if top_left_row < grid_height - 2:
            surrounding_colors['bottom'] = input_grid[top_left_row + 2, top_left_col:top_left_col+2].tolist()
        if top_left_col > 0:
            surrounding_colors['left'] = input_grid[top_left_row:top_left_row+2, top_left_col - 1].tolist()
        if top_left_col < grid_width - 2:
            surrounding_colors['right'] = input_grid[top_left_row:top_left_row+2, top_left_col+2].tolist()


        results.append({
            'example_index': i,
            'rotated': True,
            'subgrid_top_left': (top_left_row, top_left_col),
            'subgrid_colors': subgrid_colors,
            'surrounding_colors': surrounding_colors,
            'grid_size': (grid_height, grid_width)
        })

    return results

#example data provided in the next message