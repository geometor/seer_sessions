import numpy as np

def get_grid_dimensions(grid):
    return grid.shape

def count_colors(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def find_color_locations(grid, color):
    return np.where(grid == color)

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    metrics = {}
    metrics['input_dimensions'] = get_grid_dimensions(input_grid)
    metrics['output_dimensions'] = get_grid_dimensions(output_grid)
    metrics['predicted_output_dimensions'] = get_grid_dimensions(predicted_output_grid)
    metrics['input_colors'] = count_colors(input_grid)
    metrics['output_colors'] = count_colors(output_grid)
    metrics['predicted_output_colors'] = count_colors(predicted_output_grid)

    # the current transform is not good enough - use a general comparison
    metrics['match'] = np.array_equal(output_grid,predicted_output_grid)
    # metrics['gray_column_input'] = find_color_locations(input_grid, 5)[1]
    # metrics['gray_column_output'] = find_color_locations(output_grid, 5)[1]
    # metrics['gray_column_predicted'] = find_color_locations(predicted_output_grid, 5)[1]

    return metrics

# Example Usage (replace with actual grids)
# Wrap in a function
def process_examples(examples, transform_function):
    results = []
    for i, example in enumerate(examples):
        input_grid = example['input']
        output_grid = example['output']
        predicted_output_grid = transform_function(input_grid)
        metrics = calculate_metrics(input_grid, output_grid, predicted_output_grid)
        results.append({'example_index': i, 'metrics': metrics})
    return results

# Paste the transform function.
import numpy as np

def transform(input_grid):
    # Duplicate Input Rows
    intermediate_grid = np.repeat(input_grid, 2, axis=0)

    # Find the column index with gray (5)
    gray_col_indices = np.where(input_grid == 5)[1]
    gray_col_index = gray_col_indices[0] if len(gray_col_indices) > 0 else -1

    # Expand and Duplicate Columns based on Gray
    output_grid_cols = []
    for col_idx in range(intermediate_grid.shape[1]):
        if col_idx == gray_col_index:
            output_grid_cols.append(intermediate_grid[:, col_idx])
            output_grid_cols.append(intermediate_grid[:, col_idx])
            output_grid_cols.append(intermediate_grid[:, col_idx])

        else:
            output_grid_cols.append(np.zeros(intermediate_grid.shape[0],dtype=int))
            output_grid_cols.append(intermediate_grid[:, col_idx])
            output_grid_cols.append(np.zeros(intermediate_grid.shape[0],dtype=int))

    intermediate_grid = np.column_stack(output_grid_cols)


    # remove the extra columns
    output_grid = intermediate_grid[:,1:intermediate_grid.shape[1]-1]


    # Add Azure Rows
    azure_row = np.array([8 if i % 2 == 0 else 0 for i in range(output_grid.shape[1])])
    output_grid = np.vstack([azure_row, output_grid, azure_row])

    return output_grid

# input_grid = np.array([[1, 2, 3], [4, 5, 6]])
# output_grid = np.array([[8, 0, 8, 0, 8, 0], [1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 3], [4, 4, 5, 5, 6, 6], [4, 4, 5, 5, 6, 6], [8, 0, 8, 0, 8, 0]])
# # predicted_output = transform(input_grid.copy())
# # result = process_examples(input_grid, output_grid, predicted_output)
# # print(result)
# Create a basic example to work with since real data is unavailable
examples = [
    {'input': np.array([[1, 2, 3], [4, 5, 6]]), 'output': np.array([[8, 0, 8, 0, 8, 0], [1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 3], [4, 4, 5, 5, 6, 6], [4, 4, 5, 5, 6, 6], [8, 0, 8, 0, 8, 0]])},
    {'input': np.array([[7, 5, 2], [9, 0, 1]]), 'output': np.array([[8, 0, 8, 0, 8], [7, 7, 5, 2, 2], [7, 7, 5, 2, 2], [9, 9, 0, 1, 1], [9, 9, 0, 1, 1], [8, 0, 8, 0, 8]])},
    {'input': np.array([[5, 4], [1, 8]]), 'output': np.array([[8, 0, 8], [5, 5, 4], [5, 5, 4], [1, 1, 8], [1, 1, 8], [8, 0, 8]])}

]
result = process_examples(examples, transform)
print(result)
