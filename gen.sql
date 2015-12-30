CREATE TABLE weixin (
	id integer primary key autoincrement,
	href text unique,
	title text,
	img text,
	logdate date,
	key text
);
CREATE TABLE cookie (
	cookie text unique
);
CREATE TABLE clicks (
	ip text,
	logtime datetime default (datetime('now', 'localtime'))
);
CREATE TABLE lastSpider(
	id integer primary key,
	lastId integer default 0,
	logtime datetime default (datetime('now', 'localtime'))
);
