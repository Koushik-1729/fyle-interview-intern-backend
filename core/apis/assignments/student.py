from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
from core.models.assignments import AssignmentStateEnum
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    if 'content' not in incoming_payload or incoming_payload['content'] is None:
        return APIResponse.error(message="Content cannot be null", status_code=400)
    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)
    assignment = Assignment.query.get(submit_assignment_payload.id)

    if not assignment:
        return APIResponse.error(message="Assignment not found", status_code=404)

    if assignment.state != AssignmentStateEnum.DRAFT:
        return APIResponse.error(message='only draft assignment can be submitted', status_code=400)

    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
    )
    
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)

@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
# @decorators.authenticate_student
def list_student_assignments(p):
    """List all assignments created by the authenticated student."""
    assignments = Assignment.query.filter_by(student_id=p.student_id).all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@student_assignments_resources.route('/assignments/all', methods=['GET'], strict_slashes=False)
# @decorators.authenticate_student
def list_all_assignments():
    """List all assignments."""
    assignments = Assignment.query.all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)
