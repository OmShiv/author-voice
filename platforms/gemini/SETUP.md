# Gemini

If you downloaded `author-voice-gemini.zip`, unzip it and skip the build step. Use its `instructions.md`, `author-voice-knowledge.md`, and optional `starter-profile.md` in the steps below.

1. Build the packages with `python3 scripts/build.py`.
2. On the Gemini website, open **Gems → New Gem**.
3. Name it **Author Voice** and paste `platforms/gemini/instructions.md` into Instructions.
4. Optionally add `platforms/shared/knowledge.md` as `author-voice-knowledge.md`, and your own profile, under Knowledge.
5. Preview it with one of the cases in `evals/cases.json`, then save.

Use a custom instruction-based Gem, not a generated multi-step mini-app. Keep the supplied instructions as written initially so the preview tests the packaged method. Google's documentation describes instructions, knowledge files, preview, and saving. [Official Gem setup](https://support.google.com/gemini/answer/15146780?hl=en&co=GENIE.Platform%3DDesktop).

Begin a draft inside the Gem to apply the method during generation. For an existing chapter, attach or paste the text and request a light revision in book mode. Carry the same author profile between platforms.

`dist/author-voice-gemini.zip` is a convenience bundle of files to paste or attach; it is not an importable Gem manifest. Create and save the Gem through your account UI. No Gem or Google Doc was created in your account during this build.

To distribute a tested Gem, use its **Share** control, choose **Anyone with the link**, and grant **Viewer** access. Use only public package knowledge in the shared Gem; add private manuscripts or personal voice samples in a private copy. Confirm the link works for a recipient before publishing it. Sharing availability can depend on account or administrator settings. [Official Gem sharing instructions](https://support.google.com/gemini/answer/16504957?hl=en).

A Gem's knowledge files do not install Python or a Google Docs editing API. Use the host's available export/document capabilities, or transfer the revised source into your document workflow. The supplied study contains no Gemini measurements; there are no invented Gemini-specific style rules here. Platform documentation checked September 12, 2026.
