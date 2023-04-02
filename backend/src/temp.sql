create table if not exists mesh_paths (
    id integer primary key AUTOINCREMENT,
    pth text,
);

create table if not exists pcd_paths (
    id integer primary key AUTOINCREMENT,
    pth text,
);
