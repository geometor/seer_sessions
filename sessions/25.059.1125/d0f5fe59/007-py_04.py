import numpy as np

def get_azure_diagonal(grid):
    """Finds the longest continuous diagonal of azure pixels."""
    azure_pixels = []
    max_len = 0
    for start_row in range(grid.shape[0]):
        for start_col in range(grid.shape[1]):
          if grid[start_row,start_col] == 8:
            current_len = 0
            current_row = start_row
            current_col = start_col
            temp_pixels = []
            while current_row < grid.shape[0] and current_col < grid.shape[1] and grid[current_row, current_col] == 8:
                temp_pixels.append((current_row, current_col))
                current_len += 1
                current_row += 1
                current_col += 1
            if current_len > max_len:
                max_len = current_len
                azure_pixels = temp_pixels
    return azure_pixels

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    input_color_counts = {color: np.sum(input_grid == color) for color in range(10)}
    output_color_counts = {color: np.sum(output_grid == color) for color in range(10)}
    
    azure_diag = get_azure_diagonal(input_grid)
    azure_diag_len = len(azure_diag)


    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Input Color Counts: {input_color_counts}")
    print(f"  Output Color Counts: {output_color_counts}")
    print(f"  Azure Diagonal Length: {azure_diag_len}")
    print(f"  Azure Diagonal: {azure_diag}")

def analyze_task(task):
    for i, example in enumerate(task['train']):
        print(f"Example {i+1}:")
        analyze_example(example['input'], example['output'])

# provided examples
task = {
    "train": [
        {
            "input": [
                [8, 0, 8, 8, 0, 8, 8, 8],
                [0, 8, 0, 0, 8, 0, 0, 0],
                [8, 0, 8, 8, 0, 8, 8, 8],
            ],
            "output": [[8, 0], [0, 8]],
        },
        {
            "input": [
                [0, 8, 0, 0, 0, 8, 0, 0],
                [8, 0, 8, 0, 0, 0, 8, 8],
                [0, 8, 8, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 8, 0, 0],
            ],
            "output": [[8, 0], [0, 8]],
        },
        {
            "input": [
                [8, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0, 0],
                [0, 0, 8, 0, 0, 0, 0, 0],
                [0, 0, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 8, 0, 0],
                [0, 0, 0, 0, 0, 0, 8, 0],
                [0, 0, 0, 0, 0, 0, 0, 8],
            ],
            "output": [[8, 0, 0, 0], [0, 8, 0, 0], [0, 0, 8, 0], [0, 0, 0, 8]],
        },
        {
            "input": [[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8]],
            "output": [[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8]],
        },
    ]
}
analyze_task(task)