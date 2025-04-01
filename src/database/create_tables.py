from . import engine, Base
from .models import TemperatureData

# Create tables
Base.metadata.create_all(engine)
