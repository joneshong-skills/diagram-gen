# Diagram Patterns Catalog

Ready-to-use templates for common diagram types. Copy, modify, and render.

## Pattern Selection Guide

| Content Structure | Pattern | Mermaid Type |
|------------------|---------|--------------|
| Steps in order | Pipeline | `flowchart LR` |
| Steps with branches | Decision Tree | `flowchart TB` |
| Grouped components | Architecture | `flowchart TB` + subgraphs |
| Interactions over time | API/Message Flow | `sequenceDiagram` |
| States and transitions | State Machine | `stateDiagram-v2` |
| Object relationships | Class/Domain Model | `classDiagram` |
| Database tables | Data Model | `erDiagram` |
| Hierarchy/brainstorm | Mind Map | `mindmap` |
| Timeline/schedule | Project Plan | `gantt` |
| Cyclic process | Feedback Loop | `flowchart TB` + back-edge |
| Before/after | Comparison | `flowchart TB` + parallel subgraphs |
| Central hub | Hub and Spoke | `flowchart TB` + radial layout |

## 1. Pipeline / Workflow

Linear process from input to output.

```mermaid
flowchart LR
    A[Input] --> B[Step 1]
    B --> C[Step 2]
    C --> D[Step 3]
    D --> E[Output]

    style A fill:#d3f9d8,stroke:#2f9e44
    style E fill:#c5f6fa,stroke:#0c8599
```

**Variations:**
- Add `-.->` for optional paths
- Add `==>` for critical path
- Use subgraphs to group phases

## 2. Decision Tree

Branching logic with conditions.

```mermaid
flowchart TB
    Start[Start] --> Q1{Condition A?}
    Q1 -->|Yes| Q2{Condition B?}
    Q1 -->|No| PathC[Action C]
    Q2 -->|Yes| PathA[Action A]
    Q2 -->|No| PathB[Action B]
    PathA --> End[Done]
    PathB --> End
    PathC --> End

    style Start fill:#d3f9d8,stroke:#2f9e44
    style Q1 fill:#fff2cc,stroke:#d6b656
    style Q2 fill:#fff2cc,stroke:#d6b656
    style End fill:#c5f6fa,stroke:#0c8599
```

## 3. Architecture (Grouped Components)

System components organized by layer or domain.

```mermaid
flowchart TB
    subgraph client["Client Layer"]
        direction LR
        Web[Web App]
        Mobile[Mobile App]
    end

    subgraph api["API Layer"]
        Gateway[API Gateway]
        Auth[Auth Service]
    end

    subgraph data["Data Layer"]
        direction LR
        DB[(PostgreSQL)]
        Cache[(Redis)]
    end

    Web --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> DB
    Gateway --> Cache

    style Gateway fill:#dae8fc,stroke:#6c8ebf
    style Auth fill:#e5dbff,stroke:#5f3dc4
    style DB fill:#fff4e6,stroke:#e67700
    style Cache fill:#fff4e6,stroke:#e67700
```

## 4. Sequence Diagram (API Flow)

Interactions between actors over time.

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant S as Service
    participant D as Database

    C->>G: POST /api/resource
    activate G
    G->>S: Validate & forward
    activate S
    S->>D: INSERT
    D-->>S: OK
    S-->>G: 201 Created
    deactivate S
    G-->>C: 201 + resource
    deactivate G
```

**Tips:**
- Use `activate`/`deactivate` for processing blocks
- `alt`/`else`/`end` for conditional flows
- `loop`/`end` for repeated operations
- `Note over A,B: text` for annotations

## 5. State Machine

States with labeled transitions.

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review: submit()
    Review --> Approved: approve()
    Review --> Draft: reject()
    Approved --> Published: publish()
    Published --> Archived: archive()
    Archived --> [*]

    state Review {
        [*] --> Pending
        Pending --> InReview: assign()
        InReview --> [*]
    }
```

## 6. Class / Domain Model

Objects with attributes and relationships.

```mermaid
classDiagram
    class User {
        +int id
        +String name
        +String email
        +login() bool
        +logout() void
    }
    class Order {
        +int id
        +Date createdAt
        +float total
        +cancel() bool
    }
    class Product {
        +int id
        +String name
        +float price
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Product : contains
```

**Relationship types:**
- `-->` association
- `--o` aggregation
- `--*` composition
- `..|>` realization
- `--|>` inheritance

## 7. ER Diagram (Data Model)

Database schema with relationships.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "included in"

    USER {
        int id PK
        varchar name
        varchar email UK
        timestamp created_at
    }
    ORDER {
        int id PK
        int user_id FK
        decimal total
        varchar status
    }
    PRODUCT {
        int id PK
        varchar name
        decimal price
    }
    LINE_ITEM {
        int order_id FK
        int product_id FK
        int quantity
    }
```

## 8. Mind Map

Hierarchical brainstorm or concept breakdown.

```mermaid
mindmap
    root((Project))
        Frontend
            React
            Tailwind CSS
            TypeScript
        Backend
            Node.js
            PostgreSQL
            Redis
        DevOps
            Docker
            CI/CD
            Monitoring
```

## 9. Gantt Chart (Timeline)

Project schedule with dependencies.

```mermaid
gantt
    title Development Plan
    dateFormat YYYY-MM-DD

    section Design
        Requirements   :a1, 2024-01-01, 7d
        UI Mockups     :a2, after a1, 5d

    section Development
        Backend API    :b1, after a2, 14d
        Frontend UI    :b2, after a2, 14d
        Integration    :b3, after b1, 7d

    section Testing
        QA Testing     :c1, after b3, 7d
        Bug Fixes      :c2, after c1, 5d
```

## 10. Feedback Loop

Cyclic process with iteration.

```mermaid
flowchart TB
    Plan[Plan] --> Build[Build]
    Build --> Test[Test]
    Test --> Deploy[Deploy]
    Deploy --> Monitor[Monitor]
    Monitor -.->|Feedback| Plan

    style Plan fill:#e5dbff,stroke:#5f3dc4
    style Build fill:#dae8fc,stroke:#6c8ebf
    style Test fill:#fff2cc,stroke:#d6b656
    style Deploy fill:#d3f9d8,stroke:#2f9e44
    style Monitor fill:#c5f6fa,stroke:#0c8599
```

## 11. Comparison (Side by Side)

Contrasting two approaches.

```mermaid
flowchart TB
    Title["Monolith vs Microservices"]

    subgraph mono["Monolith"]
        M1[Single Deploy]
        M2[Shared DB]
        M3[Simple Ops]
    end

    subgraph micro["Microservices"]
        S1[Independent Deploy]
        S2[Own Databases]
        S3[Complex Ops]
    end

    Title --> mono
    Title --> micro

    style Title fill:#e7f5ff,stroke:#1971c2
    style M1 fill:#f8f9fa,stroke:#868e96
    style M2 fill:#f8f9fa,stroke:#868e96
    style M3 fill:#f8f9fa,stroke:#868e96
    style S1 fill:#d3f9d8,stroke:#2f9e44
    style S2 fill:#d3f9d8,stroke:#2f9e44
    style S3 fill:#ffe3e3,stroke:#c92a2a
```

## 12. Hub and Spoke

Central component with surrounding elements.

```mermaid
flowchart TB
    Hub[API Gateway]
    A[Auth Service] --> Hub
    B[User Service] --> Hub
    C[Order Service] --> Hub
    D[Payment Service] --> Hub
    Hub --> E[Client]

    style Hub fill:#dae8fc,stroke:#6c8ebf,stroke-width:3px
    style E fill:#c5f6fa,stroke:#0c8599
```

## Rendering Tips

- **Under 10 nodes**: Single diagram, any layout
- **10-30 nodes**: Use subgraphs to organize
- **30+ nodes**: Split into multiple diagrams
- **Dark mode**: Use `--theme tokyo-night --transparent` for versatile SVGs
- **Print**: Use `--theme zinc-light` or `--theme github-light`
- **Presentations**: Use `--theme dracula` for high contrast on projectors
