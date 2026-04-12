# Python Team Coding Standards

## Architecture Overview

**Clean Architecture Pattern**: Core → Infrastructure → Presentation
- **Core**: Business logic, domain models, service interfaces
- **Infrastructure**: SQLAlchemy, cloud services, repository implementations  
- **FastAPI/Flask**: API endpoints, minimal business logic

## Core Package Expectations

### Structure
```
core/
├── models/           # Domain entities and Pydantic models
├── services/         # Business logic services
├── interfaces/       # Repository and provider protocols
└── schemas/          # Request/Response DTOs
```

### Business Services
- Encapsulate all business logic
- Depend only on protocols/interfaces (no direct dependencies on Infrastructure)
- Return Result[T] pattern for error handling
- Must be unit testable with mocked dependencies

```python
from typing import Protocol
from core.interfaces import OrderRepository, PaymentProvider
from core.schemas import CreateOrderRequest, OrderDto
from core.utils import Result

class OrderService:
    def __init__(self, repository: OrderRepository, payment_provider: PaymentProvider):
        self._repository = repository
        self._payment_provider = payment_provider

    async def create_order(self, request: CreateOrderRequest) -> Result[OrderDto]:
        """Business logic only - no direct database or external service calls"""
        try:
            # Business validation logic here
            order = await self._repository.create(request.to_domain())
            return Result.success(OrderDto.from_domain(order))
        except Exception as e:
            return Result.failure(str(e))
```

### Interface Definitions (Protocols)
- Define all external dependencies as protocols in Core
- Repository protocols for data access
- Provider protocols for external services

```python
from typing import Protocol, Optional
from core.models import Order

class OrderRepository(Protocol):
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        ...
    
    async def create(self, order: Order) -> Order:
        ...
    
    async def update(self, order: Order) -> Order:
        ...

class PaymentProvider(Protocol):
    async def process_payment(self, request: PaymentRequest) -> PaymentResult:
        ...
```

### Domain Models
- Use Pydantic models for validation and serialization
- Dataclasses for simple domain entities
- Business logic methods on entities

```python
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from pydantic import BaseModel, validator

@dataclass
class Order:
    id: Optional[int] = None
    customer_id: int = 0
    total_amount: Decimal = Decimal('0.00')
    items: List['OrderItem'] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []
    
    def add_item(self, item: 'OrderItem') -> None:
        """Business logic method"""
        self.items.append(item)
        self.total_amount += item.price * item.quantity
    
    def calculate_total(self) -> Decimal:
        """Business rule implementation"""
        return sum(item.price * item.quantity for item in self.items)
```

## Infrastructure Package Expectations

### Structure
```
infrastructure/
├── database/         # SQLAlchemy models and session management
├── repositories/     # Repository implementations
└── providers/        # External service implementations
```

### Repository Pattern
- Implement Core protocols
- Use SQLAlchemy for data access
- Handle all database operations

```python
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.interfaces import OrderRepository
from core.models import Order
from infrastructure.database.models import OrderModel

class SqlAlchemyOrderRepository:
    def __init__(self, session: Session):
        self._session = session

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        stmt = select(OrderModel).where(OrderModel.id == order_id)
        result = await self._session.execute(stmt)
        order_model = result.scalar_one_or_none()
        return order_model.to_domain() if order_model else None
    
    async def create(self, order: Order) -> Order:
        order_model = OrderModel.from_domain(order)
        self._session.add(order_model)
        await self._session.commit()
        await self._session.refresh(order_model)
        return order_model.to_domain()
```

### SQLAlchemy Standards
- Separate model definitions in database package
- Use proper column types for decimals: `DECIMAL(18,2)`
- Use Alembic for migrations
- Implement domain model conversion methods

```python
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from core.models import Order

Base = declarative_base()

class OrderModel(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    total_amount = Column(DECIMAL(18, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    items = relationship("OrderItemModel", back_populates="order")
    
    def to_domain(self) -> Order:
        """Convert to domain model"""
        return Order(
            id=self.id,
            customer_id=self.customer_id,
            total_amount=self.total_amount,
            items=[item.to_domain() for item in self.items]
        )
    
    @classmethod
    def from_domain(cls, order: Order) -> 'OrderModel':
        """Create from domain model"""
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            total_amount=order.total_amount
        )
```

### Provider Implementations
- Implement Core provider protocols
- Handle external service communications (APIs, cloud services)
- Include proper error handling and logging

```python
import httpx
import logging
from core.interfaces import PaymentProvider
from core.schemas import PaymentRequest, PaymentResult

logger = logging.getLogger(__name__)

class StripePaymentProvider:
    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url
    
    async def process_payment(self, request: PaymentRequest) -> PaymentResult:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._base_url}/charges",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json=request.dict()
                )
                response.raise_for_status()
                return PaymentResult.from_dict(response.json())
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")
            raise
```

## Web Framework Expectations (FastAPI/Flask)

### Endpoint Structure
- Minimal business logic in endpoints
- Inject and use Core services directly
- Handle request/response serialization
- Use proper async patterns

```python
from fastapi import APIRouter, Depends, HTTPException
from core.services import OrderService
from core.schemas import CreateOrderRequest, OrderDto
from dependencies import get_order_service

router = APIRouter()

@router.post("/orders", response_model=OrderDto)
async def create_order(
    request: CreateOrderRequest,
    order_service: OrderService = Depends(get_order_service)
):
    result = await order_service.create_order(request)
    
    if result.is_success:
        return result.value
    else:
        raise HTTPException(status_code=400, detail=result.error)

@router.get("/orders")
async def get_orders(order_service: OrderService = Depends(get_order_service)):
    result = await order_service.get_orders()
    
    if result.is_success:
        return result.value
    else:
        raise HTTPException(status_code=500, detail=result.error)
```

### Dependency Injection
- Use FastAPI's dependency injection system
- Register services in dependencies module
- Handle database session management

```python
# dependencies.py
from sqlalchemy.orm import Session
from core.services import OrderService
from infrastructure.repositories import SqlAlchemyOrderRepository
from infrastructure.providers import StripePaymentProvider
from database import get_db_session

def get_order_service(session: Session = Depends(get_db_session)) -> OrderService:
    repository = SqlAlchemyOrderRepository(session)
    payment_provider = StripePaymentProvider(api_key="...", base_url="...")
    return OrderService(repository, payment_provider)
```

## Naming Conventions

- **Classes/Functions**: `PascalCase` for classes, `snake_case` for functions
- **Variables/Parameters**: `snake_case`  
- **Private Methods/Attributes**: `_snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Protocols**: `PascalCase` (same as classes)
- **Test Classes**: `Test{ClassName}`

## Testing Requirements

### Unit Testing
- Test all business services in Core using pytest
- Mock all dependencies using protocols
- Use AAA pattern (Arrange, Act, Assert)
- One test file per service

```python
import pytest
from unittest.mock import Mock, AsyncMock
from core.services import OrderService
from core.interfaces import OrderRepository, PaymentProvider
from core.schemas import CreateOrderRequest
from core.models import Order

class TestOrderService:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=OrderRepository)
    
    @pytest.fixture
    def mock_payment_provider(self):
        return Mock(spec=PaymentProvider)
    
    @pytest.fixture
    def service(self, mock_repository, mock_payment_provider):
        return OrderService(mock_repository, mock_payment_provider)

    @pytest.mark.asyncio
    async def test_create_order_valid_request_returns_success(
        self, service, mock_repository
    ):
        # Arrange
        request = CreateOrderRequest(customer_id=1, items=[])
        expected_order = Order(id=1, customer_id=1)
        mock_repository.create = AsyncMock(return_value=expected_order)
        
        # Act
        result = await service.create_order(request)
        
        # Assert
        assert result.is_success
        assert result.value.id == 1
        mock_repository.create.assert_called_once()
```

### Integration Testing
- Test repository implementations with test database
- Use pytest fixtures for database setup/teardown
- Test API endpoints with TestClient

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models import Base
from infrastructure.repositories import SqlAlchemyOrderRepository

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.mark.asyncio
async def test_order_repository_create(test_db):
    # Integration test with real database
    repository = SqlAlchemyOrderRepository(test_db)
    order = Order(customer_id=1)
    
    result = await repository.create(order)
    
    assert result.id is not None
    assert result.customer_id == 1
```

## Utility Classes

### Result Pattern
```python
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Result(Generic[T]):
    def __init__(self, value: Optional[T] = None, error: Optional[str] = None):
        self._value = value
        self._error = error
    
    @property
    def is_success(self) -> bool:
        return self._error is None
    
    @property
    def value(self) -> T:
        if self._error:
            raise ValueError(f"Cannot access value of failed result: {self._error}")
        return self._value
    
    @property
    def error(self) -> str:
        return self._error or ""
    
    @classmethod
    def success(cls, value: T) -> 'Result[T]':
        return cls(value=value)
    
    @classmethod
    def failure(cls, error: str) -> 'Result[T]':
        return cls(error=error)
```

## Essential Rules

### Core Package
- ✅ No dependencies on Infrastructure or Presentation
- ✅ All business logic in services
- ✅ Rich domain models with business rules
- ✅ Protocols for all external dependencies

### Infrastructure Package
- ✅ Implements Core protocols
- ✅ Uses SQLAlchemy for data access
- ✅ Handles external service communications
- ✅ Separate model definitions with domain conversion

### Web Framework Layer  
- ✅ Minimal business logic in endpoints
- ✅ Uses Core services via dependency injection
- ✅ Proper async/await patterns
- ✅ Handles request/response serialization

### General
- ✅ Follow PEP 8 naming conventions
- ✅ Include comprehensive unit and integration tests
- ✅ Use Result[T] pattern for service methods
- ✅ Implement proper logging and error handling
- ✅ Use dependency injection for service management
- ✅ Type hints for all public interfaces

## Dev Testing
- Tasks should always include unit tests for business services
- Integration tests for repository implementations
- API endpoint tests using TestClient
- Use pytest fixtures for test setup and dependency mocking
