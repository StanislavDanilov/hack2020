create table workers_coordinates
(
    id                    integer not null
        constraint workers_coordinates_pkey
            primary key,
    coordinates_latitude  double precision[],
    id_shift              integer
        constraint id_shift
            references shift,
    coordinates_longitude double precision[]
);

alter table workers_coordinates
    owner to postgres;

INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (1, null, 1, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (2, null, 2, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (3, null, 3, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (4, null, 4, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (5, null, 5, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (6, null, 6, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (7, null, 7, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (8, null, 8, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (9, null, 9, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (10, null, 10, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (11, null, 11, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (12, null, 12, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (13, null, 13, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (14, null, 14, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (15, null, 15, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (16, null, 16, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (17, null, 17, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (18, null, 18, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (19, null, 19, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (20, null, 20, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (21, null, 21, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (22, null, 22, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (23, '{55.66594570662001500}', 23, '{37.75545139630546000}');
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (25, null, 25, null);
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (26, '{37.33039971000000000,37.33019220000000000,37.33019466000000000}', 26, '{-122.02856703000000000,-122.02575657000000000,-122.02302795000000000}');
INSERT INTO public.workers_coordinates (id, coordinates_latitude, id_shift, coordinates_longitude) VALUES (0, '{null,null,null,null,1234.12450000000000000,1234.12450000000000000,1234.12450000000000000,1234.12450000000000000,1234.12450000000000000,1234.12450000000000000}', 0, '{null,null,null,null,123.41255000000000000,123.41255000000000000,123.41255000000000000,123.41255000000000000,123.41255000000000000,123.41255000000000000}');