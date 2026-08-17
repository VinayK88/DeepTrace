# Methodology

DeepTrace separates **provenance evidence**, **forensic signals**, and **coordination evidence** rather than collapsing them into one opaque "fake score."

## Content assessment

The deterministic lab combines:

- presence/validity of a provenance credential;
- signer trust status;
- metadata consistency;
- similarity to a known-source asset;
- synthetic-media signal;
- manipulation signal.

The output is one of:

`VERIFIED` · `LIKELY_AUTHENTIC` · `INCONCLUSIVE` · `LIKELY_MANIPULATED` · `HIGH_RISK_SYNTHETIC`

Confidence is evidence strength, **not proof of authorship or intent**.

## Campaign analysis

Campaign detection groups repeated narratives and scores coordination using:

- account diversity;
- temporal concentration;
- recurrence of high-risk media.

This intentionally avoids asserting a real-world actor or motive. In production, campaign attribution should be a separate, higher-evidence workflow.
