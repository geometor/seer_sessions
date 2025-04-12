
## train_1

**input:**
```
9
0
1
6
8
```


**output:**
```
0
9
1
8
6
```


## train_2

**input:**
```
4
3
6
2
8
```


**output:**
```
3
4
6
8
2
```

**Perception:**

The input is a list of single-digit integers. The output is also a list of single-digit integers, containing the same elements as the input but in a different order. The transformation involves rearranging the elements within the list. Specifically, it appears that adjacent pairs of elements are swapped. The first element is swapped with the second, the third with the fourth, and so on. If there is an odd number of elements, the last element remains in its position after the preceding pairs have been swapped.

**Facts:**


```yaml
Input:
  type: list
  elements:
    type: integer
    range: single digit (0-9)
Output:
  type: list
  elements:
    type: integer
    content: same elements as input, reordered
Transformation:
  action: pairwise swapping
  process:
    - Iterate through the input list taking elements two at a time (step of 2).
    - For each pair (element at index `i`, element at index `i+1`), swap their positions.
    - If the list has an odd number of elements, the last element remains in its final position without being swapped.
  Relationship: Output is a permutation of the input based on adjacent swaps.
```


**Natural Language Program:**

Iterate through the input list, processing elements in pairs starting from the first element. For each pair of adjacent elements encountered, swap their positions. If the list contains an odd number of elements, the final element remains unchanged in its position relative to the swapped pairs. Construct the output list by appending the swapped pairs (and the final element if applicable) in their new order.
```python
"""
Iterate through the input list, processing elements in pairs starting from the first element. 
For each pair of adjacent elements encountered, swap their positions. 
If the list contains an odd number of elements, the final element remains unchanged in its position relative to the swapped pairs. 
Construct the output list by appending the swapped pairs (and the final element if applicable) in their new order.
"""

import math # Although not strictly needed for this specific problem, it's good practice to include potential imports

def transform(input_list: list[int]) -> list[int]:
    """
    Swaps adjacent pairs of elements in a list.
    If the list has an odd number of elements, the last element remains in place.

    Args:
        input_list: A list of integers.

    Returns:
        A new list with adjacent elements swapped.
    """
    # Create a copy of the input list to avoid modifying the original
    output_list = list(input_list)
    
    # Iterate through the list indices with a step of 2
    # This naturally pairs elements (0, 1), (2, 3), etc.
    for i in range(0, len(output_list), 2):
        # Check if there is a next element to swap with
        # This condition handles both even and odd length lists correctly.
        # If i is the last index in an odd-length list, i+1 will be out of bounds.
        if i + 1 < len(output_list):
            # Perform the swap of the adjacent pair
            output_list[i], output_list[i+1] = output_list[i+1], output_list[i]
            
    # Return the modified list
    return output_list

```
