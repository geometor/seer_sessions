
## train_1

**input:**
```
0 0 2 2 0 0 0 0 1 0 0 0
```


**output:**
```
2 2 0 0 0 0 0 0 0 0 0 1
```


## train_2

**input:**
```
1 2 1 1 1 2 0 0 0 1 2 0
```


**output:**
```
2 2 2 0 0 0 0 1 1 1 1 1
```


## train_3

**input:**
```
1 1 0 0 2 2 0 1 0 2 2 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 1 1 1
```


## train_4

**input:**
```
2 2 0 0 0 2 1 2 2 0 0 0
```


**output:**
```
2 2 2 2 2 0 0 0 0 0 0 1
```


## train_5

**input:**
```
0 1 1 1 2 2 2 0 2 0 0 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 1 1 1
```


## train_6

**input:**
```
1 2 0 0 2 2 1 0 0 2 0 1
```


**output:**
```
2 2 2 2 0 0 0 0 0 1 1 1
```


## train_7

**input:**
```
0 2 0 0 1 1 2 1 2 1 0 0
```


**output:**
```
2 2 2 0 0 0 0 0 1 1 1 1
```

**Perception of Elements:**

The task involves transforming a sequence of digits (0, 1, and 2). Both the input and output are sequences of 12 digits. The core transformation appears to be a reordering of the digits present in the input sequence. The counts of each digit (0, 1, 2) remain the same between the input and the output. The output sequence follows a specific sorting order: all the '2's appear first, followed by all the '0's, and finally all the '1's.

**Facts:**


```yaml
Input:
  type: sequence
  elements: digits (0, 1, 2)
  length: 12
Output:
  type: sequence
  elements: digits (0, 1, 2)
  length: 12
  property: preserves digit counts from input
Transformation:
  action: sort/reorder
  rule: Group digits based on value
  order:
    - group 1: all digits with value 2
    - group 2: all digits with value 0
    - group 3: all digits with value 1
  relationship: Output sequence is the concatenation of group 1, group 2, and group 3 in that order.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Count the number of occurrences of the digit '2' in the input sequence.
3.  Count the number of occurrences of the digit '0' in the input sequence.
4.  Count the number of occurrences of the digit '1' in the input sequence.
5.  Construct the output sequence by:
    a.  Appending the digit '2' repeated by its count.
    b.  Appending the digit '0' repeated by its count.
    c.  Appending the digit '1' repeated by its count.
6.  Return the constructed output sequence.
```python
"""
Transforms an input sequence of digits (0, 1, 2) by reordering them.
The output sequence contains all the '2's from the input, followed by all the '0's,
and finally all the '1's. The counts of each digit remain the same.
"""

import collections

def transform(input_str: str) -> str:
    """
    Reorders the digits in the input string according to the rule: 2s, then 0s, then 1s.

    Args:
        input_str: A string containing space-separated digits (0, 1, 2).

    Returns:
        A string containing the reordered space-separated digits.
    """
    # Parse the input string into a list of integers
    input_digits = [int(d) for d in input_str.split()]

    # Count the occurrences of each digit (0, 1, 2)
    counts = collections.Counter(input_digits)
    count_2 = counts.get(2, 0)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)

    # Construct the output list based on the counts and the desired order (2, 0, 1)
    output_digits = []
    output_digits.extend([2] * count_2) # Append '2's
    output_digits.extend([0] * count_0) # Append '0's
    output_digits.extend([1] * count_1) # Append '1's

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_digits))

    return output_str

```
