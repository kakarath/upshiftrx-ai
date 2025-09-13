# Changelog

All notable changes to the UpShiftRx platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Coming Soon
- Web-based platform launch
- API access for researchers
- Interactive drug-disease network visualization
- Advanced filtering and search capabilities

## [0.2.0] - 2025-01-13

### Added
- Enhanced error handling for API failures and file operations
- Path validation to prevent security vulnerabilities
- Performance optimizations for graph generation
- Configuration system for flexible data management
- Command-line arguments for batch processing
- Rate limiting improvements (2-second delays between requests)

### Changed
- Moved large datasets to private repository for IP protection
- Updated drug and disease lists to external JSON configuration files
- Improved duplicate node handling in network visualization
- Enhanced progress tracking and error reporting

### Fixed
- Path traversal vulnerabilities (CWE-22)
- F-string syntax errors in JavaScript code generation
- IndexError when processing empty PubMed fields
- Missing directory creation for results output

### Security
- Added comprehensive input validation
- Implemented secure file path handling
- Enhanced error logging without exposing sensitive data

## [0.1.0] - 2025-01-10

### Added
- Initial PubMed literature mining pipeline
- Drug-disease relationship extraction
- Interactive network visualization with PyVis
- Batch processing for multiple drug-disease combinations
- CSV export functionality for results
- Basic configuration management

### Features
- Support for 50+ drugs and 60+ diseases
- Automated PubMed API integration
- Network graph generation with interactive controls
- Slider-based filtering for paper count thresholds
- Progress tracking for large batch operations

### Technical
- Python-based architecture with BioPython integration
- NetworkX for graph analysis
- Pandas for data manipulation
- Configurable rate limiting for API compliance

## [0.0.1] - 2025-01-05

### Added
- Project initialization
- Basic PubMed API integration
- Simple drug-disease query functionality
- Initial documentation structure

---

## Release Notes

### Version 0.2.0 Highlights
This release focuses on security, performance, and maintainability improvements. We've addressed critical vulnerabilities and enhanced the system's robustness for production use.

### Upcoming Features (v0.3.0)
- Machine learning ranking of drug-disease associations
- Integration with additional biomedical databases
- RESTful API for programmatic access
- Enhanced visualization with 3D network graphs

## Support

For questions about releases or features:
- **Contact**: upshiftrx.ai/contact
- **Issues**: [GitHub Issues](https://github.com/upshiftrx/upshiftrx-ai/issues)