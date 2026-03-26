# Project Guidelines

## Project Overview
This project is a Python + Tkinter + MySQL desktop application for a second-hand marketplace system.

Core features include:
- user signup and login
- post creation and search
- chat between users
- profile view
- review and rating flow

The codebase is primarily organized under:
- `second_hand_marketplace/database.py`
- `second_hand_marketplace/config.py`
- `second_hand_marketplace/ui_views/`

## Editing Principles
- Keep edits minimal and focused.
- Preserve current behavior as much as possible.
- Do not refactor unrelated logic.
- Do not rename files unless absolutely necessary.
- Do not redesign UI layout unless required to fix a bug.
- Prefer small, safe changes over broad rewrites.

## Audit Expectations
When auditing code:
- read all relevant Python files before making changes
- report issues with file name and line number where possible
- separate findings into:
  - security vulnerabilities
  - bugs
  - structural problems

## Security Rules
- Never hardcode database credentials in source files.
- Store DB connection settings in `.env`.
- Load DB configuration through `config.py`.
- Never commit `.env`.
- Add `.env` to `.gitignore`.
- Use `bcrypt` for password hashing and verification.
- Do not store or compare plaintext passwords directly.

## Database Rules
- Do not use a global database connection object.
- Use `get_connection()` from `database.py` for all DB access.
- Open connections locally where needed.
- Close connections in a `finally` block.
- Keep SQL changes minimal unless required for a bug fix or security fix.
- Do not modify schema definitions unless explicitly requested.

## Path Handling Rules
- Do not use hardcoded absolute local paths such as `C:\Users\...`.
- Use relative paths with `os.path.dirname(__file__)` and `os.path.join()`.
- Assume image assets are stored under `assets/images` relative to the project root.
- Preserve existing UI behavior when replacing paths.

## Code Structure Preferences
- Avoid adding more business logic directly into UI event handlers if a small helper function can contain it.
- Keep helper logic small and localized.
- Do not introduce large architectural changes unless explicitly requested.
- Avoid fragile `sys.path` manipulation unless there is no safer minimal alternative.
- When updating legacy code, prefer minimal compatibility-preserving fixes.

## Validation
After making changes, if possible:
- run a quick syntax check
- run a quick import check
- report any files that could not be safely validated
- clearly state any assumptions made

## Output Expectations
When asked to modify code:
- summarize all modified files
- explain each change briefly
- mention remaining risks, limitations, or follow-up items

## Current Project Priorities
When working on this repository, prioritize the following:
1. security fixes
2. correctness bugs
3. connection handling improvements
4. path portability
5. minimal structural cleanup

## Known Preferred Patterns
- config from `.env` via `config.py`
- password hashing with `bcrypt`
- database access through `get_connection()`
- relative asset paths
- minimal edits with low regression risk

## Language
- Code comments may be in Korean — preserve them as-is.
- Do not translate Korean comments to English.