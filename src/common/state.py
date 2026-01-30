
class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.current_user = None
            cls._instance.is_admin = False
            cls._instance.language = 'pt'
            cls._instance.check_access = False
            cls._instance.close_after = False
        return cls._instance

    def reset(self):
        self.current_user = None
        self.is_admin = False

state = AppState()
