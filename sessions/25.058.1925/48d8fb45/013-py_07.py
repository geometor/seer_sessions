import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    print("Input Grid:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)

    yellow_regions_input = get_regions(input_grid, 4)
    gray_regions_input = get_regions(input_grid, 5)

    print(f"Number of Yellow Regions (Input): {len(yellow_regions_input)}")
    print(f"Number of Gray Regions (Input): {len(gray_regions_input)}")

    if len(yellow_regions_input) == 1:
        min_row, max_row, min_col, max_col = get_bounding_box(input_grid, 4)
        print(f"Yellow Bounding Box (Input): ({min_row}, {min_col}) to ({max_row}, {max_col})")
        #count grey inside yellow box
        subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]
        gray_inside = np.count_nonzero(subgrid == 5)
        print(f"Gray Pixels Inside Yellow Bounding Box: {gray_inside}")

    if expected_output.size > 0:
       expected_yellow = np.count_nonzero(expected_output == 4)
       expected_gray = np.count_nonzero(expected_output == 5)
       print("expected yellow", expected_yellow)
       print("expected gray", expected_gray)

    if actual_output.size > 0:
       actual_yellow = np.count_nonzero(actual_output == 4)
       actual_gray = np.count_nonzero(actual_output == 5)
       print("actual yellow", actual_yellow)
       print("actual gray", actual_gray)



examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 4, 4, 4, 0],
         [0, 0, 0, 4, 5, 4, 0],
         [0, 0, 0, 4, 4, 4, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]],
        [[4, 4, 4],
         [4, 5, 4],
         [4, 4, 4]],
        [[4, 4, 4],
         [4, 5, 4],
         [4, 4, 4]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 4, 4, 4, 0, 0],
         [0, 0, 4, 5, 5, 5, 4, 0],
         [0, 0, 0, 4, 4, 4, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
        [[4, 4, 4],
         [5, 5, 5],
         [4, 4, 4]],
       [[4, 4, 4, 0, 0],
        [4, 5, 5, 5, 4],
        [0, 4, 4, 4, 0]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 4, 4, 0, 0, 0],
        [0, 0, 4, 5, 5, 5, 4, 0, 0],
        [0, 0, 0, 4, 4, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]],
       [[4, 4, 4],
        [5, 5, 5],
        [4, 4, 4]],
       [[4, 4, 4, 0, 0, 0],
        [4, 5, 5, 5, 4, 0],
        [0, 4, 4, 4, 0, 0]]
    ),
    (
      [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
       [0, 0, 0, 4, 5, 5, 5, 4, 0, 0],
       [0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      [[4, 4, 4, 0, 0],
       [5, 5, 5, 4, 0],
       [4, 4, 4, 0, 0]],
      [[4, 4, 4, 0, 0, 0],
       [4, 5, 5, 5, 4, 0],
       [0, 4, 4, 4, 0, 0]]
    ),
    (
      [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 4, 5, 5, 5, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      [[4, 4, 4],
       [5, 5, 5],
       [4, 4, 4]],
      [[4, 4, 4, 0, 0, 0, 0, 0],
       [4, 5, 5, 5, 4, 0, 0, 0],
       [0, 4, 4, 4, 0, 0, 0, 0]]
    )
]

for input_grid, expected_output, actual_output in examples:
    analyze_example(input_grid, expected_output, actual_output)
    print("-" * 30)
