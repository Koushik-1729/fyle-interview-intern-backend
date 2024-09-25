import unittest
from unittest.mock import patch, MagicMock
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core.models.students import Student
from core.models.teachers import Teacher
from core.apis.decorators import AuthPrincipal
from core.libs import assertions


class TestAssignmentModel(unittest.TestCase):
    @patch('core.models.assignments.db.session')
    def test_upsert_existing_assignment(self, mock_session):
        existing_assignment = Assignment(id=1, content="Original content", state=AssignmentStateEnum.DRAFT)
        
        with patch.object(Assignment, 'get_by_id', return_value=existing_assignment):
            new_assignment = Assignment(id=1, content="Updated content")
            result = Assignment.upsert(new_assignment)
            
            self.assertEqual(result.content, "Updated content")
            mock_session.flush.assert_called_once()
    @patch('core.models.assignments.db.session')
    def test_upsert_new_assignment(self, mock_session):
        new_assignment = Assignment(content="New assignment content")
        result = Assignment.upsert(new_assignment)
        mock_session.add.assert_called_once_with(new_assignment)
        mock_session.flush.assert_called_once()
        self.assertEqual(result.content, "New assignment content")

    @patch('core.models.assignments.db.session')
    def test_get_all_submitted_assignments(self, mock_session):
        mock_query = MagicMock()
        mock_query.all.return_value = [
            Assignment(id=1, state=AssignmentStateEnum.SUBMITTED),
            Assignment(id=2, state=AssignmentStateEnum.GRADED)
        ]
        with patch.object(Assignment, 'filter', return_value=mock_query):
            result = Assignment.get_all_submitted_assignments()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].state, AssignmentStateEnum.SUBMITTED)
            self.assertEqual(result[1].state, AssignmentStateEnum.GRADED)
# if __name__ == '__main__':
#     unittest.main()
