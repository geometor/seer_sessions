import numpy as np

def object_metrics(grid, example_id):
    """Calculates metrics for objects in a grid."""
    colors = np.unique(grid)
    metrics = {}
    for color in colors:
        objects = find_objects(grid, color)
        
        metrics[color] = {
            'count': len(objects),
            'sizes': [len(obj) for obj in objects],
            'positions': [obj[0] for obj in objects]  # Just the top-left corner
        }
        
        # Check if any object has a dimension >= 3 and is comprised of a single coordinate
        #  This captures the difference between our assumption of a 3x3 block and a row of length 3.
        for i, obj in enumerate(objects):
            rows, cols = zip(*obj)
            max_row_diff = max(rows) - min(rows)
            max_col_diff = max(cols) - min(cols)
            
            if (max_row_diff +1) * (max_col_diff + 1) != len(obj):
              print(f"    irregular object color {color} index {i}: {obj}")
            
            if max_row_diff >= 2 or max_col_diff >= 2:
                #is_single_coord = all(r == rows[0] and c == cols[0] for r, c in obj)
                is_single_coord = False
                if is_single_coord:
                    print(f"    Object of color {color} at index {i} is a single coord but is on edge")

    print(f"Example {example_id}: {metrics}")
    return metrics

def compare_grids(grid1, grid2, example_id):
    """Compares two grids and prints differences."""
    if grid1.shape != grid2.shape:
        print(f"Example {example_id}: Shapes differ: {grid1.shape} vs {grid2.shape}")
        return

    diff = grid1 != grid2
    if np.any(diff):
        print(f"Example {example_id}: Differences found at:")
        diff_indices = np.where(diff)
        for r, c in zip(*diff_indices):
            print(f"  Row: {r}, Col: {c}, Value1: {grid1[r, c]}, Value2: {grid2[r, c]}")
    else:
        print(f"Example {example_id}: Grids are identical.")

# Re-using find_objects from the provided code.
def find_objects(grid, color):
    # Find contiguous regions of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    obj_coords.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    neighbors = []
                    if curr_r > 0: neighbors.append((curr_r - 1, curr_c))
                    if curr_r < rows - 1: neighbors.append((curr_r + 1, curr_c))
                    if curr_c > 0: neighbors.append((curr_r, curr_c - 1))
                    if curr_c < cols - 1: neighbors.append((curr_r, curr_c + 1))
                    
                    for nr, nc in neighbors:
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            queue.append((nr, nc))
                            visited[nr, nc] = True

                objects.append(obj_coords)

    return objects

# Example data (replace with your actual data)
examples = [
  (np.array([[4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [2, 2, 2, 8, 2, 2, 2, 8, 2, 2, 2], [2, 2, 2, 8, 2, 2, 2, 8, 2, 2, 2], [2, 2, 2, 8, 2, 2, 2, 8, 2, 2, 2]]), np.array([[4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [2, 2, 2, 8, 2, 2, 2, 8, 2, 2, 2], [2, 2, 2, 8, 2, 2, 2, 8, 2, 2, 2], [2, 2, 2, 8, 2, 2, 2, 8, 2, 2, 2], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 8, 4, 4, 4]])),
  (np.array([[5, 0, 5, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 7, 7, 7, 7, 7, 7, 2, 7], [5, 0, 5, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7], [5, 0, 5, 7, 7, 7, 7, 7, 7, 7, 7]]), np.array([[5, 0, 5, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 7, 7, 7, 7, 7, 7, 2, 7], [5, 0, 5, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7], [5, 0, 5, 7, 7, 7, 7, 7, 7, 7, 7]])),
  (np.array([[6, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0], [0, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0], [6, 0, 0, 1, 1, 1, 1, 1, 0, 6, 0], [0, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0], [6, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0]]), np.array([[6, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0], [0, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0], [6, 0, 0, 1, 1, 1, 1, 1, 0, 6, 0], [0, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0], [6, 0, 6, 1, 1, 1, 1, 1, 0, 6, 0]])),
 (np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3], [3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3], [3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3], [3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], [3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3], [3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3], [3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3], [3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3], [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3]]), np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3], [3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3], [3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3], [3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], [3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3], [3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3], [3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3], [3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3], [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3]]))
]

# get the transform results
transformed_examples = [(input_grid, transform(input_grid)) for input_grid, _ in examples]

# Analyze and compare
for i, (input_grid, output_grid) in enumerate(examples):
    transformed_input = transformed_examples[i][1]
    print(f"--- Example {i+1} ---")
    
    print("Input Metrics:")
    object_metrics(input_grid, f"{i+1} (Input)")

    print("\nExpected Output Metrics:")
    object_metrics(output_grid, f"{i+1} (Expected Output)")
    
    print("\nTransformed Input Metrics:")
    object_metrics(transformed_input, f"{i+1} (Transformed Input)")    

    print("\nComparison (Expected Output vs Transformed Input):")
    compare_grids(output_grid, transformed_input, i+1)
    print("-" * 30)