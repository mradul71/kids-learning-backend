from flask import Blueprint, request
from app.services.Block import BlockService
from app.utils.Middleware import check_token

block_project_router = Blueprint('block_project_router', __name__)
querystring = {"base64_encoded":"true","fields":"*"}

@block_project_router.route('/create-project', methods=['POST'])
@check_token
def create_project():
    user_id = request.user["user_id"]
    file_name = request.form.get("file_name")
    try:
        BlockService.create_project(user_id, file_name)
        return {"status" : "Success"}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500

@block_project_router.route('/submit-project', methods=['POST'])
@check_token
def submit_project():
    block_code = request.form.get("block_code")
    block_code_xml = request.form.get("block_code_xml")
    user_id = request.user["user_id"]
    file_name = request.form.get("file_name")
    file_id = request.form.get("file_id")
    try:
        BlockService.submit_project(user_id, block_code, block_code_xml, file_name, file_id)
        return {"status" : "Success"}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500
    
@block_project_router.route('/update-project', methods=['POST'])
@check_token
def update_project():
    project_id = request.form.get("project_id")
    source_code = request.form.get("source_code")
    language_id = request.form.get("language_id")
    stdin = request.form.get("stdin")
    result = request.form.get("result")
    errors = request.form.get("errors")
    user_id = request.user["user_id"]
    try:
        BlockService.update_project(project_id, user_id, source_code, language_id, stdin, result, errors)
        return {"status" : "Success"}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500
    
@block_project_router.route('/all-projects', methods=['GET'])
@check_token
def get_projects():
    user_id = request.user["user_id"]
    try:
        projects = BlockService.get_all_projects(user_id)
        return {"status" : "Success", "projects": projects}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500
    
@block_project_router.route('/project-info/<projectid>', methods=['GET'])
@check_token
def get_project_info(projectid):
    user_id = request.user["user_id"]
    try:
        project_info = BlockService.get_project_info(projectid, user_id)
        return {"status" : "Success", "project_info": project_info}, 200
    except Exception as e:
        return {"status" : "Failure", "message": str(e)}, 500