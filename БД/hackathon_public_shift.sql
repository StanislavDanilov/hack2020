create table shift
(
    id           integer not null
        constraint shift_pkey
            primary key,
    status       char(30),
    login_worker char(30)
        constraint shift_workers__fk
            references workers,
    date         char(20)
);

alter table shift
    owner to postgres;

INSERT INTO public.shift (id, status, login_worker, date) VALUES (20, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (0, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (1, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (2, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (3, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (16, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (18, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (19, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (21, 'окончена                      ', 'oleg                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (22, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (7, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (8, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (9, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (10, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (11, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (23, 'окончена                      ', 'dima                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (25, 'окончена                      ', 'rogi                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (26, 'в процессе                    ', 'nya                           ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (4, 'окончена                      ', 'maks                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (5, 'окончена                      ', 'maks                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (6, 'окончена                      ', 'maks                          ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (12, 'окончена                      ', 'sanya                         ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (13, 'окончена                      ', 'sanya                         ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (14, 'окончена                      ', 'sanya                         ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (15, 'окончена                      ', 'sanya                         ', '2020-11-01          ');
INSERT INTO public.shift (id, status, login_worker, date) VALUES (17, 'в процессе                    ', 'igor                          ', '2020-11-01          ');