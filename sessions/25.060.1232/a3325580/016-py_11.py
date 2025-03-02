import numpy as np

train_data = [
    {
        'input': np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,2,0],[0,0,0,0,2,0],[0,1,0,0,2,0],[1,1,1,1,2,2]]),
        'output': np.array([[1,2],[1,2],[1,2],[1,2],[1,2]])
    },
    {
        'input':  np.array([[6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[6, 6],
               [6, 6],
               [6, 6],
               [6, 6],
               [6, 6]])
    },
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[7, 4],
               [7, 4],
               [7, 4],
               [7, 4],
               [7, 4],
               [7, 4],
               [7, 4],
               [7, 4]])
    },
    {
        'input': np.array([[0, 0, 0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 5, 0]]),
        'output': np.array([[7, 5],
               [7, 5],
               [7, 5],
               [7, 5],
               [7, 5],
               [7, 5],
               [7, 5]])
    }
]

def get_leftmost_non_background_color(grid):
    """Finds the leftmost non-background (non-zero) color in the grid."""
    for x in range(grid.shape[1]):
        for y in range(grid.shape[0]):
            if grid[y, x] != 0:
                return grid[y, x]
    return 0  # Should not be reached for non empty grids

def get_rightmost_non_background_color(grid):
     """Finds the rightmost non-background (non-zero) color in the grid."""
     for x in range(grid.shape[1]-1,-1,-1):
        for y in range(grid.shape[0]):
            if grid[y, x] != 0:
                return grid[y, x]
     return 0

for i, example in enumerate(train_data):
    input_grid = example['input']
    output_grid = example['output']
    leftmost = get_leftmost_non_background_color(input_grid)
    rightmost = get_rightmost_non_background_color(input_grid)
    input_height = input_grid.shape[0]
    output_height = output_grid.shape[0]
    bottom_row_all_zeros = np.all(input_grid[-1] == 0)

    print(f"Example {i+1}:")
    print(f"  Input shape: {input_grid.shape}")
    print(f"  Output shape: {output_grid.shape}")
    print(f"  Leftmost color: {leftmost}")
    print(f"  Rightmost color: {rightmost}")
    print(f"  Input height: {input_height}")
    print(f"  Output height: {output_height}")
    print(f"  Bottom row all zeros: {bottom_row_all_zeros}")
    print("-" * 20)