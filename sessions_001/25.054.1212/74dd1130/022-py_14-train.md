
## example 1
*input:*
```
2 1 1
1 5 1
5 2 2
```
*expected output:*
```
2 1 5
2 5 2
1 1 2
```
*transformed output:*
```
1 1 1
1 5 1
5 5 5
```
size: True
palette: True
color count: False
pixels off: 7
**FAILED!**

## example 2
*input:*
```
2 6 5
6 2 2
5 5 5
```
*expected output:*
```
2 6 5
2 2 5
5 2 5
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: integer division or modulo by zero

## example 3
*input:*
```
9 5 5
5 5 8
5 8 9
```
*expected output:*
```
9 5 5
9 5 8
5 8 9
```
*transformed output:*
```
9 5 5
5 5 8
5 8 9
```
size: True
palette: True
color count: False
pixels off: 1
**FAILED!**

## example 4
*input:*
```
2 2 6
2 1 1
2 6 2
```
*expected output:*
```
2 2 2
6 1 6
6 1 2
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: integer division or modulo by zero
