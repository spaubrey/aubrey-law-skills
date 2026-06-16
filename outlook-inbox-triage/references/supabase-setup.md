# Supabase setup — sender identification

The `identify` step tells triage whether a sender is a known **client** or
**lead**, so the urgent/lead classification is data-driven instead of guessed.
It calls one Postgres function over PostgREST. Set up once.

## 1. Config in `triage-context.md`

```
supabase_url: https://YOUR-PROJECT.supabase.co
supabase_key: sb_publishable_xxxxxxxxxxxxxxxxxxxxxxxx
```

Use the **publishable** key (`sb_publishable_…`), **not** the service-role
secret. The function below is `SECURITY DEFINER` and returns only a
classification, so no privileged secret ever lives in this file.

## 2. The `triage_match_sender` RPC

The skill reads RLS-protected `leads` and `client_intake` tables. Rather than
hand the CLI a service-role key, expose a single function that runs as definer
and returns only `kind` / `display_name` / `status`. This migration is already
applied to the "Aubrey Law App" project:

```sql
create or replace function public.triage_match_sender(p_email text)
returns table(kind text, display_name text, status text)
language plpgsql
security definer
set search_path = public
as $$
declare e text := lower(trim(coalesce(p_email, '')));
begin
  if e = '' then return; end if;

  return query
    select 'client'::text,
           coalesce(nullif(trim(ci.full_name), ''),
                    nullif(trim(concat_ws(' ', ci.first_name, ci.last_name)), '')),
           ci.status
    from client_intake ci
    where lower(ci.email) = e or lower(ci.spouse_email) = e
    limit 1;
  if found then return; end if;

  return query
    select 'lead'::text,
           nullif(trim(concat_ws(' ', l.first_name, l.last_name)), ''),
           l.status
    from leads l
    where l.deleted_at is null
      and (lower(l.email) = e or lower(l.spouse_email) = e)
    limit 1;
end;
$$;

grant execute on function public.triage_match_sender(text) to anon, authenticated;
```

Behavior:

- **Client precedence.** A converted lead (now in `client_intake`) returns
  `client`, never `lead`.
- **Spouse emails count.** Matches `email` *or* `spouse_email` on both tables.
- **Case-insensitive.** `lower()` on both sides.
- **Soft-deleted leads ignored** (`deleted_at is null`).
- **Unknown → no rows.** The CLI maps an empty result to `kind: "unknown"`.

## 3. Verify

```bash
curl -s -X POST 'https://YOUR-PROJECT.supabase.co/rest/v1/rpc/triage_match_sender' \
  -H 'apikey: sb_publishable_…' -H 'Authorization: Bearer sb_publishable_…' \
  -H 'Content-Type: application/json' \
  -d '{"p_email":"nobody@example.invalid"}' -w '\nHTTP %{http_code}\n'
# -> []   HTTP 200      (a match returns [{"kind":"client", ...}])
```

If you get `HTTP 404` the RPC isn't deployed; re-run the migration. `HTTP 401`
means a bad/!publishable key. RLS on the base tables is fine — the definer
function is what reads them.
