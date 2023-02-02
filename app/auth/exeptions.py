from pydantic.errors import PydanticValueError


class InvalidUsernameError(PydanticValueError):
    code = "invalid.user_id"
    msg_template = "{msg}"


class InvalidPasswordError(PydanticValueError):
    code = "invalid.password"
    msg_template = "{msg}"


class InvalidConfigurationError(PydanticValueError):
    code = "invalid.configuration"
    msg_template = "{msg}"
