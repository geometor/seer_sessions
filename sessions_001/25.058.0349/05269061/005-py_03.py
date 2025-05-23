import numpy as np

def compare_results(expected, actual):
    """Compares two grids and returns the number of mismatched pixels."""
    return np.sum(np.array(expected) != np.array(actual))

examples = [
    {
        "input": [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
        "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
    },
    {
        "input": [[6, 0, 0], [0, 0, 0], [0, 0, 8]],
        "output": [[6, 6, 6], [6, 6, 6], [6, 6, 8]]
    },
    {
        "input": [[0, 6, 0], [0, 0, 0], [0, 0, 5]],
        "output": [[6, 6, 6], [6, 6, 6], [6, 6, 5]]
    },
    {
       "input": [[0, 0, 0], [0, 5, 0], [0, 0, 0]],
        "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
    },
     {
        "input": [[0, 0, 8], [0, 0, 0], [0, 0, 0]],
        "output": [[8, 8, 8], [8, 8, 8], [8, 8, 8]],
    }
]
def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height, width), dtype=int)

    # 1. & 2. Pattern Replication
    for i in range(height):
        for j in range(width):
            output_grid[i, j] = input_grid[i % 3, j % 3]

    # 3. Zero Filling (Corrected)
    visited = set()
    for i in range(height):
        for j in range(width):
            if output_grid[i,j] == 0 and (i,j) not in visited:
                propagate_color(output_grid,i,j,height, width, visited)


    return output_grid.tolist()

def get_neighbors(i, j, height, width):
    """
    Get valid neighbors of a cell (i,j) in a grid.
    """
    neighbors = []
    if i > 0:
        neighbors.append((i-1,j))
    if i < height - 1:
        neighbors.append((i+1,j))
    if j > 0:
        neighbors.append((i,j-1))
    if j < width -1:
        neighbors.append((i, j+1))

    return neighbors
    

def propagate_color(output_grid, i, j, height, width, visited):
    """
    Propagate color to connected regions using a stack, handling the 3x3 cell boundaries.

    Args:
        grid (np.array): The input/output grid.
        i (int): starting row index.
        j (int): starting col index.
        height, width: dimensions of the grid
        visited: set of visited cells.

    """

    stack = [(i,j)]
    while stack:
        curr_i, curr_j = stack.pop()

        if (curr_i, curr_j) in visited:
            continue
        visited.add((curr_i,curr_j))

        # Determine the base 3x3 cell indices
        base_i = curr_i % 3
        base_j = curr_j % 3
        
        # find non-zero color source in this cell
        non_zero_color = None
        for ni,nj in get_neighbors(base_i,base_j, 3, 3):
            seed_i, seed_j = curr_i + (ni-base_i),curr_j+(nj-base_j)
            # boundary check
            if 0 <= seed_i < height and 0 <= seed_j < width:
                if output_grid[seed_i, seed_j] != 0:
                    non_zero_color = output_grid[seed_i, seed_j]
                    break # found a source
        if non_zero_color is None: # no source found, look in seed cell
             if output_grid[curr_i - base_i, curr_j - base_j] !=0:
                non_zero_color = output_grid[curr_i-base_i, curr_j-base_j]


        if non_zero_color is not None:
            output_grid[curr_i, curr_j] = non_zero_color

            for ni, nj in get_neighbors(curr_i, curr_j, height, width):
                if output_grid[ni,nj] == 0:
                    stack.append((ni,nj))
for i, example in enumerate(examples):
    actual_output = transform(example["input"])
    mismatches = compare_results(example["output"], actual_output)
    print(f"Example {i+1}: Mismatches = {mismatches}")
    print(f"Input:\n{np.array(example['input'])}")
    print(f"Expected Output:\n{np.array(example['output'])}")
    print(f"Actual Output:\n{np.array(actual_output)}")
    print("-" * 20)