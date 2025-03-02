import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_grid):
    correct_pixels = np.sum(output_grid == predicted_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    predicted_colors = np.unique(predicted_grid)

    return {
        "accuracy": accuracy,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
        "predicted_colors": predicted_colors.tolist(),
    }
def print_grid(grid, title="Grid"):
    print(f"\n--- {title} ---")
    for row in grid:
        print("".join(str(int(cell)) for cell in row))

# Example Data (replace with actual data from the task)
example_data = [
  {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 9, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0],
                            [0, 0, 0, 3, 9, 3, 0, 0, 0],
                            [0, 0, 3, 0, 3, 0, 3, 0, 0],
                            [0, 3, 0, 1, 1, 1, 0, 3, 0],
                            [0, 0, 3, 0, 3, 0, 3, 0, 0],
                            [0, 0, 0, 3, 0, 3, 0, 0, 0],
                            [0, 0, 0, 0, 3, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },
  {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 9, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                            [0, 3, 9, 3, 0, 0, 0, 0, 0, 0],
                            [3, 0, 3, 0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 0, 1, 3, 0, 0, 0, 0, 0],
                            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 3, 9, 3, 0, 0, 0],
                            [0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0],
                            [0, 0, 0, 3, 0, 1, 1, 1, 0, 3, 0],
                            [0, 0, 3, 0, 1, 0, 3, 0, 0, 0, 0],
                            [0, 3, 0, 1, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },

]

def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = np.copy(input_grid)

    # 1. Identify Maroon Regions
    maroon_regions = find_objects(input_grid, 9)

    # 2. Expand Maroon Regions
    new_regions = []

    for region in maroon_regions:
      expanded_region, output_grid = expand_region(output_grid, region, 3)
      expanded_region, output_grid = expand_region_edge(output_grid, expanded_region, 3)
      new_regions.append(expanded_region)


    # 3 & 4: Flood fill
    output_grid = flood_fill(output_grid, 12, 4, 1) # From observation

    return output_grid


def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                objects.append(dfs(r, c))
    return objects

def expand_region(grid, region, expansion_color):
    # Expand the region by one layer, adding an outline on white pixels
    expanded_region = set(region)
    output_grid = np.copy(grid)

    for r, c in region:
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            if (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and
                    grid[nr, nc] == 0):
                expanded_region.add((nr, nc))
                output_grid[nr, nc] = expansion_color
    return list(expanded_region), output_grid

def expand_region_edge(grid, region, expansion_color):
    # expand white cells adjacent to any edge
    expanded_region = set(region)
    output_grid = np.copy(grid)
    for r, c in region:
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            if (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and
                    grid[nr, nc] == 0):
               if nr == 0 or nr == output_grid.shape[0]-1 or nc == 0 or nc == output_grid.shape[1]-1:
                  output_grid[nr, nc] = expansion_color

    return list(expanded_region), output_grid

def flood_fill(grid, start_row, start_col, fill_color):
    """Fills a bounded region with the specified color."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    stack = [(start_row, start_col)]
    original_color = grid[start_row, start_col]

    if original_color == fill_color:
        return grid

    output_grid = np.copy(grid)

    while stack:
        r, c = stack.pop()
        if r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or output_grid[r,c] != original_color:
            continue

        visited[r, c] = True
        output_grid[r,c] = fill_color

        stack.append((r + 1, c))
        stack.append((r - 1, c))
        stack.append((r, c + 1))
        stack.append((r, c - 1))
    return output_grid

for i, example in enumerate(example_data):
  input_grid = example["input"]
  output_grid = example["output"]
  predicted_grid = transform(input_grid)
  print_grid(input_grid, f"Example {i+1} - Input")
  print_grid(output_grid, f"Example {i+1} - Output")
  print_grid(predicted_grid, f"Example{i+1} - Predicted")

  metrics = calculate_metrics(input_grid, output_grid, predicted_grid)
  print(f"Example {i+1} Metrics: {metrics}")