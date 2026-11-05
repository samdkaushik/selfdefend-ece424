# Add Pdirect and midpoint submission

Adds an incoming-prompt shadow gate, structured verdicts, fail-closed checks,
experiment logging, and a self-contained midpoint submission.

## Results

- 48 fresh cases, three repeats, target-only/Pdirect: 288 attempts
- Pdirect blocked 24/24 attacks and allowed 22/24 benign cases each repeat
- Two false positives; no request or verdict-format errors
- Benign median latency: 105.4 ms target-only; 139.4 ms Pdirect

## Validation

18 component tests, six archived tests, and evidence audits pass. CI covers
Windows and Linux. Baseline and teammate implementations are unchanged.

## Contribution and remaining work

See [Sharon's note](../../contributions/sharon.md) and the
[midpoint package](../../submission/midpoint/README.md). Preliminary answer labels
need confirmation. Yasmin's pilot evidence is included. Broader evaluation, repo-native Pintent and
smaller-shadow code, second review, and pilot review-file manifest updates remain pending.
