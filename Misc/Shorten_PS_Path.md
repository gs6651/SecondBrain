
- Run `Test-Path $Profile` to check if a profile file exists.
- If it returns `False`, create a profile file using `New-Item –Path $Profile –Type File –Force`.
- **Note:** This will create the profile file or overwrite the existing one. 
- Open the profile file using `notepad $Profile`
- Add the following function to the file and save

```    
function prompt {
        "PS " + (Get-Location).Drive.Name + ":\" + $( ( Get-Item $pwd ).Name ) + ">"
}
```
- Reopen PowerShell (or VS Code Terminal)
- ✌️


## Starship for PowerShell

- [Website](https://starship.rs/guide/)
- Download Fira Code. [here](https://www.nerdfonts.com/)
- Install Starship 
  - `winget install --id Starship.Starship`
- Set up your shell to use Starship
  - Add the following to the end of your PowerShell configuration (find it by running $PROFILE)
    - `Invoke-Expression (&starship init powershell)`
