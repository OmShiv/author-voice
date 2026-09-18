# Publish Author Voice

The first public release is version **0.1.0**, labeled beta, published from [OmShiv/author-voice](https://github.com/OmShiv/author-voice). Check [Releases](https://github.com/OmShiv/author-voice/releases) for downloadable packages. Curated directory submissions and host-level editorial evaluations are separate steps and have not been completed.

## 1. Set the publisher and repository

The publisher metadata is in [publishing/publisher.json](../publishing/publisher.json). The repository is `OmShiv/author-voice` and the license is MIT. Keep the full license text in both root `LICENSE` and `plugins/author-voice/LICENSE` for installers that fetch only the plugin directory. Keep `repository`, `homepage`, and `license` aligned in all three plugin manifests:

- `plugins/author-voice/plugin.json`
- `plugins/author-voice/.claude-plugin/plugin.json`
- `plugins/author-voice/.codex-plugin/plugin.json`

The public repository supplies the website, issue tracker, privacy notice, and terms URLs. Keep Issues enabled for support, and verify these URLs while signed out after pushing.

No separate server, model API subscription, OAuth app, or domain is needed for this skills-only package. A public URL is still required for each listing field.

## 2. Build and review the beta

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/prepare_submission.py --require-release --tag v0.1.0
```

The final command fails until release metadata, license, and archives are complete. Run it without `--require-release` to generate a draft submission pack while those choices are pending. It checks local files and URL syntax, not remote URL reachability or platform eligibility. Generated submission fields are a copying aid, not an official portal API schema.

| Output | Purpose |
| --- | --- |
| `dist/author-voice-plugin.zip` | Full native plugin, with portable and compatibility manifests |
| `dist/author-voice-skill.zip` | Named skill folder, references, and checker; Claude skill upload / OpenAI Skills bundle |
| `dist/author-voice-openai-marketplace.zip` | Complete local OpenAI marketplace for direct installation |
| `dist/author-voice-chatgpt.zip` | Portable instructions and knowledge for instruction-based assistants |
| `dist/author-voice-gemini.zip` | Files to configure a Gemini Gem |
| `dist/SHA256SUMS` | SHA-256 hashes for all five archives |
| `dist/submission/` | Listing fields, logo, policies, release notes, five positive and three negative test cases |

Run the cases in `dist/submission/reviewer-tests.md` against an installed plugin, starting a fresh conversation each time. Save actual responses and reviewer decisions outside `dist/`, which is regenerated. Record platform, model, date, and package version. Do not describe these specifications as passing results. The full 15-case suite is in [evals](../evals/README.md).

## 3. Make the GitHub release

Create the chosen public repository, review the source, commit it, and push the main branch. Ignore `dist/`, `.work/`, and personal manuscript files. The source research files are not in the distribution.

Once the checked commit is on `main`, create and push a version tag:

```sh
git tag -a v0.1.0 -m "Author Voice 0.1.0 public beta"
git push origin v0.1.0
```

In GitHub **Actions → Prepare draft release → Run workflow**, enter `v0.1.0`. The workflow checks out that existing tag, runs the tests, builds the five archives, enforces release metadata, and creates a **draft prerelease** with the archives and checksums attached. It does not publish automatically. Review the draft files and release notes, then publish the prerelease. GitHub CLI authentication is unnecessary for this workflow; it uses the repository's workflow token.

The validation workflow runs on main-branch pushes and pull requests with Python 3.10 and 3.14. The release workflow uses Python 3.14. These CI runs occur only after the repository is pushed; local validation does not imply CI has run.

## 4. Let Claude users install immediately

The root `.claude-plugin/marketplace.json` makes this repository a Claude Code marketplace. Users run these commands inside Claude Code:

```text
/plugin marketplace add OmShiv/author-voice
/plugin install author-voice@author-voice
```

Then invoke `/author-voice:author-voice`. Claude chat users download the skill ZIP from the GitHub release and follow [Claude setup](../platforms/claude/SETUP.md).

Direct repository distribution requires no Anthropic directory listing. For broader discovery, follow the submission options for [Anthropic's community marketplace](https://code.claude.com/docs/en/discover-plugins#community-marketplace), whose entries undergo automated validation and safety screening. Anthropic separately curates its official marketplace; community submission does not place a plugin there. Author Voice has not been submitted to either. [Official marketplace instructions](https://code.claude.com/docs/en/plugin-marketplaces).

## 5. Submit the native ChatGPT / Codex plugin

Open [OpenAI's plugin submission portal](https://platform.openai.com/plugins). Choose **Create plugin → Skills only**. The documented submission flow supports skills-only plugins, so this package needs no MCP backend. Use a verified individual or business publisher identity in the submitting organization, with the required Apps Management write access.

Copy the listing fields and starter prompts from `dist/submission/listing.json`. Upload `dist/submission/logo.png`; in Skills, upload the final skill bundle and check the imported file tree. Supply the public policy/support URLs, reviewer cases, regional availability, and release notes. Confirm that the imported instructions match the locally tested package before submitting.

Submit for review after testing and completing the portal attestations. Approval and publication are separate actions: after approval, publish from the portal to enter the shared ChatGPT/Codex Plugins Directory. The local marketplace ZIP does not create that public listing. [Official submission requirements and publishing flow](https://developers.openai.com/plugins/deploy/submission).

## 6. Share the Gemini version

Create the Gem using [Gemini setup](../platforms/gemini/SETUP.md), run the same synthetic evaluations, and use Gemini's sharing control if enabled for the account. For a public Gem, choose **Anyone with the link** with **Viewer** access. Attach only the package's public knowledge file to the public Gem; keep personal writing samples and manuscript material in private copies. Publish its share link in the repository README after checking the recipient experience. The GitHub release's Gemini ZIP remains a portable option people can configure themselves. [Official Gem sharing instructions](https://support.google.com/gemini/answer/16504957?hl=en).

## Update a published version

Keep all three manifest versions aligned, revise `publishing/release-notes.md`, rebuild, and run the checks. Create a new immutable version tag and a new draft release. Submit updated skills to each curated directory through its review flow; a GitHub push does not update a previously published directory snapshot.

Publishing documentation checked September 17, 2026. The publisher's actual portal eligibility and account UI have not been verified in this environment.
