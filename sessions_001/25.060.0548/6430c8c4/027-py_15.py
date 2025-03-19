def analyze_example(input_grid, output_grid):
    input_colors = set(input_grid.flatten())
    output_colors = set(output_grid.flatten())
    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")

    # Find connected components (shapes) in input
    def find_shapes(grid):
        visited = set()
        shapes = []

        def dfs(r, c, color, shape_coords):
            if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
                return
            visited.add((r, c))
            shape_coords.append((r, c))
            dfs(r + 1, c, color, shape_coords)
            dfs(r - 1, c, color, shape_coords)
            dfs(r, c + 1, color, shape_coords)
            dfs(r, c - 1, color, shape_coords)

        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if (r, c) not in visited:
                    color = grid[r, c]
                    if color != 0:  # Ignore background
                        shape_coords = []
                        dfs(r, c, color, shape_coords)
                        shapes.append((color, shape_coords))
        return shapes

    input_shapes = find_shapes(input_grid)
    output_shapes = find_shapes(output_grid)

    print(f"Input Shapes: {input_shapes}")
    print(f"Output Shapes: {output_shapes}")

    # rudimentary shape matching based on color and count - needs to be more intelligent
    for color, coords in input_shapes:
        if color in [c for c, _ in output_shapes]:
            print(f"Possible shape transformation: color {color} in input might be related to color {color} in output")
        else:
            print(f"Color {color} in input does NOT have a direct match")


example_inputs = task_state["train_inputs"]
example_outputs = task_state["train_outputs"]

for i in range(len(example_inputs)):
    print(f"--- Example {i+1} ---")
    analyze_example(np.array(example_inputs[i]), np.array(example_outputs[i]))
