CREATE TABLE IF NOT EXISTS public.problems
(
    id SERIAL,
    title character varying COLLATE pg_catalog."default" DEFAULT ''::character varying,
    slug character varying COLLATE pg_catalog."default" DEFAULT ''::character varying,
    problem_text text COLLATE pg_catalog."default" DEFAULT ''::text,
    topics character varying COLLATE pg_catalog."default" DEFAULT ''::character varying,
    difficulty_level character varying COLLATE pg_catalog."default" DEFAULT ''::character varying,
    success_rate double precision DEFAULT 0.0,
    total_submission bigint DEFAULT 0,
    total_accepted bigint DEFAULT 0,
    likes bigint DEFAULT 0,
    dislikes bigint DEFAULT 0,
    hints text COLLATE pg_catalog."default" DEFAULT ''::text,
    similar_ids character varying COLLATE pg_catalog."default" DEFAULT ''::character varying,
    similar_text text COLLATE pg_catalog."default" DEFAULT ''::text,
    CONSTRAINT problems_pkey PRIMARY KEY (id)
);

COPY public.problems
(id, title, slug, problem_text, topics, difficulty_level, success_rate, total_submission, total_accepted, likes, dislikes, hints, similar_ids, similar_text)
FROM '/docker-entrypoint-initdb.d/problems.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8' QUOTE '"' ESCAPE '"';