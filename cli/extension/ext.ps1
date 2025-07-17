
$ErrorActionPreference = "Stop"
function Add {
    param (
        [string]$Module
    )
    az extension add --name $Module
}
function Add-Built {
    # Add self-built extension
    param (
        [string]$Path
    )
    az extension add --source "$Path.whl"
    
}
function Windows-Only {
    # List out Windows-only extensions
    Write-Output "account"
}
function List {
    # List available extensions
    az extension list-available --output table
    
}
if ($args.Count -gt 0) {
    Invoke-Expression ($args -join " ")
}