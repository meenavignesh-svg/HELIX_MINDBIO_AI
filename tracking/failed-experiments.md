# Failed Experiments

| S.No | Experiment | Date | Failure Type | Notes | Follow-up |
| ---: | --- | --- | --- | --- | --- |
| 1 | GitHub Actions every-minute schedule | 2026-05-24 | Platform limit | GitHub scheduled workflows do not reliably run every minute. | Use fastest supported schedule and manual dispatch when needed. |
| 2 | Mandatory Ollama on hosted runner | 2026-05-24 | Reliability risk | Hosted runners may fail installing, pulling, or running local models. | Prefer self-hosted runner for reliable Ollama. |
