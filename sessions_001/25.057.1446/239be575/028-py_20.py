import numpy as np

# Provided code (slightly modified for easier testing)
def get_perimeter_colors(grid):
    """Extracts colors from the perimeter of the grid."""
    perimeter = []
    rows, cols = grid.shape
    perimeter.extend(grid[0, :])  # Top row
    perimeter.extend(grid[rows - 1, :])  # Bottom row
    perimeter.extend(grid[1:rows - 1, 0])  # Left column (excluding corners)
    perimeter.extend(grid[1:rows - 1, cols - 1])  # Right column (excluding corners)
    return perimeter

def count_occurrences(grid, color):
    """Counts the number of times a color appears in the grid."""
    return np.sum(grid == color)

def get_corner_colors(grid):
    """Returns a list of the colors at the four corners of the grid."""
    rows, cols = grid.shape
    return [grid[0, 0], grid[0, cols - 1], grid[rows - 1, 0], grid[rows - 1, cols - 1]]

def analyze_example(example):
    input_grid = example["input"]
    expected_output = example["output"]

    perimeter_colors = get_perimeter_colors(input_grid)
    unique_perimeter_colors = list(set(perimeter_colors))

    color_counts = {}
    for color in unique_perimeter_colors:
        color_counts[color] = perimeter_colors.count(color)
    
    overall_counts = {}
    for color in unique_perimeter_colors:
      overall_counts[color] = count_occurrences(input_grid, color)

    max_count = max(color_counts.values())
    most_frequent_perimeter_colors = [color for color, count in color_counts.items() if count == max_count]
    corner_colors = get_corner_colors(input_grid)
    
    print(f"Perimeter Colors: {perimeter_colors}")
    print(f"Unique Perimeter Colors: {unique_perimeter_colors}")
    print(f"Perimeter Color Counts: {color_counts}")
    print(f"Overall counts: {overall_counts}")
    print(f"Most Frequent Perimeter Colors: {most_frequent_perimeter_colors}")
    print(f"Corner Colors: {corner_colors}")
    print(f"Expected Output: {expected_output[0,0]}")

# Example data (replace with your actual task data)
train_examples = [
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5],
                           [5, 1, 1, 1, 1, 1, 5],
                           [5, 1, 1, 1, 1, 1, 5],
                           [5, 1, 1, 1, 1, 1, 5],
                           [5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5]])
    },
     {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 8, 8, 8, 8, 8, 8, 8, 5],
        [5, 8, 8, 8, 8, 8, 8, 8, 5],
        [5, 8, 8, 8, 8, 8, 8, 8, 5],
        [5, 8, 8, 8, 8, 8, 8, 8, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0]])
    },
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 1, 1, 1, 1, 1, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0]])
    }
]

for i, example in enumerate(train_examples):
  print(f"Example: {i}")
  analyze_example(example)
  print("-" * 20)
