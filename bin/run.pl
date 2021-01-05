$CURRENT_ROOT = `pwd`;
chomp($CURRENT_ROOT);
$install_root = "/home/" . getpwuid($<) . "/.microcloudchip";

$SETTING_FILE = $install_root . "/setting.cfg"; 

#	main root
#	ip
#	port
#	python root

open(FH, $SETTING_FILE);

print "get config data fron setting.cfg\n";
# get main root 
$raw_main_root = <FH>;
chomp($raw_main_root);
@splited_main_root_line = split(/:/, $raw_main_root); 
$main_root = $splited_main_root_line[1];

# get ip
$raw_ip = <FH>;
chomp($raw_ip);
@splited_ip_line = split(/:/, $raw_ip);
$ip = $splited_ip_line[1];

# get port
$raw_port = <FH>;
chomp($raw_port);
@splited_port_line = split(/:/, $raw_port);
$port = $splited_port_line[1];

#get python root
$raw_python_root = <FH>;
chomp($raw_python_root);
@splited_python_root_line = split(/:/, $raw_python_root);
$python_root = @splited_python_root_line[1];

# write to MicroCloudChip/app/app/config.json
# back to MicroCloudChip
@start_root_token_list = split('/', $CURRENT_ROOT);

$start_root_token_list_len = @start_root_token_list;

$origin_root = "";
for( $i = 0; $i < $start_root_token_list_len - 1; $i++) {
	$origin_root = $origin_root . $start_root_token_list[$i] . "/";	
}
chdir $origin_root . "app/app";

print "write to program config.json\n";
#rewrite config json
open(FH, ">config.json");
print FH "{\n\t\"root\": " . "\"$main_root\"" . "\n}";
close(FH);

print "Now Running Python Code\n";
chdir $origin_root . "app";
system $python_root, "manage.py", "runserver", $ip . ":" . $port;
