drop table if exists video;
create table video (
  id integer primary key autoincrement,
  vid_id text not null,
  data text not null
);
