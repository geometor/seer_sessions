
## example 1
*input:*
```
2 2 1
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
5 1 1
2 5 0
0 2 0
```
size: True
palette: False
color count: False
pixels off: 6
**FAILED!**

## example 2
*input:*
```
2 2 5
6 2 2
5 5 5
```
*expected output:*
```
2 6 5
2 2 5
5 2 5
```
*transformed output:*
```
2 6 0
2 2 0
5 2 5
```
size: True
palette: False
color count: False
pixels off: 2
**FAILED!**

## example 3
*input:*
```
9 9 5
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
9 0 0
8 5 0
9 8 5
```
size: True
palette: False
color count: False
pixels off: 6
**FAILED!**

## example 4
*input:*
```
2 6 6
2 1 1
2 6 2
```
*expected output:*
```
2 2 2
6 1 6
6 1 2
```
*transformed output:*
```
2 6 2
6 1 0
2 1 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**
