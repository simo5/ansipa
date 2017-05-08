This is my first attempt at using Ansible, so it may not be the most polished
example to follow, that said.

The goal is to allow me to easily test more complex FreeIPA setups for basic
smoke testing.

This script requires local root access via ssh keys atm, this is used to deal
with libvirt atm.

The script variables are all in vars/guests.yml and they define the number of
hosts to create and their relationship to each other.

To run the script simply run ansible-playbook virt-guests.yml

Each time you run it, by default the actual guests are blown away and they are
recreated from a shared base disk which is crate the first time from scratch
using a fedora 25 dvd and a kickstart file.

If you are testing stuff and do not want to blow away and recreate the VMs add
a --skip-tags=destroy to your ansible command.
