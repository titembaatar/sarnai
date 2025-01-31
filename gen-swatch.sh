#!/bin/bash
mkdir -p assets/swatches

# Dark main (shono)
dark_main=(
  "#0d1615:shono_base" "#1a2328:shono_surface" "#2a363c:shono_overlay"
  "#7c9b8e:shono_muted" "#a3aeb5:shono_subtle" "#d8e1e5:shono_text"
  "#c7958d:shono_pink" "#9d4a40:shono_red" "#b0a87a:shono_yellow" "#4a7d6a:shono_green" "#5a9b9e:shono_teal" "#6d8dad:shono_blue"
  "#1a2328:shono_low" "#2a363c:shono_mid" "#4a555c:shono_high"
)

# Dark bright (udesh)
dark_bright=(
  "#1a2328:udesh_base" "#2a363c:udesh_surface" "#4a555c:udesh_overlay" 
  "#8caa9e:udesh_muted" "#c8c194:udesh_subtle" "#e0e7eb:udesh_text"
  "#e0aeaa:udesh_pink" "#c76a5d:udesh_red" "#d8d0a0:udesh_yellow" "#689f8e:udesh_green" "#7dbfc5:udesh_teal" "#8fb3d9:udesh_blue"
  "#2a363c:udesh_low" "#4a555c:udesh_mid" "#6d8dad:udesh_high"
)

# light (ogloo)
light=(
  "#f0f5eb:ogloo_base" "#e0e7eb:ogloo_surface" "#d8e1e5:ogloo_overlay"
  "#a3aeb5:ogloo_muted" "#7c9b8e:ogloo_subtle" "#4a555c:ogloo_text"
  "#d9a8ad:ogloo_pink" "#b56359:ogloo_red" "#c8c194:ogloo_yellow" "#7c9b8e:ogloo_green" "#5a9b9e:ogloo_teal" "#6d8dad:ogloo_blue"
  "#e0e7eb:ogloo_low" "#d8e1e5:ogloo_mid" "#a3aeb5:ogloo_high"
)

generate_swatches() {
  local theme=("$@")
  for color in "${theme[@]}"; do
    hex="${color%%:*}"
    name="${color##*:}"
    magick -size 23x23 xc:none \
      -fill "$hex" -stroke "#2a363c" -strokewidth 1 \
      -draw "roundrectangle 0,0 22,22 4,4" \
      "assets/palettes/swatches/${name}.png"
  done
}

generate_swatches "${dark_main[@]}"
generate_swatches "${dark_bright[@]}"
generate_swatches "${light[@]}"
