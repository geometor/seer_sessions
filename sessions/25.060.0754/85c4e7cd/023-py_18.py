import numpy as np

def get_layer(i, j, rows, cols):
    """
    Determines the layer of a pixel at (i, j) in a grid of size (rows, cols).
    """
    dist_top = i
    dist_bottom = rows - 1 - i
    dist_left = j
    dist_right = cols - 1 - j
    
    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

    # Check if the pixel is part of the 2x2 center
    if rows % 2 == 0 and cols % 2 == 0: #even
        if i >= rows//2 -1 and i <= rows//2  and j >= cols//2 - 1 and j <= cols//2 :
            return rows//2 - 1
    else: #odd
        if i == rows//2 and j == cols//2:
          return min_dist

    return min_dist

def transform(input_grid):
    """
    Transforms the input grid according to the layer-based color mapping.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # Determine the layer of the current pixel
            layer = get_layer(i, j, rows, cols)

            # Apply color mapping based on the layer
            if layer == 0:
                if input_grid[i, j] == 7:
                    output_grid[i, j] = 3
                else:
                    output_grid[i,j] = input_grid[i,j] #handles the outside if different
            elif layer == 1:
                if input_grid[i, j] == 2:
                    output_grid[i, j] = 1
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 2:
                if input_grid[i, j] == 4:
                    output_grid[i, j] = 4
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 3:
                if input_grid[i, j] == 1:
                    output_grid[i, j] = 2
                else:
                    output_grid[i,j] = input_grid[i,j]
            elif layer == 4:
                if rows % 2 == 0: #only applies to even
                    if input_grid[i,j] == 3:
                        output_grid[i, j] = 7
                    else:
                        output_grid[i,j] = input_grid[i,j]
                else:
                    if input_grid[i, j] == 3:
                        output_grid[i,j] = 7
                    else:
                        output_grid[i,j] = input_grid[i,j]
            else:
                output_grid[i, j] = input_grid[i,j] #default

    return output_grid

def compare_grids(grid1, grid2):
    """Compares two grids and returns a detailed report."""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    
    diff = grid1 != grid2
    if not np.any(diff):
        return "Identical"

    num_diff = np.sum(diff)
    diff_indices = np.where(diff)
    report = f"{num_diff} differences:\n"
    for i in range(num_diff):
        row = diff_indices[0][i]
        col = diff_indices[1][i]
        val1 = grid1[row, col]
        val2 = grid2[row, col]
        report += f"  At ({row}, {col}): Expected {val2}, Got {val1}\n"
    return report

# Example grids provided (Replace with actual ARC task grids)
# Make sure this cell runs without error, providing the 'train' data
train = [
    {
        "input": [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 2, 2, 2, 2, 2, 2, 2, 2, 7], [7, 2, 4, 4, 4, 4, 4, 4, 2, 7], [7, 2, 4, 1, 1, 1, 1, 4, 2, 7], [7, 2, 4, 1, 3, 3, 1, 4, 2, 7], [7, 2, 4, 1, 3, 3, 1, 4, 2, 7], [7, 2, 4, 1, 1, 1, 1, 4, 2, 7], [7, 2, 4, 4, 4, 4, 4, 4, 2, 7], [7, 2, 2, 2, 2, 2, 2, 2, 2, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]],
        "output": [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 1, 1, 1, 1, 1, 1, 1, 1, 3], [3, 1, 4, 4, 4, 4, 4, 4, 1, 3], [3, 1, 4, 2, 2, 2, 2, 4, 1, 3], [3, 1, 4, 2, 7, 7, 2, 4, 1, 3], [3, 1, 4, 2, 7, 7, 2, 4, 1, 3], [3, 1, 4, 2, 2, 2, 2, 4, 1, 3], [3, 1, 4, 4, 4, 4, 4, 4, 1, 3], [3, 1, 1, 1, 1, 1, 1, 1, 1, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
    },
    {
        "input": [[7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 2, 2, 2, 2, 2, 2, 2, 7], [7, 2, 4, 4, 4, 4, 4, 2, 7], [7, 2, 4, 1, 1, 1, 4, 2, 7], [7, 2, 4, 1, 3, 1, 4, 2, 7], [7, 2, 4, 4, 4, 4, 4, 2, 7], [7, 2, 2, 2, 2, 2, 2, 2, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7]],
        "output": [[3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 1, 1, 1, 1, 1, 1, 1, 3], [3, 1, 4, 4, 4, 4, 4, 1, 3], [3, 1, 4, 2, 2, 2, 4, 1, 3], [3, 1, 4, 2, 7, 2, 4, 1, 3], [3, 1, 4, 4, 4, 4, 4, 1, 3], [3, 1, 1, 1, 1, 1, 1, 1, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3]]
    },
    {
        "input": [[7, 7, 7, 7, 7, 7, 7], [7, 2, 2, 2, 2, 2, 7], [7, 2, 4, 4, 4, 2, 7], [7, 2, 4, 1, 4, 2, 7], [7, 2, 4, 4, 4, 2, 7], [7, 2, 2, 2, 2, 2, 7], [7, 7, 7, 7, 7, 7, 7]],
        "output": [[3, 3, 3, 3, 3, 3, 3], [3, 1, 1, 1, 1, 1, 3], [3, 1, 4, 4, 4, 1, 3], [3, 1, 4, 2, 4, 1, 3], [3, 1, 4, 4, 4, 1, 3], [3, 1, 1, 1, 1, 1, 3], [3, 3, 3, 3, 3, 3, 3]]
    },
]

for i, example in enumerate(train):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    actual_output = transform(input_grid)
    comparison_result = compare_grids(actual_output, expected_output)
    print(f"Example {i + 1}: {comparison_result}")
