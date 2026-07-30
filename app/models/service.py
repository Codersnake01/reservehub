from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)  # duración en minutos
    price: Mapped[float] = mapped_column(nullable=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    provider = relationship("User", back_populates="services")
    schedules = relationship("Schedule", back_populates="service")
    reservations = relationship("Reservation", back_populates="service")