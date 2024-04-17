#!/usr/bin/env bash
# Sets up web servers for deployment

# Install Nginx if not already installed
if ! dpkg -l nginx &> /dev/null; then
	apt-get -y update
	apt-get -y install nginx
fi

# Create necessary directories
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
html_content="<html>
	<head>
	</head>
	<body>
		ALX Africa
	</body>
</html>"

echo "$html_content" > /data/web_static/releases/test/index.html


# Create symbolic link
# If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
if [ -L /data/web_static/current ]; then
	rm /data/web_static/current
fi

ln -s /data/web_static/releases/test /data/web_static/current

# Change ownership recursively
# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist).
# This should be recursive; everything inside should be created/owned by this user/group.
chown -R ubuntu:ubuntu /data

# Update Nginx configuration
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
# (ex: https://mydomainname.tech/hbnb_static)
sudo sed -i '/server_name _;/a \\n\t# Add alias for serving web_static content\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default


# Restart Nginx
service nginx restart

exit 0
