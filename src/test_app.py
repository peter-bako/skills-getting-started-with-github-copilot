import pytest
from fastapi.testclient import TestClient
from app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    # Add once
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Already signed up for this activity"

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_all_activities():
    email = "allactivities@mergington.edu"
    for activity in activities.keys():
        # Remove if already signed up
        if email in activities[activity]["participants"]:
            activities[activity]["participants"].remove(email)
        response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200, f"Failed to sign up for {activity}"
        assert email in activities[activity]["participants"], f"Email not in participants for {activity}"
