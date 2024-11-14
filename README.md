# gudlift-registration - Enhanced

This project is a forked version of the original project that implements a booking system. The purpose of this fork was to resolve critical issues, enhance test coverage, and improve code quality. Additionally, a QA branch has been prepared, ready for review by the original project developers.

## Project Overview

This repository is a fork of the original booking system project. The enhancements made here focus on fixing specific issues identified, improving user experience, and ensuring a higher code quality standard. A dedicated QA branch is ready for developer review to merge the improvements back into the main project.

## Features and Bug Fixes

### Issues Addressed
The following issues were identified and resolved:
- **Club Points Deduction:** Ensuring club points are correctly deducted upon booking.
- **Booking Limits for Competitions:** Preventing bookings for past competitions and enforcing a maximum of 12 places per club per competition.
- **Insufficient Points Check:** Clubs cannot book more places than their available points.
- **Public Points Display:** Implemented a publicly visible points leaderboard for all clubs.

### Improvements
- **Flash Messages:** Improved feedback messages for users during the booking process.
- **Code Structure:** Enhanced readability and modularity to facilitate testing.
- **User Interface:** Added validation to limit booking inputs.

## Testing

A comprehensive suite of tests has been implemented, covering unit, integration, and functional tests:
- **Unit Tests:** Testing individual functionalities.
- **Integration Tests:** Verifying system behavior across multiple components.
- **Functional Tests:** Validating full workflows.

To run the tests with coverage:
```bash
pytest --cov=server tests/
```
