# Diagram Templates Reference

Complete templates for each diagram type with copy-paste ready JSON.

## Table of Contents

1. [Class Diagram](#class-diagram)
2. [Flow Diagram](#flow-diagram)
3. [ER Diagram](#er-diagram)
4. [Feature Diagram](#feature-diagram)
5. [Component Diagram](#component-diagram)
6. [Sequence Diagram](#sequence-diagram)
7. [State Diagram](#state-diagram)
8. [Architecture Diagram](#architecture-diagram)

---

## Class Diagram

Visualize OOP structures: classes, interfaces, inheritance, associations.

### Class Box Template

```
┌─────────────────────┐
│   <<stereotype>>    │
│     ClassName       │
├─────────────────────┤
│ - privateAttr: Type │
│ + publicAttr: Type  │
├─────────────────────┤
│ + publicMethod()    │
│ - privateMethod()   │
└─────────────────────┘
```

### Full Class JSON

```json
{
  "elements": [
    {
      "type": "rectangle",
      "id": "class_user_box",
      "x": 100, "y": 100,
      "width": 220, "height": 160,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 1,
      "roundness": { "type": 3 }
    },
    {
      "type": "text",
      "id": "class_user_name",
      "x": 210, "y": 115,
      "width": 100, "height": 25,
      "text": "User",
      "fontSize": 18,
      "fontFamily": 1,
      "textAlign": "center",
      "strokeColor": "#1e1e1e"
    },
    {
      "type": "line",
      "id": "class_user_div1",
      "x": 100, "y": 145,
      "points": [[0, 0], [220, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 1
    },
    {
      "type": "text",
      "id": "class_user_attrs",
      "x": 110, "y": 155,
      "text": "- id: string\n- email: string\n+ name: string",
      "fontSize": 13,
      "fontFamily": 3,
      "textAlign": "left",
      "strokeColor": "#1e1e1e"
    },
    {
      "type": "line",
      "id": "class_user_div2",
      "x": 100, "y": 205,
      "points": [[0, 0], [220, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 1
    },
    {
      "type": "text",
      "id": "class_user_methods",
      "x": 110, "y": 215,
      "text": "+ validate(): bool\n+ save(): void",
      "fontSize": 13,
      "fontFamily": 3,
      "textAlign": "left",
      "strokeColor": "#1e1e1e"
    }
  ]
}
```

### Interface Template (Purple)

```json
{
  "type": "rectangle",
  "id": "interface_box",
  "x": 100, "y": 100,
  "width": 200, "height": 100,
  "backgroundColor": "#d0bfff"
}
```

Add `<<interface>>` stereotype text above name.

### Inheritance Arrow

```json
{
  "type": "arrow",
  "id": "inherit_arrow",
  "x": 210, "y": 260,
  "points": [[0, 0], [0, -60]],
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "endArrowhead": "triangle",
  "roughness": 1
}
```

### Implementation Arrow (Dashed)

```json
{
  "type": "arrow",
  "id": "impl_arrow",
  "x": 210, "y": 260,
  "points": [[0, 0], [0, -60]],
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "strokeStyle": "dashed",
  "endArrowhead": "triangle"
}
```

---

## Flow Diagram

Visualize algorithms, processes, control flow.

### Standard Shapes

| Purpose | Shape | Color |
|---------|-------|-------|
| Start/End | Ellipse | `#b2f2bb` |
| Process | Rectangle | `#a5d8ff` |
| Decision | Diamond | `#ffec99` |
| Input/Output | Parallelogram | `#ffd8a8` |

### Start Node

```json
{
  "type": "ellipse",
  "id": "flow_start",
  "x": 175, "y": 50,
  "width": 100, "height": 50,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#b2f2bb",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1
}
```

### Process Box

```json
{
  "type": "rectangle",
  "id": "flow_process_1",
  "x": 150, "y": 150,
  "width": 150, "height": 60,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "roundness": { "type": 3 }
}
```

### Decision Diamond

```json
{
  "type": "diamond",
  "id": "flow_decision_1",
  "x": 160, "y": 260,
  "width": 130, "height": 90,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#ffec99",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1
}
```

### Yes/No Branch Labels

```json
{
  "elements": [
    {
      "type": "text",
      "id": "label_yes",
      "x": 310, "y": 290,
      "text": "Yes",
      "fontSize": 14,
      "strokeColor": "#2f9e44"
    },
    {
      "type": "text",
      "id": "label_no",
      "x": 130, "y": 290,
      "text": "No",
      "fontSize": 14,
      "strokeColor": "#e03131"
    }
  ]
}
```

### Loop Back Arrow

```json
{
  "type": "arrow",
  "id": "loop_back",
  "x": 100, "y": 400,
  "points": [[0, 0], [-50, 0], [-50, -200], [50, -200]],
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "endArrowhead": "arrow"
}
```

---

## ER Diagram

Visualize database entities and relationships.

### Entity Box

```json
{
  "elements": [
    {
      "type": "rectangle",
      "id": "entity_user",
      "x": 100, "y": 100,
      "width": 200, "height": 160,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 1,
      "roundness": { "type": 3 }
    },
    {
      "type": "text",
      "id": "entity_user_name",
      "x": 200, "y": 115,
      "text": "USER",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "strokeColor": "#1e1e1e"
    },
    {
      "type": "line",
      "id": "entity_user_div",
      "x": 100, "y": 145,
      "points": [[0, 0], [200, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 1
    },
    {
      "type": "text",
      "id": "entity_user_attrs",
      "x": 110, "y": 155,
      "text": "🔑 id (PK)\n   username\n   email\n   password_hash\n   created_at",
      "fontSize": 13,
      "fontFamily": 3,
      "textAlign": "left",
      "strokeColor": "#1e1e1e"
    }
  ]
}
```

### Relationship Notations

| Cardinality | Symbol | Meaning |
|-------------|--------|---------|
| One | `1` or `\|` | Exactly one |
| Many | `*` or `N` | Zero or more |
| Zero-One | `0..1` | Optional one |
| One-Many | `1..*` | At least one |

### One-to-Many Relationship

```json
{
  "elements": [
    {
      "type": "line",
      "id": "rel_line",
      "x": 300, "y": 180,
      "points": [[0, 0], [100, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "rel_one",
      "x": 305, "y": 160,
      "text": "1",
      "fontSize": 14
    },
    {
      "type": "text",
      "id": "rel_many",
      "x": 385, "y": 160,
      "text": "*",
      "fontSize": 18
    }
  ]
}
```

### Crow's Foot (Many)

Create using three short lines forming a fork:

```json
{
  "type": "line",
  "id": "crowsfoot",
  "x": 400, "y": 180,
  "points": [[0, -8], [15, 0], [0, 8]],
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2
}
```

---

## Feature Diagram

Visualize system features, sub-features, and dependencies.

### Root Feature

```json
{
  "type": "rectangle",
  "id": "feature_root",
  "x": 200, "y": 50,
  "width": 180, "height": 50,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 3,
  "roughness": 1,
  "roundness": { "type": 3 }
}
```

### Mandatory Feature

```json
{
  "type": "rectangle",
  "id": "feature_mandatory",
  "x": 100, "y": 150,
  "width": 140, "height": 40,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#b2f2bb",
  "fillStyle": "solid",
  "strokeWidth": 2
}
```

### Optional Feature (Dashed Border)

```json
{
  "type": "rectangle",
  "id": "feature_optional",
  "x": 280, "y": 150,
  "width": 140, "height": 40,
  "strokeColor": "#868e96",
  "backgroundColor": "#f8f9fa",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "dashed"
}
```

### Feature Connection with Filled Circle (Mandatory)

```json
{
  "elements": [
    {
      "type": "line",
      "id": "feature_line",
      "x": 290, "y": 100,
      "points": [[0, 0], [-120, 50]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2
    },
    {
      "type": "ellipse",
      "id": "mandatory_dot",
      "x": 165, "y": 145,
      "width": 10, "height": 10,
      "backgroundColor": "#1e1e1e",
      "fillStyle": "solid"
    }
  ]
}
```

### Feature Connection with Empty Circle (Optional)

```json
{
  "type": "ellipse",
  "id": "optional_dot",
  "x": 345, "y": 145,
  "width": 10, "height": 10,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#ffffff",
  "fillStyle": "solid",
  "strokeWidth": 2
}
```

---

## Component Diagram

Visualize modules, services, and their interfaces.

### Component Box with Tabs

```json
{
  "elements": [
    {
      "type": "rectangle",
      "id": "component_main",
      "x": 100, "y": 100,
      "width": 180, "height": 100,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#e9ecef",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 1
    },
    {
      "type": "rectangle",
      "id": "component_tab1",
      "x": 85, "y": 115,
      "width": 25, "height": 12,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#e9ecef",
      "fillStyle": "solid",
      "strokeWidth": 1
    },
    {
      "type": "rectangle",
      "id": "component_tab2",
      "x": 85, "y": 132,
      "width": 25, "height": 12,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#e9ecef",
      "fillStyle": "solid",
      "strokeWidth": 1
    },
    {
      "type": "text",
      "id": "component_name",
      "x": 190, "y": 145,
      "text": "AuthService",
      "fontSize": 16,
      "textAlign": "center"
    }
  ]
}
```

### Provided Interface (Lollipop)

```json
{
  "elements": [
    {
      "type": "line",
      "id": "provided_line",
      "x": 280, "y": 150,
      "points": [[0, 0], [30, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2
    },
    {
      "type": "ellipse",
      "id": "provided_circle",
      "x": 310, "y": 142,
      "width": 16, "height": 16,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "strokeWidth": 2
    }
  ]
}
```

### Required Interface (Socket)

```json
{
  "elements": [
    {
      "type": "line",
      "id": "required_line",
      "x": 100, "y": 150,
      "points": [[-30, 0], [0, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2
    },
    {
      "type": "line",
      "id": "required_arc",
      "x": 60, "y": 142,
      "points": [[0, 8], [8, 0], [0, 16]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2
    }
  ]
}
```

---

## Sequence Diagram

Visualize interactions over time.

### Participant Box

```json
{
  "type": "rectangle",
  "id": "participant_1",
  "x": 100, "y": 50,
  "width": 120, "height": 45,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1
}
```

### Lifeline (Dashed)

```json
{
  "type": "line",
  "id": "lifeline_1",
  "x": 160, "y": 95,
  "points": [[0, 0], [0, 350]],
  "strokeColor": "#868e96",
  "strokeWidth": 1,
  "strokeStyle": "dashed"
}
```

### Synchronous Message

```json
{
  "type": "arrow",
  "id": "msg_sync",
  "x": 160, "y": 130,
  "points": [[0, 0], [180, 0]],
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "endArrowhead": "arrow"
}
```

### Asynchronous Message (Open Arrow)

```json
{
  "type": "arrow",
  "id": "msg_async",
  "x": 160, "y": 180,
  "points": [[0, 0], [180, 0]],
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "endArrowhead": "arrow"
}
```

### Return Message (Dashed)

```json
{
  "type": "arrow",
  "id": "msg_return",
  "x": 340, "y": 230,
  "points": [[0, 0], [-180, 0]],
  "strokeColor": "#868e96",
  "strokeWidth": 1,
  "strokeStyle": "dashed",
  "endArrowhead": "arrow"
}
```

### Activation Box

```json
{
  "type": "rectangle",
  "id": "activation_1",
  "x": 155, "y": 125,
  "width": 12, "height": 80,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 1
}
```

---

## State Diagram

Visualize state machines and transitions.

### Initial State (Filled Circle)

```json
{
  "type": "ellipse",
  "id": "state_initial",
  "x": 185, "y": 40,
  "width": 30, "height": 30,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#1e1e1e",
  "fillStyle": "solid"
}
```

### State Box (Rounded)

```json
{
  "type": "rectangle",
  "id": "state_idle",
  "x": 150, "y": 100,
  "width": 120, "height": 50,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "roundness": { "type": 3, "value": 20 }
}
```

### Final State (Bullseye)

```json
{
  "elements": [
    {
      "type": "ellipse",
      "id": "final_outer",
      "x": 185, "y": 400,
      "width": 30, "height": 30,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "strokeWidth": 2
    },
    {
      "type": "ellipse",
      "id": "final_inner",
      "x": 192, "y": 407,
      "width": 16, "height": 16,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#1e1e1e",
      "fillStyle": "solid"
    }
  ]
}
```

### Transition with Label

```json
{
  "elements": [
    {
      "type": "arrow",
      "id": "transition_1",
      "x": 210, "y": 150,
      "points": [[0, 0], [0, 80]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2,
      "endArrowhead": "arrow"
    },
    {
      "type": "text",
      "id": "transition_label",
      "x": 220, "y": 180,
      "text": "submit()",
      "fontSize": 12,
      "fontFamily": 3
    }
  ]
}
```

---

## Architecture Diagram

High-level system overview with layers and boundaries.

### Layer Box (Dashed Boundary)

```json
{
  "type": "rectangle",
  "id": "layer_presentation",
  "x": 50, "y": 50,
  "width": 600, "height": 120,
  "strokeColor": "#868e96",
  "backgroundColor": "#e7f5ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "dashed",
  "roughness": 0
}
```

### Layer Colors

| Layer | Background |
|-------|------------|
| Presentation | `#e7f5ff` |
| Business Logic | `#fff3bf` |
| Data Access | `#d3f9d8` |
| Infrastructure | `#ffe8cc` |

### External System

```json
{
  "type": "rectangle",
  "id": "external_api",
  "x": 700, "y": 150,
  "width": 100, "height": 60,
  "strokeColor": "#e03131",
  "backgroundColor": "#fff5f5",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "dashed"
}
```

### Database Symbol

```json
{
  "elements": [
    {
      "type": "ellipse",
      "id": "db_top",
      "x": 100, "y": 300,
      "width": 80, "height": 20,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2
    },
    {
      "type": "rectangle",
      "id": "db_body",
      "x": 100, "y": 308,
      "width": 80, "height": 50,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2
    },
    {
      "type": "ellipse",
      "id": "db_bottom",
      "x": 100, "y": 348,
      "width": 80, "height": 20,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2
    }
  ]
}
```

---

## Complete File Template

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "code-visualizer",
  "elements": [
    // ... your elements here
  ],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```
