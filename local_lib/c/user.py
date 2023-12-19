from chordate.interfaces.controller import ControllerBase
from apps.authentication.local_lib.m.user import User


class UserController(ControllerBase):
    user = User()

    def set_user_info(self,
                      username: str,
                      first_name: str,
                      last_name: str,
                      email: str,
                      organization: str,
                      phone_number: str,
                      password: str) -> None:
        self.user.update(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            organization=organization,
            phone_number=phone_number,
            password=password
        )
        return
