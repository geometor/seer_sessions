def analyze_adjacency(input_grid, output_grid):
    """
    Analyzes how adjacency relationships change between input and output.
    Focuses on pixels of different colors.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows, cols = input_grid.shape

    def get_neighbors(grid, r, c):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (dr == 0 and dc == 0) or not (0 <= r + dr < rows and 0 <= c + dc < cols):
                    continue
                neighbors.append((r + dr, c + dc, grid[r + dr, c + dc]))
        return neighbors

    print("Adjacency Changes:")
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid[r, c]
            input_neighbors = get_neighbors(input_grid, r, c)

            # Find this pixel's location(s) in the output
            output_locations = np.argwhere(output_grid == input_color)
            for out_r, out_c in output_locations:
                output_neighbors = get_neighbors(output_grid, out_r, out_c)
                
                # Compare neighbors (focus on different colors)
                print(f"Pixel at ({r}, {c}) [Color {input_color}] moved to ({out_r}, {out_c}):")

                input_neighbor_colors = {n[2] for n in input_neighbors if n[2] != input_color}
                output_neighbor_colors = {n[2] for n in output_neighbors if n[2] != input_color}

                new_neighbors = output_neighbor_colors - input_neighbor_colors
                lost_neighbors = input_neighbor_colors - output_neighbor_colors

                if new_neighbors:
                    print(f"  Gained neighbors of color(s): {new_neighbors}")
                if lost_neighbors:
                    print(f"  Lost neighbors of color(s): {lost_neighbors}")


# --- Example Usage ---
# input_grid, output_grid = example_data
# analyze_adjacency(input_grid, output_grid)