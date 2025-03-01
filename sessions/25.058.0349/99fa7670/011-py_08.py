import numpy as np

# Example data (replace with actual data from the task)
input_grid2 = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1]
])
output_grid2 = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1]
])

input_grid1 = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])
output_grid1 = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1]
])

input_grid3 = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2]
])
output_grid3 = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2]
])

def analyze_example(input_grid, output_grid):
    changed_pixels = []
    rows, cols = input_grid.shape
    source_color = None
    source_coords = None

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != output_grid[r, c]:
                changed_pixels.append(((r, c), output_grid[r, c]))

    # in this specific task, it appears a single pixel is the source
    for r in range(rows):
      for c in range(cols):
        if (input_grid[r,c] != 0) and all(input_grid[r,c] == pixel[1] for pixel in changed_pixels):
            source_color = input_grid[r,c]
            source_coords = (r,c)
            break
      if source_color is not None:
        break

    return changed_pixels, source_color, source_coords

changed_pixels1, source_color1, source_coords1 = analyze_example(input_grid1, output_grid1)
print(f"Example 1:\nChanged Pixels: {changed_pixels1}\nSource Color: {source_color1}\nSource Coords: {source_coords1}\n")

changed_pixels2, source_color2, source_coords2 = analyze_example(input_grid2, output_grid2)
print(f"Example 2:\nChanged Pixels: {changed_pixels2}\nSource Color: {source_color2}\nSource Coords: {source_coords2}\n")

changed_pixels3, source_color3, source_coords3 = analyze_example(input_grid3, output_grid3)
print(f"Example 3:\nChanged Pixels: {changed_pixels3}\nSource Color: {source_color3}\nSource Coords: {source_coords3}\n")