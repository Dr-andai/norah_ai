from fastapi import APIRouter

router = APIRouter()

@router.get("/sync/{repo_name}")
def sync_repo(repo_name: str):
    # Placeholder for GitHub repo sync logic
    return {"message": f"Synced {repo_name}"}
