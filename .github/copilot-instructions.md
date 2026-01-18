```markdown
# GitHub Copilot Instructions for dotnet

## Enforceable Rules and Constraints

1. **Input Validation**
   - All API endpoints must validate input using data annotations or FluentValidation.

2. **Async Database Operations**
   - All database operations must use async methods.
   - Never use `.Result` or `.Wait()` on async methods.

3. **XML Documentation**
   - All public methods must have XML documentation comments.

4. **Service Instantiation**
   - Avoid creating service instances directly in classes. Use dependency injection instead.

5. **Configuration Management**
   - Connection strings must be stored in `appsettings.json`.
   - Never hardcode connection strings. Use configuration files or environment variables.
   - Use strongly-typed configuration classes.

6. **Controller Responsibilities**
   - Controllers must not contain business logic. Move business logic to service classes.
   - Keep controllers thin; they should only handle HTTP concerns.

7. **Error Handling**
   - Error messages must not expose sensitive information.
   - Implement proper error handling and logging using `ILogger`.

8. **Method Design**
   - Keep methods small and focused. Extract complex logic into separate methods or classes.
   - Use cancellation tokens in async methods.

9. **Data Access Patterns**
   - Use the repository pattern for data access.
   - Use a service layer for data processing and business rules.
   - Use Entity Framework LINQ instead of raw SQL when possible. Never use string concatenation in SQL queries.

10. **Dependency Injection**
    - Register services in the DI container and inject them via constructor.
    - Use dependency injection instead of the `new` keyword for services.

11. **Code Quality**
    - Follow SOLID principles in all code.
    - Replace magic numbers with named constants or configuration values.
    - Validate all input parameters.

## Best Practices

- Use async/await for all I/O operations.
- Never expose sensitive data in error messages.
- Ensure all services are registered in the DI container.
```
