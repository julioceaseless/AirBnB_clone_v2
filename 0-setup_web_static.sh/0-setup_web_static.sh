#!/usr/bin/env bash
# script sets up web servers for deployment of web_static

# update packages
sudo apt-get -y update

# install nginx if not already installed
sudo apt-get install -y nginx

# create folder if it does not exist
sudo mkdir -p /data/web_static/{shared,releases}/

releases="/data/web_static/releases"

# create test folder
sudo mkdir $releases/test/

placeholder="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
	
# create test index.html
echo "$placeholder" | sudo tee > /dev/null $releases/test/index.html

# create a symbolic link to test folder forcefully
sudo ln -s -f $releases/test/ /data/web_static/current

# give ownership of /data/ folder to user 'ubuntu' and group 'ubuntu'
sudo chown -R ubuntu:ubuntu /data/

# set up alias
hbnb_static="\ \n \tlocation /hbnb_static {\n
                \t\talias /data/web_static/current/;\n
                \t\tautoindex off;\n
        \t}\n"

# append new alias
sudo sed -i "/^[[:space:]]}/ a $hbnb_static"\
	/etc/nginx/sites-{enabled,available}/default 

# restart nginx to apply configuration changes
sudo service nginx restart
