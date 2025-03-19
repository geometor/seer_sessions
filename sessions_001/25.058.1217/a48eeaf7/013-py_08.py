import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    center_r, center_c = rows // 2, cols // 2
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return {
        'shape': (rows, cols),
        'center': (center_r, center_c),
        'colors': color_counts
    }

def find_red_square(grid):
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 2 and grid[r+1, c] == 2 and grid[r, c+1] == 2 and grid[r+1, c+1] == 2:
                return (r, c)
    return None

def find_gray_pixels(grid):
    return np.argwhere(grid == 5)

def analyze_example(input_grid, output_grid, predicted_output_grid):
    input_desc = describe_grid(input_grid)
    output_desc = describe_grid(output_grid)
    predicted_output_desc = describe_grid(predicted_output_grid)

    red_square_input = find_red_square(input_grid)
    gray_pixels_input = find_gray_pixels(input_grid)
    
    correct = np.array_equal(output_grid,predicted_output_grid)

    return {
        'input': input_desc,
        'output': output_desc,
        'predicted_output': predicted_output_desc,
        'red_square_input': red_square_input,
        'gray_pixels_input': gray_pixels_input.tolist() if gray_pixels_input.size > 0 else [],
        'correct' : correct
    }

# Provided examples
train_input_0 = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,5,0,0],[0,0,0,0,0,0,0,0,0]])
train_output_0 = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,5,0,0]])

train_input_1 = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,5,0,0]])
train_output_1 = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,5,0,0]])

train_input_2 = np.array([[0,0,0,0,0,0,0,0,0],[0,5,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
train_output_2 = np.array([[0,0,0,0,0,0,0,0,0],[0,5,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])

train_input_3 = np.array([[5,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,5],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
train_output_3 = np.array([[5,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,5]])

train_input_4 = np.array([[5,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
train_output_4 = np.array([[5,0,0,0,0,0,0,0,5],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,2,2,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])

train_inputs = [train_input_0, train_input_1, train_input_2, train_input_3, train_input_4]
train_outputs = [train_output_0, train_output_1, train_output_2, train_output_3, train_output_4]

predicted_outputs = []
for i in train_inputs:
    predicted_outputs.append(transform(i))

results = []
for i in range(len(train_inputs)):
    results.append(analyze_example(train_inputs[i], train_outputs[i], predicted_outputs[i]))

for i, r in enumerate(results):
    print(f"Example {i}:")
    print(r)