import numpy as np

def analyze_input(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    unique_colors = np.unique(input_grid)
    num_unique_colors = len(unique_colors)
    all_same_color = np.all(input_grid == input_grid[0, 0])

    block_counts = {}
    for color in unique_colors:
        block_counts[color] = 0
    for i in range(rows - 1):
        for j in range(cols - 1):
            block = input_grid[i:i + 2, j:j + 2]
            if np.all(block == block[0, 0]):
                block_counts[block[0, 0]] += 1

    return {
        "shape": (rows, cols),
        "unique_colors": unique_colors.tolist(),
        "num_unique_colors": num_unique_colors,
        "all_same_color": bool(all_same_color),
        "2x2_block_counts": block_counts,
    }

# Example Usage with the provided training examples
train_examples = [
    {
        "input": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        "output": [[1, 1, 1, 1]]
    },
    {
        "input": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        "output": [[0]]
    },
    {
        "input": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
        "output": [[0]]
    },
    {
        "input": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]],
        "output": [[0]]
    },
    {
      "input": [[1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 3, 3]],
      "output": [[1, 1, 1, 1, 0]]
    },
]

for i, example in enumerate(train_examples):
  analysis = analyze_input(example["input"])
  print(f"Example {i+1}:")
  print(analysis)
