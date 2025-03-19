def describe_changes(input_grid, output_grid):
    """Describes the changes between input and output grids."""
    changes = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != output_grid[r, c]:
                changes.append(
                    {
                        "row": r,
                        "col": c,
                        "input_color": int(input_grid[r, c]),
                        "output_color": int(output_grid[r, c]),
                        "neighbors": get_neighbors(input_grid, r, c)
                    }
                )
    return changes

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = {}
    if row > 0:
        neighbors["up"] = int(grid[row - 1, col])
    if row < rows - 1:
        neighbors["down"] = int(grid[row + 1, col])
    if col > 0:
        neighbors["left"] = int(grid[row, col - 1])
    if col < cols - 1:
        neighbors["right"] = int(grid[row, col + 1])
    return neighbors

task = "6f8cd790"
examples = training_examples[task]

change_reports = []
for i, example in enumerate(examples):
     input_grid = np.array(example["input"])
     output_grid = np.array(example["output"])
     changes = describe_changes(input_grid, output_grid)
     change_reports.append(changes)

for i, changes in enumerate(change_reports):
   if len(changes) > 0:
        print(f"Example {i+1} Changes:")
        for change in changes:
            print(f"  Row: {change['row']}, Col: {change['col']}, Input: {change['input_color']}, Output: {change['output_color']}, Neighbors: {change['neighbors']}")
   else:
        print(f'Example {i+1}: No Changes')