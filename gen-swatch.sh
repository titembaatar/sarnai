#!/bin/bash
mkdir -p assets/swatches

# Dark Main (Shönö)
dark_main=(
  "#0d1615:Shönö_Base" "#1a2328:Shönö_Surface" "#2a363c:Shönö_Overlay"
  "#7c9b8e:Shönö_Muted" "#a3aeb5:Shönö_Subtle" "#d8e1e5:Shönö_Text"
  "#c7958d:Shönö_Pink" "#9d4a40:Shönö_Red" "#b0a87a:Shönö_Yellow" "#4a7d6a:Shönö_Green" "#5a9b9e:Shönö_Teal" "#6d8dad:Shönö_Blue"
  "#1a2328:Shönö_Low" "#2a363c:Shönö_Mid" "#4a555c:Shönö_High"
)

# Dark Bright (Üdesh)
dark_bright=(
  "#1a2328:Üdesh_Base" "#2a363c:Üdesh_Surface" "#4a555c:Üdesh_Overlay" 
  "#8caa9e:Üdesh_Muted" "#c8c194:Üdesh_Subtle" "#e0e7eb:Üdesh_Text"
  "#e0aeaa:Üdesh_Pink" "#c76a5d:Üdesh_Red" "#d8d0a0:Üdesh_Yellow" "#689f8e:Üdesh_Green" "#7dbfc5:Üdesh_Teal" "#8fb3d9:Üdesh_Blue"
  "#2a363c:Üdesh_Low" "#4a555c:Üdesh_Mid" "#6d8dad:Üdesh_High"
)

# Light (Öglöö)
light=(
  "#f0f5eb:Öglöö_Base" "#e0e7eb:Öglöö_Surface" "#d8e1e5:Öglöö_Overlay"
  "#a3aeb5:Öglöö_Muted" "#7c9b8e:Öglöö_Subtle" "#4a555c:Öglöö_Text"
  "#d9a8ad:Öglöö_Pink" "#b56359:Öglöö_Red" "#c8c194:Öglöö_Yellow" "#7c9b8e:Öglöö_Green" "#5a9b9e:Öglöö_Teal" "#6d8dad:Öglöö_Blue"
  "#e0e7eb:Öglöö_Low" "#d8e1e5:Öglöö_Mid" "#a3aeb5:Öglöö_High"
)

generate_swatches() {
  local theme=("$@")
  for color in "${theme[@]}"; do
    hex="${color%%:*}"
    name="${color##*:}"
    magick -size 23x23 xc:none \
      -fill "$hex" -stroke "#2a363c" -strokewidth 1 \
      -draw "roundrectangle 0,0 22,22 4,4" \
      "assets/swatches/${name}.png"
  done
}

generate_swatches "${dark_main[@]}"
generate_swatches "${dark_bright[@]}"
generate_swatches "${light[@]}"
