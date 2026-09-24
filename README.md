# Campus Event Hub

A Flask + SQLite campus event management application prepared for SAD Lab 4.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Main routes

- `/` - event dashboard
- `/add-event` - create an event
- `/register/<event_id>` - register for an event
- `/registrations` - view registrations
- `/health` - deployment health check

The Dockerfile is included for the Lab 4 deployment/CD steps.
Developer 2 contribution for SAD Lab 4.