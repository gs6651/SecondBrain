
# Fedora Tweaks

- To enable FlatHub
  - `flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo`
- Add SSH private key to the ssh-agent
  - `ssh-add ~/.ssh/id_ed25519`

## Google Chrome Installation

1. Download google chrome *.rpm file
2. Navigate to that folder
3. `sudo dnf install google-chrome-stable_current_x86_64.rpm`

## Misc. Apps Needed

- VLC from "Flathub"
- GIMP
- KdenLive
- Audacity
- Chrome
- Okular
- MuseScore Studio
- VScode

## To check the hostname & other system details

- `hostnamectl`
- `sudo hostnamectl set-hostname --static "NewHostname"`
