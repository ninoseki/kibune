from kibune import models, schemas

from .base import CRUDBase


class CRUDLog(CRUDBase[models.Log, schemas.LogCreate, schemas.LogUpdate]):
    pass


log = CRUDLog(models.Log)
