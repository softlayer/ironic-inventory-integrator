# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.define 'ironic_inventory' do |ironic_inventory|

    ironic_inventory.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', '512', '--cpuexecutioncap', '25']
    end

    ironic_inventory.vm.network "private_network", ip: "192.168.99.12"

  end
end
