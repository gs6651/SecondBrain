
- To disable timer for shutdown / reboot
	- `gsettings set org.gnome.SessionManager logout-prompt false`
- To disable auto ON bluetooth 'AutoEnable=false'
	- `sudo nano /etc/bluetooth/main.conf`
- Minimize, Maximize Buttons
	- `gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'`
- 