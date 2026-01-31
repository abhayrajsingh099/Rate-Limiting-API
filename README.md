# Rate-Limiting-API
Rate Limiting API.

# DAY 1
Decisions:

    Identity: IP-based
Why IP? IP is easily accessible, comes with request. and are difficult to misuse.

    Resource: Global API
    Policy: 60 requests/hour, no burst
    Override stance: single escape hatch allowed
    Block behavior: 429 + Retry-After

    - These are Desicisons made on day 1.
    - Defines a clear path to Code.

# DAY 2
Best fit algorthim:
    -> Sliding Window (dynamic window)

    Why? Fits best for requirements made on day 1. No burstiness, Fairness and explaniable Retry-After.

 Tradeoff:

    Sliding window requires more state and computation than fixed window.
