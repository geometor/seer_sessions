
## train_1

**input:**
```
2 0 0 0 0 2 0 1 0 1 1 2
```


**output:**
```
2 2 2 0 0 0 0 0 0 1 1 1
```


## train_2

**input:**
```
0 0 2 0 0 1 2 0 0 0 0 0
```


**output:**
```
2 2 0 0 0 0 0 0 0 0 0 1
```


## train_3

**input:**
```
2 0 0 1 2 0 2 0 1 0 0 0
```


**output:**
```
2 2 2 0 0 0 0 0 0 0 1 1
```


## train_4

**input:**
```
0 2 0 0 0 0 2 0 2 1 0 1
```


**output:**
```
2 2 2 0 0 0 0 0 0 0 1 1
```


## train_5

**input:**
```
1 1 2 0 2 2 0 0 1 0 0 0
```


**output:**
```
2 2 2 0 0 0 0 0 0 1 1 1
```


## train_6

**input:**
```
0 1 2 0 0 1 1 0 0 0 0 1
```


**output:**
```
2 0 0 0 0 0 0 0 1 1 1 1
```


## train_7

**input:**
```
2 0 2 1 1 0 0 0 2 0 0 2
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 1 1
```

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are single strings representing space-separated sequences of integers.
2.  **Data Type:** The sequences consist only of the integers 0, 1, and 2.
3.  **Length Consistency:** The length of the output sequence is always the same as the length of the input sequence (12 elements in all provided examples).
4.  **Element Conservation:** Comparing the frequency counts of 0s, 1s, and 2s in the input and output for each example reveals that the counts are identical. This indicates the transformation is a rearrangement or permutation of the input elements.
5.  **Sorting Pattern:** The output is not simply sorted in ascending (0, 1, 2) or descending (2, 1, 0) order. Instead, it follows a specific custom sorting order: all 2s appear first, followed by all 0s, and finally all 1s.

**YAML Fact Document:**


```yaml
Task: Rearrange sequence elements according to a custom sort order.

Input:
  Type: List of integers (represented as a space-separated string).
  Properties:
    - Contains only integers 0, 1, and 2.
    - Fixed length (e.g., 12 in examples).
  Objects: Integers (0, 1, 2).

Output:
  Type: List of integers (represented as a space-separated string).
  Properties:
    - Contains the same integers as the input, with the same frequencies.
    - Elements are arranged in a specific order.
    - Same length as the input.
  Objects: Integers (0, 1, 2).

Transformation:
  Action: Rearrange (sort) the elements of the input list.
  Rule: The elements are ordered based on the sequence: 2, 0, 1.
  Relationship: The output list is a permutation of the input list, maintaining element counts but changing their positions according to the custom sort order (2s first, then 0s, then 1s).
```


**Natural Language Program:**

1.  Receive the input sequence of integers (0s, 1s, and 2s).
2.  Count the occurrences of each integer (0, 1, and 2) in the input sequence.
3.  Construct the output sequence by first appending all the 2s (based on the count), then appending all the 0s (based on the count), and finally appending all the 1s (based on the count).
4.  Return the constructed sequence.
```python
import collections

"""
Rearrange the input sequence of integers (0, 1, 2) such that all 2s appear first, 
followed by all 0s, and finally all 1s, maintaining the original counts of each integer.
"""

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated integers (0, 1, 2)
    by rearranging them according to the custom sort order: 2, 0, 1.

    Args:
        input_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A string containing the rearranged integers, space-separated.
    """
    # Parse the input string into a list of integers
    # Handle potential empty strings resulting from multiple spaces
    numbers = [int(x) for x in input_str.split() if x]

    # Count the occurrences of each number (0, 1, 2)
    counts = collections.Counter(numbers)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)
    count_2 = counts.get(2, 0)

    # Construct the output list based on the custom sort order (2, 0, 1)
    output_list = []
    # Append all the 2s
    output_list.extend([2] * count_2)
    # Append all the 0s
    output_list.extend([0] * count_0)
    # Append all the 1s
    output_list.extend([1] * count_1)

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```
