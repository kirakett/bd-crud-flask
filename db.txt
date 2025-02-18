create extension if not exists "uuid-ossp";

drop table if exists developer, repo, repo_to_developer, ticket cascade;

create table developer
(
    id         uuid default uuid_generate_v4() primary key,
    nickname text,
    reg_date date
);

create table repo
(
    id    uuid default uuid_generate_v4() primary key,
    title text,
    descr text,
    stars  int
);

create table repo_to_developer
(
    developer_id uuid references developer,
    repo_id  uuid references repo,
    primary  key (developer_id, repo_id)
);

insert into developer(nickname, reg_date)
values
('Igor', '2017-12-05'),
('Dima', '2020-12-03'),
('Danil', '2005-11-05');

insert into repo(title, descr, stars)
values
('Aurora_OS', 'For mobile', 10),
('New hackathon', 'For website', 9),
('Sber_internship', 'Algorithm', 8),
('OCRV', 'Design', 7);

insert into repo_to_developer(developer_id, repo_id)
values
((select id from developer where nickname = 'Igor' and reg_date = '2017-12-05'), (select id from repo where title = 'Aurora_OS')),
((select id from developer where nickname = 'Igor' and reg_date = '2017-12-05'), (select id from repo where title = 'New hackathon')),
((select id from developer where nickname = 'Dima' and reg_date = '2020-12-03'), (select id from repo where title = 'Sber_internship')),
((select id from developer where nickname = 'Dima' and reg_date = '2020-12-03'), (select id from repo where title = 'OCRV')),
((select id from developer where nickname = 'Danil' and reg_date = '2005-11-05'), (select id from repo where title = 'Sber_internship')),
((select id from developer where nickname = 'Danil' and reg_date = '2005-11-05'), (select id from repo where title = 'OCRV')),
((select id from developer where nickname = 'Danil' and reg_date = '2005-11-05'), (select id from repo where title = 'New hackathon'));

create table ticket
(
    id       uuid default uuid_generate_v4() primary key,
    name_t    text,
    desc_t     text,
	stat	text,
    repo_id uuid references repo
);

insert into ticket(name_t, desc_t, stat, repo_id)
values
('New UI', 'Users do not understand our UI', 'Done', (select id from repo where title = 'Aurora_OS' and descr = 'For mobile')),
('Add gestures', 'Add new gestures in mobile version', 'In process', (select id from repo where title = 'Aurora_OS' and descr = 'For mobile')),
('Web design', 'Do website redesign', 'In process', (select id from repo where title = 'New hackathon' and descr = 'For website')),
('Unaccounted parameters', 'Write an algorithm for the remaining parameters', 'Not ready', (select id from repo where title = 'Sber_internship' and descr = 'Algorithm')),
('Optimization', 'Do an optimization, algorithm is slow', 'Not ready', (select id from repo where title = 'Sber_internship' and descr = 'Algorithm'));
