
## train_1

**input:**
```
3 3 3 3 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 3 3 3 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 2 0 3 3 0 0
```


**output:**
```
0 0 0 3 3 0 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 2 0 4
```


**output:**
```
0 0 0 0 0 0 0 4 0 2 0 0
```


## train_4

**input:**
```
0 0 0 2 9 9 9 0 0 0 0 0
```


**output:**
```
9 9 9 2 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 2 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 2 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 2 0 0 1 1 1
```


**output:**
```
0 1 1 1 0 0 2 0 0 0 0 0
```


## train_7

**input:**
```
5 5 5 0 0 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 0 0 5 5 5 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are sequences of single-digit integers, separated by spaces. All examples have a sequence length of 12.
2.  **Key Numbers:**
    *   `0`: Appears frequently and seems to act as a background or empty space.
    *   `2`: Appears exactly once in each input and output. Its position seems crucial.
    *   Other non-zero digits (`1`, `3`, `4`, `5`, `9` in the examples): These appear in contiguous groups or as single elements and are rearranged in the output.
3.  **Transformation:** The core transformation involves rearranging the non-zero digits (excluding `2`) relative to the position of `2`. The digit `2` itself remains in the same position in the sequence. The arrangement of other non-zero digits appears mirrored or reflected across the position of `2`. Zeros fill the remaining positions.

**YAML Facts:**


```yaml
task: Reflect non-zero elements (excluding pivot 2) across the pivot's position within a fixed-length list.
input_format: A string of space-separated single-digit integers.
output_format: A string of space-separated single-digit integers.
constraints:
  - List length is fixed (12 in examples).
  - The digit '2' appears exactly once and acts as the pivot.
objects:
  - name: sequence
    type: List[int]
    description: Represents the input and output data structure.
  - name: pivot_element
    type: int
    value: 2
    description: The element around which the reflection occurs. Remains fixed in position.
  - name: movable_element
    type: int
    description: Any non-zero integer other than the pivot (2). These elements change position.
  - name: placeholder_element
    type: int
    value: 0
    description: Represents empty space in the sequence. Fills positions not occupied by the pivot or reflected movable elements.
properties:
  - name: position
    type: int
    description: The index of an element within the sequence (0-based).
  - name: pivot_position
    type: int
    description: The index of the pivot element (2) in the input sequence.
  - name: distance_from_pivot
    type: int
    description: The absolute difference between an element's position and the pivot_position.
actions:
  - name: find_pivot
    description: Locate the index of the pivot element (2) in the input sequence.
  - name: identify_movable
    description: Find all non-zero elements and their positions, excluding the pivot.
  - name: calculate_reflection
    input: element_position, pivot_position
    output: reflected_position
    description: Determine the new position for a movable element by reflecting its original position across the pivot_position. If original position is `i` and pivot is at `p`, the new position is `p + (p - i) = 2*p - i`. Alternatively, if distance is `d = abs(i-p)`, new position is `p + d` if `i < p`, and `p - d` if `i > p`.
  - name: construct_output
    description: Create a new sequence initialized with placeholders (0), place the pivot element at its original position, and place each movable element at its calculated reflected position.
relationships:
  - type: reflection
    description: Each movable element's position in the output is a reflection of its input position across the pivot position.
    element1: movable_element (input position `i`)
    element2: pivot_element (position `p`)
    element3: movable_element (output position `p + (p - i)`)
  - type: invariance
    description: The pivot element (2) maintains its original position in the output sequence.
    element: pivot_element
  - type: preservation
    description: The values of movable elements are preserved during the transformation.
```


**Natural Language Program:**

1.  Read the input string and convert it into a list of integers. Note the length of the list (e.g., 12).
2.  Find the index (position) of the pivot element `2` within the input list. Let this be `pivot_index`.
3.  Create a new output list of the same length as the input list, initially filled entirely with placeholder elements `0`.
4.  Place the pivot element `2` into the output list at the `pivot_index`.
5.  Iterate through each element and its index (`i`) in the *input* list.
6.  If the current element is not the pivot (`2`) and is not a placeholder (`0`):
    a.  Calculate the distance `d` between the element's index `i` and the `pivot_index` (`d = abs(i - pivot_index)`).
    b.  Determine the element's new reflected index (`reflected_index`):
        *   If the element was originally to the left of the pivot (`i < pivot_index`), its new index is `pivot_index + d`.
        *   If the element was originally to the right of the pivot (`i > pivot_index`), its new index is `pivot_index - d`.
    c.  Place the current element's value into the output list at the calculated `reflected_index`. Ensure the `reflected_index` is within the valid bounds of the list (0 to length-1).
7.  Convert the completed output list back into a string of space-separated integers.
