# Make.com Scenario Setup Guide

## Overview

This guide walks through building the Make.com scenario that powers the
`create-lawmatics-task` skill. The scenario receives a webhook from Claude,
creates a task in Lawmatics (with optional subtasks and matter linking),
and returns a JSON response.

## Architecture

```
Claude (curl POST) → Make Webhook → Search Matter → Create Task → Create Subtasks → Response
```

## Prerequisites

- Make.com account with active plan (free tier works for low volume)
- Lawmatics API credentials (either via Make's native Lawmatics module
  or HTTP module with OAuth bearer token)
- Lawmatics Developer App Client ID and Client Secret
  (email api@lawmatics.com to enable Developer Settings if not already)

---

## Option A: Using Make's Native Lawmatics Module

Make has a built-in Lawmatics integration. If it supports Task creation
(check under Lawmatics → Create a Record → Task), use this path:

### Module 1: Webhooks → Custom Webhook
- Create a new webhook
- Name: `Claude - Create Lawmatics Task`
- Copy the webhook URL → paste into SKILL.md replacing `{{LAWMATICS_TASK_WEBHOOK_URL}}`
- Data structure (define manually or let Make learn from first request):

```json
{
  "task_name": "string (required)",
  "due_date": "string (optional, YYYY-MM-DD)",
  "description": "string (optional)",
  "matter_search": "string (optional)",
  "subtasks": ["string array (optional)"],
  "priority": "string (optional, low/medium/high)"
}
```

### Module 2: Router (two branches)

**Branch 1: Matter search provided**
- Condition: `matter_search` is not empty
- Lawmatics → Search Records → Matter (filter by name contains `matter_search`)
- If no results → Webhook Response with `{"error": "no_matter_found"}`
- If multiple results → Webhook Response with `{"error": "ambiguous_matter", "candidates": [...]}`
- If exactly one → proceed to Module 3 with `matter_id`

**Branch 2: No matter search**
- Condition: `matter_search` is empty
- Proceed directly to Module 3 with `matter_id = null`

### Module 3: Lawmatics → Create Task
- Name: `{{task_name}}`
- Due date: `{{due_date}}` (if provided)
- Description: `{{description}}` (if provided)
- Matter ID: `{{matter_id}}` (from Branch 1, or null)
- Priority: `{{priority}}` (default: medium)
- Assigned To: Scott's Lawmatics user ID (hardcode this)

### Module 4: Iterator → Subtasks (if provided)
- Condition: `subtasks` array is not empty
- Iterate over `subtasks` array
- For each: Lawmatics → Create Subtask
  - Task ID: from Module 3 output
  - Name: current subtask string

### Module 5: Webhooks → Webhook Response
- Status: 200
- Body:
```json
{
  "success": true,
  "task_id": "{{Module 3 task ID}}",
  "task_name": "{{task_name}}",
  "matter": "{{matter name or null}}",
  "subtasks_created": {{count of subtasks}}
}
```

---

## Option B: Using HTTP Module with Lawmatics API

If Make's native module doesn't support Tasks, use the HTTP module with
the Lawmatics REST API directly.

### Lawmatics API Endpoints Used

| Action | Method | Endpoint |
|---|---|---|
| Search matters | GET | `https://api.lawmatics.com/v1/matters?filter[name]={{matter_search}}` |
| Create task | POST | `https://api.lawmatics.com/v1/tasks` |
| Create subtask | POST | `https://api.lawmatics.com/v1/subtasks` |

### Authentication
- OAuth 2.0 Bearer Token
- Create a Make HTTP connection with:
  - Grant type: Authorization Code
  - Authorize URI: per Lawmatics OAuth docs
  - Token URI: per Lawmatics OAuth docs
  - Client ID: your Lawmatics app Client ID
  - Client Secret: your Lawmatics app Client Secret

### Task Creation Payload (POST /v1/tasks)

```json
{
  "data": {
    "type": "tasks",
    "attributes": {
      "name": "Review and send funding checklist",
      "due_date": "2026-06-15",
      "description": "Send trust funding instructions after signing",
      "priority": "medium"
    },
    "relationships": {
      "matter": {
        "data": {
          "type": "matters",
          "id": "{{matter_id}}"
        }
      },
      "assigned_to": {
        "data": {
          "type": "users",
          "id": "{{scott_user_id}}"
        }
      }
    }
  }
}
```

> **Note:** The exact payload shape may vary — check the Lawmatics API
> docs at https://docs.lawmatics.com for current field names. The API
> follows JSON:API conventions.

### Subtask Creation Payload (POST /v1/subtasks)

```json
{
  "data": {
    "type": "subtasks",
    "attributes": {
      "name": "Prepare funding checklist"
    },
    "relationships": {
      "task": {
        "data": {
          "type": "tasks",
          "id": "{{parent_task_id}}"
        }
      }
    }
  }
}
```

---

## After Setup

1. Copy the webhook URL from Module 1
2. Open `SKILL.md` and replace both instances of `{{LAWMATICS_TASK_WEBHOOK_URL}}`
   with the actual URL
3. Send a test payload to verify the full chain works:

```bash
curl -X POST "https://hook.us2.make.com/YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "Test task from Claude",
    "description": "Testing the webhook integration",
    "matter_search": "",
    "subtasks": [],
    "priority": "low"
  }'
```

4. Verify the task appears in Lawmatics
5. Test with a matter search term to confirm linking works
6. Test with subtasks to confirm iteration works
7. Activate the scenario and set it to "Immediately" processing

---

## Hardcoded Values to Configure

| Value | Where to find it | Used in |
|---|---|---|
| Scott's Lawmatics User ID | Lawmatics → Settings → Users, or GET /v1/users | Task assigned_to |
| Default priority | Skill default is "medium" | Task creation |
| Webhook URL | Make Module 1 after creation | SKILL.md |

---

## Troubleshooting

- **Webhook returns 404:** Scenario is paused or deleted. Reactivate in Make.
- **Matter not found:** Search only checks matters (not contacts). Verify the
  client has an active matter in Lawmatics.
- **Auth errors on HTTP module:** OAuth token may have expired. Re-authorize
  the Lawmatics connection in Make.
- **Subtasks not created:** Check that the iterator is connected and the
  task_id is being passed correctly from the Create Task module.
