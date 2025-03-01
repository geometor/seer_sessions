# Conceptual Code (not executed here)
def analyze_grids(input_grid, output_grid):
    input_blue_segments = []
    output_magenta_segments = []

    rows, cols = input_grid.shape
    for r in range(rows):
        in_blue_segment = False
        start_col = -1
        for c in range(cols):
            if input_grid[r, c] == 1:  # Blue pixel
                if not in_blue_segment:
                    in_blue_segment = True
                    start_col = c
            elif in_blue_segment:
                input_blue_segments.append(((r, start_col), (r, c - 1)))
                in_blue_segment = False
        if in_blue_segment:
            input_blue_segments.append(((r, start_col), (r, cols - 1)))
            
    rows, cols = output_grid.shape
    for r in range(rows):
        in_magenta_segment = False
        start_col = -1
        for c in range(cols):
            if output_grid[r, c] == 6:  # magenta pixel
                if not in_magenta_segment:
                    in_magenta_segment = True
                    start_col = c
            elif in_magenta_segment:
                output_magenta_segments.append(((r, start_col), (r, c - 1)))
                in_magenta_segment = False
        if in_magenta_segment:
            output_magenta_segments.append(((r, start_col), (r, cols - 1)))            

    return input_blue_segments, output_magenta_segments

# Example usage (conceptual - results presented below)
# results = []
# for i in range(len(train)):
#   input_grid = train[i]['input']
#     output_grid = train[i]['output']
#     input_segments, output_segments = analyze_grids(input_grid, output_grid)
#    results.append((input_segments, output_segments))
#
# print(results)