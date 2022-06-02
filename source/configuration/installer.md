# Installer

[Installer](../installation/vps-installer) is implemented as [Ansible](https://www.ansible.com/) collection and is configured the same way other Ansible roles are - by putting variable definitions in place where Ansible can read them.

Ansible supports [multiple levels of variable precendence rules](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable). Unless you want to incorporate installer in your own custom playbook, it's best to define variables in inventory file - just as it was shown on [installer](../installation/vps-installer.md#preparing-installation-environment) page.

Default values of variables listed below can be found in [`roles/set_variables/defaults/main.yml`](https://github.com/KustoszApp/kustosz-installer/blob/main/roles/set_variables/defaults/main.yml) file inside installer repository.

## `system_user_name`

Username of system user that will run Kustosz. User is created automatically, unless `run_system_requirements_root` is set to `false`.

## `system_user_home`

Path to home directory of system user that will run Kustosz. Directory is created automatically when creating user. Most of paths mentioned below are by default constructed relative to this directory.

## `system_user_shell`

Shell of system user that will run Kustosz. Shell is set automatically when creating user. Should be POSIX-compliant (i.e. **not** [fish](https://fishshell.com/)). There's little reason to log in as Kustosz user, apart from occasional maintenance task.

## `run_system_requirements_root`

When `false`, during first phase installer will not run steps that require superuser permissions. These steps are: installing system packages, starting and enabling NGINX and Redis system services, creating system user, ensuring `system_user_home` directory is globally readable.

Set to `false` only when you don't have root permissions on the machine.

## `use_postgres`

When `true`, installer will install system packages required to build psycopg2 (Python PostgreSQL driver), as well as psycopg2 itself in Kustosz virtual environment. This prepares your system to use Kustosz with PostgreSQL database.

Note that installer will **not** install Postgres itself, will not create Postgres database and will not configure Kustosz to connect with Postgres. Postgres configuration must be done manually.

## `use_system_nodejs`

When `true`, installer will use system-provided [Node.JS](https://nodejs.org/) instead of [NVM](https://github.com/nvm-sh/nvm)-provided one. Node.JS is needed by [kustosz-node-readability](https://github.com/KustoszApp/kustosz-node-readability). While kustosz-node-readability should work on all Node.JS LTS versions, it is only tested with Node.JS 16.

Note that installer will **not** check if Node.JS is installed at all.

## `nodejs_version`

Node.JS version string passed to `nvm install`.

## `nvm_path`

Directory where NVM itself and NVM-managed Node.JS will be installed. This is called `NVM_DIR` by NVM.

## `use_system_python`

When `true`, installer will use system-provided [Python](https://www.python.org/) instead of [pyenv](https://github.com/pyenv/pyenv)-provided one. Kustosz requires Python 3.9 or newer.

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

Directory where Kustosz virtual environment will be created.

## `force_install_backend`

By default, installer tries to *not* install server package - it will do so only if it was unable to determine installed version, or when requested version is different than installed version. By setting this to `true`, installer will always create new virtual environment and install Kustosz backend server.

## `force_install_frontend`

By default, installer tries to *not* install frontend files - it will do so only if it was unable to determine installed version, or when requested version is different than installed version. By setting this to `true`, installer will always remove existing frontend files and download fresh copy from GitHub.

## `extra_python_packages`

Any extra packages you want to install in Kustosz virtual environment. This variable is passed to `python -m pip install`. You may use it to install memcached driver or force specific version of Django.

## `kustosz_base_dir`

Value of `$KUSTOSZ_BASE_DIR` environment variable. Kustosz will read settings from directory created here.

## `db_path`

Directory where default SQLite database file will be created.

## `settings_path`

Directory where `settings.yaml` and `settings.local.yaml` files will be put. Kustosz server requires this to be `$KUSTOSZ_BASE_DIR/settings`.

## `frontend_path`

Directory where frontend files will be downloaded. This is referenced in NGINX virtual host configuration file, so NGINX server user needs to be able to read it. If you decide to use [WhiteNoise](https://whitenoise.evans.io/en/stable/), that path should be referenced in `STATICFILES_DIRS`.

## `settings_local_path`

A **local** path to file that will become `settings.local.yaml` (see [Local files section on backend configuration page](./backend.md#local-files)). This file is input value to [`ansible.builtin.template`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html), which means that you can use [jinja2](https://jinja.palletsprojects.com/) and all the variables documented on this page.

## `configure_nginx_server`

When `false`, during post-installation phase installer will not run steps related to NGINX server configuration. These steps are: configuring SELinux variables to allow NGINX to make HTTP connections, creating Kustosz virtual host configuration file in `/etc/nginx/` and running certbot, assuming `run_certbot` is `true`.

Set to `false` when you don't have root permissions on the machine or when you don't use NGINX as HTTP server.

## `configure_system_services`

When `false`, during post-installation phase installer will not run steps related to system services configuration. These steps are: putting special dispatcher script in [`systemd_dispatcher_path`](#systemd-dispatcher-path), creating template service file under `/etc/systemd/system/`, and starting and enabling four background tasks for Kustosz (gunicorn server, two Celery workers, and Celery beat).

Set to `false` when you don't have root permissions on the machine or when you don't use systemd as init.

## `nginx_template_path`

A **local** path to file that will become NGINX virtual host configuration file. This file is input value to [`ansible.builtin.template`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html), which means that you can use [jinja2](https://jinja.palletsprojects.com/) and all the variables documented on this page.

## `kustosz_internal_port`

Port to which gunicorn (web server platform that runs Kustosz) process should bind to. Most of userspace web servers bind to port 8000, 8080, or similar, and depending on number of services you are running, the default port might be already taken.

## `kustosz_nginx_listen`

**External** port on which Kustosz should be accessible. NGINX must listen on this port. Usually it's 80 or 443.

This value is passed as argument to [NGINX `listen` directive](https://nginx.org/en/docs/http/ngx_http_core_module.html#listen).

## `kustosz_nginx_server_name`

Domain name of Kustosz instance. In standard NGINX setup, multiple sites listen on the same port, and NGINX matches request's `Host` header against `server_name` directive to decide which virtual host should handle specific request.

This value is passed as argument to [NGINX `server_name` directive](https://nginx.org/en/docs/http/server_names.html).

## `kustosz_nginx_extra_config`

Anything you want to include in NGINX virtual host configuration file for Kustosz.

## `run_certbot`

When `true`, installer will run [`certbot`](https://certbot.eff.org/) to configure [Let's Encrypt](https://letsencrypt.org/) TLS certificate on virtual host.

Installer will **not** check if certbot is available or configured correctly - it blindly tries to run the binary. Set this to `true` only if you actually use certbot and have configured it on the machine.

## `certbot_extra_args`

Additional [command-line options passed to `certbot`](https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-command-line-options). By default, installer includes `--non-interactive`, `--nginx` and `--domains $kustosz_nginx_server_name`.

You need to ensure that certbot is able to run without any human interaction. At the very least, you should include `--agree-tos` and `-m EMAIL@example.com`.

## `systemd_dispatcher_path`

Path to background services dispatcher script used by systemd. Dispatcher script exists to ensure that background processes run with correct environment variables set.

## `opml_local_path`

**Local** path to directory with OPML files. Directory must exist.

When defined, installer will import OPML files into Kustosz.

## `opml_path`

Path on server where OPML files will be uploaded. When running installer on machine that will run Kustosz, this path should still be different than `opml_local_path`.

## `web_user_name`

User name that you will use to log in to Kustosz web interface.

## `web_user_password`

Password that you will use to log in to Kustosz web interface.
