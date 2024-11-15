# Machine-learning baseline

## Implementation

The baseline model is implemented using [CHIMP](https://github.com/simonpf/chimp). The CHIMP command line interface is included in the ``precipitation_forecast`` conda environment provided in the parent directory. The training can be reproduced using:

````
export TMPDIR=/path/containing/training/data
chimp eda
chimp train
````

