# .NET Core Team Coding Standards

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Library Standards](#core-library-standards)
4. [Infrastructure Layer Standards](#infrastructure-layer-standards)
5. [Blazor Server Standards](#blazor-server-standards)
6. [Naming Conventions](#naming-conventions)
7. [Code Organization](#code-organization)
8. [Testing Standards](#testing-standards)
9. [Entity Framework Core Standards](#entity-framework-core-standards)
10. [General Best Practices](#general-best-practices)

## Architecture Overview

Our application follows a Clean Architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────┐
│           Presentation              │
│        (Blazor Server)              │
├─────────────────────────────────────┤
│          Infrastructure             │
│    (EF Core, Cloud Services)        │
├─────────────────────────────────────┤
│             Core                    │
│      (Business Logic)               │
└─────────────────────────────────────┘
```

**Dependency Flow**: Presentation → Infrastructure → Core
- Core layer has no dependencies on external frameworks
- Infrastructure layer depends on Core and implements its interfaces
- Presentation layer orchestrates Infrastructure and Core

## Project Structure

### Recommended Solution Structure
```
Solution.sln
├── src/
│   ├── CompanyName.ProjectName.Core/
│   ├── CompanyName.ProjectName.Infrastructure/
│   └── CompanyName.ProjectName.Web/
├── tests/
│   ├── CompanyName.ProjectName.Core.Tests/
│   ├── CompanyName.ProjectName.Infrastructure.Tests/
│   └── CompanyName.ProjectName.Web.Tests/
└── docs/
```

### Project Dependencies
- **Core**: No external dependencies (except base .NET libraries)
- **Infrastructure**: References Core, EF Core, cloud SDKs
- **Web**: References Core and Infrastructure
- **Tests**: Reference corresponding project under test

## Core Library Standards

### Business Logic Services
```csharp
// ✅ Good: Service with clear responsibility
public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IPaymentProvider _paymentProvider;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        IOrderRepository orderRepository,
        IPaymentProvider paymentProvider,
        ILogger<OrderService> logger)
    {
        _orderRepository = orderRepository;
        _paymentProvider = paymentProvider;
        _logger = logger;
    }

    public async Task<Result<OrderDto>> CreateOrderAsync(CreateOrderRequest request)
    {
        // Business logic implementation
    }
}
```

### Interface Definitions
All external dependencies must be defined as interfaces in the Core library:

```csharp
// Repository interfaces
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task<IEnumerable<Order>> GetByCustomerIdAsync(int customerId);
    Task<Order> AddAsync(Order order);
    Task UpdateAsync(Order order);
    Task DeleteAsync(int id);
}

// Provider interfaces (for external services)
public interface IPaymentProvider
{
    Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request);
}

public interface IEmailProvider
{
    Task SendEmailAsync(EmailMessage message);
}
```

### Domain Models
```csharp
// ✅ Good: Rich domain model with business rules
public class Order
{
    public int Id { get; private set; }
    public int CustomerId { get; private set; }
    public DateTime OrderDate { get; private set; }
    public OrderStatus Status { get; private set; }
    public decimal TotalAmount => OrderItems.Sum(x => x.TotalPrice);
    
    private readonly List<OrderItem> _orderItems = new();
    public IReadOnlyList<OrderItem> OrderItems => _orderItems.AsReadOnly();

    public void AddItem(int productId, int quantity, decimal unitPrice)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException("Cannot modify confirmed order");
            
        // Business logic for adding items
    }
}
```

### Result Pattern
Use Result pattern for service methods to handle success/failure states:

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T Value { get; }
    public string Error { get; }
    
    // Implementation details...
}
```

## Infrastructure Layer Standards

### Repository Implementation
```csharp
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;

    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Order?> GetByIdAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .FirstOrDefaultAsync(o => o.Id == id);
    }

    public async Task<Order> AddAsync(Order order)
    {
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
        return order;
    }
}
```

### Provider Implementation
```csharp
public class EmailProvider : IEmailProvider
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<EmailProvider> _logger;

    public EmailProvider(IConfiguration configuration, ILogger<EmailProvider> logger)
    {
        _configuration = configuration;
        _logger = logger;
    }

    public async Task SendEmailAsync(EmailMessage message)
    {
        // Cloud service implementation
    }
}
```

## Blazor Server Standards

### Component Structure
```csharp
@page "/orders"
@using CompanyName.ProjectName.Core.Services
@inject IOrderService OrderService

<h3>Orders</h3>

<!-- Component markup -->

@code {
    private List<OrderDto> orders = new();
    private bool isLoading = true;

    protected override async Task OnInitializedAsync()
    {
        await LoadOrdersAsync();
    }

    private async Task LoadOrdersAsync()
    {
        isLoading = true;
        var result = await OrderService.GetOrdersAsync();
        
        if (result.IsSuccess)
        {
            orders = result.Value.ToList();
        }
        
        isLoading = false;
        StateHasChanged();
    }
}
```

### Component Guidelines
- Keep code-behind logic minimal
- Use services for business operations
- Handle loading and error states
- Use proper async patterns
- Implement proper disposal for resources

## Naming Conventions

### General Naming
- **Classes, Methods, Properties**: PascalCase
- **Parameters, Local Variables**: camelCase
- **Constants**: PascalCase
- **Private Fields**: _camelCase with underscore prefix

### Specific Conventions
```csharp
// ✅ Good examples
public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private const int MaxOrderItems = 50;
    
    public async Task<Result<OrderDto>> CreateOrderAsync(CreateOrderRequest request)
    {
        var validationResult = ValidateRequest(request);
        // ...
    }
}
```

### File and Folder Naming
- **Folders**: PascalCase (Services, Models, Repositories)
- **Files**: Match class name exactly
- **Test Files**: `{ClassName}Tests.cs`

## Code Organization

### Folder Structure - Core Project
```
Core/
├── Models/
│   ├── Entities/
│   ├── DTOs/
│   └── Requests/
├── Services/
│   └── Interfaces/
├── Repositories/
│   └── Interfaces/
├── Providers/
│   └── Interfaces/
├── Exceptions/
└── Common/
```

### Folder Structure - Infrastructure Project
```
Infrastructure/
├── Data/
│   ├── Configurations/
│   ├── Migrations/
│   └── ApplicationDbContext.cs
├── Repositories/
├── Providers/
└── Extensions/
```

## Testing Standards

### Unit Test Structure
```csharp
[TestClass]
public class OrderServiceTests
{
    private Mock<IOrderRepository> _mockOrderRepository;
    private Mock<IPaymentProvider> _mockPaymentProvider;
    private OrderService _orderService;

    [TestInitialize]
    public void Setup()
    {
        _mockOrderRepository = new Mock<IOrderRepository>();
        _mockPaymentProvider = new Mock<IPaymentProvider>();
        _orderService = new OrderService(_mockOrderRepository.Object, _mockPaymentProvider.Object);
    }

    [TestMethod]
    public async Task CreateOrderAsync_ValidRequest_ReturnsSuccess()
    {
        // Arrange
        var request = new CreateOrderRequest { /* ... */ };
        _mockOrderRepository.Setup(x => x.AddAsync(It.IsAny<Order>()))
            .ReturnsAsync(new Order());

        // Act
        var result = await _orderService.CreateOrderAsync(request);

        // Assert
        Assert.IsTrue(result.IsSuccess);
        _mockOrderRepository.Verify(x => x.AddAsync(It.IsAny<Order>()), Times.Once);
    }
}
```

### Testing Guidelines
- One test class per service/component
- Use AAA pattern (Arrange, Act, Assert)
- Mock all external dependencies
- Test both success and failure scenarios
- Use descriptive test method names

## Entity Framework Core Standards

### DbContext Configuration
```csharp
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Order> Orders { get; set; }
    public DbSet<OrderItem> OrderItems { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
}
```

### Entity Configuration
```csharp
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.HasKey(o => o.Id);
        
        builder.Property(o => o.OrderDate)
            .IsRequired();
            
        builder.Property(o => o.TotalAmount)
            .HasColumnType("decimal(18,2)");

        builder.HasMany(o => o.OrderItems)
            .WithOne()
            .HasForeignKey(oi => oi.OrderId);
    }
}
```

### Migration Guidelines
- Use descriptive migration names
- Review generated migrations before applying
- Include both Up and Down methods
- Test migrations on development environment first

## General Best Practices

### Error Handling
```csharp
// ✅ Good: Specific exception handling
try
{
    await _orderService.CreateOrderAsync(request);
}
catch (ValidationException ex)
{
    // Handle validation errors
    _logger.LogWarning("Validation failed: {Error}", ex.Message);
}
catch (Exception ex)
{
    // Handle unexpected errors
    _logger.LogError(ex, "Unexpected error creating order");
    throw;
}
```

### Logging
```csharp
public class OrderService : IOrderService
{
    private readonly ILogger<OrderService> _logger;

    public async Task<Result<OrderDto>> CreateOrderAsync(CreateOrderRequest request)
    {
        _logger.LogInformation("Creating order for customer {CustomerId}", request.CustomerId);
        
        try
        {
            // Implementation
            _logger.LogInformation("Order {OrderId} created successfully", order.Id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to create order for customer {CustomerId}", request.CustomerId);
            throw;
        }
    }
}
```

### Dependency Injection Registration
```csharp
// Program.cs or Startup.cs
services.AddScoped<IOrderService, OrderService>();
services.AddScoped<IOrderRepository, OrderRepository>();
services.AddScoped<IPaymentProvider, PaymentProvider>();
```

### Performance Considerations
- Use async/await consistently
- Implement proper cancellation token support
- Use appropriate EF Core query patterns
- Consider pagination for large data sets
- Implement caching where appropriate

### Security Guidelines
- Validate all inputs
- Use parameterized queries (EF Core handles this)
- Implement proper authentication/authorization
- Log security-related events
- Never expose sensitive data in logs

## Code Review Checklist

Before submitting code for review, ensure:
- [ ] Follows naming conventions
- [ ] Has appropriate unit tests
- [ ] Includes proper error handling
- [ ] Uses correct architectural layers
- [ ] Has adequate logging
- [ ] Includes XML documentation for public APIs
- [ ] Follows SOLID principles
- [ ] Has no hard-coded values (use configuration)

## Tools and Extensions

### Recommended Development Tools
- **Static Analysis**: SonarAnalyzer.CSharp
- **Code Formatting**: EditorConfig
- **Testing**: MSTest or xUnit
- **Mocking**: Moq
- **Code Coverage**: coverlet

### EditorConfig Example
```ini
root = true

[*.cs]
indent_style = space
indent_size = 4
end_of_line = crlf
insert_final_newline = true
trim_trailing_whitespace = true

dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = false
```
