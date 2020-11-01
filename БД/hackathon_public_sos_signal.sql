create table sos_signal
(
    id           integer not null
        constraint sos_signal_pkey
            primary key,
    login_worker char(30)
        constraint sos_signal_worker_login_fkey
            references workers,
    date         date
);

alter table sos_signal
    owner to postgres;

INSERT INTO public.sos_signal (id, login_worker, date) VALUES (0, 'dima                          ', '2020-11-01');