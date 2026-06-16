---
name: create-lawmatics-task
description: |
  [OUTCOME]: Creates a task in Lawmatics via a Make.com webhook, with
  optional subtasks, due date, description, and linked matter. Returns
  confirmation with task name and matter link.
  [TRIGGER]: Activates on "create a task in Lawmatics," "add a Lawmatics
  task," "task for [client] in Lawmatics," "create a task to [action],"
  "add a task on the [client] matter," or any request to create, add, or
  assign a task that references Lawmatics or a client matter.
  Also triggers on casual phrasing like "remind me to send the Smiths
  their funding checklist," "task: follow up with Jones on signatures,"
  or "add a to-do on the Davis matter."
  [ANTI-TRIGGER]: Does NOT trigger for changing matter stages (use
  change-matter-stage), creating matters, drafting documents, or
  calendar events. Does NOT trigger for tasks in other systems
  (Outlook, QuickBooks, etc.).
---

# Create Lawmatics Task

Create a task (with optional subtasks) in Lawmatics by posting to a Make
webhook. The webhook searches for the linked matter, creates the task via
the Lawmatics API, adds any subtasks, and returns confirmation.

## Prerequisites

The Make.com scenario must be active. See `references/make-scenario-setup.md`
for the full build guide if the scenario hasn't been created yet.

## Webhook

`{{LAWMATICS_TASK_WEBHOOK_URL}}`

> **Setup note:** Replace the placeholder above with the actual Make webhook
> URL after building the scenario. The URL will look like:
> `https://hook.us2.make.com/xxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 1 — Collect inputs

Read `learnings.md` before proceeding. Apply any rules during this session.

Extract these fields from Scott's request. If a value is missing or
ambiguous, ask before proceeding — but infer reasonable defaults where
possible (e.g., no due date means omit it; no description means leave blank).

| Field | Required | Notes |
|---|---|---|
| `task_name` | Yes | Short name for the task |
| `due_date` | No | ISO 8601 date (`YYYY-MM-DD`). Omit if not specified. |
| `description` | No | Additional detail. Omit if not specified. |
| `matter_search` | No | Client last name or matter name to link the task. Omit for unlinked tasks. |
| `subtasks` | No | Array of subtask name strings. Omit if none. |
| `priority` | No | `low`, `medium`, or `high`. Default: `medium`. |

**Inference rules:**
- If Scott says "next Friday," calculate the actual date.
- If Scott says "follow up with Jones," infer `matter_search: "Jones"` and
  derive a reasonable `task_name` like "Follow up with Jones."
- If Scott lists multiple action items, treat them as subtasks under one
  parent task, or ask if he wants separate tasks.

## Step 2 — POST to the webhook

```bash
curl -s -X POST "{{LAWMATICS_TASK_WEBHOOK_URL}}" \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "Review and send funding checklist",
    "due_date": "2026-06-15",
    "description": "Send trust funding instructions after signing meeting",
    "matter_search": "Smith",
    "subtasks": [
      "Prepare funding checklist",
      "Email checklist to client",
      "Calendar reminder for 30-day follow-up"
    ],
    "priority": "medium"
  }'
```

Always fire the real webhook. Never fabricate a response.

## Step 3 — Handle the response

| Response | Action |
|---|---|
| `{"success": true, "task_id": "...", "task_name": "...", "matter": "..."}` | Confirm: *"Created task **[task_name]** on the **[matter]** matter."* If subtasks were included, note how many were added. |
| `{"success": true, "task_id": "...", "task_name": "...", "matter": null}` | Confirm: *"Created task **[task_name]** (not linked to a matter)."* |
| `{"error": "no_matter_found"}` | Tell Scott no matter matched. Ask for a more specific name or offer to create the task unlinked. |
| `{"error": "ambiguous_matter", "candidates": [...]}` | List candidates, ask Scott to pick, re-fire with the specific match. |
| `{"error": "subtask_partial_failure", "created": [...], "failed": [...]}` | Report which subtasks succeeded and which failed. Offer to retry. |
| Any other error or timeout | Report the raw error. Suggest checking that the Make scenario is active. |

## Step 4 — Post-run

After completing the task, ask: "Did that work as expected? Anything to
adjust for next time?" Log useful feedback to `learnings.md`.

## Legal Compliance Guardrails

1. This skill creates internal workflow tasks only — no client-facing output.
2. Never fabricate matter names, task IDs, or confirmation responses.
3. If the webhook is unreachable, report the error — do not simulate success.
4. Flag uncertainty: if unsure whether a task should be linked to a matter,
   ask rather than guessing.
5. All task content is internal and does not constitute legal advice.
