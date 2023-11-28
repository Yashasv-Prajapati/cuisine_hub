-- drop database if exists db; 
create database db;

use db;
show tables;

-- drop table sells;
-- drop table is_made_of;
-- drop table raw_material;
-- drop table seller_info;

-- information about user - can be seller or customer
create table user(
    id int auto_increment primary key,
    role varchar(10) default 'customer',
    name varchar(50),
    phone varchar(15) check(length(phone) >= 10),
    email varchar(50) unique check (email LIKE '%_@__%.__%'),
    address varchar(100),
    password varchar(500) not null check (length(password) >= 4)
);

-- information about raw_materials, each seller can sell different
-- raw materials and multiple times  
create table raw_material(
	id int auto_increment primary key,
    name varchar(50),
    price int,
    exp_time timestamp,
    quantity_left int check(quantity_left >= 0)
);

-- recipe information 
create table recipe(
	id int auto_increment primary key,
    name varchar(100),
    description varchar(500)
);

-- relationship between customer and recipes
create table buys(
	user_id int not null,
    recipe_id int not null,
	transaction_time timestamp,
    instances int check(instances > 0),
    cost_price int check(cost_price > 0),
    selling_price int check(selling_price > 0),
    foreign key (user_id) references user(id),
    foreign key (recipe_id) references recipe(id),
    primary key (user_id, recipe_id, transaction_time)
);

-- relationship between seller and raw_material
create table sells(
	user_id int not null,
    raw_material_id int not null,
    transaction_time timestamp,
    units int,
    price int,
    exp_time timestamp,
    status varchar(10) CONSTRAINT status_check CHECK (status in ("approved", "pending", "using", "finished")),
    foreign key(user_id) references user(id),
    foreign key(raw_material_id) references raw_material(id),
    primary key(user_id, raw_material_id, transaction_time)
);

-- relationship between recipes and raw_material
create table ingredient(
	recipe_id int not null,
    raw_material_id int not null,
    quantity_required int check(quantity_required > 0), -- quantity of this raw_material required to make one unit of the recipe
    foreign key(recipe_id) references recipe(id),
    foreign key(raw_material_id) references raw_material(id),
    primary key(recipe_id,raw_material_id)
);
