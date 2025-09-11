
# git commands to start with

``` shell
git --version
where git
git config --global user.name "Name"
git config --global user.email "email.com"
```

## Git Commands

``` shell
git commit -m "Message Here"
git push -u git@github.com:<repo>.git
git clone: First-time, full copy.
git clone --depth 1 git@github.com:<repo>.git ~/Documents/Foo/Bar # Will just clone the repo, not the history
git fetch: Check for updates, store them, but don’t mix yet.
git pull: Check for updates, store them, and update your files.
git stash: Temporarily store all modified tracked files.
git stash pop: To retrieve your previously saved changes
```

### Permission Error (SSH)

`ssh-add ~/.ssh/id_ed#####` where `id_ed####` = your private key name, should be in the folder: /home/`user`/.ssh/`id_ed#####`

### Enable SSH service/agent on `Windows`

> By default the ssh-agent service is disabled. Configure it to start automatically.
> Make sure you're running as an Administrator.
> `get-Service ssh-agent | Set-Service -StartupType Automatic`

- Start the service:
  - `start-Service ssh-agent`
- This should return a status of Running
  - `get-Service ssh-agent`

```shell
ssh-add <complete-key-path-here>

Key Path Example: C:\Users\so\.ssh/key-name
```
