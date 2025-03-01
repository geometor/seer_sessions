import numpy as np

def get_surrounding_pixels(grid, row, col, radius=1):
    """Gets the surrounding pixels of a 2x2 square in a grid."""
    rows, cols = grid.shape
    min_row = max(0, row - radius)
    max_row = min(rows, row + 2 + radius)  # +2 because it's a 2x2 square
    min_col = max(0, col - radius)
    max_col = min(cols, col + 2 + radius)  # +2 because it's a 2x2 square
    return grid[min_row:max_row, min_col:max_col]

def analyze_training_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        squares = find_2x2_gray_squares(input_grid)
        
        for row, col in squares:
            surrounding1 = get_surrounding_pixels(input_grid, row, col, 1)
            surrounding2 = get_surrounding_pixels(input_grid, row, col, 2)
            
            # Check if the square was transformed in the output
            transformed = np.array_equal(output_grid[row:row+2, col:col+2], np.full((2, 2), 2))
            
            results.append({
                'example_id': example.get('id', 'N/A'),  # Use get() in case 'id' is missing.
                'row': row,
                'col': col,
                'transformed': transformed,
                'surrounding1': surrounding1.tolist(),  # Convert to list for easy viewing
                'surrounding2': surrounding2.tolist()
            })
    return results