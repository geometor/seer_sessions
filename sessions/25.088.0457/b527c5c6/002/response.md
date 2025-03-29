Okay, let's analyze the results and refine the transformation rule.

**General Assessment:**

The previous code failed on all training examples. The core issue appears to be the logic used to determine the *direction* of expansion for the identified objects. The initial hypothesis, based only on the first example, assumed the orientation of green neighbors (exclusively horizontal or vertical) determined the potential expansion axis, and an adjacent white pixel confirmed the specific direction (e.g., horizontal green neighbors + white pixel above -> expand Up).

However, examining the failed examples reveals that the red pixel often has *both* horizontal and vertical green neighbors. The `Transformed Output` in each case shows no expansion occurred, indicating the code failed to determine a valid `expansion_direction`.

The successful `Expected Output` grids suggest a simpler rule: the expansion direction is determined *solely* by the location of the single white (0) pixel directly adjacent (orthogonally) to the red (2) pixel. The green (3) pixels merely define the *shape* of the object to be expanded, along with the red pixel itself. The expansion then proceeds from each pixel of this shape in the determined direction, filling only white pixels until a non-white pixel or grid boundary is encountered.

**Gather Metrics:**

Let's confirm the adjacent white pixel rule for each example:


``` python
import numpy as np

def analyze_example(input_grid, expected_output_grid):
    input_np = np.array(input_grid)
    output_np = np.array(expected_output_grid)
    rows, cols = input_np.shape
    red_pixels = np.argwhere(input_np == 2)
    results = []

    for r, c in red_pixels:
        analysis = {
            "red_pixel_location": (r, c),
            "adjacent_pixels": {},
            "adjacent_white_locations": [],
            "expansion_direction_hypothesis": None
        }
        # Check neighbors
        for dr, dc, direction in [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                color = input_np[nr, nc]
                analysis["adjacent_pixels"][direction] = {"location": (nr, nc), "color": color}
                if color == 0: # White
                    analysis["adjacent_white_locations"].append(((nr, nc), direction))

        # Determine hypothesized direction
        if len(analysis["adjacent_white_locations"]) == 1:
             analysis["expansion_direction_hypothesis"] = analysis["adjacent_white_locations"][0][1]

        results.append(analysis)

    return results

# Example 1 Data
input1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,3,3,3,3,2,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,2,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0]
]
output1 = [
    [0,0,0,3,3,2,3,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,3,2,3,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,3,2,3,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,3,3,3,3,2,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0]
]

# Example 2 Data
input2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,0],
    [0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,2,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0]
]
output2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,3,0,0,0,0],
    [0,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,0],
    [0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [0,0,0,0,0,0,0,3,3,2,2,2,2,2,2,2,2,2,2,2],
    [0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0]
]

# Example 3 Data
input3 = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
output3 = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,3,3,3,3],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,3,3,3,3],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,3,3,3,3],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,2,2,2,2,2],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,3,3,3,3],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,3,3,3,3],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,3,3,3,3],
    [3,3,3,3,2,3,3,3,3,0,0,0,3,3,3,3,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0],
    [3,3,3,3,2,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0]
]

# Example 4 Data
input4 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,3,0,0,0,0,0],
    [0,0,0,3,3,0,0,0,0,0],
    [0,0,0,2,3,0,3,3,3,3],
    [0,0,0,3,3,0,3,3,2,3],
    [0,0,0,3,3,0,0,0,0,0],
    [0,0,0,3,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]
output4 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,3,0,0,0,0,0],
    [3,3,3,3,3,0,0,0,0,0],
    [2,2,2,2,3,0,3,3,3,3],
    [3,3,3,3,3,0,3,3,2,3],
    [0,0,0,3,3,0,0,3,2,3],
    [0,0,0,3,3,0,0,3,2,3],
    [0,0,0,0,0,0,0,3,2,3],
    [0,0,0,0,0,0,0,3,2,3]
]

analysis1 = analyze_example(input1, output1)
analysis2 = analyze_example(input2, output2)
analysis3 = analyze_example(input3, output3)
analysis4 = analyze_example(input4, output4)

print(f"Example 1 Analysis:\n{analysis1}\n")
print(f"Example 2 Analysis:\n{analysis2}\n")
print(f"Example 3 Analysis:\n{analysis3}\n")
print(f"Example 4 Analysis:\n{analysis4}\n")
```
```
Example 1 Analysis:
[{'red_pixel_location': (np.int64(3), np.int64(5)), 'adjacent_pixels': {'Up': {'location': (np.int64(2), np.int64(5)), 'color': np.int64(0)}, 'Down': {'location': (np.int64(4), np.int64(5)), 'color': np.int64(3)}, 'Left': {'location': (np.int64(3), np.int64(4)), 'color': np.int64(3)}, 'Right': {'location': (np.int64(3), np.int64(6)), 'color': np.int64(3)}}, 'adjacent_white_locations': [((np.int64(2), np.int64(5)), 'Up')], 'expansion_direction_hypothesis': 'Up'}, {'red_pixel_location': (np.int64(14), np.int64(10)), 'adjacent_pixels': {'Up': {'location': (np.int64(13), np.int64(10)), 'color': np.int64(3)}, 'Down': {'location': (np.int64(15), np.int64(10)), 'color': np.int64(3)}, 'Left': {'location': (np.int64(14), np.int64(9)), 'color': np.int64(0)}, 'Right': {'location': (np.int64(14), np.int64(11)), 'color': np.int64(3)}}, 'adjacent_white_locations': [((np.int64(14), np.int64(9)), 'Left')], 'expansion_direction_hypothesis': 'Left'}]

Example 2 Analysis:
[{'red_pixel_location': (np.int64(4), np.int64(14)), 'adjacent_pixels': {'Up': {'location': (np.int64(3), np.int64(14)), 'color': np.int64(0)}, 'Down': {'location': (np.int64(5), np.int64(14)), 'color': np.int64(3)}, 'Left': {'location': (np.int64(4), np.int64(13)), 'color': np.int64(3)}, 'Right': {'location': (np.int64(4), np.int64(15)), 'color': np.int64(3)}}, 'adjacent_white_locations': [((np.int64(3), np.int64(14)), 'Up')], 'expansion_direction_hypothesis': 'Up'}, {'red_pixel_location': (np.int64(15), np.int64(9)), 'adjacent_pixels': {'Up': {'location': (np.int64(14), np.int64(9)), 'color': np.int64(3)}, 'Down': {'location': (np.int64(16), np.int64(9)), 'color': np.int64(3)}, 'Left': {'location': (np.int64(15), np.int64(8)), 'color': np.int64(3)}, 'Right': {'location': (np.int64(15), np.int64(10)), 'color': np.int64(0)}}, 'adjacent_white_locations': [((np.int64(15), np.int64(10)), 'Right')], 'expansion_direction_hypothesis': 'Right'}]

Example 3 Analysis:
[{'red_pixel_location': (np.int64(4), np.int64(4)), 'adjacent_pixels': {'Up': {'location': (np.int64(3), np.int64(4)), 'color': np.int64(3)}, 'Down': {'location': (np.int64(5), np.int64(4)), 'color': np.int64(0)}, 'Left': {'location': (np.int64(4), np.int64(3)), 'color': np.int64(3)}, 'Right': {'location': (np.int64(4), np.int64(5)), 'color': np.int64(3)}}, 'adjacent_white_locations': [((np.int64(5), np.int64(4)), 'Down')], 'expansion_direction_hypothesis': 'Down'}, {'red_pixel_location': (np.int64(12), np.int64(15)), 'adjacent_pixels': {'Up': {'location': (np.int64(11), np.int64(15)), 'color': np.int64(3)}, 'Down': {'location': (np.int64(13), np.int64(15)), 'color': np.int64(3)}, 'Left': {'location': (np.int64(12), np.int64(14)), 'color': np.int64(3)}, 'Right': {'location': (np.int64(12), np.int64(16)), 'color': np.int64(0)}}, 'adjacent_white_locations': [((np.int64(12), np.int64(16)), 'Right')], 'expansion_direction_hypothesis': 'Right'}]

Example 4 Analysis:
[{'red_pixel_location': (np.int64(4), np.int64(3)), 'adjacent_pixels': {'Up': {'location': (np.int64(3), np.int64(3)), 'color': np.int64(3)}, 'Down': {'location': (np.int64(5), np.int64(3)), 'color': np.int64(3)}, 'Left': {'location': (np.int64(4), np.int64(2)), 'color': np.int64(0)}, 'Right': {'location': (np.int64(4), np.int64(4)), 'color': np.int64(3)}}, 'adjacent_white_locations': [((np.int64(4), np.int64(2)), 'Left')], 'expansion_direction_hypothesis': 'Left'}, {'red_pixel_location': (np.int64(5), np.int64(8)), 'adjacent_pixels': {'Up': {'location': (np.int64(4), np.int64(8)), 'color': np.int64(3)}, 'Down': {'location': (np.int64(6), np.int64(8)), 'color': np.int64(0)}, 'Left': {'location': (np.int64(5), np.int64(7)), 'color': np.int64(3)}, 'Right': {'location': (np.int64(5), np.int64(9)), 'color': np.int64(3)}}, 'adjacent_white_locations': [((np.int64(6), np.int64(8)), 'Down')], 'expansion_direction_hypothesis': 'Down'}]


```
The analysis confirms the hypothesis: in every case, the red pixel has exactly one adjacent white pixel, and the direction towards that white pixel matches the direction of the expansion seen in the expected output.

**Facts:**


```yaml
task_description: Expand specific objects into adjacent empty space based on a marker pixel.

components:
  - object: marker
    color: red (2)
    role: Indicates which objects to expand and determines the expansion direction.
    properties:
      - Must have exactly one orthogonally adjacent white (0) pixel.
      - Must be orthogonally adjacent to at least one green (3) pixel.
  - object: shape_component
    color: green (3)
    role: Forms the body of the expandable object along with the marker pixel.
    properties:
      - Must be orthogonally connected to the marker pixel or other shape_component pixels that are part of the same object.
  - object: expandable_object
    definition: A contiguous group of pixels consisting of one red marker pixel and all orthogonally connected green shape_component pixels.
  - object: empty_space
    color: white (0)
    role: The area into which the expandable_object expands.
  - object: boundary / obstruction
    color: Any non-white color (1-9) or grid edge.
    role: Stops the expansion.

actions:
  - name: identify_objects
    inputs: grid
    steps:
      - Find all red (2) pixels.
      - For each red pixel, perform a flood fill (orthogonal neighbors) to find all connected green (3) pixels.
      - The red pixel plus its connected green pixels form one `expandable_object`.
  - name: determine_expansion_direction
    inputs: red_pixel_location, grid
    steps:
      - Check the four orthogonal neighbors (up, down, left, right) of the red pixel.
      - Identify the neighbor cell that contains a white (0) pixel.
      - The direction from the red pixel to this white pixel is the `expansion_direction`.
    output: expansion_direction (e.g., 'Up', 'Down', 'Left', 'Right')
  - name: expand_object
    inputs: expandable_object_pixels, expansion_direction, grid
    steps:
      - Create a copy of the input grid to modify.
      - For each pixel (r, c) belonging to the `expandable_object`:
        - Get the original color of this pixel.
        - Determine the step vector (dr, dc) corresponding to the `expansion_direction`.
        - Start from the cell adjacent to (r, c) in the expansion direction: (nr, nc) = (r + dr, c + dc).
        - While the cell (nr, nc) is within the grid boundaries AND the cell at (nr, nc) in the *copied* grid is white (0):
          - Set the color of the cell (nr, nc) in the copied grid to the original color of the pixel (r, c).
          - Move to the next cell in the expansion direction: (nr, nc) = (nr + dr, nc + dc).
    output: modified_grid

workflow:
  - step: Initialize an output grid as a copy of the input grid.
  - step: Find all red (2) pixels in the input grid.
  - step: For each red pixel found:
      - Identify the full `expandable_object` connected to it (itself + connected green pixels). (Use `identify_objects`)
      - Determine the `expansion_direction` based on the white neighbor of the red pixel. (Use `determine_expansion_direction`)
      - If a direction is found:
          - Expand the object into the output grid. (Use `expand_object` on the output grid, using the coordinates from the `expandable_object` found in the input grid)
  - step: Return the final output grid.

constraints:
  - Expansion only fills white (0) pixels.
  - Expansion stops at grid boundaries or non-white pixels.
  - Each red pixel initiates one expansion process for its connected object.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Locate all red pixels (color 2) in the input grid.
3.  For each red pixel found at coordinates (R, C):
    a.  Identify the connected object consisting of this red pixel and all orthogonally adjacent green pixels (color 3) recursively connected to it. Store the coordinates of all pixels belonging to this object.
    b.  Find the single orthogonally adjacent white pixel (color 0) next to the *red* pixel at (R, C). Determine the direction (Up, Down, Left, or Right) from the red pixel to this white pixel. This is the expansion direction for the entire object.
    c.  For every pixel (obj_r, obj_c) belonging to the identified connected object:
        i.  Retrieve the original color of this pixel from the input grid (it will be either red or green).
        ii. Determine the directional step (dr, dc) corresponding to the expansion direction (e.g., Up is (-1, 0), Right is (0, 1)).
        iii. Start tracing a path from the pixel adjacent to (obj_r, obj_c) in the expansion direction. Let the current trace coordinates be (trace_r, trace_c) = (obj_r + dr, obj_c + dc).
        iv. While the coordinates (trace_r, trace_c) are within the grid boundaries and the pixel at (trace_r, trace_c) in the *output* grid is white (0):
            1.  Color the pixel at (trace_r, trace_c) in the output grid with the original color retrieved in step 3.c.i.
            2.  Update the trace coordinates to the next step in the expansion direction: (trace_r, trace_c) = (trace_r + dr, trace_c + dc).
4.  Return the modified output grid.