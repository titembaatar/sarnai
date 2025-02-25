package.path = package.path .. ";./lua/?.lua"

local khavar = require("palettes.khavar")
local ovol = require("palettes.ovol")

---@param style table Palette of style
---@param name string Name of style
local function generate_swatches(style, name)
	for color, hex in pairs(style) do
		os.execute(string.format([[
			magick -size 23x23 xc:none \
			-fill "%s" -stroke "#172820" -strokewidth 1 \
			-draw "roundrectangle 0,0 22,22 4,4" \
			"assets/swatches/%s.png"
		]], hex, name .. "_" .. color)
		)
	end
end

generate_swatches(khavar, "khavar")
generate_swatches(ovol, "ovol")
