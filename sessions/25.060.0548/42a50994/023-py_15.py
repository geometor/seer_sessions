import numpy as np

def count_neighbors(grid, row, col):
    """Counts neighbors with the same color, including diagonals."""
    rows, cols = grid.shape
    target_color = grid[row, col]
    count = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row or j != col) and grid[i, j] == target_color:
                count += 1
    return count

def transform(input_grid):
    """Transforms based on neighbor count, including diagonals."""
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            neighbor_count = count_neighbors(input_grid, row, col)
            if neighbor_count < 2:  # updated threshold based on example results
                output_grid[row, col] = 0
    return output_grid

# Test on provided example
input_str = """
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
"""
input_arr = np.array(eval(input_str.replace(' ', ',').replace('\n',']],[[')))

output_arr = transform(input_arr)

output_str = str(output_arr.tolist()).replace(' ', '').replace('],',']\n').replace(',',' ')
print(output_str)

input_str = """
1 1 1 1 1
1 4 4 4 1
1 4 4 4 1
1 4 4 4 1
1 1 1 1 1
"""
input_arr = np.array(eval(input_str.replace(' ', ',').replace('\n',']],[[')))

output_arr = transform(input_arr)

output_str = str(output_arr.tolist()).replace(' ', '').replace('],',']\n').replace(',',' ')
print(output_str)

input_str = """
6 6 6 6 6 6 6
6 6 6 6 6 6 6
6 6 5 5 5 6 6
6 6 5 6 5 6 6
6 6 5 5 5 6 6
6 6 6 6 6 6 6
"""
input_arr = np.array(eval(input_str.replace(' ', ',').replace('\n',']],[[')))

output_arr = transform(input_arr)

output_str = str(output_arr.tolist()).replace(' ', '').replace('],',']\n').replace(',',' ')
print(output_str)
