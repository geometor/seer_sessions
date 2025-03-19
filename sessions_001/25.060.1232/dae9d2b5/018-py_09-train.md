
## example 1
*input:*
```
4 4 0 3 3 0
4 0 0 3 0 0
0 0 0 0 0 3
```
*expected output:*
```
6 6 0
6 0 0
0 0 6
```
*transformed output:*
```
4 4 0
4 0 0
0 0 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**

## example 2
*input:*
```
4 0 4 3 3 0
4 0 0 3 0 0
0 0 4 3 0 0
```
*expected output:*
```
6 6 6
6 0 0
6 0 6
```
*transformed output:*
```
4 0 4
4 0 0
0 0 4
```
size: True
palette: False
color count: False
pixels off: 6
**FAILED!**

## example 3
*input:*
```
0 0 4 0 3 0
0 4 4 3 0 3
4 4 0 0 0 3
```
*expected output:*
```
0 6 6
6 6 6
6 6 6
```
*transformed output:*
```
0 0 4
0 4 4
4 4 0
```
size: True
palette: False
color count: False
pixels off: 8
**FAILED!**

## example 4
*input:*
```
4 4 0 3 0 0
0 0 0 0 0 3
4 0 0 0 0 0
```
*expected output:*
```
6 6 0
0 0 6
6 0 0
```
*transformed output:*
```
4 4 0
0 0 0
4 0 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**

## example 5
*input:*
```
0 0 0 0 3 0
4 0 0 0 0 0
0 0 4 3 3 0
```
*expected output:*
```
0 6 0
6 0 0
6 6 6
```
*transformed output:*
```
0 0 0
4 0 0
0 0 4
```
size: True
palette: False
color count: False
pixels off: 5
**FAILED!**
