# Upgrade FR/DE/NL translations of already-upgraded EN pattern posts

Reuses the EN images (same media), translates only the new parts, reorders the sections like the EN post.

1. Browser (wp-admin tab): fetch EN + FR/DE/NL posts (`context=edit`), PUT them as one JSON `{id:{id,slug,link,modified,raw}}` to the Worker `/tmp/<batch>.json`.
2. Workspace: `curl -o b.json https://files.sewcraftlypatterns.com/_tmp/<batch>.json`
3. `python3 brief.py b.json <EN> <FR> ...` -> EN texts to translate (alts, captions, reading paragraphs, new FAQ).
4. Write `tr-<EN>.json` = `{fr:{alt[4],cap[2],reading[],faq[[q,a]]}, de:{...}, nl:{...}}` (pills and H3 have defaults; FR vous, DE du, NL je).
5. `python3 build.py b.json <EN> tr-<EN>.json <FR> <DE> <NL|-> out.json` -> integrity check (no original line missing; only inserted lines + FAQ schema added).
6. Push out.json to `tmpup/` of this repo, in the browser fetch raw by commit SHA and POST `{content}` to each post (skip if `modified` changed), then check the live pages and delete `tmpup/` + the Worker tmp file.
