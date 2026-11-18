# Competitive Radar

Open-source, free-first, iPhone-friendly competitor webpage monitoring prototype.

## Features
- Six editable public HTTPS research targets in `targets.json`
- Python page text capture, snapshots and diffs
- Markdown pulse report
- Manually triggered GitHub Actions workflow (no schedule)

## iPhone usage
Open **Actions → Competitive Radar Manual Research → Run workflow** on GitHub, then download the `competitive-radar-pulse` artifact. This is a manual research action, not an automated schedule.

## Limitations
GitHub Actions runners start fresh each run, so cross-run comparisons are not persistent until a storage mechanism is implemented. No AI synthesis, newsletter signup, X monitoring or registration is implemented. Public Actions logs and artifacts may be accessible to others. Do not commit secrets, private records or credentials.

## JACK
Proposed isolated JACK integration: https://github.com/dgafkingcrypto/jacks-rabbit-hole/pull/68 . Not deployed.

## Status
Research-only prototype. No monitoring runs verified. No scheduled monitoring, account creation, spending or production deployment. Contributions welcome. A permissive license has not yet been selected.
