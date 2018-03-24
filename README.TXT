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
mysql -u root -p(sudo for ubuntu 18)

CREATE DATABASE partial_translate;
USE partial_translate;

PRAGMA foreign_keys=on;    поддержка внешних ключей
CREATE TABLE users(id INT(7) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20), password VARCHAR(2000), email VARCHAR(50), teacher bit NULL DEFAULT 0, g char(10) DEFAULT NULL);

для присвоения пользователю статуса администратор: UPDATE users SET teacher = 1 WHERE username = 'username(adm)';
для указания группы пользователя: UPDATE users SET g = 'a' WHERE username = 'username(pupil)';

CREATE TABLE words(id INT(7) AUTO_INCREMENT PRIMARY KEY, RU VARCHAR(100), EN VARCHAR(100), FR VARCHAR(100), DE VARCHAR(100));
CREATE TABLE words_users(id INT(20) AUTO_INCREMENT PRIMARY KEY, id_user INT(7), id_word INT(7), date DATE, FOREIGN KEY (id_user) REFERENCES users(id), FOREIGN KEY (id_word) REFERENCES words(id));

SHOW TABLES;
DESCRIBE users;
QUIT;

	sudo apt-get install python3.6-MySQLdb
!*




heroku.com
67637111Aa/

