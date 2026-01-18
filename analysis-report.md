# RepoSentinel Analysis Report

## Detected Stack

- **Language**: dotnet
- **Confidence**: 95.00%

## Risk Scores

| Category | Risk Score |
|----------|------------|
| Architecture | 0.00/10 🔴 Critical |
| Code Quality | 0.00/10 🔴 Critical |
| Security | 0.00/10 🔴 Critical |

## Findings Summary

Total findings: 10

### Architecture

- **Business logic in controllers** (MEDIUM)
  - Occurrences: 6
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Printer.Service/Controllers/ReportController.cs, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Printer.Service/Controllers/PrintController.cs, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Api/Controllers/SalesController.cs
  - Suggested constraints: 3

- **Direct instantiation instead of dependency injection** (MEDIUM)
  - Occurrences: 37
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener.Token/Program.cs:29, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener.SalesSendNotification/Program.cs:26, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener.SalesSendNotification/Program.cs:37
  - Suggested constraints: 3

- **Business logic in controllers** (MEDIUM)
  - Occurrences: 7
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Api/Controllers/ManagerController.cs:17, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Api/Controllers/BatchController.cs:23, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Api/Controllers/SalesController.cs:22
  - Suggested constraints: 1

- **Direct instantiation of services** (MEDIUM)
  - Occurrences: 1
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Auth.Application/Services/AdminStoreUserService.cs:41
  - Suggested constraints: 1

### Code Quality

- **Large methods** (LOW)
  - Occurrences: 126
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener.Token/Program.cs:18, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Elastic/ElasticsearchService.cs:8, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Simulator.Sales/Program.cs:4
  - Suggested constraints: 1

- **Missing async/await** (MEDIUM)
  - Occurrences: 32
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener.Token/Program.cs:34, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Simulator.Sales/Program.cs:23, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener.SalesSendNotification/Program.cs:32
  - Suggested constraints: 1

- **Magic numbers** (LOW)
  - Occurrences: 1492
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Notify.Api/Program.cs:25, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Notify.Api/Program.cs:29, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Auth.Api/Program.cs:26
  - Suggested constraints: 1

### Security

- **SQL injection vulnerability** (CRITICAL)
  - Occurrences: 1
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Api/Controllers/Admin/BomController.cs:151
  - Suggested constraints: 1

- **Hardcoded connection strings** (HIGH)
  - Occurrences: 36
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Simulator.Sales/Program.cs:59, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener/DatabaseListener.cs:66, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Listener/DatabaseListener.cs:80
  - Suggested constraints: 1

- **Missing input validation** (MEDIUM)
  - Occurrences: 65
  - Evidence: /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Printer.Service/Controllers/ReportController.cs:18, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Printer.Service/Controllers/HomeController.cs:17, /Users/vivek/Desktop/Projects/Repositories/Devyani/MPNC-BackEnd/Mpnc.Printer.Service/Controllers/HomeController.cs:22
  - Suggested constraints: 1

## Recommendations

The following categories require immediate attention:

- Architecture (risk score: 0.00/10)
- Security (risk score: 0.00/10)
- Code Quality (risk score: 0.00/10)
