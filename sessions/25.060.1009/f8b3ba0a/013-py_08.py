import numpy as np

def get_colors_in_reading_order(grid):
    """
    Returns a list of unique colors in the grid, ordered as if reading
    the grid from top to bottom, then left to right.
    """
    rows, cols = grid.shape
    colors_found = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color not in colors_found:
                colors_found.append(color)
    return colors_found

# Example Usage (assuming 'train' contains the training examples):

for i, example in enumerate(train):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    input_colors = get_colors_in_reading_order(input_grid)
    output_colors = get_colors_in_reading_order(output_grid)
    print(f"Example {i+1}:")
    print(f"  Input Colors (Reading Order): {input_colors}")
    print(f"  Output Colors: {output_colors}")
    print(f"  Input shape: {input_grid.shape}")
    print(f"  Output shape: {output_grid.shape}")    
    current_output = transform(input_grid)    
    print(f"  transform output: {get_colors_in_reading_order(current_output)}")
    print(f"  Correct: {np.array_equal(current_output, output_grid)}")
