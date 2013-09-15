drop table if exists sites;
create table sites (
   id integer primary key autoincrement,
   url text not null,
   contents text not null
);
