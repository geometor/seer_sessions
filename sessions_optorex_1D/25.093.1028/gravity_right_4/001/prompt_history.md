
## train_1

**input:**
```
0 5 0 0 0 8 9 0 0 0 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 5 8 9 4
```


## train_2

**input:**
```
9 3 8 7 3 2 1 0 0 0 0 4
```


**output:**
```
0 0 0 0 9 3 8 7 3 2 1 4
```


## train_3

**input:**
```
0 0 0 8 3 0 1 3 0 0 3 0
```


**output:**
```
0 0 0 0 0 0 0 8 3 1 3 3
```


## train_4

**input:**
```
4 3 0 7 6 7 0 1 0 0 0 2
```


**output:**
```
0 0 0 0 0 4 3 7 6 7 1 2
```


## train_5

**input:**
```
0 3 6 0 3 8 0 0 1 8 0 0
```


**output:**
```
0 0 0 0 0 0 3 6 3 8 1 8
```


## train_6

**input:**
```
0 0 0 0 0 5 0 0 5 2 0 5
```


**output:**
```
0 0 0 0 0 0 0 0 5 5 2 5
```


## train_7

**input:**
```
0 0 9 5 0 4 3 0 0 2 8 9
```


**output:**
```
0 0 0 0 0 9 5 4 3 2 8 9
```

**Perception of Task Elements:**

The task involves rearranging a sequence of integers. The input consists of a list of integers, containing both zeros and non-zero values. The output is a list of the same length, where all the zero elements from the input are moved to the beginning of the list, and all the non-zero elements are moved to the end, preserving their original relative order.

**Facts:**


```yaml
Input:
  type: sequence
  elements: integers
  properties:
    - contains zeros
    - contains non-zero integers
    - fixed length (e.g., 12 in examples)

Output:
  type: sequence
  elements: integers
  properties:
    - same length as input
    - same multiset of elements as input (same numbers, same counts)
    - structured arrangement

Transformation:
  action: rearrange elements
  rule: partition based on value (zero vs. non-zero)
  constraints:
    - relative order of non-zero elements is preserved
    - all zeros are grouped together at the beginning
    - all non-zeros are grouped together at the end

Relationships:
  - Input element maps to an output element.
  - The position of an element in the output depends on its value (zero or non-zero) and its original position relative to other non-zero elements.
  - The count of zeros in the input equals the count of leading zeros in the output.
  - The sequence of non-zero elements in the input is identical to the sequence of trailing non-zero elements in the output.
```


**Natural Language Program:**

1.  Accept an input sequence of integers.
2.  Create a new, empty sequence to store the non-zero elements, maintaining their original relative order.
3.  Initialize a counter for the number of zero elements to zero.
4.  Iterate through the input sequence:
    a.  If the current element is zero, increment the zero counter.
    b.  If the current element is non-zero, append it to the sequence of non-zero elements.
5.  Construct the final output sequence:
    a.  Start with a sequence consisting of the counted number of zeros.
    b.  Append the sequence of collected non-zero elements to the end of the zero sequence.
6.  Return the constructed output sequence.
