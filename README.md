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

Use the following command line to get an aggregate report:

```./nmt-parser.py -f FILES [FILES ...] -m {committed,reserved}  ```

