set search_path to arduino_api;

set schema 'public';

create table chunks
(
	id serial not null
		constraint chunks_pkey
			primary key,
	created_at timestamp,
	topic varchar(32) not null,
	name varchar(32) not null,
	long double precision not null,
	lat double precision not null,
	price double precision not null,
	description text
)
;

alter table chunks owner to postgres
;

create table users
(
	id serial not null
		constraint users_pkey
			primary key,
	created_at timestamp,
	username varchar(32),
	secret_hash varchar(128) not null,
	email varchar(128) not null
		constraint users_email_key
			unique,
	last_name varchar(32),
	first_name varchar(32),
	deposit double precision,
	is_admin boolean not null
)
;

alter table users owner to postgres
;

create unique index ix_users_username
	on users (username)
;

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
)
;

alter table mqtt_clients owner to postgres
;

create table user_chunk
(
	user_id integer not null
		constraint user_chunk_user_id_fkey
			references users,
	chunk_id integer not null
		constraint user_chunk_chunk_id_fkey
			references chunks,
	constraint user_chunk_pkey
		primary key (user_id, chunk_id)
)
;

alter table user_chunk owner to postgres
;

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
)
;

alter table mqtt_access owner to postgres
;


INSERT INTO mqtt_clients (created_at, username, password, is_admin) VALUES ('2019-04-24 06:44:13.079818', 'device01', 'PBKDF2$sha256$10000$FB3rtpBBnyEpPWuW$o0cUsHRYisKyvk6IqaesA3YN9Fv2QSg8', false);
INSERT INTO mqtt_clients (created_at, username, password, is_admin) VALUES ('2019-04-24 06:44:13.079818', 'chunk_daemon', 'PBKDF2$sha256$10000$jB5eSaLjPmq1M7YM$khKiaH1DyEetrYy5a6L6VdFOn4WIbgyv', true);
INSERT INTO mqtt_clients (created_at, username, password, is_admin) VALUES ('2019-04-24 06:44:13.079818', 'chunk_counter', 'PBKDF2$sha256$10000$8VyTNQJI1qWdxP2Y$z3UU7LdCPnEZXThP+31nS2igZYakCWAQ', true);

INSERT INTO mqtt_access (created_at, updated_at, topic, access, username) VALUES ('2019-04-24 06:45:51.039637', null, 'sensors/device01/from_clients', 1, 'device01');
INSERT INTO mqtt_access (created_at, updated_at, topic, access, username) VALUES ('2019-04-24 06:46:03.994846', null, 'sensors/device01/from_device', 2, 'device01');

INSERT INTO users (created_at, username, secret_hash, email, last_name, first_name, deposit, is_admin) VALUES ('2019-04-24 14:55:42.308812', 'rastadev', 'pbkdf2:sha256:150000$FQni21a8$5ba2e0f72c843282faf1899ee696e30c02d9de4a8457f7e507e0e699a743d328', 'rasta@dev.com', null, null, 24.25, true);
INSERT INTO chunks (created_at, topic, name, long, lat, price, description) VALUES ('2019-04-24 06:44:13.078317', 'chunks/8324716771535245060/data', 'Lille', 3.055467, 50.75, 25, 'Recense les données suivantes aux alentours de la ville de Lille : humidité, température et index de chaleur. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ligula lorem, sagittis ut ultricies non, fringilla ut nulla. Nulla quis tincidunt nisl. Ut pulvinar faucibus nunc a egestas. Donec quam lectus, gravida ac placerat vitae, fermentum sit amet erat. Nullam imperdiet ante ac arcu rhoncus maximus. Pellentesque consequat quam non pretium luctus. Nulla elementum enim sapien, et lacinia arcu volutpat in. Etiam blandit, mi et feugiat vehicula, odio quam aliquet arcu, id lacinia augue magna sed felis. Sed accumsan posuere lacus, a pellentesque neque fringilla eget. Proin elementum id est id lacinia. In ornare purus erat, id semper diam varius ac. Pellentesque lacus dui, sollicitudin at eros pharetra, vehicula gravida lacus. Vivamus id lorem congue, tempor neque non, maximus turpis. Nullam ac erat massa.

');
INSERT INTO user_chunk (user_id, chunk_id) VALUES (1, 1);
