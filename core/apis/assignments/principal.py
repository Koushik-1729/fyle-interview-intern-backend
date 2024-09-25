from flask import Blueprint,request 
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.apis.teachers.schema import TeacherSchema
from core.apis.assignments.schema import AssignmentGradeSchema
from core.models.assignments import AssignmentStateEnum
from core.models.teachers import Teacher
from .schema import AssignmentSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """List all submitted and graded assignments"""
    assignments = Assignment.get_all_submitted_assignments()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.get(grade_payload.id)
    if not assignment:
        return APIResponse.error("Assignment not found", 404)
    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.error("Cannot grade an assignment in Draft state", 400)
    assignment.grade = grade_payload.grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)
