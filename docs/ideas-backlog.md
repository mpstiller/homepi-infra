> **Status update 2026-11-06:** Paperless-ngx is no longer only an idea or a pending discovery session. It is deployed, secured via private Tailscale HTTPS, backup/isolated restore tested with synthetic docs, and in active personal document use. Original proposal text below is retained as historical exploration. Refer to `CURRENT_STATE.md` and `docs/paperless-pilot.md` for current state. Other ideas stay uncommitted.

# Ideas backlog

Recorded 2026-11-03 from the owner's exploratory self-hosting discussion. This is a collection of options, not a deployment commitment. No services were installed or configured for these ideas.

## Next session: Paperless-ngx discovery

The owner chose Paperless-ngx as the next experiment, starting in a NEW session. First understand their actual needs, then research current official recommendations, propose a tailored setup and only then implement it together in short Pi steps. Do not begin research, installation or document imports as part of this backlog-only session.

Start with [Paperless discovery brief](paperless-discovery.md). The earlier overview is initial inspiration, not a completed architecture or configuration review.

## Options

Resource notes below are planning judgments, not measured footprints or compatibility guarantees. The existing Pi 5 has 4 GB RAM and many active workloads; verify current ARM64 support and real headroom before selecting any deployment.

| Idea | Concrete value / possible personal use | Status and constraints | Starting source |
|---|---|---|---|
| Paperless-ngx | Searchable archive of invoices, contracts, house paperwork and equipment documents; OCR, correspondence and workflows | NEXT: discovery and research in a new session. No installed stack, finalized taxonomy or import plan | https://docs.paperless-ngx.com/ |
| Karakeep (formerly Hoarder) | Save design products, AI research, travel ideas and HomePi guides; search and organize saved links, notes and images | Candidate; evaluate minimal vs crawler/search stack and memory peaks. AI optional; disclose external processing before enabling it | https://docs.karakeep.com/ |
| Shared household dashboard | Calendar, shopping, messages, weather, temperatures, light/music actions | Already represented by ROADMAP household e-ink project; extend that item, not a second infrastructure dashboard. Browser/tablet prototype first; hardware later | Existing ROADMAP.md P3; Home Assistant and Music Assistant already installed |
| n8n | Cross-app workflows: research digests, document intake or proposed calendar/task entries | Candidate; choose one concrete workflow first. External APIs/LLMs may have costs and data-processing implications; no large local model assumed | https://n8n.io/workflows/categories/personal-productivity/ |
| AdGuard Home | DNS-based ad/tracker filtering, including compatible smart devices | Candidate; test one client before household DNS dependency. Does not reliably remove YouTube ads or sponsored social posts | https://github.com/AdguardTeam/AdGuardHome |
| Nextcloud | Shared file space plus optional calendar, contacts and other apps | Extends existing file-cloud evaluation; compare actual need with existing providers. Consider a reduced setup; full Hub/Office stack not assumed suitable on the busy 4-GB Pi | https://nextcloud.com/home-users/ ; https://docs.nextcloud.com/server/stable/admin_manual/installation/system_requirements.html |
| Radicale | Private CalDAV/CardDAV calendar and contacts sync | Alternative if only calendar/contacts are needed; primarily a sync server, not a full groupware UI. Check phone/client access, sharing and reliability expectations | https://radicale.org/ |
| copyparty | Private browser file transfers, resumable uploads and WebDAV | Lean file-serving candidate; not automatically a full Dropbox/Nextcloud replacement. Define access and backup scope before use | https://github.com/9001/copyparty |
| Mealie | Recipe import, meal planning and shopping lists | Exploration only. Existing quoernchenkueche stays on its current cloud hosting; no replacement/migration decision | https://github.com/mealie-recipes/mealie |
| Actual Budget | Private household budgeting and expense planning | Candidate if active budgeting is wanted; bank/ DKB compatibility not researched. Optional encryption does not automatically protect bank-sync credentials | https://actualbudget.org/docs/ |
| Wallos | Subscription inventory and recurring payment overview | Candidate that could build on the owner's previous subscription inventory; do not assume automatic transaction detection | https://github.com/ellite/Wallos |
| changedetection.io | Website changes, product availability, price or event-page alerts | Candidate; choose useful targets and distinguish basic HTTP checks from heavier browser rendering; respect site access rules | https://github.com/dgtlmoon/changedetection.io |
| FreshRSS | Personally curated AI, music and design feeds | Candidate; verify preferred iPhone reading workflow and source feed availability before deployment | https://www.freshrss.org/ |
| Audiobookshelf | Own audiobook/podcast collection and listening workflow | Candidate only if an existing collection/use case justifies another media service; check current iOS client options | https://audiobookshelf.org/docs/documentation/introduction/ |
| Dawarich | Private travel/location history, maps and trip memories | Later exploration; sensitive location history and multi-service resource needs. Do not enable tracking automatically | https://dawarich.app/docs/intro/ |

## Existing plans retained

- Photo cloud/Immich stays deferred under ADR-009 until resources justify it; this discussion did not reverse that decision.
- HDD purchase remains usage-driven; no new hardware purchase is selected.
- Existing production web apps remain on Vercel/Supabase under ADR-010.
- Matter is installed and owner-tested; it is no longer a new-service idea.
- Existing Homepage, backup, status and Arcane tools are not duplicated just to add more monitoring services.
- Device-based Seerr/Tailscale automatic login was explored and explicitly deferred by the owner; nothing was installed or changed for it.
- Current discussion picks Paperless first; the other ideas are unordered candidates, not an agreed installation queue.

## How to promote an idea

Define the daily problem and intended users, compare with current tools, verify current upstream support and resource headroom, agree the smallest useful trial and its backup/rollback/access plan. Add implementation tasks to ROADMAP only when chosen. No universal star counts or trend ranking are treated as evidence of suitability.
