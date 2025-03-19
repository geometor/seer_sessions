
## example 1
*input:*
```
5 0 5 0 0 5 0 0 0 5
0 5 0 0 5 0 0 5 0 0
0 0 0 5 0 0 5 0 5 0
```
*expected output:*
```
5 0 5 0 0 3 0 0 0 3
0 3 0 0 5 0 0 3 0 0
0 0 0 3 0 0 5 0 5 0
```
*transformed output:*
```
5 3 5 0 3 5 0 3 3 5
3 5 0 0 5 0 0 5 0 0
0 3 0 5 0 0 5 0 5 0
```
size: True
palette: True
color count: False
pixels off: 11
**FAILED!**

## example 2
*input:*
```
0 5 0 5 0 0 5 0 5 0 0 0
5 0 0 0 5 0 0 5 0 0 5 0
0 0 5 0 0 5 0 0 0 5 0 5
```
*expected output:*
```
0 3 0 3 0 0 5 0 5 0 0 0
5 0 0 0 5 0 0 3 0 0 5 0
0 0 5 0 0 3 0 0 0 3 0 3
```
*transformed output:*
```
3 5 3 5 3 3 5 3 5 0 3 0
5 0 3 0 5 0 0 5 0 0 5 0
0 0 5 0 0 5 0 3 0 5 0 5
```
size: True
palette: True
color count: False
pixels off: 14
**FAILED!**

## example 3
*input:*
```
0 0 5 0 0 5 0 5 0 0 0 5 0
5 0 0 0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 0 0 5 0 5 0 0
```
*expected output:*
```
0 0 3 0 0 5 0 5 0 0 0 5 0
3 0 0 0 3 0 3 0 0 5 0 0 3
0 5 0 5 0 0 0 0 3 0 3 0 0
```
*transformed output:*
```
3 3 5 0 3 5 3 5 0 3 3 5 0
5 0 3 0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 3 3 0 5 0 5 0 0
```
size: True
palette: True
color count: False
pixels off: 16
**FAILED!**

## example 4
*input:*
```
0 0 5 0 0 5 0 5 0 5 0 5 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 5
0 5 0 5 0 0 5 0 0 0 0 0 5 0
```
*expected output:*
```
0 0 5 0 0 3 0 3 0 3 0 3 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 3
0 3 0 3 0 0 5 0 0 0 0 0 5 0
```
*transformed output:*
```
3 3 5 0 3 5 3 5 3 5 3 5 0 0
5 0 3 0 5 0 3 0 5 0 5 0 0 5
0 5 0 5 0 0 5 0 3 3 3 0 5 0
```
size: True
palette: True
color count: False
pixels off: 18
**FAILED!**
