# mirai-cinema

Live status for the C.MiraiItem "Mirai Cinema" VRChat video player.

- `status.txt` is read by every Mirai Cinema in VRChat (https://cmiravalue.github.io/mirai-cinema/status.txt).
- `status.py` + `.github/workflows/status.yml` check the VRChat status page twice an hour, update `status.txt`, and open an issue (email) when VRChat has an incident.
- Edit `status_manual.txt` to show your own message in every world, or to change player settings remotely.
