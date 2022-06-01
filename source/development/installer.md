# Installer

Installer is implemented as [Ansible](https://www.ansible.com/) collection. You need Ansible 2.9 or newer to run it. We recommend users to create disposable virtual environment and install Ansible from PyPI, so it's generally fine to support only latest released version of Ansible.

## Preparing development environment

Create virtual environment and install Ansible:

    python3 -m venv ~/kustosz-ansible-venv/
    . ~/kustosz-ansible-venv/bin/activate
    pip install --upgrade pip
    pip install ansible

You have to put installer files in a place where Ansible can find them. You can either clone directly to Ansible directory, or clone anywhere and bind-mount to Ansible directory:

```
# Option 1: Clone directly to Ansible directory
mkdir -p ~/.ansible/collections/ansible_collections/kustosz/install
git clone https://github.com/KustoszApp/kustosz-installer.git ~/.ansible/collections/ansible_collections/kustosz/install/

# Option 2: Clone anywhere and bind-mount
mkdir -p ~/.ansible/collections/ansible_collections/kustosz/install
git clone https://github.com/KustoszApp/kustosz-installer.git
sudo mount --bind ./kustosz-installer/ ~/.ansible/collections/ansible_collections/kustosz/install/
```

## Setting up Vagrant

You need a machine you can test installer on. We suggest using [Vagrant](https://www.vagrantup.com/), which provides easy way to manage local virtual machines.

You need Vagrant and plugin to virtual machine provider. [vagrant-libvirt](https://github.com/vagrant-libvirt/vagrant-libvirt) included in most distributions, making it one of the easiest to set up - just install vagrant and vagrant-libvirt packages, make sure libvirt system service is started, add your user to `libvirt` group and you are good to go. When in doubt, consult your distribution documentation.

In root directory of installer, create file named `Vagrantfile` with following content:

```{code-block} ruby
:caption: Vagrantfile

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "centos8", autostart: false do |centos8|
    centos8.vm.box = "generic/centos8"
    centos8.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  end
  config.vm.define "ubuntu2004", autostart: true do |ubuntu2004|
    ubuntu2004.vm.box = "generic/ubuntu2004"
    ubuntu2004.vm.network "forwarded_port", guest: 80, host: 8081, host_ip: "127.0.0.1"
  end
  config.vm.define "ubuntu2204", autostart: false do |ubuntu2204|
    ubuntu2204.vm.box = "generic/ubuntu2204"
    ubuntu2204.vm.network "forwarded_port", guest: 80, host: 8082, host_ip: "127.0.0.1"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/playbook.yml"
    ansible.verbose = "v"
  end
end
```

## Running current development version

Now you can use following commands:

* `vagrant up centos8` - create new CentOS machine, start it and run installer against it
* `vagrant provision centos8` - re-run installer against started virtual machine; useful for testing failure scenarios
* `vagrant ssh centos8` - ssh into started virtual machine
* `vagrant delete -f centos8` - stop and remove running virtual machine

Vagrant will automatically route network traffic from `host:` port to virtual machine. For example, you can access Kustosz running on Ubuntu 20.04 by opening [localhost:8081/ui](http://localhost:8081/ui/).

## Changing development version configuration

If you want to test impact of various [configuration variables](../configuration/installer), the best way is to create new file `playbooks/vagrant.yml` with following content:

```{code-block} yaml
:caption: playbooks/vagrant.yml

- name: "Install Kustosz on Vagrant"
  import_playbook: kustosz.install.playbook
  vars:
    use_system_python: true
    kustosz_nginx_server_name: "127.0.0.1 localhost"
    web_user_name: kustosz
    web_user_password: kustosz
    opml_local_path: /tmp/opmls
```

Change `Vagrantfile` to use new playbook during provisioning:

```{code-block} ruby
:caption: Vagrantfile


Vagrant.configure("2") do |config|
  # ...
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/vagrant.yml"
    ansible.verbose = "v"
  end
end
```
