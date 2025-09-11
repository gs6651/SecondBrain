
# Ubuntu

## De-Snap & Install Flatpak

- `sudo apt install flatpak gnome-software-plugin-flatpak`
  - `ps -p <Process ID>` and then `sudo kill 11420`
- `flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo`
- To Stop "snap":
  - `sudo systemctl stop snapd`
  - `ps -ef | grep snap`
  - `kill -9 <PID1> <PID2>`
  - `sudo systemctl stop snapd`
- `sudo apt remove --purge --assume-yes snapd gnome-software-plugin-snap`
- `rm -rf ~/snap/`
- `sudo rm -rf /var/cache/snapd/`
- `sudo rm -rf /root/snap/`
- `sudo find / -type d -name snap`
- Update File so snap won't get preference again ever:
  - `sudo nano /etc/apt/preferences.d/nosnap.pref`
    ```
    Package: snapd
    Pin: release a=*
    Pin-Priority: -10
    ```


## Firefox from Mozilla PPA

- `sudo add-apt-repository ppa:mozillateam/ppa`
- Set PPA Priority: `echo 'Package: * Pin: release o=LP-PPA-mozillateam Pin-Priority: 1001' | sudo tee /etc/apt/preferences.d/mozilla-firefox`
- Disable Ubuntu's Snap PPA `echo 'Package: firefox* Pin: release o=Ubuntu Pin-Priority: -1' | sudo tee -a /etc/apt/preferences.d/mozilla-firefox`
- `sudo apt update`
- `sudo apt install firefox-esr`
- `sudo snap remove firefox`


## Misc

- VScode: `sudo apt install ~/Downloads/code_1.103.2-1755709794_amd64.deb`
- Fender Studio: `flatpak install ~/Downloads/fenderstudio.flatpak`
- GIMP: `flatpak install ~/Downloads/org.gimp.GIMP.flatpakref`
- Kdenlive: `flatpak install flathub org.kde.kdenlive`
- Audacity: 
- LibreOffice:
  - To run the simulation before installation: `apt install -s libreoffice-writer`
  - Writer = `sudo apt install libreoffice-writer`
  - Calc = `sudo apt install libreoffice-calc`


What is WSL Ubuntu?
