from fastapi import APIRouter

from code.api import (checker, v1)

router = APIRouter()

router.include_router(checker.router, prefix='')

router.include_router(checker.router, prefix='/api/v1')
