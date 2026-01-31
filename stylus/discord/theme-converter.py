#!/usr/bin/env python3
"""
Catppuccin to Khavar Discord Theme Converter
Converts Catppuccin Discord theme colors to Khavar palette colors
"""

import re
import colorsys
from typing import Dict, Tuple

# Khavar color palette
KHAVAR_PALETTE = {
    "base": "#172620",
    "surface": "#21362d", 
    "overlay": "#2d493d",
    "muted": "#4e7e6b",
    "subtle": "#90bbaa",
    "text": "#dfece7",
    "low": "#39ac7e",
    "mid": "#2d8662", 
    "high": "#206046",
    "sarnai": "#f0c3cb",
    "anis": "#ff6b6b",
    "chatsalgan": "#e5951a",
    "els": "#cca24d",
    "uvs": "#80b946",
    "nuur": "#2b879e",
    "mus": "#9deaea",
    "yargui": "#d5b3e5",
}

# Catppuccin color mappings (extracted from the CSS)
CATPPUCCIN_DARK = {
    "#11111b": "base",      # Catppuccin base
    "#1e1e2e": "base",      # Catppuccin surface0
    "#181825": "surface",   # Catppuccin surface1
    "#313244": "surface",   # Catppuccin surface2
    "#45475a": "overlay",   # Catppuccin overlay0
    "#585b70": "overlay",   # Catppuccin overlay1
    "#6c7086": "muted",     # Catppuccin overlay2
    "#7f849c": "muted",     # Catppuccin subtext0
    "#9399b2": "subtle",    # Catppuccin subtext1
    "#a6adc8": "subtle",    # Catppuccin subtext2
    "#bac2de": "text",      # Catppuccin text
    "#cdd6f4": "text",      # Catppuccin text
    "#f38ba8": "anis",      # Catppuccin red
    "#fab387": "chatsalgan", # Catppuccin peach
    "#f9e2af": "els",       # Catppuccin yellow
    "#a6e3a1": "uvs",       # Catppuccin green
    "#94e2d5": "mus",       # Catppuccin teal
    "#89dceb": "mus",       # Catppuccin sky
    "#74c7ec": "mus",       # Catppuccin sapphire
    "#89b4fa": "nuur",      # Catppuccin blue
    "#b4befe": "yargui",    # Catppuccin lavender
    "#cba6f7": "yargui",    # Catppuccin mauve
    "#f5c2e7": "sarnai",    # Catppuccin pink - main accent
    "#f2cdcd": "sarnai",    # Catppuccin flamingo
}

CATPPUCCIN_LIGHT = {
    "#eff1f5": "text",      # Latte base (inverted for light theme)
    "#e6e9ef": "text",      # Latte mantle (inverted for light theme)
    "#dce0e8": "subtle",    # Latte crust (inverted for light theme)
    "#ccd0da": "subtle",    # Latte surface0 (inverted for light theme)
    "#bcc0cc": "muted",     # Latte surface1 (inverted for light theme)
    "#acb0be": "muted",     # Latte surface2 (inverted for light theme)
    "#9ca0b0": "overlay",   # Latte overlay0 (inverted for light theme)
    "#8c8fa1": "overlay",   # Latte overlay1 (inverted for light theme)
    "#7c7f93": "surface",   # Latte overlay2 (inverted for light theme)
    "#6c6f85": "surface",   # Latte subtext0 (inverted for light theme)
    "#5c5f77": "base",      # Latte subtext1 (inverted for light theme)
    "#4c4f69": "base",      # Latte text (inverted for light theme)
    "#d20f39": "anis",      # Latte red
    "#fe640b": "chatsalgan", # Latte peach
    "#df8e1d": "els",       # Latte yellow
    "#40a02b": "uvs",       # Latte green
    "#179299": "mus",       # Latte teal
    "#04a5e5": "mus",       # Latte sky
    "#209fb5": "mus",       # Latte sapphire
    "#1e66f5": "nuur",      # Latte blue
    "#7287fd": "yargui",    # Latte lavender
    "#8839ef": "yargui",    # Latte mauve
    "#ea76cb": "sarnai",    # Latte pink - main accent
    "#dd7878": "sarnai",    # Latte flamingo
}

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def color_distance(color1: str, color2: str) -> float:
    """Calculate perceptual distance between two colors"""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    # Convert to LAB color space for better perceptual distance
    def rgb_to_lab(rgb):
        r, g, b = [x/255.0 for x in rgb]
        # sRGB to XYZ
        def f(t):
            return t**(1/2.4) if t > 0.04045 else t/12.92
        r, g, b = f(r), f(g), f(b)
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        # XYZ to LAB
        def lab_f(t):
            return t**(1/3) if t > 0.008856 else (7.787 * t + 16/116)
        fx, fy, fz = lab_f(x/0.95047), lab_f(y), lab_f(z/1.08883)
        l = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)
        return l, a, b
    
    lab1 = rgb_to_lab(rgb1)
    lab2 = rgb_to_lab(rgb2)
    
    return ((lab1[0] - lab2[0])**2 + (lab1[1] - lab2[1])**2 + (lab1[2] - lab2[2])**2)**0.5

def find_closest_khavar_color(target_color: str) -> str:
    """Find the closest Khavar color to the target color"""
    min_distance = float('inf')
    closest_color = KHAVAR_PALETTE["text"]  # Default fallback
    
    for khavar_color in KHAVAR_PALETTE.values():
        distance = color_distance(target_color, khavar_color)
        if distance < min_distance:
            min_distance = distance
            closest_color = khavar_color
    
    return closest_color

def map_catppuccin_to_khavar(catppuccin_color: str, theme: str = "dark") -> str:
    """Map a Catppuccin color to the appropriate Khavar color"""
    catppuccin_map = CATPPUCCIN_DARK if theme == "dark" else CATPPUCCIN_LIGHT
    
    # Direct mapping if color exists in our predefined mappings
    if catppuccin_color.lower() in catppuccin_map:
        khavar_name = catppuccin_map[catppuccin_color.lower()]
        return KHAVAR_PALETTE[khavar_name]
    
    # For colors not in our mapping, try to categorize by brightness and hue
    rgb = hex_to_rgb(catppuccin_color)
    brightness = sum(rgb) / 3
    
    # Preserve background hierarchy - don't map backgrounds to text colors
    if brightness < 50:  # Very dark colors stay as dark backgrounds
        return KHAVAR_PALETTE["base"]
    elif brightness < 80:  # Dark colors become surface
        return KHAVAR_PALETTE["surface"] 
    elif brightness < 120:  # Medium-dark colors become overlay
        return KHAVAR_PALETTE["overlay"]
    elif brightness > 200:  # Very bright colors become text
        return KHAVAR_PALETTE["text"]
    elif brightness > 150:  # Bright colors become subtle
        return KHAVAR_PALETTE["subtle"]
    else:  # Medium colors become muted
        return KHAVAR_PALETTE["muted"]

def convert_css_colors(css_content: str) -> str:
    """Convert all Catppuccin colors in CSS to Khavar colors"""
    # Regex pattern to match hex colors
    hex_pattern = r'#[0-9a-fA-F]{6}'
    
    def replace_color(match):
        original_color = match.group(0)
        
        # Determine theme based on the color (rough heuristic)
        rgb = hex_to_rgb(original_color)
        brightness = sum(rgb) / 3
        theme = "dark" if brightness < 128 else "light"
        
        # Map to Khavar color
        new_color = map_catppuccin_to_khavar(original_color, theme)
        
        return new_color
    
    # Replace all hex colors
    converted_css = re.sub(hex_pattern, replace_color, css_content)
    
    # Also handle rgba patterns
    rgba_pattern = r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)'
    
    def replace_rgba(match):
        r, g, b, a = match.groups()
        original_hex = rgb_to_hex((int(r), int(g), int(b)))
        
        # Determine theme
        brightness = (int(r) + int(g) + int(b)) / 3
        theme = "dark" if brightness < 128 else "light"
        
        # Map to Khavar color
        new_hex = map_catppuccin_to_khavar(original_hex, theme)
        new_rgb = hex_to_rgb(new_hex)
        
        return f"rgba({new_rgb[0]}, {new_rgb[1]}, {new_rgb[2]}, {a})"
    
    converted_css = re.sub(rgba_pattern, replace_rgba, converted_css)
    
    return converted_css

def main():
    """Main function to convert the theme"""
    # Read the input CSS file
    try:
        with open('discord.user.less', 'r', encoding='utf-8') as f:
            css_content = f.read()
    except FileNotFoundError:
        print("Error: discord.user.less file not found!")
        print("Please make sure the file is in the same directory as this script.")
        return
    
    # Convert colors
    print("Converting Catppuccin colors to Khavar palette...")
    converted_css = convert_css_colors(css_content)
    
    # Replace theme name in comments and selectors
    converted_css = converted_css.replace("catppuccin", "khavar")
    converted_css = converted_css.replace("Catppuccin", "Khavar")
    
    # Add header comment
    header = """/*
 * Khavar Discord Theme
 * Converted from Catppuccin theme using custom color palette
 * 
 * Khavar Palette:
 * Base: #172620 | Surface: #21362d | Overlay: #2d493d
 * Muted: #4e7e6b | Subtle: #90bbaa | Text: #dfece7
 * Low: #39ac7e | Mid: #2d8662 | High: #206046
 * Sarnai: #f0c3cb | Anis: #ff6b6b | Chatsalgan: #e5951a
 * Els: #cca24d | Uvs: #80b946 | Nuur: #2b879e
 * Mus: #9deaea | Yargui: #d5b3e5
 */

"""
    
    converted_css = header + converted_css
    
    # Write the output file
    with open('khavar.user.less', 'w', encoding='utf-8') as f:
        f.write(converted_css)
    
    print("✅ Conversion complete!")
    print("📁 Output saved as: khavar.user.less")
    print("\n🎨 Color mappings used:")
    print("• base → base, surface0 → base")
    print("• surface1 → surface, surface2 → surface") 
    print("• overlay0 → overlay, overlay1 → overlay")
    print("• overlay2 → muted, subtext0 → muted")
    print("• subtext1 → subtle, subtext2 → subtle")
    print("• text → text")
    print("• Accent colors: pink → sarnai (main accent)")
    print("• Other colors: red → anis, orange → chatsalgan, yellow → els")
    print("• green → uvs, cyan → mus, blue → nuur, purple → yargui")

if __name__ == "__main__":
    main()
