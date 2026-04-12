# .NET Core Team Coding Standards

## Architecture Overview

**Clean Architecture Pattern**: Core → Infrastructure → Presentation
- **Core**: Business logic, domain models, service interfaces
- **Infrastructure**: EF Core, cloud services, repository implementations  
- **Blazor Server**: UI components, minimal code-behind logic

## Core Library Expectations

### Structure
```
Core/
├── Models/           # Domain entities and DTOs
├── Services/         # Business logic services
└── Interfaces/       # Repository and provider contracts
```

### Business Services
- Encapsulate all business logic
- Depend only on interfaces (no direct dependencies on Infrastructure)
- Return Result<T> pattern for error handling
- Must be unit testable with mocked dependencies

```csharp
public class OrderService : IOrderService
{
    private readonly IOrderRepository _repository;
    private readonly IPaymentProvider _paymentProvider;

    public async Task<Result<OrderDto>> CreateOrderAsync(CreateOrderRequest request)
    {
        // Business logic only - no direct database or external service calls
    }
}
```

### Interface Definitions
- Define all external dependencies as interfaces in Core
- Repository interfaces for data access
- Provider interfaces for external services

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task<Order> AddAsync(Order order);
    Task UpdateAsync(Order order);
}

public interface IPaymentProvider
{
    Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request);
}
```

### Domain Models
- Rich domain models with business rules
- Private setters, public readonly collections
- Business logic methods on entities

## Infrastructure Layer Expectations

### Structure
```
Infrastructure/
├── Data/             # EF Core DbContext and configurations
├── Repositories/     # Repository implementations
└── Providers/        # External service implementations
```

### Repository Pattern
- Implement Core interfaces
- Use EF Core for data access
- Handle all database operations

```csharp
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;

    public async Task<Order?> GetByIdAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .FirstOrDefaultAsync(o => o.Id == id);
    }
}
```

### EF Core Standards
- Separate entity configurations using `IEntityTypeConfiguration<T>`
- Use proper column types for decimals: `decimal(18,2)`
- Apply configurations in `OnModelCreating` via assembly scanning

```csharp
public class ApplicationDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
}
```

### Provider Implementations
- Implement Core provider interfaces
- Handle external service communications (APIs, cloud services)
- Include proper error handling and logging

## Blazor Server Expectations

### Component Structure
- Minimal code-behind logic
- Inject and use Core services directly
- Handle loading and error states
- Use proper async patterns

```csharp
@inject IOrderService OrderService

@code {
    private List<OrderDto> orders = new();
    private bool isLoading = true;

    protected override async Task OnInitializedAsync()
    {
        isLoading = true;
        var result = await OrderService.GetOrdersAsync();
        
        if (result.IsSuccess)
            orders = result.Value.ToList();
            
        isLoading = false;
    }
}
```

### Component Guidelines
- Keep business logic in Core services
- Use dependency injection for services
- Implement proper state management
- Handle async operations correctly

## Naming Conventions

- **Classes/Methods/Properties**: `PascalCase`
- **Parameters/Variables**: `camelCase`  
- **Private Fields**: `_camelCase`
- **Interfaces**: `IPascalCase`
- **Test Classes**: `{ClassName}Tests`

## Testing Requirements

### Unit Testing
- Test all business services in Core
- Mock all dependencies using interfaces
- Use AAA pattern (Arrange, Act, Assert)
- One test class per service

```csharp
[TestClass]
public class OrderServiceTests
{
    private Mock<IOrderRepository> _mockRepository;
    private OrderService _service;

    [TestInitialize]
    public void Setup()
    {
        _mockRepository = new Mock<IOrderRepository>();
        _service = new OrderService(_mockRepository.Object);
    }

    [TestMethod]
    public async Task CreateOrder_ValidRequest_ReturnsSuccess()
    {
        // Arrange, Act, Assert
    }
}
```

## Essential Rules

### Core Layer
- ✅ No dependencies on Infrastructure or Presentation
- ✅ All business logic in services
- ✅ Rich domain models with business rules
- ✅ Interfaces for all external dependencies

### Infrastructure Layer
- ✅ Implements Core interfaces
- ✅ Uses EF Core for data access
- ✅ Handles external service communications
- ✅ Separate entity configurations

## dev testing
- tasks should always include unit tests for backend services

### Blazor Server Layer  
- ✅ Minimal code-behind logic
- ✅ Uses Core services via dependency injection
- ✅ Proper async/await patterns
- ✅ Handles loading and error states

### General
- ✅ Follow naming conventions
- ✅ Include comprehensive unit tests
- ✅ Use Result<T> pattern for service methods
- ✅ Implement proper logging and error handling
- ✅ Register services in DI container
