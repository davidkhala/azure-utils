# model deployment

## model series

Llama
- Vision
  - Llama-3.2-90B-Vision-Instruct
  - Llama-3.2-11B-Vision-Instruct
  - Llama-4-Maverick-17B-128E-Instruct-FP8 (arch: MoE)
- Instruct (arch: Dense)
  - Meta-Llama-3.1-8B-Instruct
  - Llama-3.3-70B-Instruct
  - Meta-Llama-3.1-405B-Instruct
- Llama-4-Scout-17B-16E-Instruct (arch: MoE)
- No tool/functions calling support
  - you have to use GPT series for tool use


## Dynamic quota

allows a deployment to take advantage of available capacity in service.

- If capacity is available, we will dynamically increase your quota and receive higher throughput
- We will not decrease your quota below the set amount.

## Tokens per Minute Rate Limit

The maximum number of tokens per minute for this deployment

- down to 1000
- default: 100000
- up to, per `Deployment type`:
  - `Standard`: 150000
  - `Global Standard`: 350000
