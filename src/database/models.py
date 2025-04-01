from sqlalchemy import Column, Integer, String, Date, Double, UniqueConstraint
from .database import Base  # Import Base from database.py


class TemperatureData(Base):
    __tablename__ = (
        "Temperature_Data_Test"  # Change to "Temperature_Data" for production
    )

    Temperature_ID = Column(Integer, primary_key=True, autoincrement=True)
    Source_Name = Column(String(50), nullable=False)
    Date = Column(Date, nullable=False)
    Latitude = Column(Double, nullable=False)
    Longitude = Column(Double, nullable=False)
    Min_Temp = Column(Double)
    Max_Temp = Column(Double)
    Avg_Temp = Column(Double)

    # Unique Constraint
    __table_args__ = (
        UniqueConstraint(
            "Date", "Latitude", "Longitude", "Source_Name", name="unique_test"
        ),
    )
