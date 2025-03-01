import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects within a grid.  An object is a contiguous set of
    pixels of the same color.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels:
                    objects.append({'color': color, 'pixels': object_pixels})
    return objects

def analyze_example(input_grid, output_grid):
    objects = find_objects(input_grid)
    maroon_object = None
    for obj in objects:
        if obj['color'] == 9:
            maroon_object = obj
            break
    blue_object = None
    for obj in objects:
      if obj['color'] == 1:
        blue_object = obj
        break

    output_red_pixels = []
    if output_grid is not None:
      for r in range(output_grid.shape[0]):
          for c in range(output_grid.shape[1]):
              if output_grid[r, c] == 2:
                  output_red_pixels.append((r, c))

    analysis = {
        'maroon_object_exists': maroon_object is not None,
        'maroon_object_pixels': maroon_object['pixels'] if maroon_object else [],
        'blue_object_pixels': blue_object['pixels'] if blue_object else [],
        'output_red_pixels': output_red_pixels,
        'input_grid': input_grid,
        'output_grid': output_grid
    }
    return analysis

def show_grid(grid, title):
  if grid is None:
    return title + ': None'
  return title + ':\n' + str(grid)

examples = [
    # example 1
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 9, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 9, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])
    ),
    # example 2
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([
            [2, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])
    ),
    # example 3
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([
            [0, 2, 0],
            [0, 0, 0],
            [0, 0, 0]])
    )
]

results = []
for i, (input_grid, output_grid) in enumerate(examples):
    analysis = analyze_example(input_grid, output_grid)
    results.append(analysis)
    print(f"Analysis of Example {i+1}:")
    print(f"  Maroon Object Exists: {analysis['maroon_object_exists']}")
    print(f"  Maroon Object Pixels: {analysis['maroon_object_pixels']}")
    print(f"  Blue Object Pixels: {analysis['blue_object_pixels']}")
    print(f"  Expected Output Red Pixels: {analysis['output_red_pixels']}")
    # Calculate relative position
    if analysis['maroon_object_exists']:
        maroon_top = min(analysis['maroon_object_pixels'])[0]
        maroon_left = min([c for r, c in analysis['maroon_object_pixels']])
        maroon_right = max([c for r, c in analysis['maroon_object_pixels']]) + 1
        print(f"  Maroon Top Row: {maroon_top}")
        print(f"  Maroon Left Column: {maroon_left}")
        print(f"  Maroon Right Column: {maroon_right}")

    print("-" * 30)