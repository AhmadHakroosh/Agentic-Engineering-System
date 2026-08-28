# Agent workflow threat model

Primary risks are prompt injection through tickets/comments/logs, over-privileged integrations, secret disclosure, confused-deputy writes, review self-approval, stale evidence, CI supply-chain compromise, artifact substitution, and unsafe production changes.

Controls include narrow adapters, untrusted-content rules, read-only analysis/review agents, explicit specialist allowlists, closed JSON schemas, head-SHA binding, least-privilege workflow tokens, pinned actions, build-once promotion, digest verification at every boundary, protected environments, concurrency control, and human approval.

Residual risks remain in the model/provider, extension/MCP implementation, GitHub organization settings, runner images, third-party action commits, and target-specific deploy adapter. Review and operate those as trusted computing base components.

