# Triage context (example) — copy to triage-context.md and fill in

# --- Microsoft Graph app registration (Entra) ---
tenant_id: 7866fab6-0c1c-47e0-a09c-3070332fb359
client_id: 899c8057-359d-495e-9611-82941a3fa534
client_secret: YOUR_CLIENT_SECRET_HERE

# For application-permission flow, the mailbox to act on (Scott's UPN/email).
# Omit if using a delegated /me flow.
user_id: scott@aubreylegal.com

# --- Supabase (sender identification: client vs lead) ---
# Calls the triage_match_sender RPC to tell whether a sender is a known client
# or lead. Use the PUBLISHABLE key (sb_publishable_...), not the service-role
# secret: the RPC is SECURITY DEFINER and returns only kind/name/status.
supabase_url: https://YOUR-PROJECT.supabase.co
supabase_key: sb_publishable_xxxxxxxxxxxxxxxxxxxxxxxx

# --- Standing triage preferences ---
default_count: 50
# Folder that notification-type mail is moved into (created if missing).
notifications_folder: Notifications
calendar_link: https://cal.com/aubreylaw/discoverycall
signoff: |
  Scott Aubrey
  Aubrey Law LLC
  (781) 474-3450 · aubreylegal.com
