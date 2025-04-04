import numpy as np

def analyze_example(input_grid, output_grid):
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    print("Input Objects:", input_objects)
    print("Output Objects:", output_objects)
    print("Input grid shape:", input_grid.shape)
    print("Output grid shape:", output_grid.shape)

    if 2 in input_objects:
        red_input = input_objects[2]
        red_input_height = red_input['max_row'] - red_input['min_row'] + 1
        red_input_width = red_input['max_col'] - red_input['min_col'] + 1
        print("Red Input Height:", red_input_height)
        print("Red Input Width:", red_input_width)

    if 2 in output_objects:
      red_output = output_objects[2]
      red_output_height = red_output['max_row'] - red_output['min_row'] + 1
      red_output_width = red_output['max_col'] - red_output['min_col'] + 1
      print("Red Output Height:", red_output_height)
      print("Red Output Width:", red_output_width)
    print("---")

# Example grids (replace with actual data from the task)
example_grids = [
    (np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 2, 2],
               [0, 0, 0, 0, 2, 2],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]]),
     np.array([[2, 2],
               [2, 2]])),

    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 5, 5, 5, 5, 0],
               [0, 5, 0, 0, 0, 0, 0, 0],
               [0, 5, 0, 0, 2, 2, 0, 0],
               [0, 5, 0, 0, 2, 2, 0, 0],
               [0, 5, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 5, 5, 5, 5, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[2, 2],
               [2, 2]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 2, 2, 0, 0, 0, 0],
             [0, 0, 0, 2, 2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 7, 7, 0],
             [0, 0, 0, 0, 0, 0, 7, 7, 0],
             [0, 0, 0, 0, 0, 0, 7, 7, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2],
              ])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 6, 6, 6, 6, 6, 0],
              [0, 6, 6, 6, 6, 6, 0],
              [0, 6, 6, 2, 6, 6, 0],
              [0, 6, 6, 6, 6, 6, 0],
              [0, 6, 6, 6, 6, 6, 0],
              [0, 0, 0, 0, 0, 0, 0]]),
    np.array([[2]]))
]

for input_grid, output_grid in example_grids:
    analyze_example(input_grid, output_grid)