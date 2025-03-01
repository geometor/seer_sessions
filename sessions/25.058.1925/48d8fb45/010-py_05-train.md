
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 5 0 0 0 1 1 0
0 0 0 1 0 0 0 0 1 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 1 0 0
```
*expected output:*
```
0 1 0
1 1 1
0 1 1
```
*transformed output:*
```

```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
4 4 0
0 0 4
0 4 0
```
*transformed output:*
```
0 0 0 0 0 4 4 0
0 4 0 0 0 0 0 4
4 0 4 0 0 0 4 0
0 4 4 0 0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
