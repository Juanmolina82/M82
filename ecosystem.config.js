module.exports = {
  apps: [
    {
      name: "m82-alerts",
      script: "./telegram_reporter.py",
      cwd: "/data/data/com.termux/files/home/M82",
      interpreter: "python3",
      autorestart: true,
      watch: false,
      env: { PYTHONUNBUFFERED: "1" }
    },
    {
      name: "m82-v21",
      script: "./macro_engine.py",
      cwd: "/data/data/com.termux/files/home/M82",
      interpreter: "python3",
      autorestart: true,
      watch: false,
      env: { PYTHONUNBUFFERED: "1" }
    },
    {
      name: "m82-v17",
      script: "./m82_market_scanner_v17.py",
      cwd: "/data/data/com.termux/files/home/M82",
      interpreter: "python3",
      autorestart: false,
      cron_restart: "0 2,4,9,12,16,19,21 * * *",
      watch: false,
      env: { PYTHONUNBUFFERED: "1", TZ: "America/Caracas" }
    },
    {
      name: "m82-ingestion",
      script: "./ingestion_gateway.py",
      cwd: "/data/data/com.termux/files/home/M82",
      interpreter: "python3",
      autorestart: false,
      cron_restart: "*/10 * * * *",
      watch: false,
      env: { PYTHONUNBUFFERED: "1" }
    },
    {
      name: "m82-health",
      script: "./health_monitor.py",
      cwd: "/data/data/com.termux/files/home/M82",
      interpreter: "python3",
      autorestart: false,
      cron_restart: "*/15 * * * *",
      watch: false,
      env: { PYTHONUNBUFFERED: "1" }
    }
  ]
};
