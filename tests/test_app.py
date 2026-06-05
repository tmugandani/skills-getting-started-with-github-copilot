from src import app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Basketball Club", "Art Club", "Choir", "Debate Team", "Math Olympiad"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == expected_activities
    chess_club = data["Chess Club"]
    assert isinstance(chess_club["participants"], list)
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"


def test_root_redirects_to_static_index(client):
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_signup_for_activity_succeeds(client):
    # Arrange
    email = "newstudent@mergington.edu"
    assert email not in app_module.activities["Chess Club"]["participants"]

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_existing_participant_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"
    assert email in app_module.activities["Chess Club"]["participants"]

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    email = "tempstudent@mergington.edu"
    signup_response = client.post("/activities/Gym Class/signup", params={"email": email})
    assert signup_response.status_code == 200
    assert email in app_module.activities["Gym Class"]["participants"]

    # Act
    response = client.delete("/activities/Gym Class/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Gym Class"}
    assert email not in app_module.activities["Gym Class"]["participants"]


def test_signup_for_invalid_activity_returns_not_found(client):
    # Arrange
    email = "invalid@mergington.edu"

    # Act
    response = client.post("/activities/Unknown Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_invalid_activity_returns_not_found(client):
    # Arrange
    email = "missing@mergington.edu"

    # Act
    response = client.delete("/activities/Unknown Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_nonexistent_participant_returns_not_found(client):
    # Arrange
    email = "missing@mergington.edu"
    assert email not in app_module.activities["Chess Club"]["participants"]

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
