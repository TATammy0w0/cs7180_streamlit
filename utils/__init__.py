# Make utils a package and maintain backward compatibility
from .display import (
    display_results,
    convert_api_response_to_display_format,
    RISK_COLORS,
    MODIFIABLE_STYLES,
    NON_MODIFIABLE_STYLES,
)

__all__ = [
    'display_results',
    'convert_api_response_to_display_format',
    'RISK_COLORS',
    'MODIFIABLE_STYLES',
    'NON_MODIFIABLE_STYLES',
]

