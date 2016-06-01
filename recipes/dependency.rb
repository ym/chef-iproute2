easy_install_package 'pyroute2'
easy_install_package 'netaddr'

easy_install_package 'click'


cookbook_file '/usr/sbin/iprule-smart-add' do
  source 'iprule-smart-add.py'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end
