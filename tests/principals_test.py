import pytest
from core.models.assignments import AssignmentStateEnum, GradeEnum,Assignment
from core.models.teachers import Teacher
from core import db


def test_get_assignments(client, h_principal_1):
    response = client.get(
        '/principal/assignments',
        headers=h_principal_1
    )

    assert response.status_code == 200


    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


@pytest.fixture(scope='function')
def draft_assignment(client, h_principal_1):
    """Fixture to create a draft assignment for testing."""
    assignment = Assignment(
        student_id=1,  # Adjust based on your test data
        content="Sample assignment content",
        state=AssignmentStateEnum.DRAFT
    )
    db.session.add(assignment)
    db.session.commit()
    yield assignment  # This will be the assignment used in the test
    # Cleanup code
    db.session.delete(assignment)
    db.session.commit()

def test_grade_assignment_draft_assignment(client, h_principal_1, draft_assignment):
    """
    Failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': draft_assignment.id,  # Use the dynamic ID
            'grade': GradeEnum.A.value
        },
        headers=h_principal_1
    )
    
    assert response.status_code == 400
    assert response.json['error'] == "Cannot grade an assignment in Draft state"


def test_grade_assignment(client, h_principal_1):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,
            'grade': GradeEnum.C.value
        },
        headers=h_principal_1
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal_1):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal_1
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_list_assignments(client, h_principal_1):
    """Test listing all assignments."""
    response = client.get('/principal/assignments', headers=h_principal_1)
    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)  # Check that data is a list
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED.value, AssignmentStateEnum.GRADED.value]


def test_list_teachers(client, h_principal_1):
    """Test listing all teachers."""
    response = client.get('/principal/teachers', headers=h_principal_1)
    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)  # Check that data is a list
    assert len(data) > 0  # Assuming there are teachers in the database


# def test_get_teacher_by_id(client, h_principal_1):
#     """Test getting a specific teacher by ID."""
#     # Assuming there's a teacher with ID 1
#     response = client.get('/principal/teachers?id=1', headers=h_principal_1)
#     assert response.status_code == 200

#     data = response.json['data']
#     assert data['id'] == 1  # Adjust according to your model


# def test_get_teacher_not_found(client, h_principal_1):
#     """Test getting a teacher with a non-existent ID."""
#     response = client.get('/principal/teachers?id=9999', headers=h_principal_1)
#     assert response.status_code == 404
#     assert response.json['error'] == "Teacher not found"


def test_list_teachers_no_id(client, h_principal_1):
    """Test listing all teachers without specifying an ID."""
    response = client.get('/principal/teachers', headers=h_principal_1)
    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)  

