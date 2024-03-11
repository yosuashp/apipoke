create database flask_template; 
use flask_template;

CREATE TABLE poke_review (
    id varchar(36) PRIMARY KEY,
    star tinyint,
    title varchar(2000),
  	content text, 
  	user_ip varchar(50),
  	user_agent text,
    pokemon_name varchar(30),
   	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
















