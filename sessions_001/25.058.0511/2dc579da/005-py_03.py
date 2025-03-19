import numpy as np

def grid_info(grid):
    grid = np.array(grid)
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    rows, cols = grid.shape
    return {
        'shape': (rows, cols),
        'unique_colors': unique_colors.tolist(),
        'color_counts': color_counts,
    }

task = {
    "train": [
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 0, 0]],
            "output": [[8, 8], [0, 0]],
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0]],
            "output": [[8, 8], [0, 0]],
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0], [8, 8, 8, 8, 8, 0, 0, 0, 0, 0]],
            "output": [[8, 8], [0, 0]],
        },
    ],
    "test": [
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0]],
            "output": [[8, 8], [0, 0]],
        }
    ],
}

for i, example in enumerate(task['train']):
    input_info = grid_info(example['input'])
    output_info = grid_info(example['output'])
    print(f"Example {i+1}:")
    print(f"  Input:  Shape={input_info['shape']}, Colors={input_info['unique_colors']}, Counts={input_info['color_counts']}")
    print(f"  Output: Shape={output_info['shape']}, Colors={output_info['unique_colors']}, Counts={output_info['color_counts']}")
    print("-" * 20)
