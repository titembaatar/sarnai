package.path = package.path .. ";./lua/?.lua"

local shono = require("palettes.shono")
local udesh = require("palettes.udesh")
local ogloo = require("palettes.ogloo")

---@param style table Palette of style
---@param name string Name of style
local function generate_swatches(style, name)
	for color, hex in pairs(style) do
		os.execute(string.format([[
			magick -size 23x23 xc:none \
			-fill "%s" -stroke "#0E1A16" -strokewidth 1 \
			-draw "roundrectangle 0,0 22,22 4,4" \
			"assets/swatches/%s.png"
		]], hex, name .. "_" .. color)
		)
	end
end

generate_swatches(shono, "shono")
generate_swatches(udesh, "udesh")
generate_swatches(ogloo, "ogloo")
