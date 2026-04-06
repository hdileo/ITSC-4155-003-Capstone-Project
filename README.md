# ITSC-4155-003-Capstone-Project
# Smart Task Planner

## Overview
The Smart Task Planner is a web-based productivity application that automatically generates and adjusts a weekly schedule based on task deadlines, priorities, and estimated durations.

Instead of acting like a basic to-do list or calendar, the system makes algorithm-driven decisions — detecting conflicts, rebalancing workloads, and helping users avoid unrealistic plans and missed deadlines.

Designed for students and professionals managing multiple responsibilities.

---

## Features
- Automatic weekly schedule generation
- Priority and deadline-based optimization
- Conflict detection and rescheduling
- Warnings for unrealistic workloads
- Manual edits with re-optimization
- Responsive browser-based interface

---

## How It Works
1. Users create tasks with a deadline, priority, and duration.
2. The system builds an optimized weekly plan.
3. When tasks change, the schedule updates automatically.

---

## Tech Stack

**Backend**
- Python (object-oriented)
- Scheduling & conflict resolution logic
- REST API

**Frontend**
- JavaScript, HTML, CSS
- Interactive responsive UI

**Architecture**
- Backend handles scheduling logic
- Frontend communicates via RESTful APIs

---

## Goals
- Improve prioritization
- Prevent time overload
- Reduce missed deadlines

---

## Future Improvements
- Calendar integration
- Notifications
- Time analytics

Version for Taiga Documentation
Software Design Considerations
During Sprint 2, the project design emphasized several important software quality goals.
Modularity:
The system was organized into separate areas of responsibility, including task management, scheduling, dashboard logic, rendering, validation, and testing. This made it easier for team members to work on different parts of the project while supporting integration later in the sprint.
Sufficiency:
The implementation was designed to fully support the current sprint’s user stories without adding unnecessary complexity. The goal was to build enough structure to satisfy Sprint 2 requirements while still leaving room for future growth.
Robustness:
The project includes validation, scheduling constraints, conflict detection, and multiple testing approaches. These design choices improve the system’s ability to handle realistic and incorrect inputs more safely.
Efficiency:
The scheduling algorithm processes tasks through filtering, sorting, balancing, and time assignment in an organized sequence. This reduces unnecessary work and supports a more structured scheduling process.
Reusability:
Several helper functions and rendering utilities were designed to be reused across the system. This reduces duplication and supports future development.
Extensibility:
The codebase was written so that future features such as security improvements, calendar integration, and more scheduling customization can be added without requiring a full redesign.
Understandability:
Functions were named clearly, logic was divided by responsibility, and the system was organized into understandable sections. This helped both implementation and team collaboration.
Reliability:
Reliability was supported through unit tests, integration tests, black box testing, and static analysis. Together, these help verify that completed functionality behaves as expected.
The project also connects well to future object-oriented design principles. In particular, the system aims for high cohesionby grouping related logic together, and low coupling by reducing unnecessary dependencies between components. These principles will become even more important in future sprints as the application continues to grow.


Architecture Overview
The Smart Task Planner uses both a client-server architecture and a three-layer design.
Client-Server Model:
The frontend acts as the client and the backend acts as the server. The client is responsible for collecting user input and displaying results, while the server processes requests, applies scheduling rules, performs validation, and returns data to the interface. These two sides communicate through API calls.
Three-Layer Design:
The system is organized into three main layers:
1. Presentation Layer
This includes the user interface built with HTML, CSS, and JavaScript. It manages forms, dashboards, schedule views, charts, and visual feedback for the user.
2. Application Layer
This includes the backend logic that handles scheduling, conflict detection, validation, sorting, dashboard calculations, and other decision-making processes in the system.
3. Data Layer
This layer manages task storage and retrieval. It supports the saving, updating, deleting, and loading of task information for the rest of the system.
This architecture improves separation of concerns by dividing the system into clear responsibilities. It also supports maintainability and future growth by making it easier to modify one part of the system without heavily affecting the others.

Design Principles and Patterns
The Smart Task Planner was developed with several important software design principles in mind, both in its current implementation and in areas planned for future improvement. These principles help improve maintainability, scalability, clarity, and long-term code quality.
Single Responsibility Principle
A major principle reflected in the project is the Single Responsibility Principle. Different parts of the system were organized around clear responsibilities, such as task rendering, scheduling logic, dashboard analytics, validation, and testing. This makes the code easier to understand, debug, and modify because each function or component is focused on a specific purpose rather than trying to do everything at once.
Open/Closed Principle
The project also moves toward the Open/Closed Principle, where the system is open for extension but closed for unnecessary modification. For example, scheduling behavior can be expanded with new rules such as calendar integrations, security constraints, or more advanced scheduling logic without requiring the full application to be rewritten. The modular structure of the scheduling functions and helper methods supports this principle.
Liskov Substitution Principle
Although the project is not yet heavily class-based, the design direction supports future application of the Liskov Substitution Principle. As the system grows, abstractions for schedulers, validators, or integrations could be introduced so that alternate implementations can replace base ones without breaking functionality. This would be especially useful for future calendar integrations or alternative scheduling strategies.
Interface Segregation Principle
The system also benefits from ideas related to Interface Segregation, even if formal interfaces are not yet heavily used. Different features are separated so that components only deal with the responsibilities they actually need. For example, the dashboard logic, scheduling logic, and task editing functionality do not all depend on the same large block of behavior. This keeps the system more focused and reduces unnecessary dependencies.
Dependency Inversion Principle
At a higher level, future improvements will continue moving toward the Dependency Inversion Principle. Currently, the project has some direct dependencies between UI logic, backend routes, and scheduling behavior, but the structure is already moving toward more modular helper functions and clearer layers. In the future, the system could benefit from stronger abstractions between scheduling engines, storage mechanisms, and integration services.
Cohesion and Coupling
The design also reflects the goal of high cohesion and low coupling. Related logic is grouped together, such as scheduling functions, rendering functions, and task management workflows, which improves cohesion. At the same time, the team has worked to reduce unnecessary dependencies between unrelated parts of the codebase, helping lower coupling. This is especially important as the project grows and more features are added.
Reusability
Several parts of the project were designed with reusability in mind. Helper functions for rendering, validation, scheduling, conflict detection, sorting, and formatting can be reused across multiple features. This reduces duplication and makes the codebase easier to extend in future sprints.
Extensibility
Extensibility has been an important design goal. The system is already positioned to support future enhancements such as additional scheduling rules, stronger security controls, more calendar customization, and external integrations like Google Calendar. By building around modular logic and layered organization, the project is easier to expand without requiring major redesign.
Robustness and Reliability
The project design also emphasizes robustness and reliability. Validation rules, conflict detection, automated testing, and multiple testing strategies all support more dependable system behavior. These design decisions help ensure the system behaves predictably even when users update tasks, change priorities, or create more complex scheduling scenarios.

Design Patterns Implemented or Planned
Singleton (Planned / Partial)
The Singleton pattern is not a major formal feature of the project yet, but it could be useful in future versions for managing shared configuration, schedule settings, or service-level resources. If introduced carefully, it could help centralize common system state. However, it would need to be applied selectively to avoid overusing global state.
Strategy Pattern (Strong Candidate)
The Strategy pattern is one of the strongest future design directions for this project. The scheduling system could eventually support multiple scheduling strategies, such as deadline-first, effort-balanced, calendar-aware, or user-customized scheduling. Each scheduling approach could be implemented as a separate strategy while keeping the rest of the system stable.
Factory Pattern (Future Opportunity)
A Factory pattern could be useful in the future when creating task processors, validation components, or different integration services. This would allow the system to generate the appropriate object or behavior depending on the context without hardcoding all creation logic in one place.
Observer Pattern (Future Opportunity)
The project already includes behavior that resembles the need for an Observer-style design, particularly when task updates automatically affect the dashboard, schedule, and insights. In future versions, this could be made more formal so that different parts of the system respond automatically to changes in shared data.
MVC Influence
While not a strict MVC implementation, the project shows MVC-style separation. The frontend acts as the presentation layer, the backend routes and logic serve as the controller-like behavior, and the stored task data functions as the model layer. This separation improves clarity and aligns the project with common architectural best practices.


Testing Strategy
During Sprint 2, the team applied multiple testing approaches to ensure system quality, correctness, and stability. This included unit testing, integration testing, black box testing, white box testing, and static testing.
Unit Testing
Unit tests were written to validate individual functions and features in isolation. These tests covered key functionality such as task CRUD operations, validation, scheduling logic, and conflict detection. The purpose was to confirm that each individual component behaved correctly before integration.
Integration Testing
Integration tests were used to verify that multiple components of the application worked together correctly. This included workflows such as creating a task, retrieving it, editing it, deleting it, and generating schedules that reflect those updates. These tests helped confirm that backend routes, storage logic, and scheduling behavior remained consistent across the system.
Black Box Testing
Black box testing was used to evaluate the system based on user-facing inputs and outputs. The team applied equivalence partitioning to divide inputs into valid and invalid categories, such as acceptable and unacceptable due dates, valid and invalid priorities, and valid and invalid durations. This allowed broad scenario coverage without needing to test every possible input value.
White Box Testing
White box testing was applied by designing tests with awareness of the internal code structure. This included targeting specific branches, scheduling decisions, validation conditions, and conflict detection rules. By understanding how the code works internally, the team was able to test important decision paths more intentionally.
Static Testing
Static testing was performed through code review, inspection, design review, and comparison of implementation against requirements and acceptance criteria. This helped identify issues related to readability, duplication, coupling, and logic quality before runtime. Static testing also supported documentation quality and maintainability.
Testing Outcome
Using multiple testing approaches improved confidence in both the correctness of individual features and the reliability of the overall system. This helped ensure that the completed user stories were not only implemented, but also verified from multiple quality perspectives.

