create table workers
(
    login                  char(30) not null
        constraint workers_pkey
            primary key,
    name                   char(30),
    surname                char(30),
    lastname               char(30),
    id_position            integer
        constraint workers_id_position_fkey
            references position,
    id_construction_object integer
        constraint workers_id_construction_object_fkey
            references construction_object,
    password               char(30),
    phone_number           bigint,
    device_number          bigint
);

alter table workers
    owner to postgres;

INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('vasya                         ', 'Василий                       ', 'Васильев                      ', 'Васильевич                    ', 0, null, 'qwerty                        ', null, null);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('vanya                         ', 'Иван                          ', 'Иванов                        ', 'Иванович                      ', 1, 2, 'qwerty                        ', 88005553535, 23);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('oleg                          ', 'Олег                          ', 'Олегов                        ', 'Олегович                      ', 2, 2, 'qwerty                        ', 88053535, 3);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('maks                          ', 'Максим                        ', 'Максимов                      ', 'Масимович                     ', 1, 2, 'qwerty                        ', 8803535, 2);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('dima                          ', 'Дмитрий                       ', 'Дмитриев                      ', 'Димов                         ', 1, 2, 'qwerty                        ', 5553535, 1);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('sanya                         ', 'Алесандр                      ', 'Александров                   ', 'Александрович                 ', 1, 2, 'qwerty                        ', 805553535, 12);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('igor                          ', 'Игорь                         ', 'Александров                   ', 'Игорьевич                     ', 3, 2, 'qwerty                        ', 805553535, 12);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('nya                           ', 'Алексий                       ', 'Александров                   ', 'Иванов                        ', 1, 2, 'qwerty                        ', 805553535, 12);
INSERT INTO public.workers (login, name, surname, lastname, id_position, id_construction_object, password, phone_number, device_number) VALUES ('rogi                          ', 'Михаил                        ', 'Михайлов                      ', 'Михайлович                    ', 3, 2, 'qwerty                        ', 805553535, 12);