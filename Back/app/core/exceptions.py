class AppException(Exception):
    status_code: int
    detail: str

    def __init__(self, detail: str):
        self.detail = detail




class BadRequestException(AppException):
    status_code = 400

class UnauthorizedException(AppException):
    status_code = 401

class ForbiddenException(AppException):
    status_code = 403

class NotFoundException(AppException):
    status_code = 404

class ConflictException(AppException):
    status_code = 409




