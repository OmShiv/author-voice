# ChatGPT and Codex

## Native plugin

Run `python3 scripts/build.py` from the repository root. It creates a complete local marketplace at `dist/openai-marketplace`, including the plugin and `.agents/plugins/marketplace.json`.

To register that local source when you are ready to install:

```sh
codex plugin marketplace add ./dist/openai-marketplace
```

Open the ChatGPT desktop app's Plugins Directory, select the local **Personal** source, and install **Author Voice**. Restart the app if the source is not visible. Start a new conversation and choose Author Voice with `@`; in Codex, use `$author-voice`. Local source availability differs by surface; a local bundle is not a public directory listing. [Packaging and local marketplace instructions](https://developers.openai.com/plugins/build/plugins), [plugin use and invocation](https://learn.chatgpt.com/docs/plugins).

The bundle includes a portable root `plugin.json`, the supported `.codex-plugin/plugin.json` compatibility manifest, and one skill. It needs no MCP server. [Skills without MCP](https://developers.openai.com/plugins/build/skills).

Keep the registered directory in place. Rebuild it after edits; use your client's plugin refresh/update controls and start a new chat. The build does not register, install, or update an account's cached installation.

## Portable instructions

If you downloaded `author-voice-chatgpt.zip`, unzip it first. Use its `instructions.md`, `author-voice-knowledge.md`, and optional `starter-profile.md`; no build is needed for that bundle.

For an existing Custom GPT or project that accepts instructions, paste `instructions.md` into its instruction field. Optionally upload `../shared/knowledge.md` under the name `author-voice-knowledge.md`, plus your profile. The same files are in `dist/author-voice-chatgpt.zip` for convenient sharing; the ZIP is not a Custom GPT import format.

A dedicated chat can use the instructions as its first message when configuration is unavailable. Critical fidelity rules are in the instructions; optional knowledge is not needed for ordinary edits. Avoid applying a manuscript style globally to unrelated tasks.

These files configure writing behavior. Native Google Docs edits and PDF generation depend on tools available to the conversation. Building the package does not install it into an account or create a public directory listing.
