def describe_grid(grid):
    desc = []
    desc.append(f"Shape: {grid.shape}")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    for color, count in color_counts.items():
        desc.append(f"Color {color}: {count} pixels")
    return "\n".join(desc)

def find_objects(grid, color):
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(row, col, current_object):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects
def get_adjacent_colors(grid, row, col):
    """Returns a set of colors adjacent to the given cell."""
    adjacent_colors = set()
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:  # Skip the cell itself
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                adjacent_colors.add(grid[r, c])
    return adjacent_colors