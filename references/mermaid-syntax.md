# Mermaid Syntax Reference

Complete syntax reference for Mermaid diagrams. Load this when encountering
syntax errors or needing detailed node/arrow/styling information.

## Critical Error Prevention

### 1. List Syntax Conflict (Most Common)

Mermaid parser treats `number. space` as Markdown ordered list → parse error.

```
WRONG: [1. Perception]
RIGHT: [1.Perception]          Remove space after period
RIGHT: [(1) Perception]        Parenthesized number
RIGHT: [Step 1: Perception]    Prefix word
RIGHT: [Perception]            Drop numbering
```

Circled numbers for safe numbering: ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮

### 2. Subgraph Naming

Spaces in subgraph names require ID + display name format.

```
WRONG: subgraph Core Process
RIGHT: subgraph core["Core Process"]
RIGHT: subgraph core_process
```

Referencing subgraphs:
```
WRONG: Title --> Core Process
RIGHT: Title --> core
```

### 3. Node References

Always reference by ID, never by display text.

```mermaid
A["Display Text A"]
B["Display Text B"]
A --> B              ✅ Use IDs
```

### 4. Special Characters

```
Spaces:       ["Text with spaces"]
Quotes:       use 『』 instead of "
Parentheses:  use 「」 instead of ()
Line breaks:  <br/> only in circle nodes ((Text<br/>Line 2))
```

Keep node text under 50 characters. Use annotation nodes for longer content.

## Node Types

```mermaid
A[Rectangle]              Default
B(Rounded)                Rounded corners
C([Stadium])              Pill shape
D((Circle))               Circle
E>Right Arrow]            Flag
F{Diamond}                Decision
G{{Hexagon}}              Hexagon
H[/Parallelogram/]        Input/output
I[(Database)]             Cylinder
J[/Trapezoid\]            Trapezoid
```

## Arrow Types

### Basic
```
A --> B          Solid arrow
A -.-> B         Dashed arrow
A ==> B          Thick arrow
A ~~~ B          Invisible link (layout only)
```

### With Labels
```
A -->|Label| B
A -.->|Optional| B
A ==>|Critical| B
```

### Multi-target
```
A --> B & C & D          One to many
A & B & C --> D          Many to one
A --> B --> C --> D       Chaining
```

### Bidirectional
```
A <--> B                 Solid bidirectional
A <-.-> B                Dashed bidirectional
```

## Subgraph Syntax

### Basic
```mermaid
graph TB
    subgraph id["Display Name"]
        direction TB
        A --> B
    end
```

### Nested (max 2 levels)
```mermaid
graph TB
    subgraph outer["Outer"]
        subgraph inner["Inner"]
            A --> B
        end
    end
```

### Connecting Subgraphs
```mermaid
graph TB
    subgraph g1["Group 1"]
        A[Node A]
    end
    subgraph g2["Group 2"]
        B[Node B]
    end
    A --> B           Connect via nodes (recommended)
    g1 -.-> g2        Connect subgraph IDs (for layout)
```

### Direction Inside Subgraphs
```mermaid
graph TB
    subgraph horiz["Horizontal Section"]
        direction LR
        A --> B --> C
    end
```

## Layout Directions

```
graph TB    Top to Bottom (default)
graph BT    Bottom to Top
graph LR    Left to Right
graph RL    Right to Left
graph TD    Top Down (alias for TB)
```

**Guidelines:**
- TB/TD: Sequential processes, hierarchies, decision trees
- LR: Timelines, pipelines, wide comparisons
- Mixed: Set `direction` inside individual subgraphs

## Styling

### Inline Style
```mermaid
style NodeID fill:#color,stroke:#color,stroke-width:2px
```

### Multiple Nodes
```mermaid
style A,B,C fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px
```

### Class Definitions
```mermaid
classDef green fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px
classDef blue fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px

class A,B green
class C,D blue
```

### Semantic Color Reference

| Role | Fill | Stroke |
|------|------|--------|
| Input / Start | `#d3f9d8` | `#2f9e44` |
| Process / Action | `#dae8fc` | `#6c8ebf` |
| Decision | `#fff2cc` | `#d6b656` |
| Output / Result | `#c5f6fa` | `#0c8599` |
| Warning / Error | `#ffe3e3` | `#c92a2a` |
| Storage / Data | `#fff4e6` | `#e67700` |
| Reasoning / AI | `#e5dbff` | `#5f3dc4` |
| Neutral | `#f8f9fa` | `#868e96` |
| Title / Header | `#e7f5ff` | `#1971c2` |

### Link/Edge Styling
```mermaid
linkStyle 0 stroke:#2f9e44,stroke-width:2px
linkStyle default stroke:#868e96,stroke-width:1px
```

## Sequence Diagram Syntax

```mermaid
sequenceDiagram
    participant A as Client
    participant B as Server
    participant C as Database

    A->>B: POST /api/users
    activate B
    B->>C: INSERT INTO users
    C-->>B: OK
    B-->>A: 201 Created
    deactivate B

    Note over A,B: Authentication required

    alt Success
        A->>B: GET /api/profile
    else Failure
        A->>B: Retry with token
    end

    loop Health Check
        B->>C: SELECT 1
    end
```

**Arrow types:**
- `->>` solid with arrowhead
- `-->>` dashed with arrowhead
- `-x` solid with cross
- `--x` dashed with cross

## State Diagram Syntax

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading: fetch()
    Loading --> Success: 200 OK
    Loading --> Error: 4xx/5xx
    Success --> Idle: reset()
    Error --> Loading: retry()
    Error --> [*]: give up

    state Loading {
        [*] --> Fetching
        Fetching --> Parsing
    }
```

## Class Diagram Syntax

```mermaid
classDiagram
    class User {
        +String name
        +String email
        +login() bool
    }
    class Post {
        +String title
        +String body
        +publish() void
    }
    User "1" --> "*" Post: creates
```

## ER Diagram Syntax

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    USER {
        int id PK
        string name
        string email UK
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
    }
```

**Cardinality:**
- `||` exactly one
- `o|` zero or one
- `}|` one or more
- `}o` zero or more

## Mindmap Syntax

```mermaid
mindmap
    root((Central Topic))
        Branch A
            Leaf A1
            Leaf A2
        Branch B
            Leaf B1
        Branch C
```

## Gantt Chart Syntax

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
        Design          :a1, 2024-01-01, 14d
        Prototype       :a2, after a1, 7d
    section Phase 2
        Development     :b1, after a2, 30d
        Testing         :b2, after b1, 14d
```

## Troubleshooting

### "Parse error: Unsupported markdown: list"
→ Remove space after `number.` in node text

### "Parse error: Expecting 'SEMI', 'NEWLINE', 'EOF'"
→ Subgraph name has spaces without ID format, or node reference uses display text

### "Parse error: unexpected character"
→ Unescaped special characters in node text

### Diagram renders but looks wrong
→ Check direction is set, verify style declarations, ensure IDs match

### Platform differences
- **GitHub**: Good Mermaid support, renders most modern syntax
- **Obsidian**: Older parser, stricter. Test before finalizing.
- **mermaid.live**: Latest parser. Best for testing.

## Validation Checklist

- [ ] No `number. space` patterns in any node text
- [ ] All subgraphs with spaces use `id["Display Name"]`
- [ ] All references use IDs not display text
- [ ] All arrows use valid syntax
- [ ] Style declarations use valid color format
- [ ] Direction explicitly set
- [ ] All referenced node IDs are defined
- [ ] No emoji in node text
- [ ] Under 30 nodes per diagram
