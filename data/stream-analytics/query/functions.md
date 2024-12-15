# Windowing Functions



## [Tumbling windows](https://learn.microsoft.com/en-us/stream-analytics-query/tumbling-window-azure-stream-analytics)
A series of fixed-sized, non-overlapping and contiguous time intervals

## [Hopping Window](https://learn.microsoft.com/en-us/stream-analytics-query/hopping-window-azure-stream-analytics)
It schedules overlapping windows
- parameters
    - `hopsize`: how much each window moves forward relative to the previous one
    - `offsetsize`
    - > **Advanced tumbling**: A tumbling window is simply a hopping window whose `hopsize`== `windowsize`.