import json
import re
from pathlib import Path
from typing import List

from DataTypes import Item, ItemType

LOC_PATH_GC = "data/citadel_gc_english.txt"
LOC_PATH_MODS = "data/citadel_mods_english.txt"
ITEMS_VDATA_PATH = "data/vdata/abilities.vdata.json"
STRINGMAP_PATH = "data/stringmap.json"

# 加载 JSON 数据
ITEMS_VDATA = json.loads(Path(ITEMS_VDATA_PATH).read_text())

def extract_id_by_name(name: str) -> str:
    json_map = json.loads(Path(STRINGMAP_PATH).read_text())
    for id, str_name in json_map.items():
        if str_name == name:
            return id
    return "0"

def extract_localization_item(item: str) -> str:
    with open(f"./{LOC_PATH_GC}", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if item in line:
                parts = line.strip().split("\"") 
                parts = list(filter(lambda x: x.strip() != "", parts))
                return parts[1]
    return "未找到道具"

def extract_localization_mods(item: str) -> str:
    with open(f"./{LOC_PATH_MODS}", "r", encoding="utf-8") as f:
        content = f.read()
        # 使用更精确的正则表达式来匹配整个行，并处理可能的转义引号
        pattern = rf'"{re.escape(item)}"\s*"((?:[^"\\]|\\.)*)"'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            description = match.group(1)
            # 去除所有 HTML 标签
            description = re.sub(r'<[^>]+>', '', description)
            # 替换转义字符
            description = description.replace('\\"', '"').replace('\\n', '\n').strip()
            return description
    return "未找到相关描述"

def _replace_variables(desc, item_name):
    def replace_match(match):
        key = match.group(1)
        value = get_variable_value(item_name, key)
        return value if value else match.group(0)  # 如果没有找到值，保留原始占位符

    formatted_desc = re.sub(r'\{s:(.*?)\}', replace_match, desc)
    return formatted_desc

# 找vdata中的变量值
def get_variable_value(item_name, variable_name):
    item_data = ITEMS_VDATA["Root"].get(item_name, {})
    if isinstance(item_data, dict):
        ability_properties = item_data.get("m_mapAbilityProperties", {})
        if variable_name in ability_properties:
            return ability_properties[variable_name].get("m_strValue", "???")
    return "???"


def create_items_json():
    items_vdata = json.loads(Path("data/vdata/abilities.vdata.json").read_text())
    items: List[Item] = []
    
    for item in ITEMS_VDATA["Root"]:
        item_data = ITEMS_VDATA["Root"][item]
        if "m_eItemSlotType" in item_data:
            item_type = item_data["m_eItemSlotType"]
            match item_type:
                case "EItemSlotType_Armor":
                    item_type = ItemType.ARMOR
                case "EItemSlotType_WeaponMod":
                    item_type = ItemType.WEAPON
                case "EItemSlotType_Tech":
                    item_type = ItemType.TECH
                case _: 
                    item_type = ItemType.TECH
            item_tier = int(item_data["m_iItemTier"].replace("EModTier_", "")) if "m_iItemTier" in item_data else 0
            item_image = ""
            if "m_strAbilityImage" in item_data:
                item_image = item_data["m_strAbilityImage"]
                item_image = item_image.replace("file://{images}/upgrades/", "items/")
                item_image = item_image.replace("file://{images}/hud/abilities/", "abilities/")
                item_image = item_image.replace(".psd", ".png")

            description = extract_localization_mods(item + "_desc")
            formatted_description = _replace_variables(description, item)

            items.append({
                "id": int(extract_id_by_name(item)),
                "name": item,
                "localization": extract_localization_item(item),
                "description": formatted_description,
                "tier": item_tier,
                "type": item_type,
                'image': item_image,
            })
    
    Path("data/items.json").write_text(json.dumps(items, ensure_ascii=False, indent=4), encoding="utf-8")