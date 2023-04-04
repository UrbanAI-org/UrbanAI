create table if not exists meshes (
    id integer primary key AUTOINCREMENT,
    uid text not null,
    expired integer not null,
    last_update real not null,
    pth text not null
);

create table if not exists pcds (
    id integer primary key AUTOINCREMENT,
    uid text not null,
    expired integer not null,
    last_update real not null,
    pth text not null
);

create table if not exists tifs (
    id integer primary key AUTOINCREMENT,
    uid text not null,
    filename text not null,
    pth text not null,
    origin_lat real not null,
    origin_lon real not null,
    lat_begin real,
    lat_end real,
    lon_begin real,
    lon_end real,
    pcd integer references pcds(id),
    mesh integer references meshs(id)

);

create table if not exists chunks (
    id text primary key,
    center_x real not null,
    center_y real not null,
    min_bound_x real not null,
    min_bound_y real not null,
    max_bound_x real not null,
    max_bound_y real not null,
    origin_lat real not null,
    origin_lon real not null,
    parent text not null,
    pcd integer references pcds(id),
    mesh integer references meshs(id)

);
