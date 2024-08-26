#!/usr/bin/env bash
# prepares simple nginx servers for static deployment of `web-static`
if ! service nginx status &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
    if ! find /var/www/html/index.html &> /dev/null; then
        mkdir -p /var/www/html/
        echo 'Holberton School' > /var/www/html/index.html
    fi
    service nginx restart
fi

mkdir -p /data/web_static/shared/
if ! find /data/web_static/releases/test/index.html; then
	mkdir -p /data/web_static/releases/test/
	echo "<html>
	<head>
	</head>
	<body>
	Holberton School
	</body>
	</html>" > /data/web_static/releases/test/index.html
	ln -sf /data/web_static/releases/test/ /data/web_static/current
fi

chown -R ubuntu:ubuntu /data/

if ! grep -q "location \/hbnb_static\/ {" /etc/nginx/sites-available/default; then
	cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bup
	sed -i '/^\tlocation \/ {$/a \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}' /etc/nginx/sites-available/default
	service nginx reload
fi
