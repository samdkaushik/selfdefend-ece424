# Shadow-defense workspaces

Pdirect is owned by Sharon; Pintent and the smaller-shadow comparison by Yasmin. These directories are contribution locations, not completed implementations.

Recommended integration contract to agree before merging: a detector accepts the prompt and configured model and returns a structured decision (`ALLOW` or `BLOCK`), raw response, elapsed time, model, and an error field. Invalid/failed detector output should fail closed while retaining a distinguishable error status. Dataset labels must not be sent to the detector.

For a simplified sequential defense: call the detector; if ALLOW, call the same target as the baseline; otherwise return a refusal. Preserve original prompt, detector raw output, decision, released response, and errors. Samarth's current root harness is target-only; it does not yet import these modules.

Each component should include actual code, a short README with an exact command, a small run in experiments/, and its owner's dated contribution entry. Do not copy original-paper code without preserving attribution/license requirements.
