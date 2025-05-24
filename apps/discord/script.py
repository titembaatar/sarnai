import re
import os
import textwrap

# --- Configuration ---

INPUT_CSS_FILE = 'discord.css'
OUTPUT_CSS_FILE = 'discord_themed.css'

# Your color scheme
dark_theme = {
    "base": "#172620", "surface": "#21362d", "overlay": "#2d493d",
    "muted": "#4e7e6b", "subtle": "#90bbaa", "text": "#dfece7",
    "pink": "#f0c3cb", "red": "#ff6b6b", "orange": "#e5951a",
    "yellow": "#cca24d", "green": "#80b946", "dark_blue": "#2b879e",
    "light_blue": "#9deaea", "purple": "#d5b3e5"
}

light_theme = {
    "base": "#dceae4", "surface": "#b6d2c7", "overlay": "#90bbaa",
    "muted": "#81b19e", "subtle": "#446f5e", "text": "#13201b",
    "pink": "#b93d4d", "red": "#cc2929", "orange": "#da730c",
    "yellow": "#df9b23", "green": "#4c890f", "dark_blue": "#0a728c",
    "light_blue": "#12adad", "purple": "#a353c6"
}

# --- Helper Functions ---
def hex_to_rgb(hex_color):
    """Converts a hex color string (e.g., #ffffff) to an RGB tuple (e.g., (255, 255, 255))."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color format: {hex_color}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_fecolormatrix_values(hex_color):
    """Creates the feColorMatrix 'values' string for forcing a specific color."""
    rgb = hex_to_rgb(hex_color)
    # Normalize RGB values to 0.0 - 1.0
    r_norm, g_norm, b_norm = [round(x / 255.0, 10) for x in rgb] # Increase precision
    # Format the matrix values string
    matrix_values = f"""
    0 0 0 0 {r_norm}
    0 0 0 0 {g_norm}
    0 0 0 0 {b_norm}
    0 0 0 1 0
    """.strip()
    # Clean up extra whitespace to create a consistent key format
    return re.sub(r'\s+', ' ', matrix_values)


# --- Mappings (Source Color -> Target Theme Color Name) ---
# Using Mocha and Latte as base assumptions

# Hex Mappings
hex_mappings_dark = {
    # Base Tones
    "#1e1e2e": "base", "#181825": "base", "#11111b": "base",
    "#1c1c2b": "base", # Mocha Mantle/background-base-low
    "#313244": "surface", "#45475a": "surface", "#585b70": "muted",
    "#6c7086": "subtle", # Corrected: Overlay0 -> Subtle (for --interactive-muted)
    "#7f849c": "overlay", "#9399b2": "overlay",
    # Text Tones
    "#cdd6f4": "text", "#bac2de": "subtle", "#a6adc8": "subtle",
    # Icon/Channel Colors
    "#969ebe": "pink", # Corrected: Default icon/channel color -> Pink
    # Accent Colors (Original Catppuccin)
    "#f5e0dc": "pink", "#f2cdcd": "pink", "#f5c2e7": "pink",
    "#f38ba8": "red", "#eba0ac": "orange", "#fab387": "orange",
    "#f9e2af": "yellow", "#a6e3a1": "green", "#94e2d5": "light_blue",
    "#89dceb": "light_blue",
    "#74c7ec": "pink", # Original Sapphire -> Pink
    "#89b4fa": "pink", # Original Blue -> Pink
    "#cba6f7": "purple", "#b4befe": "purple", # Original Mauve/Lavender
    # Specific Hardcoded Values & Remaining Blues/Purples -> Pink
    "#ebf2fe": "text", # Used in SVG backgrounds
    "#bad3fc": "subtle", # Used in SVG backgrounds
    "#b077f3": "purple", # Twitch/Premium Purple -> Your Purple
    "#07070b": "base", # Dark input border hover
    "#71a4f9": "pink", # brand-530, button outline active bg
    "#5895f8": "pink", # brand-560, premium-perk-dark-blue, playstation
    "#4085f7": "pink", # brand-600
    "#2776f6": "pink", # brand-630
    "#0f66f5": "pink", # brand-660
    "#0a5be0": "pink", # brand-700
    "#0956d4": "pink", # brand-730
    "#0851c8": "pink", # brand-760
    "#084cbc": "pink", # brand-800
    "#0747b0": "pink", # brand-830
    "#0742a3": "pink", # brand-860
    "#063d97": "pink", # brand-900
    "#a1c4fb": "pink", # premium-perk-light-blue
    "#7dacf9": "pink", # button outline hover bg/border
    "#649df8": "pink", # button filled hover
    "#4c8df7": "pink", # button filled active
    "#aebced": "pink", # button filled inverted hover
    "#99abe9": "pink", # button filled inverted active
    "#525569": "pink", # button outline primary hover bg/border
    "#4d4f62": "pink", # button outline primary active bg/border
    "#3a3c4c": "pink", # button secondary hover/active
    "#63677e": "overlay", # __spoiler-warning-background-color
}
hex_mappings_light = {
    # Base Tones
    "#eff1f5": "base", "#e6e9ef": "base", "#dce0e8": "base",
    "#eceef3": "base", # Latte Mantle/background-base-low
    "#ccd0da": "surface", "#bcc0cc": "surface", "#acb0be": "muted",
    "#9ca0b0": "subtle", # Corrected: Overlay0 -> Subtle (for --interactive-muted)
    "#8c8fa1": "overlay", "#7c7f93": "overlay",
    # Text Tones
    "#4c4f69": "text", "#5c5f77": "subtle", "#6c6f85": "subtle",
    # Icon/Channel Colors
    "#616377": "pink", # Corrected: Default icon/channel color -> Pink
    # Accent Colors (Original Catppuccin)
    "#dc8a78": "pink", "#dd7878": "pink", "#ea76cb": "pink",
    "#d20f39": "red", "#e64553": "orange", "#fe640b": "orange",
    "#df8e1d": "yellow", "#40a02b": "green", "#179299": "light_blue",
    "#04a5e5": "light_blue",
    "#209fb5": "dark_blue", # Original Sapphire -> Your Dark Blue
    "#1e66f5": "dark_blue", # Original Blue -> Your Dark Blue
    "#8839ef": "purple", "#7287fd": "purple", # Original Mauve/Lavender
    # Specific Hardcoded Values & Remaining Blues/Purples -> Your Dark Blue
    "#fafbff": "base", "#eef3fe": "base", "#e1ebfe": "base",
    "#d5e3fd": "base", "#c9dafd": "base", "#bdd2fc": "base",
    "#b0cafc": "base",
    "#98b9fa": "dark_blue", # brand-330
    "#80a8f9": "dark_blue", # brand-360
    "#6798f8": "dark_blue", # brand-400
    "#4f87f7": "dark_blue", # brand-430
    "#3677f6": "dark_blue", # brand-460, premium-perk-light-blue
    "#0b57ef": "dark_blue", # brand-530, button outline active bg
    "#0a4ed6": "dark_blue", # brand-560, premium-perk-dark-blue, playstation
    "#0845be": "dark_blue", # brand-600
    "#073ca6": "dark_blue", # brand-630
    "#06338d": "dark_blue", # brand-660
    "#052b75": "dark_blue", # brand-700
    "#052669": "dark_blue", # brand-730
    "#04225c": "dark_blue", # brand-760
    "#041d50": "dark_blue", # brand-800
    "#031944": "dark_blue", # brand-830
    "#021438": "dark_blue", # brand-860
    "#02102c": "dark_blue", # brand-900
    "#6d12e3": "purple", # Twitch/Premium Purple -> Your Purple
    "#cdd2de": "surface", # Light input border hover
    "#125ef4": "dark_blue", # button outline hover bg/border
    "#0a53e3": "dark_blue", # button filled hover
    "#094aca": "dark_blue", # button filled active
    "#3c3e53": "dark_blue", # button filled inverted hover (mapping to dark blue for contrast)
    "#313344": "dark_blue", # button filled inverted active (mapping to dark blue for contrast)
    "#a5a9b8": "dark_blue", # button outline primary hover bg/border (mapping to dark blue for contrast)
    "#9ea2b3": "dark_blue", # button outline primary active bg/border (mapping to dark blue for contrast)
    "#aeb2c1": "dark_blue", # button secondary hover/active (mapping to dark blue for contrast)
    "#babec9": "overlay", # __spoiler-warning-background-color
}

# RGB Mappings
rgb_mappings = {
    (202, 150, 84): "yellow", (216, 58, 66): "red", (67, 162, 90): "green",
    (130, 131, 139): "overlay", (145, 71, 255): "purple",
}

# SVG Fill Mappings
svg_fill_mappings = {
    "#ca9654": "yellow", "#f9e2af": "yellow", "#df8e1d": "yellow",
    "#d83a42": "red", "#f38ba8": "red", "#d20f39": "red",
    "#43a25a": "green", "#a6e3a1": "green", "#40a02b": "green",
    "#82838b": "overlay", "#11111b": "base", "#dce0e8": "base",
    "#9147ff": "purple",
    "#89b4fa": "pink",       # SVG Icon Fill (Mocha Blue) -> Dark Pink
    "#1e66f5": "dark_blue", # SVG Icon Fill (Latte Blue) -> Light Dark Blue
}

# RGBA Mappings
rgba_mappings = {
    # Dark Theme Sources -> Target Name
    (137, 180, 250): "pink", # Mocha Blue -> Dark Pink
    (166, 227, 161): "green",
    (243, 139, 168): "red",
    (249, 226, 175): "yellow",
    (137, 220, 235): "light_blue",
    (147, 153, 178): "subtle",
    (108, 112, 134): "muted",
    (205, 214, 244): "text",
    (17, 17, 27):    "base",
    (245, 224, 220): "pink",
    (88, 91, 112):   "muted",
    (49, 50, 68):    "surface",
    (69, 71, 90):    "subtle", # Corrected: Overlay0 -> Subtle (for --interactive-muted rgba)
    # Light Theme Sources -> Target Name
    (30, 102, 245):  "dark_blue", # Latte Blue -> Light Dark Blue
    (64, 160, 43):   "green",
    (210, 15, 57):   "red",
    (223, 142, 29):  "yellow",
    (4, 165, 229):   "light_blue",
    (124, 127, 147): "subtle",
    (156, 160, 176): "muted",
    (76, 79, 105):   "text",
    (220, 224, 232): "base",
    (220, 138, 120): "pink",
    (172, 176, 190): "muted",
    (204, 208, 218): "surface",
    (188, 192, 204): "surface",
}

# FeColorMatrix Mappings - Keys now use higher precision matching the generator
fe_matrix_mappings = {
    # Dark Theme Originals -> Target Name
    "0 0 0 0 0.6509803922 0 0 0 0 0.8901960784 0 0 0 0 0.631372549 0 0 0 1 0": "purple", # Filter 1 & 4 (Mocha Blue/Lavender -> Purple)
    "0 0 0 0 0.6509803922 0 0 0 0 0.6784313725 0 0 0 0 0.7843137255 0 0 0 1 0": "subtle", # Filter 2 (Mocha Subtext0 -> Subtle)
    "0 0 0 0 0.9529411765 0 0 0 0 0.5450980392 0 0 0 0 0.6588235294 0 0 0 1 0": "red",    # Filter 3 (Mocha Red -> Red)
    "0 0 0 0 0.0666666667 0 0 0 0 0.0666666667 0 0 0 0 0.1058823529 0 0 0 1 0": "base",   # Filter 5 (Mocha Crust -> Base)
    # Light Theme Originals -> Target Name
    "0 0 0 0 0.2509803922 0 0 0 0 0.6274509804 0 0 0 0 0.168627451 0 0 0 1 0": "green",  # Filter 1 & 4 (Latte Green -> Green)
    "0 0 0 0 0.4235294118 0 0 0 0 0.4352941176 0 0 0 0 0.5215686275 0 0 0 1 0": "subtle", # Filter 2 (Latte Subtext0 -> Subtle)
    "0 0 0 0 0.8235294118 0 0 0 0 0.0588235294 0 0 0 0 0.2235294118 0 0 0 1 0": "red",    # Filter 3 (Latte Red -> Red)
    "0 0 0 0 0.862745098 0 0 0 0 0.8784313725 0 0 0 0 0.9098039216 0 0 0 1 0": "base",   # Filter 5 (Latte Base/Mantle -> Base)
}

# Pre-calculate target matrix values
target_fe_matrices_dark = {name: create_fecolormatrix_values(hex_val) for name, hex_val in dark_theme.items()}
target_fe_matrices_light = {name: create_fecolormatrix_values(hex_val) for name, hex_val in light_theme.items()}
all_target_matrix_values = set(target_fe_matrices_dark.values()) | set(target_fe_matrices_light.values())

# --- Processing ---

def replace_colors(css_content):
    """Performs all color replacements on the CSS content."""
    output_parts = []
    last_index = 0
    theme_block_pattern = re.compile(r'((?:\.theme-dark|\.theme-light)[^{]*\{[^}]*\})', re.IGNORECASE | re.DOTALL)

    for match in theme_block_pattern.finditer(css_content):
        start, end = match.span()
        output_parts.append(css_content[last_index:start])
        
        original_block = match.group(1)
        block = original_block
        is_dark = bool(re.search(r'\.theme-dark', block, re.IGNORECASE))
        theme_map = dark_theme if is_dark else light_theme
        hex_mappings = hex_mappings_dark if is_dark else hex_mappings_light
        target_fe_matrices = target_fe_matrices_dark if is_dark else target_fe_matrices_light

        # Apply hex mappings
        for source_hex, target_name in hex_mappings.items():
            if target_name in theme_map:
                block = re.sub(re.escape(source_hex), theme_map[target_name], block, flags=re.IGNORECASE)
            
        # Apply RGB mappings
        for source_rgb, target_name in rgb_mappings.items():
             if target_name in theme_map:
                 target_hex = theme_map[target_name]
                 rgb_str_pattern = r'rgb\(\s*' + r'\s*,\s*'.join(map(str, source_rgb)) + r'\s*\)'
                 block = re.sub(rgb_str_pattern, target_hex, block, flags=re.IGNORECASE)

        # Apply SVG fill mappings
        for source_hex, target_name in svg_fill_mappings.items():
            if target_name in theme_map:
                target_hex = theme_map[target_name]
                fill_pattern = r'fill="' + re.escape(source_hex) + r'"'
                block = re.sub(fill_pattern, f'fill="{target_hex}"', block, flags=re.IGNORECASE)
                encoded_source = source_hex.replace("#", "%23")
                encoded_target = target_hex.replace("#", "%23")
                fill_encoded_pattern = r"fill='" + re.escape(encoded_source) + r"'"
                block = re.sub(fill_encoded_pattern, f"fill='{encoded_target}'", block, flags=re.IGNORECASE)

        # Apply RGBA mappings
        for source_rgb, target_name in rgba_mappings.items():
            if target_name in theme_map:
                target_rgb = hex_to_rgb(theme_map[target_name])
                rgba_pattern = re.compile(
                    r'rgba\(\s*' + r'\s*,\s*'.join(map(str, source_rgb)) + r'\s*,\s*([0-9.]+)\s*\)',
                    re.IGNORECASE
                )
                def replace_rgba(rgba_match):
                    alpha = rgba_match.group(1)
                    return f'rgba({target_rgb[0]}, {target_rgb[1]}, {target_rgb[2]}, {alpha})'
                block = rgba_pattern.sub(replace_rgba, block)

        # Apply FeColorMatrix replacements
        fe_matrix_pattern = re.compile(r'(<feColorMatrix[^>]*values=")([^"]*)(")', re.IGNORECASE | re.DOTALL)
        def replace_fe_matrix_values(fe_match):
            prefix = fe_match.group(1)
            original_values_multiline = fe_match.group(2)
            suffix = fe_match.group(3)
            original_values_cleaned = re.sub(r'\s+', ' ', original_values_multiline.strip())
            
            if original_values_cleaned in all_target_matrix_values:
                return fe_match.group(0)

            target_name = None
            matched_key = None
            for key_matrix in fe_matrix_mappings.keys():
                 try:
                      key_nums = [float(x) for x in key_matrix.split()]
                      orig_nums = [float(x) for x in original_values_cleaned.split()]
                      if len(key_nums) == len(orig_nums) and all(abs(k - o) < 1e-6 for k, o in zip(key_nums, orig_nums)):
                           target_name = fe_matrix_mappings[key_matrix]
                           matched_key = key_matrix
                           break
                 except ValueError:
                     continue

            if target_name and target_name in target_fe_matrices:
                new_values_single_line = target_fe_matrices[target_name]
                new_values_formatted = "\n" + textwrap.indent(new_values_single_line.replace(" ", "\n    "), "        ") + "\n      "
                return prefix + new_values_formatted + suffix
            else:
                if original_values_cleaned not in all_target_matrix_values:
                     print(f"  WARNING: No mapping found for feColorMatrix values: {original_values_cleaned}")
                return fe_match.group(0)

        block = fe_matrix_pattern.sub(replace_fe_matrix_values, block)
            
        output_parts.append(block)
        last_index = end

    output_parts.append(css_content[last_index:])
    processed_css = "".join(output_parts)

    # --- Final Global Replacements (Optional) ---
    # Consider if this is needed or if block processing is sufficient

    return processed_css

# --- Main Execution ---
if __name__ == "__main__":
    if not os.path.exists(INPUT_CSS_FILE):
        print(f"Error: Input file '{INPUT_CSS_FILE}' not found.")
    else:
        print(f"Reading CSS from '{INPUT_CSS_FILE}'...")
        with open(INPUT_CSS_FILE, 'r', encoding='utf-8') as f_in:
            original_css = f_in.read()

        print("Applying color theme replacements...")
        themed_css = replace_colors(original_css)

        print(f"Writing themed CSS to '{OUTPUT_CSS_FILE}'...")
        with open(OUTPUT_CSS_FILE, 'w', encoding='utf-8') as f_out:
            f_out.write(themed_css)

        print("Done!")
