# Claude

Author Voice is distributed through our own public GitHub marketplace. Installing from it does not require inclusion in Anthropic's community or official marketplaces. Author Voice is not listed in either. Organization policies can restrict custom marketplaces. [Official marketplace documentation](https://code.claude.com/docs/en/discover-plugins).

## Claude Desktop and Cowork plugin

1. Open **Customize → Plugins**. In Cowork, open the Cowork tab first.
2. Under **Personal plugins**, select **+ → Add marketplace → Add from a repository**.
3. Enter `https://github.com/OmShiv/author-voice`.
4. Install **Author Voice** from the added marketplace.
5. In a conversation, type `/` or use the `+` menu to select the plugin's skill.

These steps add the project's GitHub catalog directly. They do not depend on finding Author Voice in Anthropic's default catalog. [Official Claude plugin instructions](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

## Claude chat skill upload

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

In Claude Code, choose user scope to make the plugin available across projects. In a new conversation, invoke the skill explicitly with a short sample to check that it is available.
