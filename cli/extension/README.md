# Extension for the Azure CLI

Extensions for the Azure CLI aren't shipped as part of the CLI but run as CLI commands.
With extensions, you gain access to experimental and pre-release commands

- Characterized as Python wheels. It have the ability to write your own CLI module.

Please note that for different OS, available extensions are different.

## Popular extension

- `az interactive`: interactive mode
  - change `az` behavior to IDE. e.g. autocompletion, command descriptions
- `az vm extension set ...` 用来安装、配置虚拟机拓展
- `az vm extension set --name customScript --publisher Microsoft.Azure.Extensions`
  - Custom Script Extension: An easy way to download and run scripts on your Azure VMs