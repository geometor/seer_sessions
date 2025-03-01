import numpy as np

def find_cells_by_color(grid, color):
    """Finds the positions of cells with the specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Key Cells
    red_cells = find_cells_by_color(input_grid, 2)
    magenta_cells = find_cells_by_color(input_grid, 6)

    # 2. Check for Both Colors
    if len(red_cells) > 0 and len(magenta_cells) > 0:
        # 3. Bounding Rectangle
        min_row = min(red_cells[:, 0].min(), magenta_cells[:, 0].min())
        min_col = min(red_cells[:, 1].min(), magenta_cells[:, 1].min())
        max_row = max(red_cells[:, 0].max(), magenta_cells[:, 0].max())
        max_col = max(red_cells[:, 1].max(), magenta_cells[:, 1].max())

        # 4. Fill Rectangle
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                output_grid[r, c] = 1

        # 5. Preserve Markers
        for r, c in red_cells:
            output_grid[r, c] = 2
        for r, c in magenta_cells:
            output_grid[r, c] = 6

        return output_grid.tolist()
    else:
      # no transformation
      return input_grid.tolist()

def compare_grids(grid1, grid2):
    return np.array_equal(np.array(grid1), np.array(grid2))

# Task examples (replace with actual data)
task_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [6, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[2, 0, 0, 0, 0, 0, 0, 0, 0, 6]],
        "output": [[2, 1, 1, 1, 1, 1, 1, 1, 1, 6]]
    },
        {
        "input": [[2, 0, 0, 0, 6]],
        "output": [[2, 1, 1, 1, 6]]
    }
]

for i, example in enumerate(task_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    is_correct = compare_grids(predicted_output, expected_output)
    print(f"Example {i+1}: Correct = {is_correct}")
    if not is_correct:
        print(f"  Predicted Output:\n{np.array(predicted_output)}")
        print(f"  Expected Output:\n{np.array(expected_output)}")
