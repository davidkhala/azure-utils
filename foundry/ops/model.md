# model deployment configurations

## Dynamic quota

allows a deployment to take advantage of available capacity in service.

- If capacity is available, we will dynamically increase your quota and receive higher throughput
- We will not decrease your quota below the set amount.​

## Tokens per Minute Rate Limit

The maximum number of tokens per minute for this deployment

- down to 1000
- default: 100000
- up to, per `Deployment type`:
  - `Standard`: 150000
  - `Global Standard`: 350000
