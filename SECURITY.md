# Security Policy

## Supported versions

The project is pre-release. Security fixes are applied to the latest development
line until the first supported release policy is published.

## Reporting a vulnerability

Do not disclose exploitable details in a public issue. Use the repository's
private **Report a vulnerability** channel (GitHub Security Advisories). If that
channel is unavailable, contact a maintainer privately using the contact method
listed on the repository owner profile and ask for a secure reporting channel
without sending sensitive details first.

Include affected version/commit, impact, minimal reproduction, and any suggested
mitigation. This is a pre-release, single-maintainer project: reports are
acknowledged and triaged on a best-effort basis rather than under a guaranteed
response SLA. Maintainers will coordinate disclosure after evidence is assessed
and a fix or mitigation is available.

Scientific-correctness defects that can corrupt, mislabel, or silently alter data
may have security-like impact. Report them privately when exploitation or
sensitive data is involved; otherwise use the normal issue process and label the
scientific risk clearly.

## Scope principles

SMR is local-first and must not add telemetry, mandatory cloud services, or
silent data transmission. Dependencies and release artifacts require provenance
and license/security review appropriate to their risk.
