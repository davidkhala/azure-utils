- [Catalog admin page](https://accounts.azuredatabricks.net/data) allow user to manage **Metastore Admin**
  - Write permission: the Entra ID signed in must has `Account admin` role (see in Account console>`User management`), to have access more than workspace permission.

- **Workspace catalog**: default catalog in all new workspaces.
  - Azure will auto provision it
  - Named as your workspace name (with replacing `-` to `_`)