#!/usr/bin/env python3
"""
generate_diagram.py - Helper utilities for generating Excalidraw diagram elements

Usage:
    python generate_diagram.py --type class --output diagram.excalidraw
    python generate_diagram.py --type flow --output diagram.excalidraw
    python generate_diagram.py --type er --output diagram.excalidraw

This script provides utility functions for programmatically generating Excalidraw elements.
"""

import json
import uuid
import argparse
from typing import Dict, List, Any, Optional, Tuple


class Color:
    """Standard color palette for diagrams."""
    CLASS = "#a5d8ff"
    INTERFACE = "#d0bfff"
    ENTITY = "#b2f2bb"
    DECISION = "#ffec99"
    START_END = "#ffc9c9"
    PROCESS = "#e9ecef"
    EXTERNAL = "#ffd8a8"
    ERROR = "#ff8787"
    STROKE = "#1e1e1e"
    STROKE_LIGHT = "#868e96"
    STROKE_SUCCESS = "#2f9e44"
    STROKE_ERROR = "#e03131"
    BACKGROUND = "#ffffff"


def generate_id(element_type: str = "elem") -> str:
    """Generate a unique element ID."""
    return f"{element_type}_{uuid.uuid4().hex[:8]}"


def create_rectangle(
    x: float, y: float, width: float, height: float,
    bg_color: str = Color.CLASS,
    stroke_color: str = Color.STROKE,
    stroke_width: int = 2,
    roughness: int = 1,
    rounded: bool = True
) -> Dict[str, Any]:
    """Create a rectangle element."""
    elem = {
        "type": "rectangle",
        "id": generate_id("rect"),
        "x": x, "y": y,
        "width": width, "height": height,
        "strokeColor": stroke_color,
        "backgroundColor": bg_color,
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "roughness": roughness
    }
    if rounded:
        elem["roundness"] = {"type": 3}
    return elem


def create_ellipse(
    x: float, y: float, width: float, height: float,
    bg_color: str = Color.START_END,
    stroke_color: str = Color.STROKE
) -> Dict[str, Any]:
    """Create an ellipse element."""
    return {
        "type": "ellipse",
        "id": generate_id("ellipse"),
        "x": x, "y": y,
        "width": width, "height": height,
        "strokeColor": stroke_color,
        "backgroundColor": bg_color,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "roughness": 1
    }


def create_diamond(
    x: float, y: float, width: float, height: float,
    bg_color: str = Color.DECISION
) -> Dict[str, Any]:
    """Create a diamond element."""
    return {
        "type": "diamond",
        "id": generate_id("diamond"),
        "x": x, "y": y,
        "width": width, "height": height,
        "strokeColor": Color.STROKE,
        "backgroundColor": bg_color,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "roughness": 1
    }


def create_text(
    x: float, y: float, text: str,
    font_size: int = 14,
    font_family: int = 1,
    text_align: str = "center",
    stroke_color: str = Color.STROKE
) -> Dict[str, Any]:
    """Create a text element."""
    return {
        "type": "text",
        "id": generate_id("text"),
        "x": x, "y": y,
        "text": text,
        "fontSize": font_size,
        "fontFamily": font_family,
        "textAlign": text_align,
        "strokeColor": stroke_color
    }


def create_line(
    x: float, y: float,
    points: List[List[float]],
    stroke_width: int = 1,
    stroke_style: str = "solid"
) -> Dict[str, Any]:
    """Create a line element."""
    elem = {
        "type": "line",
        "id": generate_id("line"),
        "x": x, "y": y,
        "points": points,
        "strokeColor": Color.STROKE,
        "strokeWidth": stroke_width
    }
    if stroke_style != "solid":
        elem["strokeStyle"] = stroke_style
    return elem


def create_arrow(
    x: float, y: float,
    points: List[List[float]],
    stroke_width: int = 2,
    stroke_style: str = "solid",
    start_arrowhead: Optional[str] = None,
    end_arrowhead: str = "arrow"
) -> Dict[str, Any]:
    """Create an arrow element."""
    elem = {
        "type": "arrow",
        "id": generate_id("arrow"),
        "x": x, "y": y,
        "points": points,
        "strokeColor": Color.STROKE,
        "strokeWidth": stroke_width,
        "roughness": 1,
        "startArrowhead": start_arrowhead,
        "endArrowhead": end_arrowhead
    }
    if stroke_style != "solid":
        elem["strokeStyle"] = stroke_style
    return elem


def create_class_box(
    x: float, y: float,
    name: str,
    attributes: List[str],
    methods: List[str],
    is_interface: bool = False,
    stereotype: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Create a complete class box with sections."""
    elements = []
    
    width = 200
    header_height = 45 if stereotype else 35
    attrs_height = max(30, len(attributes) * 18 + 10)
    methods_height = max(30, len(methods) * 18 + 10)
    total_height = header_height + attrs_height + methods_height
    
    bg_color = Color.INTERFACE if is_interface else Color.CLASS
    
    # Main box
    elements.append(create_rectangle(x, y, width, total_height, bg_color))
    
    # Stereotype
    current_y = y + 10
    if stereotype:
        elements.append(create_text(
            x + width / 2, current_y,
            f"<<{stereotype}>>",
            font_size=11,
            stroke_color=Color.STROKE_LIGHT
        ))
        current_y += 18
    
    # Class name
    elements.append(create_text(x + width / 2, current_y, name, font_size=16))
    current_y = y + header_height
    
    # Divider 1
    elements.append(create_line(x, current_y, [[0, 0], [width, 0]]))
    current_y += 10
    
    # Attributes
    if attributes:
        elements.append(create_text(
            x + 10, current_y,
            "\n".join(attributes),
            font_size=12, font_family=3, text_align="left"
        ))
    current_y = y + header_height + attrs_height
    
    # Divider 2
    elements.append(create_line(x, current_y, [[0, 0], [width, 0]]))
    current_y += 10
    
    # Methods
    if methods:
        elements.append(create_text(
            x + 10, current_y,
            "\n".join(methods),
            font_size=12, font_family=3, text_align="left"
        ))
    
    return elements


def create_entity_box(
    x: float, y: float,
    name: str,
    attributes: List[Tuple[str, bool, bool]]  # (name, is_pk, is_fk)
) -> List[Dict[str, Any]]:
    """Create an ER diagram entity box."""
    elements = []
    
    width = 180
    header_height = 35
    attrs_height = len(attributes) * 18 + 20
    total_height = header_height + attrs_height
    
    elements.append(create_rectangle(x, y, width, total_height, Color.ENTITY))
    elements.append(create_text(x + width / 2, y + 12, name.upper(), font_size=16))
    elements.append(create_line(x, y + header_height, [[0, 0], [width, 0]]))
    
    attr_lines = []
    for attr_name, is_pk, is_fk in attributes:
        prefix = "🔑 " if is_pk else ("FK " if is_fk else "   ")
        attr_lines.append(f"{prefix}{attr_name}")
    
    elements.append(create_text(
        x + 10, y + header_height + 10,
        "\n".join(attr_lines),
        font_size=12, font_family=3, text_align="left"
    ))
    
    return elements


def create_flow_start(x: float, y: float, label: str = "Start") -> List[Dict[str, Any]]:
    """Create a flow diagram start node."""
    return [
        create_ellipse(x, y, 100, 45, Color.ENTITY),
        create_text(x + 50, y + 15, label)
    ]


def create_flow_end(x: float, y: float, label: str = "End") -> List[Dict[str, Any]]:
    """Create a flow diagram end node."""
    return [
        create_ellipse(x, y, 100, 45, Color.START_END),
        create_text(x + 50, y + 15, label)
    ]


def create_flow_process(x: float, y: float, label: str) -> List[Dict[str, Any]]:
    """Create a flow diagram process box."""
    return [
        create_rectangle(x, y, 150, 50, Color.CLASS),
        create_text(x + 75, y + 17, label, font_size=13)
    ]


def create_flow_decision(x: float, y: float, label: str) -> List[Dict[str, Any]]:
    """Create a flow diagram decision diamond."""
    return [
        create_diamond(x, y, 130, 80),
        create_text(x + 65, y + 32, label, font_size=13)
    ]


def create_excalidraw_file(elements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a complete Excalidraw file structure."""
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "code-visualizer",
        "elements": elements,
        "appState": {
            "gridSize": 20,
            "viewBackgroundColor": Color.BACKGROUND
        },
        "files": {}
    }


def save_excalidraw(data: Dict[str, Any], filepath: str) -> None:
    """Save Excalidraw data to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Saved diagram to: {filepath}")


def example_class_diagram() -> Dict[str, Any]:
    """Generate an example class diagram."""
    elements = []
    
    elements.extend(create_class_box(
        250, 50, "IRepository", [""],
        ["+ findById(id): T", "+ save(entity): void"],
        is_interface=True, stereotype="interface"
    ))
    
    elements.extend(create_class_box(
        250, 250, "UserRepository",
        ["- db: Database"],
        ["+ findById(id): User", "+ save(user): void"]
    ))
    
    elements.append(create_arrow(350, 250, [[0, 0], [0, -80]], stroke_style="dashed", end_arrowhead="triangle"))
    
    return create_excalidraw_file(elements)


def example_flow_diagram() -> Dict[str, Any]:
    """Generate an example flow diagram."""
    elements = []
    
    elements.extend(create_flow_start(175, 50))
    elements.append(create_arrow(225, 95, [[0, 0], [0, 30]]))
    elements.extend(create_flow_process(150, 125, "Get Input"))
    elements.append(create_arrow(225, 175, [[0, 0], [0, 30]]))
    elements.extend(create_flow_decision(160, 205, "Valid?"))
    elements.append(create_arrow(290, 245, [[0, 0], [60, 0]]))
    elements.append(create_text(310, 225, "Yes", stroke_color=Color.STROKE_SUCCESS))
    elements.extend(create_flow_process(350, 220, "Process"))
    elements.append(create_arrow(425, 270, [[0, 0], [0, 80]]))
    elements.extend(create_flow_end(375, 350))
    
    return create_excalidraw_file(elements)


def example_er_diagram() -> Dict[str, Any]:
    """Generate an example ER diagram."""
    elements = []
    
    elements.extend(create_entity_box(100, 100, "User", [
        ("id", True, False),
        ("email", False, False),
        ("name", False, False),
        ("created_at", False, False)
    ]))
    
    elements.extend(create_entity_box(400, 100, "Post", [
        ("id", True, False),
        ("user_id", False, True),
        ("title", False, False),
        ("content", False, False)
    ]))
    
    elements.append(create_line(280, 170, [[0, 0], [120, 0]], stroke_width=2))
    elements.append(create_text(290, 150, "1"))
    elements.append(create_text(385, 150, "*"))
    
    return create_excalidraw_file(elements)


def main():
    parser = argparse.ArgumentParser(description='Generate Excalidraw diagrams')
    parser.add_argument('--type', '-t', choices=['class', 'flow', 'er'],
                        default='class', help='Diagram type to generate')
    parser.add_argument('--output', '-o', default='diagram.excalidraw',
                        help='Output file path')
    
    args = parser.parse_args()
    
    if args.type == 'class':
        data = example_class_diagram()
    elif args.type == 'flow':
        data = example_flow_diagram()
    elif args.type == 'er':
        data = example_er_diagram()
    
    save_excalidraw(data, args.output)
    print(f"\nOpen at: https://excalidraw.com")


if __name__ == '__main__':
    main()
