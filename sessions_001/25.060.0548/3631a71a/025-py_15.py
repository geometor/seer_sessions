import numpy as np

def get_connected_component(grid, start_row, start_col, color):
    """
    Finds the connected component of a given color starting from a given cell.
    Uses Depth First Search (DFS).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    component = []

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        component.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    dfs(start_row, start_col)
    return component

def analyze_example(input_grid, output_grid):
    """Analyzes a single input/output pair."""
    rows, cols = input_grid.shape
    changed_pixels = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != output_grid[r, c]:
                changed_pixels.add((r, c))

    components = {}
    visited = np.zeros_like(input_grid, dtype=bool)
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = input_grid[r, c]
                component = get_connected_component(input_grid, r, c, color)
                for row, col in component:
                    visited[row, col] = True
                components[tuple(component)] = color  # Use tuple for hashability

    component_changes = {}
    for component, color in components.items():
        changed = any(pixel in changed_pixels for pixel in component)
        component_changes[component] = (color, changed)

    return changed_pixels, component_changes

# Example usage (replace with actual input/output grids from the task):
task_id = '3906de3d'
task_data = eval(open(f'ARC/data/training/{task_id}.json').read())

for idx, example in enumerate(task_data['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])

    changed_pixels, component_changes = analyze_example(input_grid, output_grid)

    print(f"Example {idx + 1}:")
    print("  Changed Pixels:", changed_pixels)
    print("  Component Changes:")
    for component, (color, changed) in component_changes.items():
        print(f"    Color: {color}, Changed: {changed}, Component: {component}")
    print("-" * 20)
