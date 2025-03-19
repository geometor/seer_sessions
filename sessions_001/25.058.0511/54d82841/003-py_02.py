import numpy as np

def get_black_pixel_columns(grid):
    """Returns a list of column indices where black pixels (value 0) are present."""
    black_pixel_columns = []
    for col in range(grid.shape[1]):
        if 0 in grid[:, col]:
            black_pixel_columns.append(col)
    return black_pixel_columns

def get_yellow_pixel_columns(grid):
    """Returns a list of column indices where yellow pixels (value 4) are present."""
    yellow_pixel_columns = []
    for col in range(grid.shape[1]):
        if 4 in grid[:, col]:
            yellow_pixel_columns.append(col)
    return yellow_pixel_columns
def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns relevant information."""
    
    input_black_cols = get_black_pixel_columns(input_grid)
    output_yellow_cols = get_yellow_pixel_columns(output_grid)

    analysis = {
        'input_black_cols': input_black_cols,
        'output_yellow_cols': output_yellow_cols,
    }
    return analysis

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[6, 0, 6, 3, 6, 6, 0, 6, 6],
                           [0, 6, 6, 6, 6, 0, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6]]),
        "output": np.array([[6, 0, 6, 3, 6, 6, 0, 6, 6],
                            [0, 6, 6, 6, 6, 0, 6, 6, 6],
                            [6, 6, 4, 6, 6, 6, 4, 6, 6]]),
    },
     {
        "input": np.array([[6, 0, 6, 3, 6, 6, 6, 6, 6],
                           [0, 6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6]]),
        "output": np.array([[6, 0, 6, 3, 6, 6, 6, 6, 6],
                            [0, 6, 6, 6, 6, 6, 6, 6, 6],
                            [6, 6, 4, 6, 6, 6, 6, 6, 6]]),
    },
     {
        "input": np.array([[6, 0, 6, 3, 6, 6, 0, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6]]),
        "output": np.array([[6, 0, 6, 3, 6, 6, 0, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 4, 6, 6, 6, 4, 6, 6]]),
    },
        {
        "input": np.array([[0, 6, 6, 6, 6, 6, 6, 6, 0],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6]]),

        "output": np.array([[0, 6, 6, 6, 6, 6, 6, 6, 0],
                           [6, 6, 6, 6, 6, 6, 6, 6, 6],
                           [4, 6, 6, 6, 6, 6, 6, 6, 4]]),
    },
]

# Analyze all examples
for i, example in enumerate(examples):
    analysis = analyze_example(example['input'], example['output'])
    print(f"Example {i+1}:")
    print(f"  Input Black Pixel Columns: {analysis['input_black_cols']}")
    print(f"  Output Yellow Pixel Columns: {analysis['output_yellow_cols']}")