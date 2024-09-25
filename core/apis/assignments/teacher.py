from flask import Blueprint
from core import db
from core.libs import assertions

from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments for the authenticated teacher"""
    teacher_id = p.teacher_id  
    teachers_assignments = Assignment.get_assignments_by_teacher(teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)



@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


@teacher_assignments_resources.route('/assignments/submitted', methods=['GET'], strict_slashes=False)
@decorators.authenticate_teacher
def list_teacher_assignments(p):
    """List all assignments submitted to the teacher"""
    # Fetch assignments for the teacher using their ID
    assignments = Assignment.query.filter_by(teacher_id=p.teacher_id).all()
    
    # Serialize the assignments to return
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    
    # Return the response
    return APIResponse.respond(data=assignments_dump)



