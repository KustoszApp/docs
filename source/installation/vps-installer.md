# VPS (Raspberry Pi, DigitalOcean Droplet)

Automatic installer is designed to provide streamlined experience to majority of users. The idea is that you spin up virtual machine in the cloud, assign it domain, run installer and then you have fully operational Kustosz instance. To achieve this goal, installer performs few steps as **superuser** (root) that impact global state of the system:

* install [Redis](https://redis.io/), [NGINX](https://www.nginx.com/) and some packages needed to compile Python
* create new system user
* create NGINX virtual server configuration file, systemd unit file, and systemd unit Exec script
* enable systemd services for background tasks.

You can skip each of these steps, but Kustosz might not work correctly until you perform their equivalent on your system.

If you require greater flexibility than installer can provide, please read documentation on [manual installation](./vps).

## Prerequisites

Kustosz is web application. You probably want to access it from any network using dedicated (sub)domain. Configuration of domain and access control is outside of scope of this guide.

Kustosz needs at least 256 MiB of memory.

Installer must be run on Linux machine and it needs to be able to connect with the machine where Kustosz will be installed. You can run installer on the machine where Kustosz will be running.

You need superuser (root) access to machine where Kustosz is installed. You can configure installer to skip steps that require elevated permissions.

## Preparing installation

- create ansible venv
- install ansible
- install collection
- create playbook
    - mention kustosz_nginx_server_name, web_user_name, web_user_password, opml_local_path, settings_local_path
    - refer to backend configuration page
    - refer to installer configuration page


```{code-block} yaml
:caption: inventory.yml
:emphasize-lines: 5,8,9

all:
  children:
    kustosz:
      hosts:
        host_ip_or_name
      vars:
        ansible_port: 22
        ansible_user: 'name_of_user_to_connect'
        ansible_ssh_private_key_file: '/path/to/file/id_rsa'

        kustosz_nginx_server_name: "host_domain_name"
        web_user_name: kustosz
        web_user_password: kustosz
```

    # this requires ansible 2.11
    ansible-playbook kustosz.install.playbook -i ./inventory.yml


## Running the installer

- command to run
- provisioning
- now head to URL
