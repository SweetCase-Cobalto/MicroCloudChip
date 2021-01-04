print "MicroCloudChip Installer\n";
print "Version 0.2.0 Alpha1 in 2021.01.04\n";
print "\n";
print "Before Install, please write some config\n";

# Set Main Root
$main_root = "";
$default_root = "/home/" . getpwuid($<) . "/microcloudchip";

while (1) {
    printf "[1] set your main root.[default: %s]>", $default_root;
    $main_root = <STDIN>;
    chomp($main_root);
    if(length($main_root) == 0) {
        print "ok, main root will be default root: $default_root\n";
        $main_root = $default_root;
        last;
    }
    
    if( -d $main_root ) {
        last;
    } else {
        print "This directory does not exist\n";
    }
}

# Setting Port
$port = 0;
$default_port = 8000;

while($port <= 1023) {
    printf "[2] set your port.[default %s]>", $default_port;
    $port = <STDIN>;
    chomp($port);
    if(length($port) == 0) {
        print "ok, port will be default port: $default_port\n";
        $port = $defualt_port;
        last;
    }
    if($port <= 1023) {
        print "port range 1024 ~  65353\n";
    }
}


#Setting ip range
$ip = "0";
$default_ip = "0.0.0.0";
while(1) {
    printf "[3] set you ip range.[default %s]>", $default_ip;
    $ip = <STDIN>;
    chomp($ip);
    if(length($ip) == 0) {
        print "ok, ip range wil be default: $default_ip\n";
        $ip = $default_ip;
        last;
    }
    if($ip =~ /^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$/) {
        print "ok\n";
        last;
    }
}