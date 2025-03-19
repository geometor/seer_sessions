import numpy as np

#Helper functions from previous runs
def get_objects(grid, color=None):
    """Identifies contiguous objects of the specified color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        """Depth-First Search to find contiguous pixels of the same color."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or (color is not None and grid[row, col] != color)
        ):
            return

        visited[row, col] = True
        current_object.append((row, col))

        # Explore adjacent pixels
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and (color is None or grid[row, col] == color):
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_bounding_box(objects):
    """Calculates the bounding box for a list of objects."""
    if not objects:
        return None

    min_row = min(pixel[0] for obj in objects for pixel in obj)
    max_row = max(pixel[0] for obj in objects for pixel in obj)
    min_col = min(pixel[1] for obj in objects for pixel in obj)
    max_col = max(pixel[1] for obj in objects for pixel in obj)

    return (min_row, min_col, max_row, max_col)

def transform(grid):
    """
    Identifies red objects and creates a minimum bounding box
    """
    red_objects = get_objects(grid, 2)
    bounding_box = get_bounding_box(red_objects)
    
    if bounding_box is None:
        return np.zeros((1, 1), dtype=int)
        
    min_row, min_col, max_row, max_col = bounding_box
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)
    
    for obj in red_objects:
        for row, col in obj:
            output_grid[row-min_row,col-min_col] = 2

    return output_grid
#Provided test code:
def analyze_results(task_examples):
    results = []
    for example in task_examples:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)

        # Input Analysis
        input_red_objects = get_objects(input_grid, 2)
        num_input_red_objects = len(input_red_objects)
        
        #count output colors
        unique_colors_predicted = np.unique(predicted_output_grid)
        unique_colors_expected = np.unique(expected_output_grid)


        # Expected Output Analysis
        expected_red_pixels = np.where(expected_output_grid == 2)
        num_expected_red_pixels = len(expected_red_pixels[0])
        
        if(num_expected_red_pixels > 0):
            expected_red_object = list(zip(expected_red_pixels[0], expected_red_pixels[1]))
            expected_bounding_box = get_bounding_box([expected_red_object])
        else:
            expected_bounding_box = None

        # Predicted Output Analysis (Current Code)
        
        predicted_red_pixels = np.where(predicted_output_grid == 2)
        num_predicted_red_pixels = len(predicted_red_pixels[0])
        if(num_predicted_red_pixels > 0):
            predicted_red_object = list(zip(predicted_red_pixels[0], predicted_red_pixels[1]))
            predicted_bounding_box = get_bounding_box([predicted_red_object])
        else:
            predicted_bounding_box = None

        results.append({
            'num_input_red_objects': num_input_red_objects,
            'num_expected_red_pixels': num_expected_red_pixels,
            'expected_bounding_box': expected_bounding_box,
            'num_predicted_red_pixels': num_predicted_red_pixels,
            'predicted_bounding_box': predicted_bounding_box,
            'predicted_colors': unique_colors_predicted,
            'expected_colors': unique_colors_expected
        })
    return results

# Assuming 'train' contains the training examples
# task_examples = train
# analysis_results = analyze_results(task_examples)
# print(analysis_results)

#Example use - will be commented after one run.
task_examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2], [2, 2]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2, 2], [2, 2, 2], [2, 2, 2]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2, 2, 2]]}
]
analysis_results = analyze_results(task_examples)
print(analysis_results)