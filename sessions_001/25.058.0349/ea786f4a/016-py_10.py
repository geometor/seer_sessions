import numpy as np

def analyze_grids(input_grid, output_grid):
    # Find rows with at least one white pixel
    rows_with_white = np.any(input_grid == 0, axis=1)
    
    # Determine output height 
    output_height = np.sum(rows_with_white)
    
    #find column indexes that have white
    white_cols = np.where(np.any(input_grid == 0, axis=0))[0]


    input_white_pixels = np.sum(input_grid == 0)
    output_white_pixels = np.sum(output_grid == 0)
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    
    gray_positions = np.where(input_grid == 5)
    gray_values_output = output_grid[gray_positions[0][:output_shape[0]], gray_positions[1][:output_shape[1]]]


    return {
        "input_white_pixels": int(input_white_pixels),
        "output_white_pixels": int(output_white_pixels),
        "input_shape": input_shape,
        "output_shape": output_shape,
        "rows_with_white": rows_with_white.tolist(),
        "output_height": int(output_height),
        "white_cols": white_cols.tolist(),
        "gray_matches": np.all(gray_values_output == 5)

    }

examples = [
    (np.array([[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 0, 5],
               [5, 5, 5, 5, 5, 5]]),
     np.array([[5, 5, 5, 5, 0, 5],
               [5, 5, 5, 5, 0, 5],
               [5, 5, 5, 5, 0, 5]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 0, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5]]),
     np.array([[5, 5, 5, 0, 5, 5, 5],
               [5, 5, 5, 0, 5, 5, 5],
               [5, 5, 5, 0, 5, 5, 5],
               [5, 5, 5, 0, 5, 5, 5],
               [5, 5, 5, 0, 5, 5, 5]])),
    (np.array([[5, 5, 5, 5, 5, 5],
              [5, 5, 5, 0, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 0],
              [5, 5, 5, 5, 5, 5]]),
     np.array([[5, 5, 5, 0, 5, 0],
               [5, 5, 5, 0, 5, 0],
               [5, 5, 5, 0, 5, 0],
               [5, 5, 5, 0, 5, 0],
               [5, 5, 5, 0, 5, 0]]))
]

results = [analyze_grids(inp, out) for inp, out in examples]
for i, res in enumerate(results):
    print(f"Example {i+1}: {res}")