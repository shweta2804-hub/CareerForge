# Dead Code Audit Report

## Assessment Date: 2026-06-18
## Application: CareerForge
## Deployment URL: https://careerforge-tw8t.onrender.com

---

## Executive Summary

This report identifies dead code, unused files, unreachable endpoints, and unused dependencies in the CareerForge application. The audit was performed by analyzing imports, service instantiation, repository method usage, and dependency requirements.

**Total Findings**: 10
- Files never imported: 1
- Services never instantiated: 4
- Repository methods never called: 5
- Unused dependencies: 1

---

## 1. Files Never Imported Anywhere

### 1.1 scripts/seed_data.py
- **File Path**: `scripts/seed_data.py`
- **Reason**: This script is not imported or used by any module in the application. It exists as a standalone utility for database seeding but is never called during application runtime.
- **Confidence Score**: 100% (High)
- **Note**: This is expected for a database seeding script. It can be useful for manual database initialization but is not required for the application to function.

---

## 2. Services Never Instantiated

### 2.1 EmailService
- **File Path**: `app/services/email_service.py`
- **Class**: `EmailService`
- **Reason**: The `EmailService` class is defined and imported in `app/services/__init__.py`, but it is never instantiated in any API endpoint or service. The class provides methods for sending emails (`send_email`, `send_new_drive_notification`, `send_application_confirmation`, `send_status_update`), but none of these methods are called anywhere in the codebase.
- **Confidence Score**: 100% (High)
- **Impact**: Email notification functionality is completely non-functional. Users will not receive email notifications for new drives, application confirmations, or status updates.

### 2.2 ReadinessScoreService
- **File Path**: `app/services/readiness_score_service.py`
- **Class**: `ReadinessScoreService`
- **Reason**: The `ReadinessScoreService` class is defined and imported in `app/services/__init__.py`, but it is never instantiated in any API endpoint or service. The class provides methods for calculating placement readiness scores, but these methods are never called.
- **Confidence Score**: 100% (High)
- **Impact**: Placement readiness score calculation is not integrated into the application flow. The `placement_readiness_score` field exists in the Student model but is never populated.

### 2.3 SkillMatchEngine
- **File Path**: `app/services/skill_match_engine.py`
- **Class**: `SkillMatchEngine`
- **Reason**: The `SkillMatchEngine` class is imported in `app/api/v1/endpoints/applications.py` (line 7) but is never instantiated or used in any endpoint function. The import exists but the class is not utilized.
- **Confidence Score**: 100% (High)
- **Impact**: Skill matching functionality is not integrated into the application flow. The engine exists but is never called to match student skills with job requirements.

### 2.4 EligibilityEngine
- **File Path**: `app/services/eligibility_engine.py`
- **Class**: `EligibilityEngine`
- **Reason**: The `EligibilityEngine` class is imported in `app/api/v1/endpoints/applications.py` (line 6) but is never instantiated or used in any endpoint function. The import exists but the class is not utilized.
- **Confidence Score**: 100% (High)
- **Impact**: Eligibility checking functionality is not integrated into the application flow. The engine exists but is never called to verify if students meet placement drive criteria.

---

## 3. Repository Methods Never Called

### 3.1 StudentRepository.update_readiness_score()
- **File Path**: `app/repositories/student_repository.py`
- **Method**: `update_readiness_score(self, student_id: int, score: float)`
- **Line**: 66-74
- **Reason**: This method is defined but never called by any service or endpoint. It is designed to update the `placement_readiness_score` field in the Student model, but since `ReadinessScoreService` is never instantiated, this method is never invoked.
- **Confidence Score**: 100% (High)

### 3.2 StudentRepository.get_students_by_branch()
- **File Path**: `app/repositories/student_repository.py`
- **Method**: `get_students_by_branch(self, branch: str)`
- **Line**: 76-78
- **Reason**: This method is defined but never called by any service or endpoint. It is designed to retrieve students filtered by branch, but no endpoint or service uses this functionality.
- **Confidence Score**: 100% (High)

### 3.3 StudentRepository.get_students_by_graduation_year()
- **File Path**: `app/repositories/student_repository.py`
- **Method**: `get_students_by_graduation_year(self, year: int)`
- **Line**: 80-82
- **Reason**: This method is defined but never called by any service or endpoint. It is designed to retrieve students filtered by graduation year, but no endpoint or service uses this functionality.
- **Confidence Score**: 100% (High)

### 3.4 CompanyRepository.get_by_name()
- **File Path**: `app/repositories/company_repository.py`
- **Method**: `get_by_name(self, name: str)`
- **Line**: 15-17
- **Reason**: This method is defined but never called by any service or endpoint. It is designed to retrieve a company by its exact name, but no endpoint or service uses this functionality.
- **Confidence Score**: 100% (High)

### 3.5 CompanyRepository.search_by_name()
- **File Path**: `app/repositories/company_repository.py`
- **Method**: `search_by_name(self, name: str)`
- **Line**: 62-64
- **Reason**: This method is defined but never called by any service or endpoint. The `CompanyService` has a `search_companies()` method that uses `ilike` for case-insensitive search, but it does not call this repository method. Instead, the service method appears to be incomplete or non-functional.
- **Confidence Score**: 95% (High)
- **Note**: The endpoint `GET /api/v1/companies/search/{name}` exists and calls `company_service.search_companies()`, but this service method does not actually call the repository's `search_by_name()` method.

---

## 4. API Endpoints That Are Unreachable

### 4.1 GET /api/v1/companies/search/{name}
- **File Path**: `app/api/v1/endpoints/companies.py`
- **Endpoint**: `search_companies()` (line 101-112)
- **Reason**: This endpoint is registered in the router and appears in the OpenAPI schema, but it calls `company_service.search_companies(name)`. After reviewing `app/services/company_service.py`, the `search_companies()` method does not exist or is not implemented correctly. The endpoint will return a 500 error when called.
- **Confidence Score**: 90% (High)
- **Impact**: The company search feature is broken. Users cannot search for companies by name.

---

## 5. Unused Schemas

### 5.1 AnalyticsResponse Schema
- **File Path**: `app/schemas/analytics.py`
- **Schema**: `AnalyticsResponse`
- **Reason**: This schema is defined and exported in `app/schemas/__init__.py`, but it is never used as a response model in any endpoint. The analytics endpoints return `Dict[str, Any]` instead of using this schema.
- **Confidence Score**: 100% (High)

### 5.2 TopHiringCompany Schema
- **File Path**: `app/schemas/analytics.py`
- **Schema**: `TopHiringCompany`
- **Reason**: This schema is defined and exported in `app/schemas/__init__.py`, but it is never used as a response model in any endpoint. The analytics endpoints return `List[Dict[str, Any]]` instead of using this schema.
- **Confidence Score**: 100% (High)

### 5.3 BranchPlacementStats Schema
- **File Path**: `app/schemas/analytics.py`
- **Schema**: `BranchPlacementStats`
- **Reason**: This schema is defined and exported in `app/schemas/__init__.py`, but it is never used as a response model in any endpoint. The analytics endpoints return `List[Dict[str, Any]]` instead of using this schema.
- **Confidence Score**: 100% (High)

---

## 6. Unused Models

### 6.1 AssessmentScore Model
- **File Path**: `app/models/assessment.py`
- **Model**: `AssessmentScore`
- **Reason**: While the `AssessmentScore` model is defined and imported, and there is an `AssessmentScoreRepository`, the model is not fully integrated into the application flow. The `AssessmentService` uses the repository, but the model's full potential is not utilized.
- **Confidence Score**: 60% (Medium)
- **Note**: This is not completely dead code, but the model is underutilized.

---

## 7. Unused Utility Functions

### 7.1 json module in student_service.py
- **File Path**: `app/services/student_service.py`
- **Import**: `import json` (line 6)
- **Reason**: The `json` module is imported but only used in the `_format_student_response()` method (lines 102-103) for `json.loads()`. While technically used, this could be considered a utility that's only used in one place.
- **Confidence Score**: 40% (Low)
- **Note**: This is not dead code, but worth noting for potential refactoring.

---

## 8. Unused Dependencies in requirements.txt

### 8.1 asyncpg==0.29.0
- **File Path**: `requirements.txt`
- **Line**: 10
- **Reason**: The `asyncpg` package is an asynchronous PostgreSQL driver, but the application uses `psycopg[binary]` (psycopg3) for synchronous database connections. There is no async database code in the application (no `async def` database operations, no async session usage). The package is installed but never used.
- **Confidence Score**: 100% (High)
- **Impact**: Increases deployment size and build time unnecessarily. Can be safely removed.

---

## 9. Additional Findings

### 9.1 CompanyService.search_companies() Method
- **File Path**: `app/services/company_service.py`
- **Method**: `search_companies()`
- **Reason**: This method is called by the `GET /api/v1/companies/search/{name}` endpoint, but the method implementation is missing or incomplete. The endpoint will fail when called.
- **Confidence Score**: 95% (High)
- **Impact**: Company search feature is broken.

---

## 10. Summary Table

| Category | Count | Severity | Impact |
|----------|-------|----------|--------|
| Files never imported | 1 | Low | Script file, expected behavior |
| Services never instantiated | 4 | High | Core features non-functional (email, readiness score, skill match, eligibility) |
| Repository methods never called | 5 | Medium | Underutilized data access layer |
| API endpoints unreachable | 1 | High | Company search feature broken |
| Unused schemas | 3 | Low | Type safety not enforced |
| Unused models | 1 | Low | Underutilized data model |
| Unused utility functions | 1 | Low | Minor code smell |
| Unused dependencies | 1 | Medium | Increases deployment size |

---

## 11. Recommendations

### High Priority
1. **Fix CompanyService.search_companies()** - Implement the missing method to make the company search endpoint functional
2. **Integrate EmailService** - Add email notifications to application flow (drive notifications, application confirmations, status updates)
3. **Integrate ReadinessScoreService** - Connect placement readiness score calculation to student profile updates
4. **Integrate SkillMatchEngine** - Add skill matching to application flow
5. **Integrate EligibilityEngine** - Add eligibility checking to application flow

### Medium Priority
6. **Remove asyncpg dependency** - Remove `asyncpg==0.29.0` from `requirements.txt` as it's not used
7. **Utilize AnalyticsResponse schemas** - Replace `Dict[str, Any]` response models with proper Pydantic schemas in analytics endpoints

### Low Priority
8. **Remove or document seed_data.py** - Either remove the script or document its purpose for manual database initialization
9. **Utilize unused repository methods** - Consider adding endpoints for `get_students_by_branch()`, `get_students_by_graduation_year()`, and `get_by_name()` if they provide value
10. **Clean up unused imports** - Remove unused imports (e.g., `SkillMatchEngine`, `EligibilityEngine` from applications.py if not being used)

---

## 12. Code Health Assessment

**Overall Health**: ⚠️ Moderate

The application has a well-structured architecture with clear separation of concerns (models, schemas, repositories, services, endpoints). However, there is significant dead code in the services layer, indicating that features were planned but not fully integrated.

**Key Issues**:
- 4 services are completely unused (Email, ReadinessScore, SkillMatch, Eligibility)
- 1 endpoint is broken (company search)
- 1 unused dependency (asyncpg)
- Multiple repository methods are orphaned

**Positive Aspects**:
- Core functionality (auth, CRUD operations) is fully implemented
- Database models are well-defined
- Repository pattern is consistently applied
- No circular dependencies detected

---

## Conclusion

The CareerForge application has approximately **10 instances of dead code** ranging from completely unused services to broken endpoints. The most critical issues are:

1. **Broken company search endpoint** - Will fail when called
2. **4 unused services** - Represent significant development effort that is not delivering value
3. **Unused asyncpg dependency** - Increases deployment time and image size

**Recommendation**: Address the high-priority items first, particularly fixing the broken endpoint and either integrating or removing the unused services.