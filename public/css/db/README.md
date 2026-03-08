# Database Setup (MySQL)

This folder contains SQL for the basic `jarvisai` database.

## Steps
1. Open phpMyAdmin (XAMPP) or MySQL terminal.
2. Import `jarvis.sql`.
3. Update database settings in root `.env`:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_USER`
   - `DB_PASS`
   - `DB_NAME`
4. Set `DB_CONNECT=true` only if you need DB connection at runtime.

## Notes
- Current web dashboard mainly uses Weather + News APIs.
- `users` table is included for future authentication/features.
