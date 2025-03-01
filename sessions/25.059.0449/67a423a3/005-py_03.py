import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns the differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    diff = grid1 != grid2
    num_diff = np.sum(diff)
    indices = np.where(diff)
    return list(zip(indices[0], indices[1])), num_diff

# Example grids from the training data (replace with actual data)
# Example usage (replace with actual data):
examples = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 5, 5, 5, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 5, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 5, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]),
    },
     {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 5, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 5, 4, 4, 4, 5, 4, 4],
            [4, 4, 4, 5, 4, 4, 4, 5, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]),
    },
        {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 5, 5, 5, 5, 5, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 5, 5, 5, 5, 5, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0],
            [0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0],
            [0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4, 4, 4, 4],
            [4, 5, 5, 5, 4],
            [4, 4, 4, 4, 4],
            [4, 5, 5, 5, 4],
            [4, 4, 4, 4, 4],
        ]),
    },
      {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 5, 5, 5, 5, 5, 5, 5, 5, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        ]),
    }
]

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # preservation of non-white pixel
            if input_grid[r, c] != 0:
                continue

            # conditional change for white pixels
            is_above_green = (r > 0 and input_grid[r-1, c] == 3)
            is_below_green = (r < rows - 1 and input_grid[r+1, c] == 3)
            is_adjacent_yellow = False

            if c > 0 and output_grid[r,c-1] == 4:
                is_adjacent_yellow = True
            if r > 0 and output_grid[r-1,c] == 4:
                is_adjacent_yellow = True    
            if c < cols -1 and output_grid[r,c+1] == 4:
                is_adjacent_yellow = True
            if r < rows - 1 and output_grid[r+1, c] == 4:
                is_adjacent_yellow = True
            
            if not (is_above_green or is_below_green or is_adjacent_yellow):
                 output_grid[r, c] = 4

    return output_grid

results = []
for i, example in enumerate(examples):
    predicted_output = transform(example["input"])
    diff_indices, num_diff = compare_grids(example["output"], predicted_output)
    results.append({
        "example_index": i,
        "num_differences": num_diff,
        "diff_indices": diff_indices,
    })

for result in results:
    print(result)