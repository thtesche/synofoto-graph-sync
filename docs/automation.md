# Automation (Task Scheduler)

To keep your graph database up-to-date, set up a task in the **Synology Task Scheduler**.

## Creating the Task

1. Open **Control Panel** -> **Task Scheduler**.
2. Click **Create** -> **Scheduled Task** -> **User-defined script**.
3. **General**: Task name `Photo-Graph-Sync`, User `root`.
4. **Schedule**: Set to Daily or hourly as desired.
5. **Task Settings**: Run command:

   ```bash
   cd /volume1/scripts/synofoto-graph-sync && ./venv/bin/python sync.py >> sync.log 2>&1
   ```

## Why root?
The task must run as `root` because the script needs access to the Synology Photos PostgreSQL Unix socket, which is restricted to the root user.

## Monitoring
The output is redirected to `sync.log` in the project directory. You can check this file to see the results of each run.
