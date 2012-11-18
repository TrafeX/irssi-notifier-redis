#!/usr/bin/env perl
#
# Irssi notifier using Redis
#
# Copyright (c) 2012, Tim de Pater <code AT trafex DOT nl>
# <https://github.com/TrafeX/irssi-notifier-redis>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Based on irssi-notify from Luke Macken

use strict;
use Irssi;
use Redis;
use vars qw($VERSION %IRSSI);

$VERSION = "1.00";
%IRSSI = (
    authors     => 'Luke Macken, Tim de Pater',
    contact     => 'code@trafex.nl',
    name        => 'notify_redis.pl',
    description => 'Send notifications from highlights or private messages to Redis',
    license     => 'GNU General Public License',
    url         => 'http://www.trafex.nl',
);

sub priv_msg {
	my ($server,$msg,$nick,$address,$target) = @_;
    $msg =~ s/[^a-zA-Z0-9 .,!?\@:\/\>\=]//g;

    my $redis = Redis->new(server => 'localhost:6379', password => false);
    $redis->publish('irssi', "Private Message  $nick> $msg");
}

sub notify {
    my ($dest, $text, $stripped) = @_;
    my $server = $dest->{server};

    return if (!$server || !($dest->{level} & MSGLEVEL_HILIGHT));

    $stripped =~ s/[^a-zA-Z0-9 .,!?\@:\/\>\=]//g;

    my $redis = Redis->new(server => 'localhost:6379');
    $redis->publish('irssi', "$dest->{target} $stripped");
}

Irssi::signal_add_last('message private', 'priv_msg');
Irssi::signal_add('print text', 'notify');
