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


def transform(input_grid):
    """Transforms the input grid to the output grid based on the described rule."""
    perimeter_colors = get_perimeter_colors(input_grid)
    unique_perimeter_colors = list(set(perimeter_colors))
    
    color_counts = {}
    for color in unique_perimeter_colors:
        color_counts[color] = perimeter_colors.count(color)

    max_count = max(color_counts.values())
    most_frequent_perimeter_colors = [color for color, count in color_counts.items() if count == max_count]

    if len(most_frequent_perimeter_colors) == 1:
        output_color = most_frequent_perimeter_colors[0]
    else:
        # Tiebreaker: Check for corner colors
        corner_colors = get_corner_colors(input_grid)
        corner_color_present = None
        for color in most_frequent_perimeter_colors:
            if color in corner_colors:
                corner_color_present = color
                break

        if corner_color_present is not None:
            output_color = corner_color_present
        else:
            # If no corner color is present, use overall count
            overall_counts = {}
            for color in most_frequent_perimeter_colors:
                overall_counts[color] = count_occurrences(input_grid, color)
            
            max_overall_count = max(overall_counts.values())
            output_color = [color for color, count in overall_counts.items() if count == max_overall_count][0]

    output_grid = np.array([[output_color]])
    return output_grid
    

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

# Run the tests and print results
for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    correct = np.array_equal(predicted_output, expected_output)
    print(f"Example {i+1}:")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output: {expected_output}")
    print(f"  Predicted Output: {predicted_output}")
    print(f"  Correct: {correct}")
    print("-" * 20)