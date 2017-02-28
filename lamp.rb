require 'ble'

# Selecter adapter
$a = BLE::Adapter.new('hci0')
puts "Info: #{$a.iface} #{$a.address} #{$a.name}"

# Run discovery
#$a.start_discovery
#sleep(2)
#$a.stop_discovery

# Get device and connect to it
$d = $a['F8:1D:78:60:0A:85']
$d.connect

# Dump device information
srv = :device_information
$d.characteristics(srv).each {|uuid|
  info  = BLE::Characteristic[uuid]
  name  = info.nil? ? uuid : info[:name]
  value = $d[srv, uuid] rescue '/!\\ not-readable /!\\'
  puts "%-30s: %s" % [ name, value ]
}