import uvicorn
from fastapi import FastAPI

from application.api.view_auth import router as router_auth
from application.api.view_user import router as router_user
from application.api.view_project import router as router_project
from application.api.view_tasks import router as router_task
from application.pages.router_base import router as router_pages
from application.pages.router_admin import router as router_admin

main_app = FastAPI()


main_app.include_router(router_auth)
main_app.include_router(router_user)
main_app.include_router(router_project)
main_app.include_router(router_task)
main_app.include_router(router_pages)
main_app.include_router(router_admin)


if __name__ == "__main__":
    uvicorn.run("application.main:main_app", reload=True)
