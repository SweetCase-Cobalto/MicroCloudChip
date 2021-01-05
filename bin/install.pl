print "MicroCloudChip Installer\n";
print "Version 0.2.0 Alpha1 in 2021.01.04\n";
print "\n";
print "Before Install, please write some config\n";

# Set Main Root
$main_root = "";
$default_root = "/home/" . getpwuid($<) . "/microcloudchip";
$install_root = "/home/" . getpwuid($<) . "/.microcloudchip";

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
$port = "0";
$default_port = "8000";

while($port <= 1023) {
    printf "[2] set your port.[default %s]>", $default_port;
    $port = <STDIN>;
    chomp($port);
    if(length($port) == 0) {
        print "ok, port will be default port: $default_port\n";
        $port = $default_port;
        last;
    }
	elsif($port <= 1023) {
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
    if($ip =~ /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/) {
        print "ok\n";
        last;
    }
}

$start_path = `pwd`;
chomp($start_path);

#remove bin for install main path
$bin_token = index($start_path, "/bin");

substr($start_path, $bin_token) = "";

#setting directory
system "mkdir", $main_root;
system "mkdir", $install_root;

chdir $install_root;

# Write Python root
$python_root = $install_root . "/chip-venv/bin/python";

# write setting.cfg
print "write setting.cfg\n";
open(FH, ">setting.cfg");
print FH "main root:" . $main_root . "\n";
print FH "ip:" . $ip . "\n";
print FH "port:" . $port . "\n";
print FH "python root:" . $python_root;
close(FH);

# install python venv
print "install python venv\n";
system "mkdir", "chip-venv";
system "python3", "-m", "venv", "chip-venv", "chip-venv";

# move to microcloudchip and install requirements
print "install python modules\n";
chdir $start_path;
system $python_root, "-m", "pip", "install", "-r", "requirements.txt";

print "migrate Django DB\n";
chdir "app";

system $python_root, "manage.py", "makemigrations";
system $python_root, "manage.py", "migrate";
system $python_root, "manage.py", "makemigrations", "app";
system $python_root, "manage.py", "migrate", "app";

print "\n\n";
print "================================================\n";
print "Complete To Install\n";
print "Now If you want to run, perl run.pl\n";
print "Or If you want to check or change config\n";
print "You Can access " , $install_root . "/setting.cfg\n";
