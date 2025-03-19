import numpy as np

# Provided functions (find_all_objects, crop_to_bounds, transform) - copied from previous turn
# ... (paste the code here) ...
def find_all_objects(grid):
    # Find all objects (contiguous regions of the same color) in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, coords):
        # Depth-first search to find all connected pixels of the same color.
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        coords.append((row, col))
        dfs(row + 1, col, color, coords)
        dfs(row - 1, col, color, coords)
        dfs(row, col + 1, color, coords)
        dfs(row, col - 1, color, coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                coords = []
                dfs(row, col, grid[row, col], coords)
                if coords:
                    # Calculate bounding box and size for each object
                    min_row, max_row = min(coords, key=lambda x: x[0])[0], max(coords, key=lambda x: x[0])[0]
                    min_col, max_col = min(coords, key=lambda x: x[1])[1], max(coords, key=lambda x: x[1])[1]
                    size = (max_row - min_row + 1) * (max_col - min_col + 1)
                    objects.append({
                        'color': grid[row, col],
                        'coords': coords,
                        'bbox': (min_row, max_row, min_col, max_col),
                        'size': size
                    })
    return objects

def crop_to_bounds(grid, bbox):
    # Crop the grid to the given bounding box.
    min_row, max_row, min_col, max_col = bbox
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find all objects in the input grid.
    objects = find_all_objects(input_grid)

    # Handle different cases based on object analysis
    if not objects:
        return []

    # Case: Scattered single pixels (check if any object has size 1 and non-contiguous neighbors)
    scattered_pixels = [obj for obj in objects if obj['size'] == 1]
    if scattered_pixels:
        for obj in scattered_pixels: #check neighbors of single pixels
            r,c = obj['coords'][0]
            neighbors = 0
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < input_grid.shape[0] and 0 <= nc < input_grid.shape[1]:
                        if input_grid[nr,nc] == obj['color']:
                            neighbors+=1
            if neighbors == 0: #disconnected
                if obj['color'] == 1: #blue
                    return [[1]]

    # Case: Multiple objects of the same color - select smallest.
    if len(objects) > 1:
        smallest_object = min(objects, key=lambda x: x[size])
        cropped_region = crop_to_bounds(input_grid, smallest_object['bbox'])
        mask = np.zeros_like(cropped_region,dtype=bool)
        for r,c in smallest_object['coords']:
            mask[r-smallest_object['bbox'][0],c-smallest_object['bbox'][2]] = True
        return np.where(mask, smallest_object['color'], 0).tolist()
        

    # Case: Single contiguous object.
    if len(objects) == 1:
        object_ = objects[0]
        cropped_region = crop_to_bounds(input_grid, object_['bbox'])
        mask = np.zeros_like(cropped_region,dtype=bool)
        for r,c in object_['coords']:
            mask[r-object_['bbox'][0],c-object_['bbox'][2]] = True
        return np.where(mask, object_['color'], 0).tolist()

    return []


task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[1]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[3]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[5]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8]]
        }
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4]]
        }
    ]
}

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)
        objects_info = find_all_objects(np.array(input_grid))
        results.append({
            'input': input_grid,
            'expected_output': expected_output,
            'predicted_output': predicted_output,
            'objects_info': objects_info,
            'correct': predicted_output == expected_output
        })
    return results

results = analyze_examples(task_data)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input:\n{np.array(result['input'])}")
    print(f"  Expected Output: {result['expected_output']}")
    print(f"  Predicted Output: {result['predicted_output']}")
    print(f"  Objects Info: {result['objects_info']}")
    print(f"  Correct: {result['correct']}")
    print("-" * 20)