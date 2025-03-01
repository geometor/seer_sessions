import numpy as np

def find_objects(grid):
    """Finds non-white objects in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj_id, color):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return []

        visited.add((r, c))
        object_pixels = [(r, c)]

        # Check adjacent pixels (horizontal and vertical)
        neighbors = [(r, c + 1), (r, c - 1), (r+1, c), (r-1, c)]  # Simplified to horizontal for this specific pattern
        for nr, nc in neighbors:
             object_pixels.extend(dfs(nr, nc, obj_id, color))

        return object_pixels

    obj_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_pixels = dfs(r, c, obj_id_counter, grid[r, c])
                if obj_pixels:
                    objects.append({
                        "id": obj_id_counter,
                        "color": grid[r, c],
                        "pixels": obj_pixels
                    })
                    obj_id_counter += 1

    return objects

def calculate_object_metrics(objects):
    """Calculates metrics for each object like bounding box and centroid."""
    metrics = []
    for obj in objects:
        pixels = np.array(obj['pixels'])
        min_row, min_col = np.min(pixels, axis=0)
        max_row, max_col = np.max(pixels, axis=0)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        centroid_row = (min_row + max_row) / 2
        centroid_col = (min_col + max_col) / 2
        metrics.append({
            'id': obj['id'],
            'color': obj['color'],
            'min_row': min_row,
            'min_col': min_col,
            'max_row': max_row,
            'max_col': max_col,
            'width': width,
            'height': height,
            'centroid_row': centroid_row,
            'centroid_col': centroid_col
        })
    return metrics

def analyze_transformation(input_grid, output_grid):
    """Analyzes the transformation between input and output grids."""
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    input_metrics = calculate_object_metrics(input_objects)
    output_metrics = calculate_object_metrics(output_objects)
    
    print("Input Grid Metrics")
    print(input_metrics)
    print("Output Grid Metrics")
    print(output_metrics)

    rows, cols = input_grid.shape
    print(f"Input Grid Dimensions: {rows}x{cols}")
    
    rows, cols = output_grid.shape
    print(f"Output Grid Dimensions: {rows}x{cols}")    

# Example Usage (replace with your actual task data):
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 4, 4, 0, 0], [0, 0, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0], [8, 8, 0, 0, 0, 0], [8, 8, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 4, 4, 0, 0], [0, 0, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0], [8, 8, 0, 0, 0, 0], [8, 8, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
    ],
        "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0]],
        }
    ]
}

for example in task["train"]:
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    analyze_transformation(input_grid, output_grid)
    print("-" * 30)