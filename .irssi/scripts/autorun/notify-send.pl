use Irssi;
use vars qw($VERSION %IRSSI);

$VERSION = '0.0.3';
%IRSSI = (
    authors     => 'Chrelad',
    name        => 'notify',
    description => 'Display a pop-up alert for different events.',
    url         => 'http://google.com',
    license     => 'GNU General Public License',
);

$_nick = Client->{nick};

sub pub_msg {
  my ($server, $msg, $nick, $address, $target) = @_;

  if ($msg =~ $_nick) {
    `notify-send -a irssi -t 8000 "${target}: ${nick}" "${msg}"`;
  }
}

sub priv_msg {
  my ($server, $msg, $nick, $address) = @_;

  `notify-send -a irssi -t 8000 ${nick} ${msg}`;
}

Irssi::signal_add_last("message public", "pub_msg");
Irssi::signal_add_last("message private", "priv_msg");
