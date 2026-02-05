#!/usr/bin/env python3
"""
validate_excalidraw.py - Comprehensive Excalidraw JSON validator

Usage:
    python validate_excalidraw.py <file.excalidraw> [options]

Options:
    --strict        Enable strict validation (all warnings become errors)
    --fix           Attempt to fix common issues and output corrected file
    --stats         Show statistics about the diagram
    --json          Output results as JSON
    --quiet         Only show errors, no success messages
"""

import json
import sys
import argparse
import uuid
import copy
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


class ExcalidrawValidator:
    """Validates Excalidraw JSON files for correctness and compatibility."""
    
    VALID_ELEMENT_TYPES = [
        'rectangle', 'ellipse', 'diamond', 'line', 'arrow', 'text',
        'freedraw', 'image', 'frame', 'group', 'embeddable'
    ]
    
    VALID_ARROWHEADS = [
        None, 'arrow', 'bar', 'dot', 'triangle', 'triangle_outline',
        'diamond', 'diamond_outline'
    ]
    
    VALID_STROKE_STYLES = ['solid', 'dashed', 'dotted']
    
    VALID_FILL_STYLES = ['solid', 'hachure', 'cross-hatch', 'zigzag', 'dots']
    
    VALID_TEXT_ALIGN = ['left', 'center', 'right']
    
    VALID_FONT_FAMILIES = {1: 'Virgil', 2: 'Helvetica', 3: 'Cascadia'}
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, Any] = {}
    
    def validate_file(self, filepath: str) -> bool:
        """Validate an Excalidraw file from path."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.validate(data)
        except FileNotFoundError:
            self.errors.append(f"File not found: {filepath}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate Excalidraw data structure."""
        self.errors = []
        self.warnings = []
        self.stats = {'element_counts': {}, 'total_elements': 0}
        
        # Validate top-level structure
        self._validate_top_level(data)
        
        # Validate elements
        if 'elements' in data and isinstance(data['elements'], list):
            self._validate_elements(data['elements'])
        
        # Validate appState
        if 'appState' in data:
            self._validate_app_state(data['appState'])
        
        # In strict mode, warnings become errors
        if self.strict:
            self.errors.extend(self.warnings)
            self.warnings = []
        
        return len(self.errors) == 0
    
    def _validate_top_level(self, data: Dict[str, Any]) -> None:
        """Validate top-level structure."""
        # Required fields
        if 'type' not in data:
            self.errors.append("Missing required field: 'type'")
        elif data['type'] != 'excalidraw':
            self.errors.append(f"Invalid type: expected 'excalidraw', got '{data['type']}'")
        
        if 'version' not in data:
            self.warnings.append("Missing 'version' field (recommended)")
        elif data['version'] not in [1, 2]:
            self.warnings.append(f"Unexpected version: {data['version']}")
        
        if 'elements' not in data:
            self.errors.append("Missing required field: 'elements'")
        elif not isinstance(data['elements'], list):
            self.errors.append("'elements' must be an array")
        
        # Optional but recommended
        if 'source' not in data:
            self.warnings.append("Missing 'source' field (recommended for tracking)")
    
    def _validate_elements(self, elements: List[Dict]) -> None:
        """Validate all elements."""
        element_ids = set()
        
        for i, elem in enumerate(elements):
            if not isinstance(elem, dict):
                self.errors.append(f"Element {i}: Must be an object")
                continue
            
            # Track statistics
            elem_type = elem.get('type', 'unknown')
            self.stats['element_counts'][elem_type] = \
                self.stats['element_counts'].get(elem_type, 0) + 1
            self.stats['total_elements'] += 1
            
            # Validate element
            self._validate_element(elem, i)
            
            # Check for duplicate IDs
            elem_id = elem.get('id')
            if elem_id:
                if elem_id in element_ids:
                    self.errors.append(f"Element {i}: Duplicate ID '{elem_id}'")
                element_ids.add(elem_id)
        
        # Validate bindings reference existing elements
        for elem in elements:
            self._validate_bindings(elem, element_ids)
    
    def _validate_element(self, elem: Dict, index: int) -> None:
        """Validate a single element."""
        prefix = f"Element {index}"
        
        # Required fields
        for field in ['type', 'id', 'x', 'y']:
            if field not in elem:
                self.errors.append(f"{prefix}: Missing required field '{field}'")
        
        # Validate type
        elem_type = elem.get('type')
        if elem_type and elem_type not in self.VALID_ELEMENT_TYPES:
            self.warnings.append(f"{prefix}: Unknown type '{elem_type}'")
        
        # Validate coordinates
        for coord in ['x', 'y']:
            if coord in elem and not isinstance(elem[coord], (int, float)):
                self.errors.append(f"{prefix}: '{coord}' must be a number")
        
        # Type-specific validation
        if elem_type in ['rectangle', 'ellipse', 'diamond', 'image', 'frame']:
            self._validate_shape(elem, prefix)
        elif elem_type == 'text':
            self._validate_text(elem, prefix)
        elif elem_type in ['arrow', 'line']:
            self._validate_connector(elem, prefix)
        
        # Common style properties
        self._validate_styles(elem, prefix)
    
    def _validate_shape(self, elem: Dict, prefix: str) -> None:
        """Validate shape-specific properties."""
        for dim in ['width', 'height']:
            if dim not in elem:
                self.warnings.append(f"{prefix}: Missing '{dim}'")
            elif not isinstance(elem[dim], (int, float)):
                self.errors.append(f"{prefix}: '{dim}' must be a number")
            elif elem[dim] < 0:
                self.warnings.append(f"{prefix}: '{dim}' is negative ({elem[dim]})")
    
    def _validate_text(self, elem: Dict, prefix: str) -> None:
        """Validate text element properties."""
        if 'text' not in elem:
            self.errors.append(f"{prefix}: Missing 'text' field")
        
        if 'fontSize' in elem:
            if not isinstance(elem['fontSize'], (int, float)):
                self.errors.append(f"{prefix}: 'fontSize' must be a number")
            elif elem['fontSize'] <= 0:
                self.warnings.append(f"{prefix}: 'fontSize' should be positive")
        
        if 'fontFamily' in elem:
            if elem['fontFamily'] not in self.VALID_FONT_FAMILIES:
                self.warnings.append(
                    f"{prefix}: fontFamily {elem['fontFamily']} not standard "
                    f"(valid: {list(self.VALID_FONT_FAMILIES.keys())})"
                )
        
        if 'textAlign' in elem and elem['textAlign'] not in self.VALID_TEXT_ALIGN:
            self.warnings.append(f"{prefix}: Invalid textAlign '{elem['textAlign']}'")
    
    def _validate_connector(self, elem: Dict, prefix: str) -> None:
        """Validate line/arrow properties."""
        if 'points' not in elem:
            self.errors.append(f"{prefix}: Missing 'points' array")
        elif not isinstance(elem['points'], list):
            self.errors.append(f"{prefix}: 'points' must be an array")
        elif len(elem['points']) < 2:
            self.errors.append(f"{prefix}: 'points' must have at least 2 points")
        else:
            for i, point in enumerate(elem['points']):
                if not isinstance(point, list) or len(point) != 2:
                    self.errors.append(f"{prefix}: Point {i} must be [x, y]")
                elif not all(isinstance(c, (int, float)) for c in point):
                    self.errors.append(f"{prefix}: Point {i} coordinates must be numbers")
        
        # Validate arrowheads
        for arrowhead in ['startArrowhead', 'endArrowhead']:
            if arrowhead in elem and elem[arrowhead] not in self.VALID_ARROWHEADS:
                self.warnings.append(f"{prefix}: Unknown {arrowhead} '{elem[arrowhead]}'")
    
    def _validate_bindings(self, elem: Dict, valid_ids: set) -> None:
        """Validate that bindings reference existing elements."""
        if elem.get('type') not in ['arrow', 'line']:
            return
        
        for binding_key in ['startBinding', 'endBinding']:
            binding = elem.get(binding_key)
            if binding and isinstance(binding, dict):
                ref_id = binding.get('elementId')
                if ref_id and ref_id not in valid_ids:
                    self.warnings.append(
                        f"Element '{elem.get('id')}': {binding_key} references "
                        f"non-existent element '{ref_id}'"
                    )
    
    def _validate_styles(self, elem: Dict, prefix: str) -> None:
        """Validate common style properties."""
        # Colors
        for color_field in ['strokeColor', 'backgroundColor']:
            if color_field in elem and not self._is_valid_color(elem[color_field]):
                self.warnings.append(f"{prefix}: Invalid {color_field} '{elem[color_field]}'")
        
        # Stroke width
        if 'strokeWidth' in elem:
            if not isinstance(elem['strokeWidth'], (int, float)):
                self.errors.append(f"{prefix}: 'strokeWidth' must be a number")
            elif elem['strokeWidth'] < 0:
                self.warnings.append(f"{prefix}: 'strokeWidth' is negative")
        
        # Stroke style
        if 'strokeStyle' in elem and elem['strokeStyle'] not in self.VALID_STROKE_STYLES:
            self.warnings.append(f"{prefix}: Unknown strokeStyle '{elem['strokeStyle']}'")
        
        # Fill style
        if 'fillStyle' in elem and elem['fillStyle'] not in self.VALID_FILL_STYLES:
            self.warnings.append(f"{prefix}: Unknown fillStyle '{elem['fillStyle']}'")
        
        # Roughness
        if 'roughness' in elem:
            if not isinstance(elem['roughness'], (int, float)):
                self.errors.append(f"{prefix}: 'roughness' must be a number")
            elif not 0 <= elem['roughness'] <= 2:
                self.warnings.append(f"{prefix}: 'roughness' typically 0-2")
    
    def _validate_app_state(self, app_state: Dict) -> None:
        """Validate appState object."""
        if not isinstance(app_state, dict):
            self.errors.append("'appState' must be an object")
            return
        
        if 'viewBackgroundColor' in app_state:
            if not self._is_valid_color(app_state['viewBackgroundColor']):
                self.warnings.append(
                    f"Invalid viewBackgroundColor '{app_state['viewBackgroundColor']}'"
                )
        
        if 'gridSize' in app_state:
            if not isinstance(app_state['gridSize'], (int, float)):
                self.warnings.append("gridSize should be a number")
            elif app_state['gridSize'] <= 0:
                self.warnings.append("gridSize should be positive")
    
    @staticmethod
    def _is_valid_color(color: str) -> bool:
        """Check if color value is valid."""
        if color == 'transparent':
            return True
        if color.startswith('#'):
            hex_part = color[1:]
            if len(hex_part) in [3, 4, 6, 8]:
                try:
                    int(hex_part, 16)
                    return True
                except ValueError:
                    pass
        if color.startswith(('rgb', 'hsl')):
            return True
        return False
    
    def get_report(self) -> Dict[str, Any]:
        """Get validation report as dictionary."""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'stats': self.stats
        }


def fix_common_issues(data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Attempt to fix common issues in Excalidraw data."""
    fixed = copy.deepcopy(data)
    fixes = []
    
    # Ensure required top-level fields
    if 'type' not in fixed:
        fixed['type'] = 'excalidraw'
        fixes.append("Added missing 'type' field")
    
    if 'version' not in fixed:
        fixed['version'] = 2
        fixes.append("Added missing 'version' field")
    
    if 'elements' not in fixed:
        fixed['elements'] = []
        fixes.append("Added missing 'elements' array")
    
    if 'appState' not in fixed:
        fixed['appState'] = {'gridSize': 20, 'viewBackgroundColor': '#ffffff'}
        fixes.append("Added default 'appState'")
    
    if 'files' not in fixed:
        fixed['files'] = {}
        fixes.append("Added missing 'files' object")
    
    # Fix elements
    seen_ids = set()
    for i, elem in enumerate(fixed.get('elements', [])):
        if not isinstance(elem, dict):
            continue
        
        # Generate missing ID
        if 'id' not in elem or elem['id'] in seen_ids:
            new_id = f"{elem.get('type', 'elem')}_{i}_{uuid.uuid4().hex[:8]}"
            elem['id'] = new_id
            fixes.append(f"Generated ID for element {i}")
        seen_ids.add(elem['id'])
        
        # Add missing coordinates
        if 'x' not in elem:
            elem['x'] = i * 50
            fixes.append(f"Element {i}: Added default x coordinate")
        if 'y' not in elem:
            elem['y'] = i * 50
            fixes.append(f"Element {i}: Added default y coordinate")
        
        # Fix shapes missing dimensions
        if elem.get('type') in ['rectangle', 'ellipse', 'diamond']:
            if 'width' not in elem:
                elem['width'] = 100
                fixes.append(f"Element {i}: Added default width")
            if 'height' not in elem:
                elem['height'] = 100
                fixes.append(f"Element {i}: Added default height")
        
        # Fix connectors missing points
        if elem.get('type') in ['arrow', 'line'] and 'points' not in elem:
            elem['points'] = [[0, 0], [100, 0]]
            fixes.append(f"Element {i}: Added default points")
    
    return fixed, fixes


def main():
    parser = argparse.ArgumentParser(
        description='Validate Excalidraw JSON files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('file', help='Excalidraw file to validate')
    parser.add_argument('--strict', action='store_true', help='Strict mode (warnings are errors)')
    parser.add_argument('--fix', action='store_true', help='Fix common issues')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('-o', '--output', help='Output file for --fix')
    
    args = parser.parse_args()
    
    # Load file
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Fix if requested
    if args.fix:
        data, fixes = fix_common_issues(data)
        if fixes and not args.quiet:
            print("Applied fixes:")
            for fix in fixes:
                print(f"  • {fix}")
            print()
        
        # Save fixed file
        output_path = args.output or args.file.replace('.excalidraw', '_fixed.excalidraw')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        if not args.quiet:
            print(f"Fixed file saved to: {output_path}\n")
    
    # Validate
    validator = ExcalidrawValidator(strict=args.strict)
    is_valid = validator.validate(data)
    report = validator.get_report()
    
    # Output results
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if not args.quiet:
            print(f"Validating: {args.file}")
            print("-" * 50)
        
        if args.stats:
            print(f"Total elements: {report['stats']['total_elements']}")
            print("Element types:")
            for etype, count in sorted(report['stats']['element_counts'].items()):
                print(f"  {etype}: {count}")
            print()
        
        if report['warnings'] and not args.quiet:
            print("\033[1;33mWarnings:\033[0m")
            for w in report['warnings']:
                print(f"  ⚠ {w}")
            print()
        
        if report['errors']:
            print("\033[0;31mErrors:\033[0m")
            for e in report['errors']:
                print(f"  ✗ {e}")
            print()
        
        if is_valid:
            if not args.quiet:
                print("\033[0;32m✓ Validation PASSED\033[0m")
        else:
            print("\033[0;31m✗ Validation FAILED\033[0m")
    
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
