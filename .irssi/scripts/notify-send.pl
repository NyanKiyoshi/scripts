# irssi-notify.pl
use Irssi;
use Net::DBus;
 
$::VERSION='0.0.1';
%::IRSSI = (
    authors => 'Haelwenn MONNIER',
    contact => '@lanodan',
    name => 'notify-send',
    description => 'Displays a pop-up message for message received',
    license => 'CC-BY-SA',
    );
 
my $APPNAME = 'irssi';
 
my $bus = Net::DBus->session;
my $notifications = $bus->get_service('org.freedesktop.Notifications');
my $object = $notifications->get_object('/org/freedesktop/Notifications', 'org.freedesktop.Notifications');
 
sub pub_msg {
    my ($server,$msg,$nick,$address,$target) = @_;
 
    if ($msg =~ $notify_nick) {
      $object->Notify("${APPNAME}:${server}", 0, 'info', "Public Message in ${target}", "$nick: $msg", [], { }, 3000);
    }
}
 
sub priv_msg {
    my ($server,$msg,$nick,$address) = @_;
    $object->Notify("${APPNAME}:${server}", 0, 'info', 'Private Message', "$nick: $msg", [], { }, 3000);
}
 
Irssi::signal_add_last('message public', \&pub_msg);
Irssi::signal_add_last('message private', \&priv_msg);
