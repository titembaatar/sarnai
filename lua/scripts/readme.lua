package.path = package.path .. ";./lua/?.lua"

local color_metadata = {
	sarnai     = { mn = "Сарнай", en = "Rose", desc = "Mountain wild flower" },
	anis       = { mn = "Аньс", en = "Cowberry", desc = "Wild berry" },
	chatsalgan = { mn = "Чацаргана", en = "Hippophae", desc = "Juicy berry for syrup" },
	els        = { mn = "Элс", en = "Sand", desc = "Gobi desert" },
	uvs        = { mn = "Өвс", en = "Grass", desc = "Green steppes" },
	nuur       = { mn = "Нуур", en = "Lake", desc = "Lake Hovsgol" },
	mus        = { mn = "Мөс", en = "Ice", desc = "Snow on frozen lake" },
	yargui     = { mn = "Яргуй", en = "Pasqueflower", desc = "Flower blooming at spring's dawn" },
}

local function hex_to_rgb(hex)
	hex = hex:gsub("#", "")
	return string.format("rgb(%d, %d, %d)",
		tonumber(hex:sub(1, 2), 16),
		tonumber(hex:sub(3, 4), 16),
		tonumber(hex:sub(5, 6), 16)
	)
end

-- New function to convert hex to HSL
local function hex_to_hsl(hex)
	hex = hex:gsub("#", "")
	local r = tonumber(hex:sub(1, 2), 16) / 255
	local g = tonumber(hex:sub(3, 4), 16) / 255
	local b = tonumber(hex:sub(5, 6), 16) / 255

	local max = math.max(r, g, b)
	local min = math.min(r, g, b)
	local h, s, l

	l = (max + min) / 2

	if max == min then
		h = 0
		s = 0
	else
		local d = max - min
		s = l > 0.5 and d / (2 - max - min) or d / (max + min)

		if max == r then
			h = (g - b) / d + (g < b and 6 or 0)
		elseif max == g then
			h = (b - r) / d + 2
		else
			h = (r - g) / d + 4
		end

		h = h / 6
	end

	h = math.floor(h * 360)
	s = math.floor(s * 100)
	l = math.floor(l * 100)

	return string.format("hsl(%d, %d%%, %d%%)", h, s, l)
end

local function generate_color_row(style, palette_name, color)
	local meta = color_metadata[color] or {}
	local hex = style[color]
	local color_name = color
	palette_name = string.lower(palette_name)

	-- Format the color names as requested
	local name_column = color_name
	if meta.mn and meta.en then
		name_column = string.format("%s<br>%s<br>%s", color_name, meta.mn, meta.en)
	end

	local row = string.format([[
  <tr>
    <td><img src="assets/swatches/%s_%s.png" width="23" style="border-radius:4px"></td>
    <td>%s</td>
    <td><code>%s</code></td>
    <td><code>%s</code></td>
  </tr>]],
		palette_name, color, name_column, hex, hex_to_hsl(hex)
	)

	return row
end

local function generate_palette_section(palette, name, mn_title, en_title)
	local rows = {}
	local order = {
		"base", "surface", "overlay",
		"muted", "subtle", "text",
		"low", "mid", "high",
		"sarnai", "anis", "chatsalgan",
		"els", "uvs", "nuur",
		"mus", "yargui"
	}

	-- Generate table header
	local header = [[
<table>
  <tr>
    <th>Swatch</th>
    <th>Name</th>
    <th>Hex</th>
    <th>HSL</th>
  </tr>]]

	for _, color in ipairs(order) do
		if palette[color] then
			table.insert(rows, generate_color_row(palette, name, color))
		end
	end

	return string.format([[
<details>
<summary>%s (%s) - %s</summary>
%s
%s
</table>
</details>]],
		mn_title, name, en_title, header, table.concat(rows, "\n"))
end

local function update_readme()
	local readme_path = "./README.md"
	local readme = io.open(readme_path, "r")
	if not readme then return false end

	local content = readme:read("*all")
	readme:close()

	-- Generate palette sections
	local palettes = {
		{ key = "khavar", mn = "🌸 Хавар", en = "Spring" },
		{ key = "ovol", mn = "❄️ Өвөл", en = "Winter" }
	}
	local sections = {}

	for _, palette in ipairs(palettes) do
		local data = require("palettes." .. palette.key)
		table.insert(sections, generate_palette_section(
			data,
			palette.key:gsub("^%l", string.upper),
			palette.mn,
			palette.en
		))
	end

	-- Find the start and end positions of the section
	local start_pos, end_pos = content:find("## 🎨 Palette.-\n%-%-%-")

	if start_pos and end_pos then
		-- Create new content
		local header = "## 🎨 Palette\n"
		local images = [[<p align="center">
  <img src="assets/palettes/khavar.png" style="width: 33%">
  <img src="assets/palettes/ovol.png" style="width: 33%">
</p>

]]
		local sections_text = table.concat(sections, "\n\n")
		local footer = "\n\n---"

		-- Combine new content
		local new_content = header .. images .. sections_text .. footer

		-- Replace the section
		local updated_content = content:sub(1, start_pos - 1) .. new_content .. content:sub(end_pos + 1)

		-- Write back to file
		readme = io.open(readme_path, "w")
		if not readme then return false end

		readme:write(updated_content)
		readme:close()

		return true
	end

	return false
end

update_readme()

