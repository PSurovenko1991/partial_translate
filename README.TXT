БД:
sudo apt install mariadb-server

После завершения установки, запустите простой скрипт безопасности, который удалит некоторые настройки по умолчанию и чуть заблокирует доступ к нашей системе. Запустите интерактивный скрипт командой:

sudo mysql_secure_installation

root-password: 67637111Aa
Первый вход:
sudo mysql 
MariaDB> use mysql;
MariaDB> update user set plugin='' where User='root';
MariaDB> flush privileges;
MariaDB> exit

sudo systemctl restart mysql.service
mysql -u root -p

Последующие:
mysql -u root -p

CREATE DATABASE partial_translate;
USE partial_translate;
CREATE TABLE users(uid INT(7) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20), password VARCHAR(2000), email VARCHAR(50), settings VARCHAR(33000), tracking VARCHAR(33000), rank INT(3));
SHOW TABLES;
DESCRIBE users;
QUIT;

sudo apt-get install python3.5-MySQLdb
