$sankhara_ip = '10.107.110.2'
$phassa_ip = '10.107.110.3'

# Configuration of vagrant
def configure_vagrant
    Vagrant.configure(2) do |config|
        # See https://docs.vagrantup.com/v2/multi-machine/
        def common(config, hostname)
            config.vm.box = "debian/jessie64"
            config.vm.hostname = "vagrant-" + hostname + ".lan"
            # config.vm.box_url = "https://atlas.hashicorp.com/debian/boxes/" \
            #        + "jessie64/versions/8.0.3/providers/virtualbox.box"
            config.vm.synced_folder "salt/states", "/srv/salt"
            config.vm.synced_folder "salt/pillar", "/srv/pillar"
            config.vm.provision :salt do |salt|
                salt.run_highstate = true
                salt.verbose = true
                salt.minion_config = "salt/vagrant_minion_config"
            end
        end

        int = preferred_interface

        config.vm.define "sankhara", primary: true do |config|
            common config, "sankhara"
            config.vm.network :public_network, :bridge => int
            config.vm.network :private_network, ip: $sankhara_ip
        end

        config.vm.define "phassa" do |config|
            common config, "phassa"
            config.vm.network :public_network, :bridge => int
            config.vm.network :private_network, ip: $phassa_ip
        end

        # vagrant plugin install vagrant-cachier
        if Vagrant.has_plugin? "vagrant-cachier"
            config.cache.scope = :box
        end
    end
end

# Helpers (eg. generating passwords)
require 'yaml'
require 'securerandom'

def ensure_pillar_is_generated
    names = ['chucknorris', 'django_secret_key', 'apikey', 'mysql_giedo',
                'mysql_wiki', 'mysql_wolk', 'mysql_forum', 'mysql_root',
                'mysql_daan', 'mailman_default', 'ldap_infra',
                'ldap_daan', 'ldap_freeradius', 'ldap_admin',
                'wiki_key', 'wiki_upgrade_key', 'wiki_admin']

    path = File.join(File.dirname(__FILE__), 'salt', 'pillar', 'vagrant.sls')
    return if File.exists?(path) and File.mtime(path) >= File.mtime(__FILE__)

    puts 'Generating passwords ...'
    if File.exists? path
        pillar = YAML.load_file(path)
    else
        pillar = {'secrets' => {}}
    end

    # Generate secrets
    for name in names
        next if pillar['secrets'].include? name
        pillar['secrets'][name] = SecureRandom.hex
    end

    # Some other settings
    pillar['ldap-suffix'] = 'dc=vagrant-sankhara,dc=lan'
    pillar['ip-phassa'] = $phassa_ip
    pillar['ip-sankhara'] = $sankhara_ip

    File.open(path, 'w') do |f|
        f.write "# autogenerated by Vagrantfile"
        YAML.dump pillar, f
    end
end

def preferred_interface
    path = File.join(File.dirname(__FILE__), '.vagrant-network-interface')
    return false unless File.exists? path
    return File.open(path).read.strip
end

ensure_pillar_is_generated
configure_vagrant

# vi: set ft=ruby :
