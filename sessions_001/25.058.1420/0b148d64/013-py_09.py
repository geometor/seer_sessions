import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    print(f"Input shape: {input_grid.shape}")
    print(f"Output shape: {output_grid.shape}")

    unique_input_colors = np.unique(input_grid)
    unique_output_colors = np.unique(output_grid)
    print(f"Input colors: {unique_input_colors}")
    print(f"Output colors: {unique_output_colors}")

    #check context of green
    green_objects = find_object_with_context(input_grid, 3)
    for obj in green_objects:
      print(f"  Green object: {obj}")
      min_row, max_row, min_col, max_col = obj['bounding_box']

      #check for white surrounding the bounding box
      white_context = []
      for r in range(min_row-1, max_row+2):
        for c in range(min_col-1, max_col+2):
          if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
            if (r,c) not in obj['coords']:
              if input_grid[r,c] == 0: #white
                white_context.append((r,c))
      print(f"  White Context: {white_context}")

      #check for red around white
      red_context = []
      if len(white_context) > 0:
        w_rows, w_cols = zip(*white_context)
        min_w_row, max_w_row = min(w_rows), max(w_rows)
        min_w_col, max_w_col = min(w_cols), max(w_cols)
        for r in range(min_w_row-1, max_w_row+2):
          for c in range(min_w_col-1, max_w_col+2):
            if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
              if (r,c) not in white_context and (r,c) not in obj['coords']:
                if input_grid[r,c] == 2:
                  red_context.append((r,c))
        print(f"  Red Context: {red_context}")

example_pairs = [
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 2, 0, 3, 3, 3, 3, 0, 2, 0],
        [0, 2, 0, 3, 3, 3, 3, 0, 2, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 3, 3, 3, 3, 0, 2],
        [2, 0, 3, 3, 3, 3, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2]
    ]),
   ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 3, 3, 0, 3, 3, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 3, 3, 0, 3, 3, 2],
        [2, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2]
    ]),
    ([
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2],
        [2, 2, 2, 2, 0, 3, 3, 0, 2, 2, 2, 2],
        [2, 2, 2, 2, 0, 3, 3, 0, 2, 2, 2, 2],
        [2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ],
    [
        [0, 0, 0, 0],
        [0, 3, 3, 0],
        [0, 3, 3, 0],
        [0, 0, 0, 0]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [3, 3, 3, 3]
    ]),
    ([
        [3, 3, 0, 0, 0, 0, 0],
        [3, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [3, 3],
        [3, 3]
    ]),
    ([
      [3,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]
    ],
    [
      [3]
    ])
]

for i, (input_grid, output_grid) in enumerate(example_pairs):
  print(f"Example {i+1}:")
  analyze_example(input_grid, output_grid)
  print("-" * 20)