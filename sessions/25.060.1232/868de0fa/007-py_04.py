import numpy as np

# --- (Provided code: find_objects, get_border_pixels, get_interior_pixels, is_in_top_left_quadrant) ---
# ... (Paste the provided functions here) ...
def find_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    Uses depth first search (DFS), but only considers directly adjacent neighbors.
    """
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        # Check only 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_border_pixels(grid):
    border_pixels = set()
    rows, cols = grid.shape
    for r in range(rows):
        border_pixels.add((r, 0))
        border_pixels.add((r, cols - 1))
    for c in range(cols):
        border_pixels.add((0, c))
        border_pixels.add((rows - 1, c))
    return border_pixels

def get_interior_pixels(grid, object_pixels):
    interior_pixels = set()
    for r, c in object_pixels:
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        is_interior = True
        for nr, nc in neighbors:
            if not (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and (nr, nc) in object_pixels):
                is_interior = False
                break
        if is_interior:
            interior_pixels.add((r, c))
    return interior_pixels
    
def is_in_top_left_quadrant(grid, object_pixels):
    rows, cols = grid.shape
    quadrant_row_limit = rows // 2
    quadrant_col_limit = cols // 2
    for r, c in object_pixels:
        if r < quadrant_row_limit and c < quadrant_col_limit:
            return True
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()

    # Find blue objects
    blue_objects = find_objects(input_grid, 1)
    
    # Get border pixels
    border_pixels = get_border_pixels(input_grid)

    # Iterate through blue objects
    for obj in blue_objects:
        # Get interior pixels
        interior_pixels = get_interior_pixels(input_grid, obj)
        
        # Check if all pixels are border pixels
        all_border = all(pixel in border_pixels for pixel in obj)

        # Color transformation rules for interior pixels
        if not all_border:
          if is_in_top_left_quadrant(input_grid, obj):
              for r, c in interior_pixels:
                  output_grid[r, c] = 2  # Red
          elif len(obj) > 4 :
              for r, c in interior_pixels:
                  output_grid[r, c] = 7  # Orange

    return output_grid

def analyze_example(input_grid, expected_output_grid):
    """Analyzes a single example and returns metrics."""
    blue_objects = find_objects(input_grid, 1)
    border_pixels = get_border_pixels(input_grid)
    analysis = {
        "blue_objects": [],
        "output_matches": False,
        "changed_pixels": [], #added to collect pixel deltas
    }
    
    output_grid = transform(input_grid)
    if np.array_equal(output_grid, expected_output_grid):
      analysis["output_matches"] = True

    for obj in blue_objects:
        all_border = all(pixel in border_pixels for pixel in obj)
        interior_pixels = get_interior_pixels(input_grid, obj)
        object_analysis = {
            "size": len(obj),
            "all_border_pixels": all_border,
            "interior_pixels": list(interior_pixels),
            "in_top_left_quadrant": is_in_top_left_quadrant(input_grid, obj),
        }
        analysis["blue_objects"].append(object_analysis)

    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] != output_grid[r,c]:
                analysis["changed_pixels"].append(
                    {
                        "location": (r,c),
                        "from": int(input_grid[r,c]),
                        "to": int(output_grid[r,c])
                    }
                )

    return analysis


# Example data (replace with actual task data)
task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0], [0, 0, 0, 0, 0, 1, 2, 1, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 7, 7, 7, 1], [0, 0, 0, 0, 0, 1, 7, 7, 7, 1], [0, 0, 0, 0, 0, 1, 7, 7, 7, 1], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
    },
    {
      "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
      "output": [[1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 7, 7, 7, 7, 7, 7, 7, 7, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }
  ]
}

results = []
for example in task["train"]:
    results.append(analyze_example(np.array(example["input"]), np.array(example["output"])))

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Output Matches Expected: {result['output_matches']}")
    print(f"  Blue Objects:")
    for j, obj in enumerate(result["blue_objects"]):
        print(f"    Object {j+1}:")
        print(f"      Size: {obj['size']}")
        print(f"      All Border Pixels: {obj['all_border_pixels']}")
        print(f"      Interior Pixels: {obj['interior_pixels']}")
        print(f"      In Top-Left Quadrant: {obj['in_top_left_quadrant']}")
    print(f" Changed Pixels: {result['changed_pixels']}")
    print("-" * 20)