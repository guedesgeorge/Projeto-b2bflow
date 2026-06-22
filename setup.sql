-- Setup da tabela no Supabase
-- Cole e rode no SQL Editor do projeto (Supabase > SQL Editor > New query)

create table if not exists public.contatos (
    id           bigint generated always as identity primary key,
    nome_contato text not null,
    telefone     text not null,  -- formato DDI+DDD+numero, ex.: 5567999999999
    created_at   timestamptz default now()
);

-- Contatos de exemplo (troque pelos números reais que você controla)
insert into public.contatos (nome_contato, telefone) values
    ('George',  '5567991870207'),
    ('Maria',   '5567981297313'),
    ('João',    '5567992020634');
