# VPS (Raspberry Pi, DigitalOcean Droplet)

Automatic installer is designed to enable fully-operational Kustosz instance on machine where you have **superuser** (root) permissions. Read [](#impact-of-the-installer-on-the-system) section below for overview of changes that installer does to the system.

If you require greater flexibility than installer can provide, we have separate page discussing [manual installation](./vps).

Installer installs latest released version of Kustosz. You can re-run the installer to upgrade existing Kustosz instance to newer version.

## Prerequisites

Kustosz is web application. You probably want to access it from any network using dedicated (sub)domain. Configuration of domain and access control is outside of scope of this guide.

Kustosz needs at least 256 MiB of memory.

Installer must be run on Linux machine and it needs to connect with the machine where Kustosz will be installed. You can run the installer on the machine where Kustosz will be running.

You need superuser (root) access to machine where Kustosz is installed. You can configure installer to skip steps that require elevated permissions.

## Preparing installation environment

Installer is implemented as [Ansible](https://www.ansible.com/) collection with a playbook. You need Ansible 2.9 or newer to run it. Ansible must be installed on Linux, and you can install it on the machine where Kustosz will be running.

Many Linux distributions provide Ansible package. We recommend that you install Ansible in a disposable virtual environment:

    python3 -m venv /tmp/ansible-venv/
    . /tmp/ansible-venv/bin/activate
    pip install --upgrade pip
    pip install ansible

Now you can install the installer itself:

    ansible-galaxy collection install kustosz.install

The last piece is creating inventory file. It tells Ansible where your host is and allows you to configure the installer (see [Installer configuration](/configuration/installer.md) page).

```{code-block} yaml
:caption: inventory.yml
:emphasize-lines: 5,8,9, 10

all:
  children:
    kustosz:
      hosts:
        kustosz_server_ip_or_domain_name OR localhost
      vars:
        ansible_port: 22
        ansible_user: 'name_of_user_that_can_ssh_to_host'
        ansible_ssh_private_key_file: '/path/to/file/id_rsa'
        ansible_connection: local  # only if hosts is localhost

        web_user_name: kustosz
        web_user_password: kustosz
        settings_local_path: /tmp/kustosz/settings/settings.local.yml
        opml_local_path: /tmp/kustosz/opmls/
        kustosz_nginx_server_name: "kustosz.example.com"
        run_certbot: true
        certbot_extra_args: >
          --agree-tos
          --email somename@example.com
```

`vars` section is optional, but recommended. Apart from [Ansible connection variables](https://docs.ansible.com/ansible/2.9/reference_appendices/special_variables.html#connection-variables), you should consider setting following variables:

* `web_user_name` - user name that you will use while logging into Kustosz
* `web_user_password` - password that you will use while logging into Kustosz
* `settings_local_path` - **local** path to `settings.local.yaml` file (see [backend configuration](/configuration/backend.md) page)
* `opml_local_path` - **local** path to directory with OPML files that should be imported during installation
* `kustosz_nginx_server_name` - domain name of your Kustosz instance (technically, value of [`server_name` directive in NGINX configuration file](https://nginx.org/en/docs/http/server_names.html))
* `run_certbot` - whether [`certbot`](https://certbot.eff.org/) should be called to configure [Let's Encrypt](https://letsencrypt.org/) TLS certificate
* `certbot_extra_args` - additional [`certbot` command-line options](https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-command-line-options=)

Full list of variables recognized by the installer is available on [installer configuration](/configuration/installer.md) page.

## Running the installer

    ansible-playbook kustosz.install.playbook -i ./inventory.yml

When installer finishes, open [KUSTOSZ_SERVER_NAME/ui/](https://KUSTOSZ_SERVER_NAME/ui/) in your web browser to access Kustosz. 

If installer fails for any reason (usually due to intermittent problem with access to external resources), you can run above command again. Installer will automatically pick up where it left.

Running above command on server with Kustosz already installed is also safe, as installer will not make any changes that are not required. You can use the same command to upgrade Kustosz to the newest version.

## Impact of the installer on the system

Automatic installer is primarily designed with new systems in mind. The idea is that you spin up virtual machine in the cloud, assign it domain, run installer and then you have fully operational Kustosz instance. To achieve this goal, installer needs to change global configuration of the system.

Specifically, installer will:

* install [Redis](https://redis.io/), [NGINX](https://www.nginx.com/) and some packages needed to compile Python
* create new system user
* create NGINX virtual server configuration file, systemd unit file, and systemd unit Exec script
* enable systemd services for background tasks.

You can skip each of these steps, but Kustosz might not work correctly until you perform their equivalent on your system.

Everything else is done within the scope of separate system user and will not impact other services running on the system.
