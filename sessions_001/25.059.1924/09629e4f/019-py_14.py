import numpy as np
from collections import Counter

def get_adjacent_colors(grid, row_index, col_index):
    """Gets colors adjacent to a given cell, handling boundaries."""
    rows, cols = grid.shape
    adjacent_colors = []

    if row_index > 0:
        adjacent_colors.append(grid[row_index - 1, col_index])  # Up
    if row_index < rows - 1:
        adjacent_colors.append(grid[row_index + 1, col_index])  # Down
    if col_index > 0:
        adjacent_colors.append(grid[row_index, col_index - 1])  # Left
    if col_index < cols - 1:
        adjacent_colors.append(grid[row_index, col_index + 1])  # Right
    #diagonals
    if row_index > 0 and col_index > 0:
        adjacent_colors.append(grid[row_index - 1, col_index - 1]) #Up-Left
    if row_index > 0 and col_index < cols - 1:
        adjacent_colors.append(grid[row_index - 1, col_index + 1]) # Up-Right
    if row_index < rows - 1 and col_index > 0:
        adjacent_colors.append(grid[row_index+1, col_index-1]) # Down-Left
    if row_index < rows - 1 and col_index < cols - 1:
        adjacent_colors.append(grid[row_index+1, col_index+1]) # Down-Right


    return adjacent_colors

def most_frequent_color(colors):
    """Returns the most frequent color, defaulting to 0 if the list is empty or tied."""
    counts = Counter(colors)
    
    # Remove 0 from counts if other colors exist
    if 0 in counts and len(counts) > 1:
        del counts[0]    
    
    if not counts:
        return 0
    
    max_count = max(counts.values())
    most_frequent = [color for color, count in counts.items() if count == max_count]
    
    return most_frequent[0] if most_frequent else 0  # Return 0 if empty, or the first most frequent


def get_adjacent_to_line(grid, line_row):
    """ get the colors from grid adjacent to line_row """
    adjacent_colors = []
    for col in range(grid.shape[1]):
        if grid[line_row,col] == 5:
            adjacent_colors.append(get_adjacent_colors(grid,line_row,col))
    adjacent_colors = [item for sublist in adjacent_colors for item in sublist] #flatten
    return adjacent_colors
def get_adjacent_to_bottom(grid):
    rows, cols = grid.shape
    adjacent_colors = []
    for col in range(cols):
        adjacent_colors.append(get_adjacent_colors(grid,rows-1,col))
    return [item for sublist in adjacent_colors for item in sublist]

def calculate_metrics(task):
    metrics = []
    for example in task['train']:
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)  # Use the provided transform function

        # Convert to numpy arrays for easier comparison
        expected_output_np = np.array(expected_output)
        predicted_output_np = np.array(predicted_output)

        # Basic checks
        correct_shape = predicted_output_np.shape == expected_output_np.shape
        all_pixels_correct = np.array_equal(predicted_output_np, expected_output_np) if correct_shape else False

        # Find gray lines
        input_grid_np = np.array(input_grid)
        gray_lines = [r for r in range(input_grid_np.shape[0]) if np.all(input_grid_np[r] == 5)]
        num_gray_lines = len(gray_lines)

        # Check for empty prediction
        is_empty_prediction = predicted_output_np.size == 0
        metrics.append({
            'example_id': example.get('id', 'N/A'),
            'correct_shape': correct_shape,
            'all_pixels_correct': all_pixels_correct,
            'num_gray_lines': num_gray_lines,
            'is_empty_prediction': is_empty_prediction
        })

    return metrics
task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "id": "train_0"
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
      ],
      "id": "train_1"
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0]
      ],
      "output": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      ],
      "id": "train_2"
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      ],
      "id": "train_3"
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0],
        [0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0]
      ],
      "output": [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
      ],
      "id": "train_4"
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      ]
    }
  ]
}

metrics = calculate_metrics(task)
print(metrics)
