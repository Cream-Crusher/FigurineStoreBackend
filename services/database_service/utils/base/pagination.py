from typing import Optional

from fastapi import Query, HTTPException


class Pagination:
    def __init__(self,
                 page: Optional[int] = Query(default=None, ge=1, description="page > 1"),
                 size: Optional[int] = Query(default=None, le=50, description="size > 1 and <= 50")):

        if not page or not size:
            raise HTTPException(status_code=400, detail='page and size must be specified together')

        self.page = page
        self.size = size
        self.skip = (page - 1) * size if page else 0
        self.limit = size
