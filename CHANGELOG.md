# Changelog

All notable changes to UpShiftRx AI will be documented in this file.

## [2.0.0] - 2024-01-15

### 🚀 Major Release - Real PubMed Integration

#### Added
- **Real-time PubMed integration** - Live literature searches
- **XML parsing** for paper metadata (titles, journals, years)
- **Enhanced API responses** with paper counts and search metadata
- **Comprehensive API documentation** (API.md)
- **Postman collection** for easy testing
- **OpenAPI/Swagger specification** for interactive docs
- **Security enhancements** with input validation and sanitization
- **Error handling** with proper HTTP status codes
- **CORS support** for cross-origin requests

#### Changed
- **Analyze endpoint** now returns real PubMed data instead of mock data
- **Response format** enhanced with additional metadata fields
- **Input validation** strengthened with character filtering
- **Error messages** improved for better debugging

#### Security
- Updated `requests` library to fix vulnerability (CVE-2024-35195)
- Added input sanitization to prevent injection attacks
- Implemented proper error handling to prevent information leakage
- Added SECURITY.md with security policy

#### Technical
- Serverless architecture on Netlify Functions
- 15-second timeout handling for API requests
- Rate limiting considerations documented
- Production-ready error handling

---

## [1.0.0] - 2024-01-14

### 🎉 Initial Release

#### Added
- Basic API structure with health, drugs, diseases endpoints
- Mock data responses for testing
- Netlify Functions deployment
- Basic CORS support
- Simple input validation

#### Features
- Health check endpoint
- Drug and disease list endpoints
- Basic analyze endpoint with mock data
- Netlify serverless deployment