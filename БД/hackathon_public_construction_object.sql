create table construction_object
(
    id         integer not null
        constraint construction_object_pkey
            primary key,
    id_company integer
        constraint construction_object_id_company_fkey
            references company,
    name       char(30)
);

alter table construction_object
    owner to postgres;

INSERT INTO public.construction_object (id, id_company, name) VALUES (0, 0, 'Й                             ');
INSERT INTO public.construction_object (id, id_company, name) VALUES (1, 0, 'Песочница                     ');
INSERT INTO public.construction_object (id, id_company, name) VALUES (2, 0, 'Apple                         ');
INSERT INTO public.construction_object (id, id_company, name) VALUES (3, 0, 'Любой объект                  ');