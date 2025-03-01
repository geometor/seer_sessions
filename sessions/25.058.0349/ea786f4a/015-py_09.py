import numpy as np

def analyze_grids(input_grid, output_grid):
    input_white_pixels = np.sum(input_grid == 0)
    output_white_pixels = np.sum(output_grid == 0)
    input_shape = input_grid.shape
    output_shape = output_grid.shape

    return {
        "input_white_pixels": int(input_white_pixels),
        "output_white_pixels": int(output_white_pixels),
        "input_shape": input_shape,
        "output_shape": output_shape,
    }

# Example Usage (assuming the first training pair is available)
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
