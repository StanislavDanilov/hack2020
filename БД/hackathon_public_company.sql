create table company
(
    id       integer  not null
        constraint company_pkey
            primary key,
    name     char(30) not null,
    ogrn     bigint   not null,
    inn      bigint   not null,
    login    char(30),
    password char(30)
);

alter table company
    owner to postgres;

INSERT INTO public.company (id, name, ogrn, inn, login, password) VALUES (0, 'пик                           ', 1027739137084, 7713011336, null, null);
INSERT INTO public.company (id, name, ogrn, inn, login, password) VALUES (1, 'grm group                     ', 1147746830615, 7716780474, null, null);
INSERT INTO public.company (id, name, ogrn, inn, login, password) VALUES (2, 'кип                           ', 1234215512525, 325326326263, 'login                         ', 'password                      ');
INSERT INTO public.company (id, name, ogrn, inn, login, password) VALUES (3, 'qwer                          ', 123456543, 342325235, 'ret                           ', 'qwqewq                        ');