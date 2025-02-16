package.path = package.path .. ";./lua/?.lua"

local lfs = require("lfs")

---Convert HEX to HSL
---@param hex string
---@return integer Hue
---@return integer Saturation
---@return integer Luminance
local function convert_to_hsl(hex)
	hex = hex:gsub("#", "")

	local r = tonumber(hex:sub(1, 2), 16) / 255
	local g = tonumber(hex:sub(3, 4), 16) / 255
	local b = tonumber(hex:sub(5, 6), 16) / 255

	local max = math.max(r, g, b)
	local min = math.min(r, g, b)
	local delta = max - min

	local l = (max + min) / 2

	local s = 0
	if delta ~= 0 then
		s = delta / (1 - math.abs(2 * l - 1))
	end

	local h = 0
	if delta ~= 0 then
		if max == r then
			h = (g - b) / delta
		elseif max == g then
			h = (b - r) / delta + 2
		else
			h = (r - g) / delta + 4
		end
		h = h * 60
		if h < 0 then
			h = h + 360
		end
	end

	return math.floor(h), math.floor(s * 100), math.floor(l * 100)
end

---Convert HSL to HEX
---@param h integer
---@param s integer
---@param l integer
---@return string Hex code
local function convert_to_hex(h, s, l)
	s = s / 100
	l = l / 100

	local c = (1 - math.abs(2 * l - 1)) * s
	local x = c * (1 - math.abs((h / 60) % 2 - 1))
	local m = l - c / 2

	local r, g, b
	if h < 60 then
		r, g, b = c, x, 0
	elseif h < 120 then
		r, g, b = x, c, 0
	elseif h < 180 then
		r, g, b = 0, c, x
	elseif h < 240 then
		r, g, b = 0, x, c
	elseif h < 300 then
		r, g, b = x, 0, c
	else
		r, g, b = c, 0, x
	end

	r = math.floor((r + m) * 255 + 0.5)
	g = math.floor((g + m) * 255 + 0.5)
	b = math.floor((b + m) * 255 + 0.5)

	return string.format("#%02x%02x%02x", r, g, b)
end

---Create palette for bgs, fgs and hls from base color
---@param base string Hex code of base color
---@return table, table Dark and light palettes
local function create_palette(base)
	local base_h, base_s, base_l = convert_to_hsl(base)

	local dark = {
		-- Backgrounds
		base    = base,
		surface = convert_to_hex(base_h, base_s, base_l + 6),
		overlay = convert_to_hex(base_h, base_s, base_l + 12),
		-- Foregrounds
		muted   = convert_to_hex(base_h, base_s, 40),
		subtle  = convert_to_hex(base_h, base_s, 65),
		text    = convert_to_hex(base_h, base_s, 90),
		-- Highlights
		high    = convert_to_hex(base_h, 50, 25),
		mid     = convert_to_hex(base_h, 50, 35),
		low     = convert_to_hex(base_h, 50, 45),
		-- Main colors
		sarnai  = "#f0c3cb",
		anis    = "#ff6b6b",
		els     = "#cca24d",
		nuur    = "#2b879e",
		mus     = "#9deaea",
		uvs     = "#80b946",
	}

	local light = {
		-- Backgrounds
		base    = convert_to_hex(base_h, base_s, 100 - base_l),
		surface = convert_to_hex(base_h, base_s, 100 - base_l - 12),
		overlay = convert_to_hex(base_h, base_s, 100 - base_l - 24),
		-- Foregrounds
		muted   = convert_to_hex(base_h, base_s, 60),
		subtle  = convert_to_hex(base_h, base_s, 35),
		text    = convert_to_hex(base_h, base_s, 10),
		-- Highlights
		high    = convert_to_hex(base_h, 50, 45),
		mid     = convert_to_hex(base_h, 50, 35),
		low     = convert_to_hex(base_h, 50, 25),
		-- Main colors
		sarnai  = "#b93d4d",
		anis    = "#cc2929",
		els     = "#df9b23",
		nuur    = "#0a728c",
		mus     = "#12adad",
		uvs     = "#4c890f",
	}

	return dark, light
end

--- Write palette to file
---@param filename string
---@param palette table
local function write_palette(filename, palette)
	local file = io.open(filename, "w")
	if not file then
		print("ERROR: Unable to open " .. filename)
		return
	end

	local key_order = {
		"base", "surface", "overlay",
		"muted", "subtle", "text",
		"low", "mid", "high",
		"sarnai", "anis", "els", "nuur", "mus", "uvs"
	}

	file:write("return {\n")
	for _, k in ipairs(key_order) do
		if palette[k] then
			file:write(string.format("\t%s = \"%s\",\n", k, palette[k]))
		end
	end
	file:write("}\n")
	file:close()
end

--- Create or update a palette file
---@param base string Hex code
---@param name_dark string Dark colorscheme name
---@param name_light? string Light colorscheme name
local function update_palette(base, name_dark, name_light)
	local dark, light = create_palette(base)
	local dir = "./lua/palettes/"
	local dark_file = dir .. name_dark .. ".lua"
	local light_file = dir .. name_light .. ".lua"

	if not lfs.attributes(dir, "mode") then
		lfs.mkdir(dir)
	end

	if name_light ~= nil then
		write_palette(light_file, light)
		print("Palette generated: " .. light_file)
	end

	write_palette(dark_file, dark)
	print("Palette generated: " .. dark_file)
end

---Main exec
local args = { ... }
if #args < 3 then
	print("Usage: lua scripts/palette.lua <hex_color> <name-dark> <name-light>")
	os.exit(1)
end

local hex = args[1]
local name_dark = args[2]
local name_light = args[3]
if name_light ~= nil then
	update_palette(hex, name_dark, name_light)
else
	update_palette(hex, name_dark)
end
