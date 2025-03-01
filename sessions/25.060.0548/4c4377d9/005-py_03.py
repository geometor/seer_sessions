import numpy as np

def get_grid_dimensions(grid):
    return len(grid), len(grid[0]) if grid else 0

def calculate_pixel_count(grid):
    return sum(row.count(pixel) for row in grid for pixel in set(row))

def count_colors(grid):
    color_counts = {}
    for row in grid:
        for pixel in row:
            if pixel not in color_counts:
              color_counts[pixel] = 0
            color_counts[pixel] += 1
    return color_counts

def are_grids_equal(grid1, grid2):
    return grid1 == grid2

def get_diff(grid1, grid2):
    # Ensure grids are of the same dimensions
    if len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        return "Grids have different dimensions"

    diff = []
    for i in range(len(grid1)):
        row_diff = []
        for j in range(len(grid1[0])):
            if grid1[i][j] != grid2[i][j]:
                row_diff.append((grid1[i][j], grid2[i][j]))
            else:
                row_diff.append(grid1[i][j])
        diff.append(row_diff)
    return diff
    

task = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 0, 0, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5], [5, 5, 0, 0, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 0, 0, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 0, 0, 5]],
        },
        {
            "input": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]],
            "output": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]],
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 8, 8, 8]],
            "output": [[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 8, 8, 8]],
        },
    ],
    "test": [{"input": [[7, 7, 7, 7, 7], [7, 7, 7, 0, 7], [7, 7, 7, 7, 7]], "output": []}],
}

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid.
    rows, cols = input_array.shape
    
    # Initialize an empty output array with doubled row count.
    output_array = np.zeros((rows * 2, cols), dtype=int)
    
    # Row Replication: Duplicate each row from input to output.
    for i in range(rows):
        output_array[2*i, :] = input_array[i, :]
        output_array[2*i + 1, :] = input_array[i, :]

    # Swap the second and third rows.
    output_array[[1, 2]] = output_array[[2, 1]]

        # Swap the forth and fifth rows.
    output_array[[3, 4]] = output_array[[4, 3]]    

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()
    
    return output_grid


results = []
for example in task["train"]:
  transformed = transform(example['input'])
  results.append({
      'input_dimensions': get_grid_dimensions(example['input']),
      'output_dimensions': get_grid_dimensions(example['output']),
      'transformed_dimensions': get_grid_dimensions(transformed),
      'input_colors': count_colors(example['input']),
      'output_colors': count_colors(example['output']),
      'transformed_colors': count_colors(transformed),
      'grids_equal_output_transformed': are_grids_equal(example['output'], transformed),
      'diff_output_transformed': get_diff(example['output'], transformed)
  })

for result in results:
  print(result)