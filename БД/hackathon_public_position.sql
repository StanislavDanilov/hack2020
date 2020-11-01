create table position
(
    id   integer not null
        constraint position_pkey
            primary key,
    name char(120)
);

alter table position
    owner to postgres;

INSERT INTO public.position (id, name) VALUES (0, 'строитель                                                                                                               ');
INSERT INTO public.position (id, name) VALUES (1, 'инженер                                                                                                                 ');
INSERT INTO public.position (id, name) VALUES (2, 'арматурщик                                                                                                              ');
INSERT INTO public.position (id, name) VALUES (3, 'сварщик                                                                                                                 ');