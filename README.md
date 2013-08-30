Irssi Notifier Using Redis
==========================
*Running irssi on a remote server and want to receive notifications on your local computer?*

This irssi notifier uses Redis to connect your local computer to your remote irssi.
Notifications will be displayed using the Freedesktop Notifications, meaning you'll see a nice notification bubble when you're on Ubuntu.

Install
=======

Irssi server
------------
* Install Redis server: http://redis.io/download
* Install Redis with cpan: http://search.cpan.org/~melo/Redis-1.955/lib/Redis.pm
* Place notify_redis.pl in ~/.irssi/scripts/autorun
* Edit notify_redis.pl to configure your Redis server
* Start irssi and type;
<pre>
/load perl
/script load autorun/notify_redis.pl
</pre>

Local client
-------------
* Install redis-py: https://github.com/andymccurdy/redis-py
* Copy config.dist.py to config.py and enter the correct settings
* Start listen_redis.py
* Enjoy!

Security
========
Don't forget to secure your server and enable the requirepass option in your redis.conf.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/TrafeX/irssi-notifier-redis/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

