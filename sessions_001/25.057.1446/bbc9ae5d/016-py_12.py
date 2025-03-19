import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    gray_length = 0
    for pixel in input_grid[0]:  # Check the FIRST row only
        if pixel == 5:
            gray_length += 1
        else:
            break

    print(f"Input Dimensions: {input_height} x {input_width}")
    print(f"Output Dimensions: {output_height} x {output_width}")
    print(f"Initial Gray Region Length (first row): {gray_length}")
    print(f"Output Height - Input Height: {output_height - input_height}")
    print(f"Gray Length + Input Height - 1 = {gray_length + input_height -1}")
    print("Input grid:")
    print(input_grid)
    print("Output grid:")
    print(output_grid)
    print("-" * 20)
    return gray_length, input_height, input_width, output_height, output_width


examples = [
    ([[5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
     [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0],
     [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
     [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0],
     [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
     [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),

    ([[5, 5, 5, 5, 0, 0, 0, 0, 0]],
     [[5, 5, 5, 5, 0, 0, 0, 0, 0],
      [5, 5, 5, 5, 5, 0, 0, 0, 0],
      [5, 5, 5, 5, 5, 5, 0, 0, 0],
      [5, 5, 5, 5, 5, 5, 5, 0, 0]]),

    ([[5, 5, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0]],
     [[5, 5, 0, 0, 0, 0, 0, 0, 0],
      [5, 5, 5, 0, 0, 0, 0, 0, 0],
      [5, 5, 5, 5, 0, 0, 0, 0, 0]]),

     ([[5,0,0,0,0,0,0,0,0]],
      [[5, 0, 0, 0, 0, 0, 0, 0, 0],
       [5, 5, 0, 0, 0, 0, 0, 0, 0],
       [5, 5, 5, 0, 0, 0, 0, 0, 0]
      ])
]

results = []
for inp, out in examples:
  results.append(analyze_example(inp,out))