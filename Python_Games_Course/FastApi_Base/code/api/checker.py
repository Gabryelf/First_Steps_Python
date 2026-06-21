from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter()


@router.get('/healthchecker', include_in_schema=False,)
async def get_healthchecker() -> Response:
    return Response(status_code=status.HTTP_200_OK)
