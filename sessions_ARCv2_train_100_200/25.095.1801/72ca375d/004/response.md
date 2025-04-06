**General Assessment:**

The initial code (`code_00.py` based on the second provided logic: min unique digits -> min density diff -> max area) successfully solved Examples 1 and 3 but failed on Example 2 according to the provided results. However, a manual walkthrough of that code's logic suggests it *should* have selected the correct object (Object 6) for Example 2. There appears to be a discrepancy between the reported execution result for Example 2 (`7`) and the expected behavior of the provided `code_00.py`.

Assuming the *expected outputs* for all examples are the ground truth, the previous hypotheses (max density -> max area; min unique digits -> min density diff -> max area) are incorrect as they fail on at least one example when checked against the expected outputs.

A new hypothesis is needed. By analyzing the relationship between the input objects and the expected output object across all three examples, a pattern emerges: the selected object consistently corresponds to the *median* digit value among all unique object digits present in the input grid.

**Strategy:**

1.  Identify all distinct connected non-zero objects and their corresponding digit values.
2.  Determine the unique set of these digit values.
3.  Calculate the median of this unique set of digits.
4.  Select the object whose digit matches the calculated median.
5.  Extract the bounding box of this selected object as the output.

This strategy successfully explains all three training examples.

**Metrics:**

``` python
import numpy as np
from collections import deque

# --- Helper functions ---
def _find_objects(grid: np.ndarray) -> list[dict]:
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                digit = grid[r, c]
                object_cells = []
                q = deque([(r, c)])
                visited.add((r, c)) # Mark starting cell visited
                while q:
                    curr_r, curr_c = q.popleft()
                    object_cells.append((curr_r, curr_c))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == digit and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                if object_cells:
                    rows_obj = [row for row, col in object_cells]
                    cols_obj = [col for row, col in object_cells]
                    min_row, max_row = min(rows_obj), max(rows_obj)
                    min_col, max_col = min(cols_obj), max(cols_obj)
                    bbox_subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]
                    objects.append({
                        'digit': digit, 
                        'cell_count': len(object_cells),
                        'bbox': [min_row, max_row, min_col, max_col],
                        'bbox_area': (max_row - min_row + 1) * (max_col - min_col + 1),
                        'unique_digits_in_bbox': len(np.unique(bbox_subgrid))
                    })
    return objects

def calculate_median(digits: list[int]) -> float | int | None:
    n = len(digits)
    if n == 0: return None
    sorted_digits = sorted(digits)
    mid = n // 2
    if n % 2 == 1: return sorted_digits[mid]
    else: return (sorted_digits[mid - 1] + sorted_digits[mid]) / 2

# --- Example Data ---
inputs = [
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,4,4,0,0,0,0,0,0],[0,0,4,4,0,0,8,8,8,0],[0,0,0,0,0,0,8,0,8,8],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,0,0,0,0],[0,2,2,2,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]], dtype=int),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,2,2,0,0,0,0,0,0,0],[0,0,2,2,2,0,0,7,7,0],[0,0,0,0,0,0,7,0,7,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,6,6,6,6,0,0,0],[0,0,0,0,6,6,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]], dtype=int),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,3,3,0,0,0,0,0,0,0],[0,0,3,0,0,5,0,0,5,0],[0,0,3,0,0,5,5,5,5,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,8,8,8,0,0,0,0],[8,8,8,8,0,8,8,0,0,0],[0,0,0,0,0,0,0,0,0,0]], dtype=int)
]
expected_outputs = [
    [[4, 4], [4, 4]],
    [[6, 6, 6, 6], [0, 6, 6, 0]],
    [[5, 0, 0, 5], [5, 5, 5, 5]]
]

# --- Calculations & Report ---
print("Example Analysis:")
for i, grid in enumerate(inputs):
    print(f"\n--- Example {i+1} ---")
    objects = _find_objects(grid)
    unique_digits = sorted(list(set(obj['digit'] for obj in objects)))
    median_digit = calculate_median(unique_digits)
    print(f"  Objects Found: {len(objects)}")
    print(f"  Unique Object Digits: {unique_digits}")
    print(f"  Median Digit: {median_digit}")
    
    selected_object = None
    for obj in objects:
        obj['density'] = obj['cell_count'] / obj['bbox_area'] if obj['bbox_area'] > 0 else 0
        print(f"    - Object Digit: {obj['digit']}, Cells: {obj['cell_count']}, BBox: {obj['bbox']}, Area: {obj['bbox_area']}, Density: {obj['density']:.3f}, UniqueDigitsInBox: {obj['unique_digits_in_bbox']}")
        if obj['digit'] == median_digit:
            selected_object = obj
            
    print(f"  Selected Object Digit (based on median): {selected_object['digit'] if selected_object else 'None'}")
    
    # Verify selected object's bounding box matches expected output shape
    if selected_object:
        min_r, max_r, min_c, max_c = selected_object['bbox']
        output_shape = (max_r - min_r + 1, max_c - min_c + 1)
        expected_shape = (len(expected_outputs[i]), len(expected_outputs[i][0]))
        print(f"  Selected Object BBox Shape: {output_shape}")
        print(f"  Expected Output Shape: {expected_shape}")
        print(f"  Shape Match: {output_shape == expected_shape}")
    else:
        print("  No object selected based on median digit.")


```
```
Example Analysis:

--- Example 1 ---
  Objects Found: 3
  Unique Object Digits: [np.int64(2), np.int64(4), np.int64(8)]
  Median Digit: 4
    - Object Digit: 4, Cells: 4, BBox: [1, 2, 2, 3], Area: 4, Density: 1.000, UniqueDigitsInBox: 1
    - Object Digit: 8, Cells: 6, BBox: [2, 3, 6, 9], Area: 8, Density: 0.750, UniqueDigitsInBox: 2
    - Object Digit: 2, Cells: 7, BBox: [7, 8, 1, 5], Area: 10, Density: 0.700, UniqueDigitsInBox: 2
  Selected Object Digit (based on median): 4
  Selected Object BBox Shape: (2, 2)
  Expected Output Shape: (2, 2)
  Shape Match: True

--- Example 2 ---
  Objects Found: 4
  Unique Object Digits: [np.int64(2), np.int64(6), np.int64(7)]
  Median Digit: 6
    - Object Digit: 2, Cells: 5, BBox: [1, 2, 1, 4], Area: 8, Density: 0.625, UniqueDigitsInBox: 2
    - Object Digit: 7, Cells: 3, BBox: [2, 3, 7, 8], Area: 4, Density: 0.750, UniqueDigitsInBox: 2
    - Object Digit: 7, Cells: 1, BBox: [3, 3, 6, 6], Area: 1, Density: 1.000, UniqueDigitsInBox: 1
    - Object Digit: 6, Cells: 6, BBox: [6, 7, 3, 6], Area: 8, Density: 0.750, UniqueDigitsInBox: 2
  Selected Object Digit (based on median): 6
  Selected Object BBox Shape: (2, 4)
  Expected Output Shape: (2, 4)
  Shape Match: True

--- Example 3 ---
  Objects Found: 3
  Unique Object Digits: [np.int64(3), np.int64(5), np.int64(8)]
  Median Digit: 5
    - Object Digit: 3, Cells: 4, BBox: [1, 3, 1, 2], Area: 6, Density: 0.667, UniqueDigitsInBox: 2
    - Object Digit: 5, Cells: 6, BBox: [2, 3, 5, 8], Area: 8, Density: 0.750, UniqueDigitsInBox: 2
    - Object Digit: 8, Cells: 9, BBox: [7, 8, 0, 6], Area: 14, Density: 0.643, UniqueDigitsInBox: 2
  Selected Object Digit (based on median): 5
  Selected Object BBox Shape: (2, 4)
  Expected Output Shape: (2, 4)
  Shape Match: True

```
**YAML Facts:**


```yaml
task_elements:
  - element: input_grid
    description: A 10x10 grid of single digits (0-9).
    properties:
      - dimensions: [10, 10]
      - background_digit: 0
      - contains: non_zero_objects
  - element: non_zero_objects
    description: Connected components of identical non-zero digits.
    properties:
      - digit_value: The digit making up the object (1-9).
      - cells: List of coordinates [(row, col), ...] occupied by the object.
      - bounding_box: The smallest rectangle containing all object cells [min_row, max_row, min_col, max_col].
  - element: unique_object_digits
    description: The set of unique digit values present across all non_zero_objects in the input grid.
    properties:
      - count: Number of unique digits.
      - values: List of the unique digits.
  - element: median_digit
    description: The median value calculated from the sorted list of unique_object_digits.
    constraints:
      - Assumes an odd number of unique_object_digits based on examples.
  - element: selected_object
    description: The non_zero_object whose digit_value matches the median_digit.
    constraints:
      - Assumes only one object will match the median_digit based on examples.
  - element: output_grid
    description: A rectangular subgrid extracted from the input grid.
    properties:
      - content: Matches the content within the bounding_box of the selected_object.
      - dimensions: Determined by the bounding box size of the selected_object.

transformation:
  input: input_grid
  output: output_grid
  steps:
    - action: identify_objects
      description: Find all distinct connected non-zero objects and their digit values in the input grid.
      input: input_grid
      output: list_of_objects
    - action: find_unique_digits
      description: Create a sorted list of unique digit values from all identified objects.
      input: list_of_objects
      output: unique_object_digits_list
    - action: calculate_median_digit
      description: Calculate the median value from the unique_object_digits_list.
      input: unique_object_digits_list
      output: median_digit_value
    - action: select_object_by_median
      description: Identify the object from list_of_objects whose digit_value equals the median_digit_value.
      input: list_of_objects, median_digit_value
      output: selected_object
    - action: determine_bounding_box
      description: Find the bounding box coordinates of the selected_object.
      input: selected_object
      output: bounding_box_coords
    - action: extract_subgrid
      description: Extract the subgrid from the input_grid corresponding to the bounding_box_coords.
      input: input_grid, bounding_box_coords
      output: output_grid

relationships:
  - The output_grid's content and dimensions are determined by the bounding_box of the selected_object.
  - The selected_object is chosen based on its digit_value matching the median of all unique object digit values in the input grid.
```


**Natural Language Program:**

1.  Identify all distinct connected groups (objects) of the same non-zero digit within the input grid.
2.  Create a list containing the unique digit value associated with each distinct object found.
3.  Sort this list of unique digit values in ascending order.
4.  Determine the median value from this sorted list. (For a list with an odd number of elements, this is the middle element).
5.  Find the specific object identified in step 1 whose digit value is equal to the calculated median value.
6.  Determine the bounding box (minimum and maximum row and column indices) of this selected object.
7.  Extract the rectangular subgrid from the original input grid defined by this bounding box. This subgrid is the final output.