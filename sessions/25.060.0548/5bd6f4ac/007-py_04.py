import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    in_height, in_width = input_grid.shape
    out_height, out_width = output_grid.shape

    # Find subgrid location
    start_row, start_col = -1, -1  # Initialize to -1
    for i in range(in_height - out_height + 1):
        for j in range(in_width - out_width + 1):
            sub_grid = input_grid[i:i+out_height, j:j+out_width]
            if np.array_equal(sub_grid, output_grid):
                start_row, start_col = i, j
                break  # Exit inner loop once found
        if start_row != -1:
            break  # Exit outer loop once found
            
    #find the 3x3 area enclosed by a single color
    enclosed_coords = []
    for row in range(1, in_height - 1):
        for col in range(1, in_width -1):
            values = [
              input_grid[row-1, col-1],
              input_grid[row-1, col],
              input_grid[row-1, col+1],
              input_grid[row, col-1],
              input_grid[row, col+1],
              input_grid[row+1, col-1],
              input_grid[row+1, col],
              input_grid[row+1, col+1],
            ]
            if len(set(values)) == 1:
                enclosed_coords.append(((row, col), values[0]))

    return {
        "input_shape": (in_height, in_width),
        "output_shape": (out_height, out_width),
        "subgrid_start": (start_row, start_col) if start_row != -1 else None,
        "enclosed_coords": enclosed_coords
    }

examples = [
    (
        [[9, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [4, 8, 4, 4, 8, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [4, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[9, 7, 0],
         [4, 8, 4],
         [4, 0, 0]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 2, 2],
         [0, 2, 0],
         [0, 0, 0]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
       [[0, 0, 7],
        [0, 8, 0],
        [7, 0, 0]]
    )
]

results = [analyze_example(in_grid, out_grid) for in_grid, out_grid in examples]

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Subgrid Start (row, col): {result['subgrid_start']}")
    print(f" enclosed coordinates: {result['enclosed_coords']}")
    print("-" * 20)