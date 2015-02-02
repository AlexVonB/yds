# YDS-Algorithm implementation

This script calculates a scheduling using the
[YDS-Algorithm](https://en.wikipedia.org/wiki/YDS_algorithm).

## Usage

```python
import yds

tasks = [
    # task name (can have any type), release time, deadline, execution time
    yds.Task("t1",  0, 17,  5),
    yds.Task("t2",  1, 11,  3),
    yds.Task("t3", 12, 20,  4),
    yds.Task("t4",  7, 11,  2),
    yds.Task("t5",  1, 20,  4),
    yds.Task("t6", 14, 20, 12),
    yds.Task("t7", 14, 17,  4),
    yds.Task("t8",  1,  7,  2)
]

scheduling = yds.calc_scheduling(tasks)
print scheduling
```

Returns:

```
# task name, execution timeframe, cpu-frequency-factor
[   t8: 0.0 - 1.5, f=1.33333333333,
    t2: 1.5 - 3.75, f=1.33333333333,
    t4: 3.75 - 5.25, f=1.33333333333,
    t1: 5.25 - 9.0, f=1.33333333333,
    t5: 9.0 - 12.0, f=1.33333333333,
    t3: 12.0 - 14.0, f=2.0,
    t7: 14.0 - 15.5, f=2.66666666667,
    t6: 15.5 - 20.0, f=2.66666666667]
```
