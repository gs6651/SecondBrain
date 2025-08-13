### git commands to start with

```
git --version
where git
git config --global user.name "Name"
git config --global user.email "email.com"
```

### Git Commands
```
git push -u git@github.com:<repo>.git
git clone: First-time, full copy.
git fetch: Check for updates, store them, but don’t mix yet.
git pull: Check for updates, store them, and update your files.
git stash: Temporarily store all modified tracked files.
git stash pop: To retrieve your previously saved changes
```


### Permission Error (SSH)

`ssh-add ~/.ssh/id_ed#####`  id_ed#### = your private key name, should be in the folder: /home/<user>/.ssh/id_ed#####


### Enable SSH service/agent on Windows


```
Get-Service ssh-agent | Set-Service -StartupType Automatic

# By default the ssh-agent service is disabled. Configure it to start automatically.
# Make sure you're running as an Administrator.
```

```
Start-Service ssh-agent

# Start the service
```
```
Get-Service ssh-agent

# This should return a status of Running
```

```
ssh-add <complete-key-path-here>

Key Path Example: C:\Users\so\.ssh/key-name
```
