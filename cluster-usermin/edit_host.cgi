#!/usr/bin/perl
# edit_host.cgi
# Show details of a managed host, and all the modules on it

require './cluster-usermin-lib.pl';
&ReadParse();
&ui_print_header(undef, $text{'host_title'}, "");

@hosts = &list_usermin_hosts();
($host) = grep { $_->{'id'} eq $in{'id'} } @hosts;
$server = &foreign_call("servers", "get_server", $in{'id'});
@modules = @{$host->{'modules'}};
@themes = @{$host->{'themes'}};
@users = @{$host->{'users'}};
@groups = @{$host->{'groups'}};

# Show host details
print "<input type=hidden name=id value=$in{'id'}>\n";
print "<table border width=100%>\n";
print "<tr $tb> <td><b>$text{'host_header'}</b></td> </tr>\n";
print "<tr $cb> <td><table width=100%>\n";

print "<tr> <td><b>$text{'host_name'}</b></td>\n";
if ($server->{'id'}) {
	printf "<td>%s</td>\n",
		$server->{'desc'} ? $server->{'desc'} : $server->{'host'};
	}
else {
	print "<td>$text{'this_server'}</td>\n";
	}

if ($server->{'id'}) {
	print "<td><b>$text{'host_type'}</b></td> <td>\n";
	foreach $t (@servers::server_types) {
		print $t->[1] if ($t->[0] eq $server->{'type'});
		}
	print "</td>\n";
	}
print "</tr>\n";

print "<tr> <td><b>$text{'host_count'}</b></td>\n";
printf "<td>%d</td>\n", scalar(@modules);

print "<td><b>$text{'host_tcount'}</b></td>\n";
printf "<td>%d</td> </tr>\n", scalar(@themes);

print "<tr> <td><b>$text{'host_os'}</b></td>\n";
print "<td>$host->{'real_os_type'} $host->{'real_os_version'}</td>\n";

print "<td><b>$text{'host_version'}</b></td>\n";
printf "<td>%s</td> </tr>\n", $host->{'version'};

print "</table></td></tr></table>\n";

# Show delete and refresh buttons
print "<table width=100%><tr>\n";
print "<form action=delete_host.cgi>\n";
print "<input type=hidden name=id value=$in{'id'}>\n";
print "<td><input type=submit value='$text{'host_delete'}'></td>\n";
print "</form>\n";

print "<form action=refresh.cgi>\n";
print "<input type=hidden name=id value=$in{'id'}>\n";
print "<td align=right><input type=submit value='$text{'host_refresh'}'></td>\n";
print "</form>\n";
print "</tr></table>\n";

# Show table of modules and themes
print "<table border width=100%>\n";
print "<tr $tb> <td><b>$text{'host_header_m'}</b></td> </tr>\n";
print "<tr $cb> <td><table width=100%>\n";

$i = 0;
foreach $m (sort { $a->{'desc'} cmp $b->{'desc'} } @modules) {
	print "<tr>\n" if ($i%3 == 0);
	print "<td width=33%><a href='edit_mod.cgi?mod=$m->{'dir'}&host=$in{'id'}'>",$m->{'desc'},"</td>\n";
	print "</tr>\n" if ($i%3 == 2);
	$i++;
	}
if (@themes) {
	$i = 0;
	print "</table></td></tr>\n";
	print "<tr $tb> <td><b>$text{'host_header_t'}</b></td> </tr>\n";
	print "<tr $cb> <td><table width=100%>\n";
	foreach $t (sort { $a->{'desc'} cmp $b->{'desc'} } @themes) {
		print "<tr>\n" if ($i%3 == 0);
		print "<td width=33%><a href='edit_mod.cgi?theme=$t->{'dir'}$in{'id'}'>",$t->{'desc'},"</td>\n";
		print "</tr>\n" if ($i%3 == 2);
		$i++;
		}
	}
print "</table></td></tr></table><br>\n";

&ui_print_footer("", $text{'index_return'});

