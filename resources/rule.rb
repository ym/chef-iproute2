actions :add
default_action :add

attribute :src      , :kind_of => String, :required => true,
                      :name_attribute => true
attribute :table    , :kind_of => Fixnum, :required => true

attr_accessor :exists
