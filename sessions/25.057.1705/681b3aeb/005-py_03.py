import numpy as np

def find_objects(grid):
    """
    Finds all contiguous non-zero regions (objects) in the grid.
    Returns a list of objects, where each object is a tuple: (color, [(row, col), ...]).
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, object_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                objects.append((grid[r, c], object_pixels))
    return objects

def bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return (0, 0, 0, 0)
    min_r, min_c = pixels[0]
    max_r, max_c = pixels[0]
    for r, c in pixels:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c, max_r, max_c)
def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns object information."""
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    input_data = []
    for color, pixels in input_objects:
        bbox = bounding_box(pixels)
        input_data.append({
            'color': color,
            'pixels': pixels,
            'bounding_box': bbox,
            'area': len(pixels)
        })


    output_data = []
    for color, pixels in output_objects:
        bbox = bounding_box(pixels)
        output_data.append({
            'color': color,
            'pixels': pixels,
            'bounding_box': bbox,
            'area': len(pixels)
        })

    return input_data, output_data

def calculate_metrics(input_grid, output_grid, predicted_grid):

    correct = np.all(predicted_grid == output_grid)
    return {
        'correct': correct,
        'input_grid_shape': input_grid.shape,
        'output_grid_shape': output_grid.shape,
        'predicted_grid_shape': predicted_grid.shape
        }
examples = [
    {'input': np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]), 'output': np.array([[9, 0, 0, 0, 0, 0], [9, 0, 0, 0, 0, 0], [9, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])},
    {'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'output': np.array([[5, 5, 5, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])},
    {'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]), 'output': np.array([[8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])}
]

results = []
for example in examples:
    input_grid = example['input']
    output_grid = example['output']
    predicted_grid = transform(input_grid)  # Use the provided transform function
    metrics = calculate_metrics(input_grid, output_grid, predicted_grid)
    input_data, output_data = analyze_example(input_grid, output_grid)
    results.append({
        'metrics': metrics,
        'input_objects': input_data,
        'output_objects': output_data
    })
print(results)