import numpy as np

def check_examples(examples):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        # --- Metrics ---
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)

        # 1. Check column 4 (index 3) for all blue
        column_4_all_blue = np.all(input_grid[:, 3] == 1) if input_grid.shape[1] > 3 else False

        # 2. check output color
        output_color = expected_output[0,0]
        
        # 3. Check for green output
        is_output_green = np.all(expected_output == 3)

        results.append({
            "example_index": i,
            "column_4_all_blue": column_4_all_blue,
            "output_color": output_color,
            "is_output_green": is_output_green,

        })
    return results
# Mock Example Data (replace with actual data)
examples = [
    (  # Example 0
        [[0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0]],
        [[3, 3, 3],
         [3, 3, 3],
         [3, 3, 3],
         [3, 3, 3]]
    ),
    (  # Example 1
      [[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]],
      [[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]]
    ),
    (  # Example 2
       [[0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0]],
       [[3, 3, 3],
        [3, 3, 3],
        [3, 3, 3],
        [3, 3, 3]]
    ),
        (  # Example 3
      [[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0]],
      [[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]]
    ),
       (  # Example 4
      [[0, 0, 0, 1, 0, 0],
       [0, 0, 0, 1, 0, 0],
       [0, 0, 0, 1, 0, 0],
       [0, 0, 0, 1, 0, 0]],
      [[3, 3, 3],
       [3, 3, 3],
       [3, 3, 3],
       [3, 3, 3]]
    ),

]
results = check_examples(examples)
for r in results:
    print(r)
