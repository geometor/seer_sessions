# Simulated execution and analysis
import numpy as np

# Mockup of the provided example data (replace with actual data)
train_examples = [
    {
        "input": np.array([[1, 1, 2], [1, 1, 2], [8, 8, 2]]),
        "output": np.array([[5, 5, 2], [5, 5, 2], [5, 5, 2]])
    },
    {
        "input": np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 1, 2]]),
        "output": np.array([[0, 5, 2, 3], [4, 5, 6, 7], [5, 9, 5, 2]])
    },
    {
        "input": np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]]),
        "output": np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]])
    }
]

def analyze_example(example):
    input_grid = example["input"]
    output_grid = example["output"]
    changed_pixels = []

    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != output_grid[i, j]:
                changed_pixels.append({
                    "row": i,
                    "col": j,
                    "input_color": int(input_grid[i, j]),
                    "output_color": int(output_grid[i, j]),
                    "neighbors": get_neighbors(input_grid, i, j)
                })

    return changed_pixels

def get_neighbors(grid, row, col):
    neighbors = {}
    rows, cols = grid.shape
    if row > 0:
        neighbors["up"] = int(grid[row-1, col])
    if row < rows - 1:
        neighbors["down"] = int(grid[row+1, col])
    if col > 0:
        neighbors["left"] = int(grid[row, col-1])
    if col < cols - 1:
        neighbors["right"] = int(grid[row, col+1])
    return neighbors

analysis_results = []
for i, example in enumerate(train_examples):
    changes = analyze_example(example)
    analysis_results.append({
        "example": i + 1,
        "changes": changes
    })

print(analysis_results)
