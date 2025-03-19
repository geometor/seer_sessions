import numpy as np

# Provided training examples (replace with actual data loading if available)
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [3, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [4, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                           [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [4, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                            [4, 4, 4, 4, 4, 4, 4, 4, 4, 0]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 0, 0, 0, 0, 0, 0, 0, 5],
                           [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 0]]),
    }
]

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the seed structure
    start_row, height, expansion_color = find_seed_structure(input_grid)

    # Handle cases with no seed structure.
    if start_row == -1:
        return output_grid
    
    # Perform horizontal expansion
    for r in range(start_row, min(start_row + height, rows)):
        for c in range(0, cols - 1):
            output_grid[r, c] = expansion_color

    # Remove isolated pixels
    output_grid = remove_isolated_pixels(output_grid)
            
    return output_grid

def find_seed_structure(grid):
    """Finds the seed structure and its properties."""
    rows, cols = grid.shape
    start_row = -1
    height = 0
    expansion_color = 0

    for r in range(rows):
        if grid[r, 0] != 0:
            if start_row == -1:
                start_row = r
                expansion_color = grid[r, 0]
            height += 1
        elif height > 0:
            break  # Stop once we find a gap

    return start_row, height, expansion_color

def remove_isolated_pixels(grid):
    """Removes isolated pixels from the grid."""
    rows, cols = grid.shape
    output_grid = np.copy(grid)

    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != 0:
                is_isolated = True
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        if (i != r or j != c) and output_grid[i, j] == output_grid[r, c]:
                            is_isolated = False
                            break
                    if not is_isolated:
                        break
                if is_isolated:
                    output_grid[r, c] = 0
    return output_grid

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    if not np.array_equal(predicted_output, expected_output):
        diff = predicted_output - expected_output
        print("Differences found:")
        print(diff)
        
        #check for isolated pixel errors
        isolated_err = False
        rows, cols = diff.shape
        for r in range(rows):
          for c in range(cols):
            if diff[r,c] != 0:
              for i in range(max(0, r - 1), min(rows, r + 2)):
                for j in range(max(0, c - 1), min(cols, c + 2)):
                  if (i != r or j != c) and diff[i, j] == 0:
                    isolated_err = True
                    break
                if isolated_err:
                  break
        if isolated_err:
          print("isolated pixel removal error")
    else:
        print("Prediction matches expected output.")
    print("-" * 20)