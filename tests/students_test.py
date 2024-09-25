def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None
def test_submit_assignment_student_1(client, h_student_1):
    # Create a draft assignment first
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': 'Draft Assignment Content'}
    )
    
    assert create_response.status_code == 200
    assignment_id = create_response.json['data']['id']  # Get the newly created assignment ID

    # Now submit the created assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'teacher_id': 2  # Use a valid teacher ID
        }
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2
def test_assignment_resubmit_error(client, h_student_1):
    # Create a draft assignment
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': 'This is a draft assignment.'}
    )
    assert create_response.status_code == 200
    assignment_id = create_response.json['data']['id']

    # Submit the assignment for the first time
    submit_response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': assignment_id, 'teacher_id': 1}
    )
    assert submit_response.status_code == 200  # First submission should succeed

    # Attempt to resubmit the same assignment
    resubmit_response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': assignment_id, 'teacher_id': 1}
    )
    assert resubmit_response.status_code == 400  # Resubmission should fail
    assert resubmit_response.json['error'] == 'only draft assignment can be submitted'  # Adjust based on your actual error message

def test_list_student_assignments(client, h_student_1):
        response = client.get('/student/assignments', headers=h_student_1)

        assert response.status_code == 200
        data = response.json['data']
        assert isinstance(data, list)
        for assignment in data:
            assert assignment['student_id'] == 1  
def test_list_all_assignments(client):
    response = client.get('/student/assignments/all')

    assert response.status_code == 200
    data = response.json['data']
    assert isinstance(data, list)  # Ensure the data is a list
    # You may want to add more assertions based on expected results

