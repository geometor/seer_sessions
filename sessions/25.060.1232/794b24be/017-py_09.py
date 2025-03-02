import numpy as np

def analyze_grid_pairs(input_grid, output_grid):
    """Analyzes input and output grids to find differences and relationships."""

    input_blue_pixels = np.argwhere(input_grid == 1)
    output_red_pixels = np.argwhere(output_grid == 2)

    print("Input Blue Pixels:")
    if input_blue_pixels.size > 0:
        for pixel in input_blue_pixels:
            print(f"  - Row: {pixel[0]}, Col: {pixel[1]}")
    else:
        print("  - None")

    print("Output Red Pixels:")
    if output_red_pixels.size > 0:
        for pixel in output_red_pixels:
            print(f"  - Row: {pixel[0]}, Col: {pixel[1]}")
    else:
        print("  - None")
    
    # additional information - other colors that are the same
    input_other = []
    output_other = []
    
    for color in range(10):
        if color != 1 and color != 2:  # exclude blue and red
            input_coords = np.argwhere(input_grid == color)
            output_coords = np.argwhere(output_grid == color)
            if not np.array_equal(input_coords, output_coords):
                print(f"color {color} not equal")
            else:
                if input_coords.size > 0:
                    input_other.append(color)
                    output_other.append(color)

    print(f"other input colors present {input_other}")
    print(f"other output colors present {output_other}")



task_examples = [
    (np.array([[0, 0, 0, 0, 0, 0],
               [0, 5, 5, 5, 5, 0],
               [0, 5, 5, 1, 5, 0],
               [0, 5, 5, 5, 5, 0],
               [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
               [0, 5, 5, 5, 5, 0],
               [0, 5, 5, 2, 2, 0],
               [0, 5, 5, 5, 5, 0],
               [0, 0, 0, 0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 2, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]])),
     (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 2, 2],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1]]),
     np.array([[0, 0, 2, 2, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]))
]

for i, (input_grid, output_grid) in enumerate(task_examples):
    print(f"Example {i + 1}:")
    analyze_grid_pairs(input_grid, output_grid)
    print("-" * 20)