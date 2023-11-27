-- drop database if exists db; 
create database db;

use db;
show tables;

-- drop table sells;
-- drop table is_made_of;
-- drop table raw_material;
-- drop table seller_info;

-- information about seller 
create table seller_info(
	id int auto_increment primary key,
    role varchar(10) default 'seller',
    name varchar(50),
    phone varchar(15) check( length(phone) >= 10),
    email varchar(50) check (email LIKE '%_@__%.__%'),
    address varchar(100)
);

-- information about raw_materials, each seller can sell different
-- raw materials and multiple times  
create table raw_material(
	id int auto_increment primary key,
    name varchar(50),
    price int,
    transaction_time timestamp,
    exp_time timestamp,
    quantity_left int check(quantity_left >= 0),
    seller_id int,
    foreign key (seller_id) references seller_info(id)
);

-- recipe information 
create table recipe(
	id int auto_increment primary key,
    name varchar(100),
    cost_price int check(cost_price > 0), 
    selling_price int check(selling_price > 0),
    available int check(available >= 0)
);

-- information about customer
create table customer_info(
	id int auto_increment primary key,
    role varchar(10) default 'seller',
    name varchar(50),
    phone varchar(15) check( length(phone) >= 10),
    email varchar(50) check (email LIKE '%_@__%.__%')
);

-- relationship between customer and recipes
create table buys(
	customer_id int not null,
    recipe_id int not null,
	transaction_time timestamp,
    instances int check(instances > 0),
    amount_paid int check(amount_paid > 0),
    foreign key (customer_id) references customer_info(id),
    foreign key (recipe_id) references recipe(id),
    primary key (customer_id, recipe_id, transaction_time)
);

-- relationship between seller and raw_material
create table sells(
	seller_id int not null,
    raw_material_id int not null,
    transaction_time timestamp,
    status varchar(10) check( status="approved" or status="pending"),
    foreign key(seller_id) references seller_info(id),
    foreign key(raw_material_id) references raw_material(id),
    primary key(seller_id, raw_material_id, transaction_time)
);

-- relationship between recipes and raw_material
create table is_made_of(
	recipe_id int not null,
    raw_material_id int not null,
    quantity_required int check(quantity_required > 0),
    foreign key(recipe_id) references recipe(id),
    foreign key(raw_material_id) references raw_material(id),
    primary key(recipe_id,raw_material_id)
);

call get_all_recipes;
