def display_grid(grid, title="Grid"):
    """Displays a grid with row and column numbers."""
    grid = np.array(grid)
    num_rows, num_cols = grid.shape

    # Print column numbers
    print("   ", end="")
    for j in range(num_cols):
        print(f"{j:2d}", end=" ")
    print()

    # Print separator
    print("   " + "--" * num_cols)

    # Print rows with row numbers
    for i in range(num_rows):
        print(f"{i:2d}|", end="")
        for j in range(num_cols):
            print(f"{grid[i, j]:2d}", end=" ")
        print()