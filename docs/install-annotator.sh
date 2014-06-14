# Install SSH public key
vim .ssh/authorized_keys 

# Install git, java
add-apt-repository ppa:webupd8team/java
apt-get update
apt-get install git oracle-java7-installer nginx python-setuptools unzip
# java -version

# Install elasticsearch
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.2.0.deb
dpkg -i elasticsearch-1.2.0.deb 
sudo update-rc.d elasticsearch defaults 95 10
sudo /etc/init.d/elasticsearch start

# curl -X GET 'http://localhost:9200'

# Install Python
easy_install virtualenv
# pip install nosetests mock

# Install annotator-store
# git clone https://github.com/openannotation/annotator-store.git

# cd annotator-store
# virtualenv pyenv
# source pyenv/bin/activate
# pip install -e .
# cp annotator.cfg.example annotator.cfg

# Install annotateit
git clone https://github.com/wordtreefoundation/annotateit.git
cd annotateit
virtualenv pyenv
apt-get install libevent-dev
apt-get build-dep python-psycopg2
pip install -e .
pip install -e . -r requirements.txt

# Install annotator
#wget https://github.com/downloads/openannotation/annotator/annotator-full.1.2.7.zip
#unzip annotator-full.1.2.7.zip
#cd annotator-full.1.2.7/
#cp annotator-full.min.js annotator.min.css /usr/share/nginx/html/

# Edit nginx config
vim /etc/nginx/sites-available/default

# --- default ---
upstream annotator {
  server 127.0.0.1:5000;
}

server {
  listen 80 default_server;
  listen [::]:80 default_server ipv6only=on;

  root /usr/share/nginx/html;
  index index.html index.htm;

  # Make site accessible from http://localhost/
  server_name localhost;

  location = /api {
    return 302 /api/;
  }
  location /api {
    rewrite /api/(.*) /$1  break;
    proxy_pass http://annotator;
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }

  location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    try_files $uri $uri/ =404;
    # Uncomment to enable naxsi on this location
    # include /etc/nginx/naxsi.rules
  }
}

# --- default ---

service nginx restart

# Running annotator-store:
cd ~/annotator-store
python run.py >run.log 2>&1 &

mkdir /usr/share/nginx/html/book-of-mormon/
