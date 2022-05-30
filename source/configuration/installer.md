# Installer

[Installer](../installation/vps-installer) is implemented as [Ansible](https://www.ansible.com/) collection and is configured the same way as other Ansible roles - by putting variable definitions in place where Ansible can read them.

Ansible supports [multiple levels of variable precendence rules](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable). Unless you want to incorporate installer in your own custom playbook, it's best to define variables in inventory file - just as it was shown on [installer](../installation/vps-installer.md#preparing-installation-environment) page.

Default values of variables listed below can be found in [`roles/set_variables/defaults/main.yml`](https://github.com/KustoszApp/kustosz-installer/blob/main/roles/set_variables/defaults/main.yml) file inside installer repository.

## `system_user_name`

Username of system user that will run Kustosz. User is created automatically, unless `run_system_requirements_root` is set to `false`.

## `system_user_home`

Path to home directory of system user that will run Kustosz. Is created automatically when creating user. Most of paths mentioned below are by default constructed relative to this directory.

## `system_user_shell`

Shell of system user that will run Kustosz. Is set automatically when creating user. Should be POSIX-compliant (i.e. **not** [fish](https://fishshell.com/)). There's little reason to log in as Kustosz user, apart from occasional maintenance task.

## `run_system_requirements_root`

When `false`, during first phase installer will not run steps that require superuser permissions. These steps are: installing system packages, starting and enabling NGINX and Redis system services, creating system user, ensuring `system_user_home` directory is globally readable.

Set to `false` only when you don't have root permissions on the machine.

## `use_postgres`

When `true`, installer will install system packages required to build psycopg2 (Python PostgreSQL driver), as well as psycopg2 itself in Kustosz virtual environment. This preapres your system to use Kustosz with PostgreSQL database.

Note that installer will **not** install Postgres itself, will not create Postgres database and will not configure Kustosz to connect with Postgres. Postgres configuration must be done manually.

## `use_system_nodejs`

When `true`, installer will use system-provided [Node.JS](https://nodejs.org/) instead of [NVM](https://github.com/nvm-sh/nvm). Node.JS is needed by [kustosz-node-readability](https://github.com/KustoszApp/kustosz-node-readability). While kustosz-node-readability should work on all Node.JS LTS versions, it is only tested with Node.JS 16.

Note that installer will **not** check if Node.JS is installed at all.

## `nodejs_version`

Node.JS version string passed to `nvm install`.

## `nvm_path`

Directory where NVM itself and NVM-managed Node.JS will be installed. This is called `NVM_DIR` by NVM.

## `use_system_python`

When `true`, installer will use system-provided [Python](https://www.python.org/) instead of [pyenv](https://github.com/pyenv/pyenv). Kustosz requires Python 3.9 or newer.

Note that installer will check Python version and will emit appropriate failure message if system-provided Python version is too old.

## `python_path`

Path to Python binary. Binary names will be searched for in `$PATH`.

## `pyenv_path`

Directory where pyenv itself and pyenv-managed Python will be installed. This is called `PYENV_ROOT` by pyenv.

## `pyenv_python_version`

Version of Python to install with pyenv. This is passed to `pyenv install` and used while checking if required Python version is already installed.

## `kustosz_frontend_version`

Version of [Kustosz web-ui](https://github.com/KustoszApp/web-ui) to install. Special string "latest" evaluates to latest released version.

## `kustosz_backend_version`

Version of [Kustosz server](https://github.com/KustoszApp/server) to install. Special string "latest" evaluates to latest released version.

## `venv_path`

## `force_install_backend`

## `force_install_frontend`

## `extra_python_packages`

## `kustosz_base_dir`

## `db_path`

## `settings_path`

## `frontend_path`

## `settings_local_path`

## `configure_nginx_server`

## `configure_system_services`

## `nginx_template_path`

## `kustosz_internal_port`

## `kustosz_nginx_listen`

## `kustosz_nginx_server_name`

## `kustosz_nginx_extra_config`

## `run_certbot`

## `certbot_extra_args`

## `systemd_dispatcher_path`

## `opml_path`

## `opml_local_path`

## `web_user_name`

## `web_user_password`
