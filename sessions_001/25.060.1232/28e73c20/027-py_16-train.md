
## example 1
*input:*
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
3 3 3 3 3 3
0 0 0 0 0 3
3 3 3 3 0 3
3 0 3 3 0 3
3 0 0 0 0 3
3 3 3 3 3 3
```
*transformed output:*
```
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
*expected output:*
```
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 3
3 3 3 3 3 3 0 3
3 0 0 0 0 3 0 3
3 0 3 3 0 3 0 3
3 0 3 3 3 3 0 3
3 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3
```
*transformed output:*
```
3 3 3 3 3 3 3 3
3 3 3 0 0 3 3 3
3 3 3 3 3 3 3 3
3 0 3 3 3 3 0 3
3 0 3 3 3 3 0 3
3 3 3 3 3 3 3 3
3 3 3 0 0 3 3 3
3 3 3 3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 16
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 3 3 3 0 3 0 3
3 0 3 0 0 0 0 0 0 0 3 0 3 0 3
3 0 3 0 3 3 3 3 3 0 3 0 3 0 3
3 0 3 0 3 0 0 0 3 0 3 0 3 0 3
3 0 3 0 3 0 3 3 3 0 3 0 3 0 3
3 0 3 0 3 0 0 0 0 0 3 0 3 0 3
3 0 3 0 3 3 3 3 3 3 3 0 3 0 3
3 0 3 0 0 0 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
*transformed output:*
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 0 0 0 0 0 0 0 0 0 3 3 3
3 3 3 3 0 0 0 0 0 0 0 3 3 3 3
3 0 3 3 3 0 0 0 0 0 3 3 3 0 3
3 0 0 3 3 3 0 0 0 3 3 3 0 0 3
3 0 0 0 3 3 3 0 3 3 3 0 0 0 3
3 0 0 0 0 3 3 3 3 3 0 0 0 0 3
3 0 0 0 0 0 3 3 3 0 0 0 0 0 3
3 0 0 0 0 3 3 3 3 3 0 0 0 0 3
3 0 0 0 3 3 3 0 3 3 3 0 0 0 3
3 0 0 3 3 3 0 0 0 3 3 3 0 0 3
3 0 3 3 3 0 0 0 0 0 3 3 3 0 3
3 3 3 3 0 0 0 0 0 0 0 3 3 3 3
3 3 3 0 0 0 0 0 0 0 0 0 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 78
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 3 0 3 0 3
3 0 3 0 0 0 0 0 3 0 3 0 3
3 0 3 0 3 3 3 0 3 0 3 0 3
3 0 3 0 3 0 0 0 3 0 3 0 3
3 0 3 0 3 3 3 3 3 0 3 0 3
3 0 3 0 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3
```
*transformed output:*
```
3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 0 0 0 0 0 0 0 3 3 3
3 3 3 3 0 0 0 0 0 3 3 3 3
3 0 3 3 3 0 0 0 3 3 3 0 3
3 0 0 3 3 3 0 3 3 3 0 0 3
3 0 0 0 3 3 3 3 3 0 0 0 3
3 0 0 0 0 3 3 3 0 0 0 0 3
3 0 0 0 3 3 3 3 3 0 0 0 3
3 0 0 3 3 3 0 3 3 3 0 0 3
3 0 3 3 3 0 0 0 3 3 3 0 3
3 3 3 3 0 0 0 0 0 3 3 3 3
3 3 3 0 0 0 0 0 0 0 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 56
**FAILED!**

## example 5
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 0 3 0 3
3 0 3 0 3 3 0 3 0 3
3 0 3 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3
```
*transformed output:*
```
3 3 3 3 3 3 3 3 3 3
3 3 3 0 0 0 0 3 3 3
3 3 3 3 0 0 3 3 3 3
3 0 3 3 3 3 3 3 0 3
3 0 0 3 3 3 3 0 0 3
3 0 0 3 3 3 3 0 0 3
3 0 3 3 3 3 3 3 0 3
3 3 3 3 0 0 3 3 3 3
3 3 3 0 0 0 0 3 3 3
3 3 3 3 3 3 3 3 3 3
```
size: True
palette: True
color count: False
pixels off: 32
**FAILED!**
