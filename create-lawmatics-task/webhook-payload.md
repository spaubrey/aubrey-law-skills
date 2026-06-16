# Webhook Payload Reference

## Request Payload (Claude → Make)

```json
{
  "task_name": "string (required) — short name for the task",
  "due_date": "string (optional) — ISO 8601 date, YYYY-MM-DD",
  "description": "string (optional) — additional task detail",
  "matter_search": "string (optional) — client last name or matter name for linking",
  "subtasks": ["string (optional) — array of subtask names"],
  "priority": "string (optional) — low, medium, or high. Default: medium"
}
```

### Examples

**Full task with subtasks:**
```json
{
  "task_name": "Prepare Smith trust closing package",
  "due_date": "2026-06-20",
  "description": "All documents signed 6/15. Prepare and send closing package.",
  "matter_search": "Smith",
  "subtasks": [
    "Draft closing letter",
    "Prepare funding instructions",
    "Draft assignment of personal property",
    "Email package to client"
  ],
  "priority": "high"
}
```

**Simple task, no matter link:**
```json
{
  "task_name": "Renew CLE registration",
  "due_date": "2026-07-01",
  "description": "",
  "matter_search": "",
  "subtasks": [],
  "priority": "low"
}
```

**Task inferred from casual request:**

User says: *"Remind me to follow up with the Davis family next Monday about
their signed documents."*

```json
{
  "task_name": "Follow up with Davis re: signed documents",
  "due_date": "2026-06-01",
  "description": "Check whether signed estate plan documents have been returned.",
  "matter_search": "Davis",
  "subtasks": [],
  "priority": "medium"
}
```

---

## Response Payloads (Make → Claude)

### Success — task created with matter link
```json
{
  "success": true,
  "task_id": "12345",
  "task_name": "Prepare Smith trust closing package",
  "matter": "Smith, John & Jane",
  "subtasks_created": 4
}
```

### Success — task created without matter link
```json
{
  "success": true,
  "task_id": "12346",
  "task_name": "Renew CLE registration",
  "matter": null,
  "subtasks_created": 0
}
```

### Error — no matter found
```json
{
  "error": "no_matter_found",
  "search_term": "Daviss"
}
```

### Error — ambiguous matter
```json
{
  "error": "ambiguous_matter",
  "candidates": [
    {"id": "100", "name": "Davis, Michael"},
    {"id": "101", "name": "Davis, Sarah & Tom"}
  ]
}
```

### Error — subtask partial failure
```json
{
  "error": "subtask_partial_failure",
  "task_id": "12345",
  "task_name": "Prepare Smith trust closing package",
  "created": ["Draft closing letter", "Prepare funding instructions"],
  "failed": ["Draft assignment of personal property", "Email package to client"]
}
```
