import numpy as np

def get_all_neighbors(grid, row, col):
    rows, cols = grid.shape
    neighbors = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i != 0 or j != 0) and 0 <= row + i < rows and 0 <= col + j < cols:
                neighbors.append(grid[row + i, col + j])
    return neighbors

def transform(input_grid):
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)
    for row in range(rows):
        for col in range(cols):
            neighbors = get_all_neighbors(input_grid, row, col)
            current_color = input_grid[row, col]
            different_color_count = 0
            for neighbor_color in neighbors:
                if neighbor_color != current_color:
                    different_color_count += 1
            if different_color_count >= 2:
                output_grid[row, col] = 5
            else:
                output_grid[row, col] = 0
    return output_grid

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

def analyze_example(input_grid, expected_output_grid):
    transformed_grid = transform(input_grid)
    is_correct = compare_grids(transformed_grid, expected_output_grid)
    
    mismatches = []
    if not is_correct:
        mismatches = np.where(transformed_grid != expected_output_grid)
        mismatches = list(zip(mismatches[0], mismatches[1]))

    return {
        'is_correct': is_correct,
        'mismatches': mismatches,
        'transformed_grid': transformed_grid.tolist(),  # Convert to list for easier handling
        'expected_output_grid': expected_output_grid.tolist()
    }

# Provided training examples (replace with actual data from the task)
train_examples = [
    (np.array([[5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0],
              [5, 0, 5, 0, 5, 0, 5]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0]])),
    
    (np.array([[5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 8, 0, 8, 0, 8, 0, 8, 0],
              [5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 8, 0, 8, 0, 8, 0, 8, 0],
              [5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 8, 0, 8, 0, 8, 0, 8, 0],
              [5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 8, 0, 8, 0, 8, 0, 8, 0],
              [5, 0, 5, 0, 5, 0, 5, 0, 5]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    
    (np.array([[5, 0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [5, 0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [5, 0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [5, 0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [5, 0, 5, 0, 5, 0, 5, 0, 5, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5]]))
]

results = [analyze_example(inp, out) for inp, out in train_examples]
print(results)

