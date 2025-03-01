import numpy as np

def analyze_example(input_grid, output_grid):
    gray_pixels = []
    changed_white_pixels = []
    unchanged_white_pixels = []

    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 5:
                gray_pixels.append((r, c))
            elif input_grid[r, c] == 0:
                if output_grid[r, c] == 2:
                    changed_white_pixels.append((r, c))
                elif output_grid[r,c] == 0:
                    unchanged_white_pixels.append((r,c))

    return {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'gray_pixels': gray_pixels,
        'changed_white_pixels': changed_white_pixels,
        'unchanged_white_pixels': unchanged_white_pixels,
    }

# dummy data for demonstration,
# will replace with actual examples in the next turn
examples = [
    (np.array([[0, 5, 0], [0, 0, 0], [0, 5, 0]]), np.array([[2, 5, 2], [0, 0, 0], [2, 5, 2]])),
    (np.array([[0, 0, 5], [0, 0, 0], [5, 0, 0]]), np.array([[2, 2, 5], [0, 0, 0], [5, 2, 2]])),
    (np.array([[5, 0, 0], [0, 0, 0], [0, 0, 5]]), np.array([[5, 2, 2], [0, 0, 0], [2, 2, 5]])),
    (np.array([[0, 0, 0, 5], [0, 0, 0, 0], [5, 0, 0, 0]]), np.array([[2, 0, 2, 5], [0, 0, 0, 0], [5, 2, 2, 2]])),
]

results = []

for input, output in examples:
  analysis = analyze_example(input,output)
  results.append(analysis)

for i, r in enumerate(results):
    print(f"Example {i+1}:")
    print(r)