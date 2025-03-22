from fastapi import APIRouter
from models.role_model import Role,RoleOut
from controllers.role_controller import addRoles,getRoles,deleteRole,getRoleById

router = APIRouter()

@router.post("/role/")
async def add_Role(role:Role):
    return await addRoles(role)

@router.get("/role/")
async def ger_Roles():
    return await getRoles()

@router.delete("/role/{roleId}")
async def delete_role(roleId:str):
    return await deleteRole(roleId)

@router.get("/role/{roleId}")
async def get_role_byId(roleId:str):
    return await getRoleById(roleId)