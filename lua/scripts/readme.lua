package.path = package.path .. ";./lua/?.lua"

local color_metadata = {
	sarnai 			= { mn = "Сарнай", en = "Rose", desc = "Mountain wild flower" },
	anis   			= { mn = "Аньс", en = "Cowberry", desc = "Wild berry" },
	chatsalgan 	= { mn = "Чацаргана", en = "Hippophae", desc = "Juicy berry for syrup" },
	els    			= { mn = "Элс", en = "Sand", desc = "Gobi desert" },
	uvs    			= { mn = "Өвс", en = "Grass", desc = "Green steppes" },
	nuur   			= { mn = "Нуур", en = "Lake", desc = "Lake Hovsgol" },
	mus    			= { mn = "Мөс", en = "Ice", desc = "Snow on frozen lake" },
	yargui 			= { mn = "Яргуй", en = "Pasqueflower", desc = "Flower blooming at spring's dawn" },
}

local function hex_to_rgb(hex)
	hex = hex:gsub("#", "")
	return string.format("rgb(%d, %d, %d)",
		tonumber(hex:sub(1, 2), 16),
		tonumber(hex:sub(3, 4), 16),
		tonumber(hex:sub(5, 6), 16)
	)
end

local function generate_color_row(style, palette_name, color)
	local meta = color_metadata[color] or {}
	local hex = style[color]
	local color_name = color
	palette_name = string.lower(palette_name)

	local row = string.format([[
  <tr>
    <td><img src="assets/swatches/%s_%s.png" width="23" style="border-radius:4px"></td>
    <td>%s</td>
    <td><code>%s</code></td>
    <td><code>%s</code></td>]],
		palette_name, color, color_name, hex, hex_to_rgb(hex)
	)

	row = row .. "\n"

	if meta.mn then
		row = row .. string.format([[
    <td>%s (%s)</td>
    <td>%s</td>]],
			meta.mn, meta.en, meta.desc
		)
	else
		row = row .. [[
    <td></td>
    <td></td>]]
	end

	return row .. "\n  </tr>"
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

	for _, color in ipairs(order) do
		if palette[color] then
			table.insert(rows, generate_color_row(palette, name, color))
		end
	end

	return string.format([[
<details>
<summary>%s (%s) - %s</summary>
<table>
%s
</table>
</details>]],
		mn_title, name, en_title, table.concat(rows, "\n"))
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
