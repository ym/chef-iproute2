use_inline_resources

def whyrun_supported?
  true
end

action :add do
  include_recipe 'iproute2::dependency'

  execute "add_iprule_from_#{new_resource.src}_lookup_#{new_resource.table}" do
    command "/usr/sbin/iprule-smart-add #{new_resource.src} #{new_resource.table}"
  end

end
