def get_object_properties(grid):
    """
    Identifies contiguous objects within a grid and returns their properties.
    An object is a set of connected pixels.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        # Explore adjacent cells (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                if color != 0:  # Ignore background
                    current_object = []
                    dfs(r, c, color, current_object)
                    if current_object:
                        min_r = min(pos[0] for pos in current_object)
                        max_r = max(pos[0] for pos in current_object)
                        min_c = min(pos[1] for pos in current_object)
                        max_c = max(pos[1] for pos in current_object)
                        objects.append({
                            "color": color,
                            "min_row": min_r,
                            "max_row": max_r,
                            "min_col": min_c,
                            "max_col": max_c,
                            "size": len(current_object),
                            "shape": (max_r - min_r + 1, max_c - min_c + 1),
                            "positions": current_object,
                        })

    return objects

def show_grid(grid, title):
  print(title)
  for row in grid:
    print(row)
  print()

task = task_data[TASK_ID]
for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    output_grid = example["output"]
    predicted = transform(np.array(input_grid))
    correct = np.array_equal(predicted, np.array(output_grid))
    print(f"Example: train_{i}")
    print(f"Input Shape: {np.array(input_grid).shape}")
    print(f"Output Shape: {np.array(output_grid).shape}")
    print(f"Correct: {correct}")
    show_grid(input_grid, "input grid")
    input_objects = get_object_properties(input_grid)
    for i, obj in enumerate(input_objects):
      print(f"Input Object {i}:")
      for k, v in obj.items():
        print(f"  {k}: {v}")
    show_grid(output_grid, "output_grid")
    output_objects = get_object_properties(output_grid)
    for i, obj in enumerate(output_objects):
      print(f"Output Object {i}:")
      for k, v in obj.items():
        print(f"  {k}: {v}")

    print()