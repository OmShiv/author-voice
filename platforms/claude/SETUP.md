# Claude

## Claude chat

Build from the repository root with `python3 scripts/build.py`. In Claude, open **Customize → Skills → + → Create skill → Upload a skill**, then upload `dist/author-voice-skill.zip` and enable it. The ZIP contains the named skill folder and its references. Availability depends on your account's skill and code-execution settings. [Official skill instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

Start with: “Use Author Voice to revise this research paper. Preserve the evidence and return clean text.” For drafting, invoke it before generating the manuscript. Add your own voice profile or `profiles/starter.md` as project context if desired.

## Claude Code

Add the public repository marketplace and install the plugin:

```text
/plugin marketplace add OmShiv/author-voice
/plugin install author-voice@author-voice
```

These commands run inside Claude Code. For local development, use the command below.

From the repository root:

```sh
claude --plugin-dir ./plugins/author-voice
```

Then invoke:

```text
/author-voice:author-voice Revise chapter.md in book mode, light edit.
```

The repeated name is the plugin namespace followed by the skill name. `--plugin-dir` loads the local plugin for that session. Use `/reload-plugins` after edits. [Official plugin development instructions](https://code.claude.com/docs/en/plugins).

If skill uploads are unavailable, use the generated portable instructions from `platforms/chatgpt/instructions.md` as project instructions; optional supporting knowledge is in `platforms/shared/knowledge.md`. This fallback provides the editing method, not a new document tool.

Package format checked locally; account upload and manuscript behavior require testing in your Claude account. UI documentation checked September 12, 2026.
