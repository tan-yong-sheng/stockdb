from app.core.models.system_model import SystemModel

system_model = SystemModel()


def get_current_system():
    return system_model
