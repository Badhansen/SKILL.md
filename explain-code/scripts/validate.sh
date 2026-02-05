#!/bin/bash
# validate.sh - Validate Excalidraw JSON files
# Usage: ./validate.sh <file.excalidraw> [--strict]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if file argument provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: No file specified${NC}"
    echo "Usage: $0 <file.excalidraw> [--strict]"
    exit 1
fi

FILE="$1"
STRICT=false

if [ "$2" == "--strict" ]; then
    STRICT=true
fi

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo -e "${RED}Error: File not found: $FILE${NC}"
    exit 1
fi

# Check file extension
if [[ ! "$FILE" == *.excalidraw ]]; then
    echo -e "${YELLOW}Warning: File does not have .excalidraw extension${NC}"
fi

echo "Validating: $FILE"
echo "----------------------------------------"

# Run Python validation
python3 - "$FILE" "$STRICT" << 'PYTHON_SCRIPT'
import json
import sys
from pathlib import Path

def validate_excalidraw(filepath, strict=False):
    errors = []
    warnings = []
    
    # Load and parse JSON
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\033[0;31m✗ Invalid JSON: {e}\033[0m")
        return False
    
    # Check required top-level fields
    required_fields = ['type', 'version', 'elements']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
    
    # Validate type
    if data.get('type') != 'excalidraw':
        errors.append(f"Invalid type: expected 'excalidraw', got '{data.get('type')}'")
    
    # Validate version
    if 'version' in data and data['version'] not in [1, 2]:
        warnings.append(f"Unexpected version: {data['version']} (expected 1 or 2)")
    
    # Validate elements array
    if 'elements' in data:
        if not isinstance(data['elements'], list):
            errors.append("'elements' must be an array")
        else:
            element_ids = set()
            valid_types = ['rectangle', 'ellipse', 'diamond', 'line', 'arrow', 'text', 
                          'freedraw', 'image', 'frame', 'group', 'embeddable']
            
            for i, elem in enumerate(data['elements']):
                elem_errors = validate_element(elem, i, valid_types, strict)
                errors.extend(elem_errors['errors'])
                warnings.extend(elem_errors['warnings'])
                
                # Check for duplicate IDs
                if 'id' in elem:
                    if elem['id'] in element_ids:
                        errors.append(f"Element {i}: Duplicate ID '{elem['id']}'")
                    element_ids.add(elem['id'])
            
            # Validate bindings reference existing elements
            for elem in data['elements']:
                if elem.get('type') in ['arrow', 'line']:
                    for binding_key in ['startBinding', 'endBinding']:
                        binding = elem.get(binding_key)
                        if binding and 'elementId' in binding:
                            if binding['elementId'] not in element_ids:
                                warnings.append(
                                    f"Element '{elem.get('id')}': {binding_key} references "
                                    f"non-existent element '{binding['elementId']}'"
                                )
    
    # Validate appState if present
    if 'appState' in data:
        if not isinstance(data['appState'], dict):
            errors.append("'appState' must be an object")
        else:
            if 'viewBackgroundColor' in data['appState']:
                color = data['appState']['viewBackgroundColor']
                if not is_valid_color(color):
                    warnings.append(f"Invalid viewBackgroundColor: '{color}'")
    
    # Print results
    print(f"Elements: {len(data.get('elements', []))}")
    print()
    
    if warnings:
        print("\033[1;33mWarnings:\033[0m")
        for w in warnings:
            print(f"  ⚠ {w}")
        print()
    
    if errors:
        print("\033[0;31mErrors:\033[0m")
        for e in errors:
            print(f"  ✗ {e}")
        print()
        print("\033[0;31m✗ Validation FAILED\033[0m")
        return False
    
    print("\033[0;32m✓ Validation PASSED\033[0m")
    return True


def validate_element(elem, index, valid_types, strict):
    errors = []
    warnings = []
    prefix = f"Element {index}"
    
    if not isinstance(elem, dict):
        errors.append(f"{prefix}: Element must be an object")
        return {'errors': errors, 'warnings': warnings}
    
    # Required fields for all elements
    required = ['type', 'id', 'x', 'y']
    for field in required:
        if field not in elem:
            errors.append(f"{prefix}: Missing required field '{field}'")
    
    # Validate type
    elem_type = elem.get('type')
    if elem_type and elem_type not in valid_types:
        warnings.append(f"{prefix}: Unknown type '{elem_type}'")
    
    # Validate coordinates
    for coord in ['x', 'y']:
        if coord in elem and not isinstance(elem[coord], (int, float)):
            errors.append(f"{prefix}: '{coord}' must be a number")
    
    # Type-specific validation
    if elem_type in ['rectangle', 'ellipse', 'diamond', 'image', 'frame']:
        for dim in ['width', 'height']:
            if dim not in elem:
                if strict:
                    errors.append(f"{prefix}: Missing '{dim}' for {elem_type}")
            elif not isinstance(elem[dim], (int, float)):
                errors.append(f"{prefix}: '{dim}' must be a number")
            elif elem[dim] < 0:
                warnings.append(f"{prefix}: '{dim}' is negative")
    
    if elem_type == 'text':
        if 'text' not in elem:
            errors.append(f"{prefix}: Missing 'text' field for text element")
        if 'fontSize' in elem and not isinstance(elem['fontSize'], (int, float)):
            errors.append(f"{prefix}: 'fontSize' must be a number")
        if 'fontFamily' in elem and elem['fontFamily'] not in [1, 2, 3]:
            warnings.append(f"{prefix}: Unusual fontFamily value {elem['fontFamily']}")
    
    if elem_type in ['arrow', 'line']:
        if 'points' not in elem:
            errors.append(f"{prefix}: Missing 'points' for {elem_type}")
        elif not isinstance(elem['points'], list):
            errors.append(f"{prefix}: 'points' must be an array")
        elif len(elem['points']) < 2:
            errors.append(f"{prefix}: 'points' must have at least 2 points")
        else:
            for i, point in enumerate(elem['points']):
                if not isinstance(point, list) or len(point) != 2:
                    errors.append(f"{prefix}: Point {i} must be [x, y] array")
    
    # Validate colors
    for color_field in ['strokeColor', 'backgroundColor']:
        if color_field in elem:
            if not is_valid_color(elem[color_field]):
                warnings.append(f"{prefix}: Invalid {color_field}: '{elem[color_field]}'")
    
    # Validate strokeWidth
    if 'strokeWidth' in elem:
        if not isinstance(elem['strokeWidth'], (int, float)):
            errors.append(f"{prefix}: 'strokeWidth' must be a number")
        elif elem['strokeWidth'] < 0:
            warnings.append(f"{prefix}: 'strokeWidth' is negative")
    
    # Validate arrowheads
    valid_arrowheads = [None, 'arrow', 'bar', 'dot', 'triangle', 'triangle_outline', 
                       'diamond', 'diamond_outline']
    for arrowhead in ['startArrowhead', 'endArrowhead']:
        if arrowhead in elem and elem[arrowhead] not in valid_arrowheads:
            warnings.append(f"{prefix}: Unknown {arrowhead}: '{elem[arrowhead]}'")
    
    return {'errors': errors, 'warnings': warnings}


def is_valid_color(color):
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
    if color.startswith('rgb') or color.startswith('hsl'):
        return True
    # Named colors
    named_colors = ['red', 'green', 'blue', 'black', 'white', 'yellow', 'orange', 
                    'purple', 'pink', 'gray', 'grey', 'cyan', 'magenta']
    if color.lower() in named_colors:
        return True
    return False


if __name__ == '__main__':
    filepath = sys.argv[1]
    strict = sys.argv[2] == 'True' if len(sys.argv) > 2 else False
    success = validate_excalidraw(filepath, strict)
    sys.exit(0 if success else 1)
PYTHON_SCRIPT

exit_code=$?

echo "----------------------------------------"
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}File is valid and can be opened at excalidraw.com${NC}"
else
    echo -e "${RED}Fix the errors above before using the file${NC}"
fi

exit $exit_code
