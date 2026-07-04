# Contributing

PRs are welcome. Ground rules:

- **CI must pass.** [validate-template.yml](.github/workflows/validate-template.yml)
  parse-gates the executable surface: `bootstrap/` stays pure ASCII (Windows
  PowerShell 5.1 decodes BOM-less files as ANSI, so multi-byte characters break it),
  PowerShell scripts must parse, hooks must pass `bash -n`, and the JSON manifests
  must be valid.
- **Update provenance.** If you materially change a forked skill or add a
  third-party one, update its row in
  [`.claude/skills/PROVENANCE.md`](.claude/skills/PROVENANCE.md) and keep the
  upstream LICENSE/NOTICE files in the skill folder.
- **Bump the plugin version** when a change touches the shared surface
  (`.claude/skills`, `.claude/hooks`, `.claude/settings.json`): edit `version` in
  `.claude-plugin/plugin.json`, patch for fixes, minor for new skills.
- **Keep the kernel lean.** New always-loaded rules, skills, and reference entries
  must earn their place; prefer pruning to accreting. Check the per-turn cost with
  `bash .claude/scripts/context-weight.sh`.
- **The intended loop.** Most improvements arrive via `/sync-starter` from projects
  spawned off this template, but direct PRs are just as welcome.
