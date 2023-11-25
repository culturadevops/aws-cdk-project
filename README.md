instalacion 

comandos de instalacion de cdk
curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt-get install -y nodejs
sudo npm install -g aws-cdk

comando para crear el proyecto inicial
cdk init app --language python


Forma de desinstalar node y npm
sudo apt remove nodejs
sudo apt remove npm
sudo apt autoremove