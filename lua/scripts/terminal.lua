package.path = package.path .. ";./lua/?.lua"

local function adjust_color(hex, factor)
	hex = hex:gsub("#", "")
	local r = tonumber(hex:sub(1, 2), 16)
	local g = tonumber(hex:sub(3, 4), 16)
	local b = tonumber(hex:sub(5, 6), 16)

	r = math.floor(math.min(r * factor, 255) + 0.5)
	g = math.floor(math.min(g * factor, 255) + 0.5)
	b = math.floor(math.min(b * factor, 255) + 0.5)

	return string.format("#%02x%02x%02x", r, g, b)
end

local function generate_kitty_config(colors, name)
	local lines = {
		string.format("foreground     %s", colors[7]),
		string.format("background     %s", colors[0]),
		string.format("cursor         %s", colors[7]),
		""
	}
	for i = 0, 15 do
		table.insert(lines, string.format("color%d         %s", i, colors[i]))
	end
	return table.concat(lines, "\n")
end

local function generate_alacritty_config(colors, name)
	return string.format([[
[colors]
primary.background = "%s"
primary.foreground = "%s"
cursor.text = "%s"
cursor.cursor = "%s"

[colors.normal]
black = "%s"
red = "%s"
green = "%s"
yellow = "%s"
blue = "%s"
magenta = "%s"
cyan = "%s"
white = "%s"

[colors.bright]
black = "%s"
red = "%s"
green = "%s"
yellow = "%s"
blue = "%s"
magenta = "%s"
cyan = "%s"
white = "%s"
]],
		colors[0], colors[7], colors[0], colors[7],
		colors[0], colors[1], colors[2], colors[3],
		colors[4], colors[5], colors[6], colors[7],
		colors[8], colors[9], colors[10], colors[11],
		colors[12], colors[13], colors[14], colors[15])
end

local function generate_ghostty_config(colors, name)
	local lines = {}
	for i = 0, 15 do
		table.insert(lines, string.format("palette = %d=%s", i, colors[i]))
	end
	table.insert(lines, string.format("\nbackground = %s", colors[0]))
	table.insert(lines, string.format("foreground = %s", colors[7]))
	table.insert(lines, string.format("cursor-color = %s", colors[7]))
	table.insert(lines, string.format("cursor-text = %s", colors[0]))
	return table.concat(lines, "\n")
end

local function generate_terminal_configs(style, name)
	local colors = {
		[0] = style.base,
		[1] = style.anis,
		[2] = style.uvs,
		[3] = style.els,
		[4] = style.mus,
		[5] = style.sarnai,
		[6] = style.nuur,
		[7] = style.text
	}

	local factor = (name == "ogloo") and 0.9 or 1.1
	for i = 0, 7 do
		colors[i + 8] = adjust_color(colors[i], factor)
	end

	local base_path = "terminals/"
	local formats = {
		["kitty"]     = { generate_kitty_config, "conf" },
		["alacritty"] = { generate_alacritty_config, "toml" },
		["ghostty"]   = { generate_ghostty_config, "" }
	}

	for term, data in pairs(formats) do
		local generator, ext = table.unpack(data)
		local ext_part = (ext ~= "") and ("." .. ext) or ""
		local path = string.format("%s%s/sarnai-%s%s",
			base_path, term, name, ext_part)
		local file = io.open(path, "w")
		if file then
			file:write(generator(colors, name))
			file:close()
		end
	end
end

local palettes = {
	khavar = require("palettes.khavar"),
	ovol = require("palettes.ovol"),
}

for name, palette in pairs(palettes) do
	generate_terminal_configs(palette, name)
end
