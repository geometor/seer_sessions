def assess_transformation(grid, transformed_grid):
    """
    Detailed assessment of the transformation applied to a single grid.
    """
    changes = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != transformed_grid[i, j]:
                changes.append({
                    "row": i,
                    "col": j,
                    "from": int(grid[i, j]),
                    "to": int(transformed_grid[i, j]),
                    "grid_value": int(grid[i,j]),
                    "transformed_value": int(transformed_grid[i, j]),
                })

    if not changes:
        return "No changes detected."
    
    return changes