from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate

migration = Migrate()
bcrypt_flask = Bcrypt()
cors = CORS()

try:
    from .src.entities.model import db
    from .src.entities.model.chip import Chip
    from .src.entities.model.board import Board
    from .src.entities.model.theme import Theme
    from .src.entities.model.user import User
    from .src.entities.model.inventory import Inventory
    from .src.utils.messages import MSG_TOKEN_EXPIRED, MSG_INVALID_CREDENTIALS, MSG_PERMISSION_DENIED
    from .src.entities.DTO import ma
    from .config import config
except ImportError:
    from src.entities.model import db
    from src.entities.model.chip import Chip
    from src.entities.model.board import Board
    from src.entities.model.theme import Theme
    from src.entities.model.user import User
    from src.entities.model.inventory import Inventory
    from src.utils.messages import MSG_TOKEN_EXPIRED, MSG_INVALID_CREDENTIALS
    from src.entities.DTO import ma
    from config import config