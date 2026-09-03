# Schemas

This directory separates schema from instance data:

- `quantity-definition.schema.json` is an actual JSON Schema 2020-12 document.
- `quantity-definitions.v0.1.json` is versioned seed data validated against that
  schema; it is not itself a JSON Schema and therefore does not claim the JSON
  Schema meta-schema.

M1 will add normative record schemas only after the conceptual model is
implemented and tested.

Schema changes that alter persisted meaning require a decision record, version
change, migration plan, and deterministic compatibility tests.

These top-level files are repository/specification and M0-test assets. Any
resource required at runtime must be packaged inside the installed `smr`
distribution and loaded through a supported package-resource API; runtime code
must not assume this source-checkout directory exists.
