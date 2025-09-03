# Load balance



## Session persistence
distribution modes for routing connections to instances in the backend pool:
- aka. session affinity, source IP affinity, or client IP affinity
- configuration types
  - **Client IP**. 2-tuple (source IP and destination IP)
  - **Client IP and protocol**. 3-tuple (source IP, destination IP, and protocol type)
  - **None**. 5-tuple (Source IP, Source port, Destination IP, Destination port, Protocol type)
    - aka. Hash based distribution mode
    - the default of Azure Load Balancer