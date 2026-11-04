# Original assisted software snapshot

This source belongs to the original synthetic trace in runs/fallback_sanity/ and is not Samarth's current root harness. Keep harness.py and fixture data unchanged because stored hashes refer to their exact bytes. Archived test_harness.py tests this archived source.

From repository root:

```sh
python3 snapshots/initial/harness.py verify --out runs/fallback_sanity
python3 -m unittest discover -s snapshots/initial -p test_harness.py -v
```
