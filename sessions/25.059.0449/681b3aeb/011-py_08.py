import numpy as np

def find_objects(grid):
    # Find all contiguous regions of non-zero color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                objects.append(obj_pixels)
    return objects

def get_bounding_box(objects):
    # Determine bounding box that encompasses all objects
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for obj in objects:
      for r,c in obj:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    input_bb = get_bounding_box(input_objects)
    output_bb = get_bounding_box(output_objects)
    
    input_bb_height = input_bb[1][0] - input_bb[0][0] + 1 if input_objects else 0
    input_bb_width = input_bb[1][1] - input_bb[0][1] + 1 if input_objects else 0
    output_bb_height = output_bb[1][0] - output_bb[0][0] + 1 if output_objects else 0
    output_bb_width = output_bb[1][1] - output_bb[0][1] + 1 if output_objects else 0

    print(f"Input Grid Shape: {input_grid.shape}")
    print(f"Output Grid Shape: {output_grid.shape}")
    print(f"Input Objects: {len(input_objects)}")
    print(f"Output Objects: {len(output_objects)}")
    print(f"Input Bounding Box: {input_bb}")
    print(f"Output Bounding Box: {output_bb}")
    print(f"Input Bounding Box Shape: ({input_bb_height},{input_bb_width})")
    print(f"Output Bounding Box Shape: ({output_bb_height},{output_bb_width})")
    print(f"Objects are equal: {input_objects == output_objects}")


# Example data (replace with actual data from the task)
task_examples = [
    ([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5, 5, 0, 0]], [[5, 5, 5, 5, 5, 5, 5, 8, 8], [5, 5, 5, 5, 5, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5, 5, 0, 0]]),
    ([[5, 5, 5, 5, 5, 5, 5, 8, 8], [5, 5, 5, 5, 5, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5, 5, 0, 0]], [[5, 5, 5, 5, 5, 5, 5, 8, 8], [5, 5, 5, 5, 5, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5, 5, 0, 0]]),
    ([[5, 0, 5, 5, 5, 5, 5, 8, 8], [5, 0, 5, 5, 5, 5, 5, 0, 0], [5, 0, 5, 5, 5, 5, 5, 0, 0]], [[5, 0, 5, 5, 5, 5, 5, 8, 8], [5, 0, 5, 5, 5, 5, 5, 0, 0], [5, 0, 5, 5, 5, 5, 5, 0, 0]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 8]], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 8]]),
    ([[5, 5, 5, 5, 5, 5, 5, 8, 8], [5, 5, 5, 5, 5, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], [[5, 5, 5, 5, 5, 5, 5, 8, 8], [5, 5, 5, 5, 5, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5, 5, 0, 0]]),
]

for i, (input_grid, output_grid) in enumerate(task_examples):
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid)