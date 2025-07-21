

function Run {
    param (
        [string]$VM,
        [string]$ScriptPath,
        [string]$CMD

    )
    # --protected-settings: 执行该脚本的命令，不会明文显示。
    az vm extension set --resource-group $env:rg --vm-name $VM --name customScript --publisher Microsoft.Azure.Extensions --version 2.1 --settings "{`"fileUris`":[`"$ScriptPath`"]}" --protected-settings "{`"commandToExecute`": `"$CMD`"}"
}

if ($args.Count -gt 0) {
    Invoke-Expression ($args -join " ")
}

