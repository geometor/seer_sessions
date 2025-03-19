import numpy as np

def find_2x2_blocks(grid):
    """Finds all 2x2 blocks of the same color and returns their top-left coordinates and color."""
    blocks = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            color = grid[r, c]
            if (grid[r:r+2, c:c+2] == color).all():
                blocks.append((r, c, color))
    return blocks

def calculate_output_size(input_grid):
    blocks = find_2x2_blocks(input_grid)
    rows, cols = input_grid.shape
    additional_cols = 0
    for r, c, color in blocks:
        if color == 2 or color == 3: #red or green
            additional_cols += 2 #one 2x2 is added
    return rows, cols + additional_cols

def report(grid):
    blocks = find_2x2_blocks(grid)
    print(f"  Grid shape: {grid.shape}")
    rows, cols = calculate_output_size(grid)
    print(f"  calculated output size: {rows, cols}")
    print(f"  2x2 Blocks:")
    for r, c, color in blocks:
        color_name = {0: 'white', 1: 'blue', 2: 'red', 3: 'green', 4: 'yellow', 5: 'gray', 6: 'magenta', 7: 'orange', 8: 'azure', 9: 'maroon'}[color]
        print(f"    - Top-left: ({r}, {c}), Color: {color_name}")

task_examples = {
    "example_1": {
        "input": np.array([[0,0,0,0,0],[0,2,2,0,0],[0,2,2,0,0],[0,0,0,0,0],[0,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0,0,0],[0,2,2,2,2,0,0],[0,2,2,2,2,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
    },
    "example_2": {
        "input": np.array([[0,0,0,0,0],[0,3,3,0,0],[0,3,3,0,0],[0,0,0,1,1],[0,0,0,1,1]]),
        "output": np.array([[0,0,0,0,0,0,0],[0,3,3,3,3,0,0],[0,3,3,3,3,0,0],[0,0,0,1,1,0,0],[0,0,0,1,1,0,0]])
    },
    "example_3": {
        "input": np.array([[0,0,0,0,0,0],[0,2,2,3,3,0],[0,2,2,3,3,0],[0,0,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0,0,0,0,0,0],[0,2,2,2,2,3,3,3,3,0],[0,2,2,2,2,3,3,3,3,0],[0,0,0,0,0,0,0,0,0,0]])
    },
    "example_4": {
        "input": np.array([[1,1,0,3,3,0],[1,1,0,3,3,0],[0,0,0,2,2,0],[0,0,0,2,2,0]]),
        "output": np.array([[1,1,0,0,3,3,3,3,0,0],[1,1,0,0,3,3,3,3,0,0],[0,0,0,0,0,0,2,2,2,2,0],[0,0,0,0,0,0,2,2,2,2,0]])
    }
}
for example, data in task_examples.items():
  print(f"{example}:")
  print(f"  Input:")
  report(data["input"])
  print(f"  Output:")
  report(data["output"])
  print("-" * 20)
