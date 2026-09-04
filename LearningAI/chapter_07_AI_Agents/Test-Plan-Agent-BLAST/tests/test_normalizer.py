from tools.normalizer import DataNormalizer


def test_normalize_issue_handles_atlassian_doc_description():
    raw_issue = {
        "key": "PROJ-123",
        "fields": {
            "summary": "User login validates credentials",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Given the user enters a valid email"},
                            {"type": "text", "text": "When they click login"},
                            {"type": "text", "text": "Then they are redirected to the dashboard"},
                        ],
                    }
                ],
            },
            "status": {"name": "In Progress"},
            "priority": {"name": "High"},
            "labels": [],
            "components": [],
            "assignee": None,
            "created": "2026-09-01T10:00:00.000-0400",
            "updated": "2026-09-01T10:30:00.000-0400",
            "customfield_10001": None,
        },
    }

    normalized = DataNormalizer().normalize_issue(raw_issue)

    assert normalized["issueKey"] == "PROJ-123"
    assert normalized["title"] == "User login validates credentials"
    assert len(normalized["acceptanceCriteria"]) > 0
