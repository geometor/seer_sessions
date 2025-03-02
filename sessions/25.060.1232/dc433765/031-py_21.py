import numpy as np

def find_pixel_by_color(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        return coords[0]
    return None

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example['input']
        expected_output = example['output']
        actual_output = transform(input_grid)  # Using the provided transform function

        green_pixel_coords = find_pixel_by_color(input_grid, 3)

        if green_pixel_coords is not None:
            row, col = green_pixel_coords
            moved_expected = not np.array_equal(input_grid, expected_output)
            moved_actual = not np.array_equal(input_grid, actual_output)

            color_above = input_grid[row - 1, col] if row > 0 else None
            color_right = input_grid[row, col+1] if col < input_grid.shape[1] -1 else None
            color_below = input_grid[row + 1, col] if row < input_grid.shape[0] - 1 else None


            results.append({
                'example': i + 1,
                'green_pixel_row': row,
                'green_pixel_col': col,
                'moved_expected': moved_expected,
                'moved_actual': moved_actual,
                'color_above': color_above,
                'color_right': color_right,
                'color_below': color_below,
            })
        else:
            results.append({
                'example': i + 1,
                'green_pixel_row': None,
                'green_pixel_col': None,
                'moved_expected': False,
                'moved_actual': False,
                'color_above': None,
                'color_right': None,
                'color_below':None,
            })
    return results

examples = [
    {'input': np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 3]]),
     'output': np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 3],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]])},
    {'input': np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 3],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
     'output': np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 3],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]])},
    {'input': np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 3],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
     'output': np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 3],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]])}
]

analysis_results = analyze_examples(examples)
print(analysis_results)