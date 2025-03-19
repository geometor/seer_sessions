def find_vertical_lines(grid, color=5):
    """Finds vertical lines of a specified color in the grid."""
    lines = []
    rows, cols = grid.shape
    for c in range(cols):
        start = -1
        for r in range(rows):
            if grid[r, c] == color:
                if start == -1:
                    start = r
            elif start != -1:
                lines.append((start, r - 1, c))
                start = -1
        if start != -1:
            lines.append((start, rows - 1, c))
    return lines

example_grids = task_data["train"]

# store line information
line_data = []

for i, eg in enumerate(example_grids):
    input_grid = np.array(eg['input'])
    output_grid = np.array(eg['output'])
    lines = find_vertical_lines(input_grid)

    # determine if the transformed lines are in the output
    output_lines = find_vertical_lines(output_grid, 1) + \
                   find_vertical_lines(output_grid, 2) + \
                   find_vertical_lines(output_grid, 4)
    line_data.append(
        {
            'example': i,
            'input_lines': lines,
            'output_lines': output_lines,
        }
    )

for item in line_data:
    print(item)
