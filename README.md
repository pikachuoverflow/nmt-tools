## NMT Tools

### Overview

The Native Memory Tracking (NMT) is a Java Hotspot VM feature that tracks internal memory usage for a HotSpot JVM.
First, enable NMT using the following command line. Note that enabling this will cause 5-10% performance overhead.

```-XX:NativeMemoryTracking=[off | summary | detail]```

- ```off``` NMT is turned off by default
- ```summary``` only collect memory usage aggregated by subsystem
- ```detail``` collect memory usage by individual call sites

Use ```jcmd``` to dump the data collected and optionally compare it to the last baseline, such as:

```jcmd <pid> VM.native_memory [summary | detail] > report.out```

### NMT Parser tool

Basic usage is:

```./nmt-parser.py -f FILES [FILES ...] -m {committed,reserved}  ```

For example, we have a bunch of NMT report files gathered with:

```jcmd <pid> VM.native_memory [summary | detail] > report_$(date +"%Y%m%d%H%M").out```.

```bash
$ ls reports/report*.out

reports/report_202004231400.out reports/report_202004231500.out reports/report_202004231600.out reports/report_202004231700.out

```

Using the following command line, we can obtain an aggregate report:

```bash

$ ./nmt-parser.py --files reports/report*.out --mode reserved | column -t -s ';'

File Name                        Java Heap  Class      Thread  Code     GC       Compiler  Internal  Symbol  Native Memory Tracking  Arena Chunk  Unknown  Total
reports/report_202004231400.out  5,242,880  1,130,054  93,092  266,025  254,062  284       14,263    14,022  4,429                   1,533        10,240   7,030,885
reports/report_202004231500.out  5,242,880  1,144,882  92,060  268,552  256,064  278       15,895    14,257  5,331                   189          10,240   7,050,628
reports/report_202004231600.out  5,242,880  1,152,964  93,892  269,720  256,363  288       17,229    14,424  5,951                   190          10,240   7,064,142
reports/report_202004231700.out  5,242,880  1,155,161  92,860  270,544  256,544  293       17,073    14,587  5,126                   190          10,240   7,065,497


$ ./nmt-parser.py --files reports/report*.out --mode committed | column -t -s ';'

File Name                        Java Heap  Class    Thread  Code     GC       Compiler  Internal  Symbol  Native Memory Tracking  Arena Chunk  Unknown  Total
reports/report_202004231400.out  5,242,880  94,750   93,092  100,925  254,062  284       14,263    14,022  4,429                   1,533        0        5,820,241
reports/report_202004231500.out  5,242,880  112,010  92,060  117,820  256,064  278       15,895    14,257  5,331                   189          0        5,856,784
reports/report_202004231600.out  5,242,880  124,956  93,892  125,876  256,363  288       17,229    14,424  5,951                   190          0        5,882,050
reports/report_202004231700.out  5,242,880  128,877  92,860  133,200  256,544  293       17,073    14,587  5,126                   190          0        5,891,629

```
