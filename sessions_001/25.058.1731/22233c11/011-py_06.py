import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    output_grid[1, 0] = 8
    output_grid[2, 0] = 8
    output_grid[7, 5] = 8
    output_grid[8, 5] = 8
    return output_grid

def analyze_example(input_grid, output_grid):
    transformed_grid = transform(input_grid)
    correct = np.array_equal(transformed_grid, output_grid)
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    if not correct:
      diff = transformed_grid != output_grid
      
    else:
        diff = None
    return {
        'input_shape': input_shape,
        'output_shape': output_shape,
        'correct': correct,
        'diff': diff,
    }
# dummy data for simulation
train_ex_input_1 = np.array([[1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1]])
train_ex_output_1 = np.array([[1, 1, 1, 1, 1, 1],
       [8, 1, 1, 1, 1, 1],
       [8, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 8],
       [1, 1, 1, 1, 1, 8],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1]])
train_ex_input_2 = np.array([[5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5]])
train_ex_output_2 = np.array([[8, 5, 5, 5, 5],
       [8, 5, 5, 5, 5],
       [5, 5, 5, 5, 5],
       [5, 5, 5, 5, 8],
       [5, 5, 5, 5, 8]])

train_ex_input_3 = np.array([[7, 7, 7],
       [7, 7, 7],
       [7, 7, 7],
       [7, 7, 7]])
train_ex_output_3 = np.array([[8, 7, 7],
       [8, 7, 7],
       [7, 7, 8],
       [7, 7, 8]])

examples = [
    (train_ex_input_1, train_ex_output_1),
    (train_ex_input_2, train_ex_output_2),
    (train_ex_input_3, train_ex_output_3)
    ]

results = [analyze_example(inp, outp) for inp, outp in examples]
for i, r in enumerate(results):
    print (f'example: {i + 1} input_shape: {r["input_shape"]}, output_shape: {r["output_shape"]}, correct: {r["correct"]}')
    if not r["correct"]:
      for row in range(r["diff"].shape[0]):
         for col in range(r["diff"].shape[1]):
            if r["diff"][row,col]:
               print(f'mismatch at: {row},{col}')
