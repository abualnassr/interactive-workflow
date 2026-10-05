# Cron registry — captured 2026-10-05 (from ~/.hermes/cron/jobs.json)

28 jobs total. `st` = last run status, `streak` = consecutive failures.

| id | job | schedule | enabled | last run | st | streak |
|---|---|---|---|---|---|---|
| 2ab26bc4f9a0 | context-factory | 0 */3 * * * | yes | 2026-10-05T06:14:18.267625+03:00 | ok | 0 |
| a77189a256bd | skills-factory | 45 */3 * * * | yes | 2026-10-05T03:59:35.728158+03:00 | ok | 0 |
| 5d7b5986300b | agents-factory | 30 1-23/3 * * * | yes | 2026-10-05T04:37:16.129892+03:00 | ok | 0 |
| 19c455715735 | loops-factory | 15 2-23/3 * * * | yes | 2026-10-05T05:19:42.009382+03:00 | ok | 0 |
| 0f83e6cf07a9 | ofm-daily-briefing | 0 9 * * * | yes | 2026-10-04T09:17:34.449902+03:00 | ok | 0 |
| 8d4f08a05067 | ofm-missing-metrics | 10 9 * * * | yes | 2026-10-04T09:25:01.169001+03:00 | ok | 0 |
| cba76d51fe34 | ofm-weekly-analytics | 20 9 * * 1 | yes | 2026-09-28T09:20:52.661735+03:00 | error | 1 |
| 2f281e578690 | ofm-asset-hygiene | 0 3 * * * | yes | 2026-10-05T03:20:17.326187+03:00 | error | 1 |
| 2ddbe890df74 | ig-daily-fetch | 26 * * * * | **no** | 2026-09-30T03:27:12.029467+03:00 | error | 20 |
| 1da58addf01d | ofm-stewardship-cycles | 45 8 * * * | yes | 2026-10-04T08:46:00.099319+03:00 | ok | 0 |
| 380f01f5ef93 | ofm-prompt-forge | 30 10 * * * | yes | 2026-10-04T10:39:22.954790+03:00 | ok | 0 |
| 725f8a0a01eb | ofm-daily-plan | 15 8 * * * | yes | 2026-10-04T08:24:48.872012+03:00 | ok | 0 |
| 0114b245ad6b | ofm-fanvue-billing | 30 9 * * * | yes | 2026-10-04T09:31:02.600093+03:00 | ok | 0 |
| e8ce5d2f4de2 | ofm-analytics-rows | 40 9 * * * | yes | 2026-10-04T09:40:55.526523+03:00 | ok | 0 |
| 3fb45b6b59ac | ofm-ig-health | 50 9 * * * | **no** | 2026-09-29T09:50:28.110020+03:00 | ok | 0 |
| b020396dacb7 | ofm-comment-scan | 0 10 * * * | yes | 2026-10-04T10:01:08.586617+03:00 | ok | 0 |
| 7ba8323a230d | ofm-policy-digest | 30 9 * * 1 | yes | 2026-09-28T09:30:53.003508+03:00 | error | 1 |
| a7475622e5be | ofm-backup-readback | 30 3 * * * | yes | 2026-10-05T03:31:17.053824+03:00 | error | 2 |
| 75b2f9734284 | ofm-fanvue-chatter | 45 10 * * * | yes | 2026-10-04T10:46:05.431608+03:00 | error | 1 |
| c923c12f1155 | lora-forge-biweekly | every 360m | yes | 2026-10-05T01:11:55.059445+03:00 | ok | 0 |
| 73e19abe221c | game-extract-obsidian-sync | every 30m | **no** | 2026-09-29T10:26:47.210905+03:00 | ok | 0 |
| 6ad8cbabae13 | game-extract-continuation-watchdog | every 120m | **no** | 2026-09-29T09:35:52.557412+03:00 | ok | 0 |
| 6519b41f9c60 | ig-pause-verify | once in 70m | **no** | 2026-09-30T04:47:54.462915+03:00 | ok | 0 |
| 2be74008ab60 | pawg-krea2-snapshot-watch | once at 2026-10-06 09:00 | yes | — | — | 0 |
| ddcbf26abd1e | studio-library-index | 20 8 * * * | yes | 2026-10-04T08:25:12.329985+03:00 | ok | 0 |
| 2edd3674019a | ofm-engagement-research | 0 11 * * 1 | yes | 2026-10-01T05:13:14.597469+03:00 | ok | 0 |
| 897d6ccdec4e | hermes-bug-loop | every 30m | yes | 2026-10-05T06:18:18.106710+03:00 | error | 15 |
| 9167a4e3b41f | ofm-fanvue-drop | 0 3 * * 2,4,6 | yes | 2026-10-03T08:26:53.976700+03:00 | ok | 0 |
