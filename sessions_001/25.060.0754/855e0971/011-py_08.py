import numpy as np

def analyze_grid(grid):
    """Analyzes the grid for white and red pixel positions and states."""
    white_pixels = []
    red_pixels_before = []
    red_pixels_after = []

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0:
                white_pixels.append((r, c))
            elif grid[r,c] == 2:
                red_pixels_before.append((r,c))

    return {
        "white_pixels": white_pixels,
        "red_pixels_before": red_pixels_before,

    }

def compare_io(input, output):
    input_analysis = analyze_grid(input)
    output_analysis = analyze_grid(output)

    print("Input:")
    print(input)
    print(f"  White Pixels: {input_analysis['white_pixels']}")
    print(f"  Red Pixels  : {input_analysis['red_pixels_before']}")
    print("Output:")
    print(output)
    print(f"  White Pixels: {output_analysis['white_pixels']}")
    print(f"  Red Pixels  : {output_analysis['red_pixels_before']}")

    return

#Example Usage (substitute with actual input/output grids later)

#input_grid = np.array([[1,0], [2,3]])
#output_grid = np.array([[0,0],[0,3]])
#compare_io(input_grid, output_grid)
