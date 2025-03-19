def analyze_color_changes(input_grid, output_grid):
    """
    Analyzes and reports color changes between input and output grids.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows, cols = input_grid.shape
    color_changes = {}
    
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid[r,c]
            output_color = output_grid[r,c]
            
            if input_color != output_color:
                if (input_color, output_color) not in color_changes:
                    color_changes[(input_color, output_color)] = 0
                color_changes[(input_color, output_color)] += 1
    print("Color Changes Report")
    for change, count in color_changes.items():
        print(f"  From {change[0]} to {change[1]}: {count} changes")
    return color_changes
    
# --- Example Usage ---
# input_grid, output_grid = example_data
# color_changes = analyze_color_changes(input_grid, output_grid)