from typing import Annotated

from fastapi import Depends, Cookie, Header

from api.dependencies.current_user_deps import CurrentUserDep
from common.schemas.filters.mixins import DataRangeBaseFilterSchema
from core.constants import REFRESH
from modules.users.schemas.auth import EmptyUserSchema
from modules.users.services.auth import AuthService
from modules.users.services.user import UserService
from modules.users.unit_of_works.auth import AuthUOW
from modules.users.unit_of_works.user import UserUOW

# region ---------------------------------- COMMON ---------------------------------------
UserDep = Annotated[EmptyUserSchema, Depends(CurrentUserDep.get_current_user)]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- USER ---------------------------------------
UserUOWDep = Annotated[UserUOW, Depends(UserUOW)]
UserServiceDep = Annotated[UserService, Depends(UserService)]
UserFilterDep = Annotated[DataRangeBaseFilterSchema, Depends(DataRangeBaseFilterSchema)]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- AUTH ---------------------------------------
AuthUOWDep = Annotated[AuthUOW, Depends(AuthUOW)]
AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
# endregion ------------------------------------------------------------------------------

# region ---------------------------------- JWT ---------------------------------------
RefreshDep = Annotated[str, Cookie(alias=REFRESH, include_in_schema=False)]
TokenDep = Annotated[str, Header()]
RolesDep = Annotated[tuple[str, ...], Header()]
HeadersDep = Annotated[str, Header(...)]
# endregion ------------------------------------------------------------------------------
