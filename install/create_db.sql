set search_path to arduino_api;

set schema 'public';

create table users
(
	id serial not null
		constraint users_pkey
			primary key,
	created_at timestamp,
	username varchar(32),
	secret_hash varchar(128) not null
);

alter table users owner to postgres;

create unique index ix_users_username
	on users (username);

create table mqtt_clients
(
	id serial not null
		constraint mqtt_clients_pkey
			primary key,
	created_at timestamp,
	username varchar(32) not null
		constraint mqtt_clients_username_key
			unique,
	password varchar(128) not null,
	is_admin boolean not null
);

alter table mqtt_clients owner to postgres;

create table mqtt_access
(
	id serial not null
		constraint mqtt_access_pkey
			primary key,
	created_at timestamp,
	updated_at timestamp,
	topic varchar(256) not null,
	access integer not null,
	username varchar(32)
		constraint mqtt_access_username_fkey
			references mqtt_clients (username)
);

alter table mqtt_access owner to postgres;
