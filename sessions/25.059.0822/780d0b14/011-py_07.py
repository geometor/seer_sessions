import numpy as np

def find_regions(grid):
    """
    Finds contiguous regions of the same color in a grid.
    Returns a dictionary mapping (row, col) of top-left pixel to color.
    """
    visited = set()
    regions = {}

    def dfs(row, col, color):
        if (row, col) in visited or row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col] != color:
            return
        visited.add((row, col))
        dfs(row + 1, col, color)
        dfs(row - 1, col, color)
        dfs(row, col + 1, color)
        dfs(row, col - 1, color)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                color = grid[row, col]
                dfs(row, col, color)
                regions[(row, col)] = color
    return regions

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_regions = find_regions(input_grid)
    output_regions = find_regions(output_grid)
    
    print("Input Grid:")
    print(input_grid)
    print("Number of Input Regions:", len(input_regions))
    print("Input Region Colors:", set(input_regions.values()))
    print("\nOutput Grid:")
    print(output_grid)
    print("Number of Output Regions:", len(output_regions))
    print("Output Region Colors:", set(output_regions.values()))
    print("Output dimensions:", output_grid.shape)
    print("-" * 20)
    

# Provide the training examples directly
train_examples = [
    (
        [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 8, 3, 3, 3, 8, 8, 2, 8, 8],
         [8, 8, 3, 3, 3, 8, 2, 2, 2, 8],
         [8, 8, 3, 3, 3, 8, 8, 2, 8, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        [[8, 3, 2]]
    ),
    (
        [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 8, 3, 3, 3, 8, 8, 8, 2, 8],
         [8, 8, 3, 3, 3, 8, 8, 2, 2, 8],
         [8, 8, 3, 3, 3, 8, 8, 8, 2, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        [[8, 3, 2]]
    ),
     (
        [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 8, 3, 3, 3, 8, 8, 8, 8, 8],
         [8, 8, 3, 3, 3, 8, 2, 2, 2, 8],
         [8, 8, 3, 3, 3, 8, 8, 8, 8, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        [[8, 3, 2]]
    ),
      (
        [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 8, 3, 3, 3, 8, 2, 2, 8, 8],
         [8, 8, 3, 3, 3, 8, 2, 2, 8, 8],
         [8, 8, 3, 3, 3, 8, 8, 8, 8, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        [[8, 3, 2]]
    )
]
for input_grid, output_grid in train_examples:
  analyze_example(input_grid, output_grid)
