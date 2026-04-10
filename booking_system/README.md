# Online Reservation System for Teaching

This project implements a **group-based time-slot reservation website** for semester project demos.
It follows a **3-tier architecture** and runs with **Docker Compose** on Linux-style containers.

## 1. Assignment Requirement Coverage
- Online reservation website for groups of students: **Done**
- Teachers can collect preferences and assign demo slots: **Done**
- Runnable dockerized deployment: **Done**
- Linux programming and 3-tier website programming: **Done** (`Nginx + FastAPI + MySQL`)

## 2. System Architecture
- Presentation tier: `Nginx`
- Application tier: `FastAPI + Jinja2`
- Data tier: `MySQL`

Main file: `docker-compose.yml`

## 3. Core Functions
### Teacher
1. Create meeting
2. Import group roster (`text / csv / xlsx`)
3. Publish meeting code and group credentials
4. Send automatic notification emails for credentials, results, and next-round reminders
5. Run FCFS allocation
6. Start next round if some groups remain unscheduled

### Group
1. Login with meeting code + group code + password
2. Submit ranked preferences
3. Check final assigned slot

Authentication now uses signed server sessions after login, so passwords are no longer carried in page URLs.

## 4. Run Instructions
### Start
```bash
docker compose -p reservation up --build -d
```

### Access
- Home: `http://localhost`
- Teacher login: `http://localhost/teacher/login`
- Group login: `http://localhost/group/login`

### Stop
```bash
docker compose -p reservation down -v
```

## 5. SMTP Email Configuration
Real email delivery is controlled by environment variables passed into the backend container. Docker Compose reads these values from a local `.env` file in the project root.

### Step 1. Create `.env`
Copy `.env.example` to `.env`.

Windows PowerShell:
```powershell
Copy-Item .env.example .env
```

Linux / macOS:
```bash
cp .env.example .env
```

### Step 2. Fill the SMTP fields in `.env`
Required fields:
- `APP_SECRET`: any long random string used for signed session cookies and password hashing.
- `BASE_URL`: the externally accessible site URL, for example `http://localhost` during local demo or your campus server URL during deployment.
- `SMTP_ENABLED=true`
- `SMTP_HOST`: your mail server hostname, for example `smtp.office365.com`
- `SMTP_PORT`: usually `587` for TLS or `465` for SSL
- `SMTP_USERNAME`: the sender mailbox account
- `SMTP_PASSWORD`: the mailbox password or app password
- `SMTP_USE_TLS=true` when using port `587`
- `SMTP_USE_SSL=true` when using port `465`
- `MAIL_FROM`: the address shown in outgoing email

Recommended example for TLS on port `587`:
```env
APP_SECRET=replace-with-a-long-random-secret
BASE_URL=http://localhost
SMTP_ENABLED=true
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=your_account@example.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TIMEOUT=15
MAIL_FROM=your_account@example.com
```

Recommended example for SSL on port `465`:
```env
APP_SECRET=replace-with-a-long-random-secret
BASE_URL=http://localhost
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=your_account@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=false
SMTP_USE_SSL=true
SMTP_TIMEOUT=15
MAIL_FROM=your_account@gmail.com
```

### Step 3. Restart the stack after editing `.env`
```bash
docker compose -p reservation down
docker compose -p reservation up --build -d
```

### Step 4. Verify delivery
Create a meeting and check:
1. The teacher mailbox receives the meeting code and teacher password.
2. Each group mailbox receives its group code and password.
3. After allocation, assigned groups receive result emails.
4. If a next round is opened, unscheduled groups receive reminder emails.

If `SMTP_ENABLED=false`, the same email content is still generated but printed in `reservation-backend` logs for demo purposes.

Check backend logs:
```bash
docker logs reservation-backend --tail 100
```

## 6. Demo Data
- `demo_data/groups_demo.csv`
- `demo_data/schedule_round1.txt`
- `demo_data/schedule_round2.txt`

## 7. Demo Scripts
- `scripts/demo_run.ps1` : deterministic full demo flow. By default it clears old containers and the MySQL volume, rebuilds the stack, and then runs create -> submit -> allocate -> optional round 2.
- `scripts/demo_reset.ps1` : reset containers and database volume
- `scripts/demo_check.ps1` : quick container/runtime check

Run full demo:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_run.ps1
```

Skip database reset only when you intentionally want to keep current data:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_run.ps1 -NoResetDb
```

`scripts/demo_record.ps1` keeps its own deterministic reset flow and then calls `demo_run.ps1 -NoResetDb`.

## 8. Accounts
### Teacher account
Teacher `meeting_code` and `teacher_password` are generated after each meeting creation.

### Group accounts (from `demo_data/groups_demo.csv`)
- `G01 / g01pass`
- `G02 / g02pass`
- `G03 / g03pass`
- `G04 / g04pass`
- `G05 / g05pass`
- `G06 / g06pass`
- `G07 / g07pass`
- `G08 / g08pass`

## 9. Notes
- DB host port is `3308` to avoid common local conflicts.
- The project uses mirror-friendly images suitable for CN network environment.
- New meetings store teacher and group passwords as hashes in MySQL.
- Teacher and group pages use signed server sessions after login, so sensitive credentials are not carried in URL query strings anymore.
