# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = ldtk_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, List, Any, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


class AllowedRefs(Enum):
    """Possible values: `Any`, `OnlySame`, `OnlyTags`"""
    ANY = "Any"
    ONLY_SAME = "OnlySame"
    ONLY_TAGS = "OnlyTags"


class EditorDisplayMode(Enum):
    """Possible values: `Hidden`, `ValueOnly`, `NameAndValue`, `EntityTile`, `Points`,
    `PointStar`, `PointPath`, `PointPathLoop`, `RadiusPx`, `RadiusGrid`,
    `ArrayCountWithLabel`, `ArrayCountNoLabel`, `RefLinkBetweenPivots`,
    `RefLinkBetweenCenters`
    """
    ARRAY_COUNT_NO_LABEL = "ArrayCountNoLabel"
    ARRAY_COUNT_WITH_LABEL = "ArrayCountWithLabel"
    ENTITY_TILE = "EntityTile"
    HIDDEN = "Hidden"
    NAME_AND_VALUE = "NameAndValue"
    POINTS = "Points"
    POINT_PATH = "PointPath"
    POINT_PATH_LOOP = "PointPathLoop"
    POINT_STAR = "PointStar"
    RADIUS_GRID = "RadiusGrid"
    RADIUS_PX = "RadiusPx"
    REF_LINK_BETWEEN_CENTERS = "RefLinkBetweenCenters"
    REF_LINK_BETWEEN_PIVOTS = "RefLinkBetweenPivots"
    VALUE_ONLY = "ValueOnly"


class EditorDisplayPos(Enum):
    """Possible values: `Above`, `Center`, `Beneath`"""
    ABOVE = "Above"
    BENEATH = "Beneath"
    CENTER = "Center"


class TextLanguageMode(Enum):
    LANG_C = "LangC"
    LANG_HAXE = "LangHaxe"
    LANG_JS = "LangJS"
    LANG_JSON = "LangJson"
    LANG_LOG = "LangLog"
    LANG_LUA = "LangLua"
    LANG_MARKDOWN = "LangMarkdown"
    LANG_PYTHON = "LangPython"
    LANG_RUBY = "LangRuby"
    LANG_XML = "LangXml"


class FieldDefinition:
    """This section is mostly only intended for the LDtk editor app itself. You can safely
    ignore it.
    """
    """Human readable value type. Possible values: `Int, Float, String, Bool, Color,
    ExternEnum.XXX, LocalEnum.XXX, Point, FilePath`.<br/>  If the field is an array, this
    field will look like `Array<...>` (eg. `Array<Int>`, `Array<Point>` etc.)<br/>  NOTE: if
    you enable the advanced option **Use Multilines type**, you will have "*Multilines*"
    instead of "*String*" when relevant.
    """
    type: Optional[str]
    """Optional list of accepted file extensions for FilePath value type. Includes the dot:
    `.ext`
    """
    accept_file_types: Optional[List[str]]
    """Possible values: `Any`, `OnlySame`, `OnlyTags`"""
    allowed_refs: Optional[AllowedRefs]
    allowed_ref_tags: Optional[List[str]]
    allow_out_of_level_ref: Optional[bool]
    """Array max length"""
    array_max_length: Optional[int]
    """Array min length"""
    array_min_length: Optional[int]
    auto_chain_ref: Optional[bool]
    """TRUE if the value can be null. For arrays, TRUE means it can contain null values
    (exception: array of Points can't have null values).
    """
    can_be_null: Optional[bool]
    """Default value if selected value is null or invalid."""
    default_override: Any
    editor_always_show: Optional[bool]
    editor_cut_long_values: Optional[bool]
    """Possible values: `Hidden`, `ValueOnly`, `NameAndValue`, `EntityTile`, `Points`,
    `PointStar`, `PointPath`, `PointPathLoop`, `RadiusPx`, `RadiusGrid`,
    `ArrayCountWithLabel`, `ArrayCountNoLabel`, `RefLinkBetweenPivots`,
    `RefLinkBetweenCenters`
    """
    editor_display_mode: Optional[EditorDisplayMode]
    """Possible values: `Above`, `Center`, `Beneath`"""
    editor_display_pos: Optional[EditorDisplayPos]
    editor_text_prefix: Optional[str]
    editor_text_suffix: Optional[str]
    """User defined unique identifier"""
    identifier: Optional[str]
    """TRUE if the value is an array of multiple values"""
    is_array: Optional[bool]
    """Max limit for value, if applicable"""
    max: Optional[float]
    """Min limit for value, if applicable"""
    min: Optional[float]
    """Optional regular expression that needs to be matched to accept values. Expected format:
    `/some_reg_ex/g`, with optional "i" flag.
    """
    regex: Optional[str]
    symmetrical_ref: Optional[bool]
    """Possible values: &lt;`null`&gt;, `LangPython`, `LangRuby`, `LangJS`, `LangLua`, `LangC`,
    `LangHaxe`, `LangMarkdown`, `LangJson`, `LangXml`, `LangLog`
    """
    text_language_mode: Optional[TextLanguageMode]
    """UID of the tileset used for a Tile"""
    tileset_uid: Optional[int]
    """Internal enum representing the possible field types. Possible values: F_Int, F_Float,
    F_String, F_Text, F_Bool, F_Color, F_Enum(...), F_Point, F_Path, F_EntityRef, F_Tile
    """
    field_definition_type: Optional[str]
    """Unique Int identifier"""
    uid: Optional[int]
    """If TRUE, the color associated with this field will override the Entity or Level default
    color in the editor UI. For Enum fields, this would be the color associated to their
    values.
    """
    use_for_smart_color: Optional[bool]

    def __init__(self, type: Optional[str], accept_file_types: Optional[List[str]], allowed_refs: Optional[AllowedRefs], allowed_ref_tags: Optional[List[str]], allow_out_of_level_ref: Optional[bool], array_max_length: Optional[int], array_min_length: Optional[int], auto_chain_ref: Optional[bool], can_be_null: Optional[bool], default_override: Any, editor_always_show: Optional[bool], editor_cut_long_values: Optional[bool], editor_display_mode: Optional[EditorDisplayMode], editor_display_pos: Optional[EditorDisplayPos], editor_text_prefix: Optional[str], editor_text_suffix: Optional[str], identifier: Optional[str], is_array: Optional[bool], max: Optional[float], min: Optional[float], regex: Optional[str], symmetrical_ref: Optional[bool], text_language_mode: Optional[TextLanguageMode], tileset_uid: Optional[int], field_definition_type: Optional[str], uid: Optional[int], use_for_smart_color: Optional[bool]) -> None:
        self.type = type
        self.accept_file_types = accept_file_types
        self.allowed_refs = allowed_refs
        self.allowed_ref_tags = allowed_ref_tags
        self.allow_out_of_level_ref = allow_out_of_level_ref
        self.array_max_length = array_max_length
        self.array_min_length = array_min_length
        self.auto_chain_ref = auto_chain_ref
        self.can_be_null = can_be_null
        self.default_override = default_override
        self.editor_always_show = editor_always_show
        self.editor_cut_long_values = editor_cut_long_values
        self.editor_display_mode = editor_display_mode
        self.editor_display_pos = editor_display_pos
        self.editor_text_prefix = editor_text_prefix
        self.editor_text_suffix = editor_text_suffix
        self.identifier = identifier
        self.is_array = is_array
        self.max = max
        self.min = min
        self.regex = regex
        self.symmetrical_ref = symmetrical_ref
        self.text_language_mode = text_language_mode
        self.tileset_uid = tileset_uid
        self.field_definition_type = field_definition_type
        self.uid = uid
        self.use_for_smart_color = use_for_smart_color

    @staticmethod
    def from_dict(obj: Any) -> 'FieldDefinition':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("__type"))
        accept_file_types = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("acceptFileTypes"))
        allowed_refs = from_union([AllowedRefs, from_none], obj.get("allowedRefs"))
        allowed_ref_tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("allowedRefTags"))
        allow_out_of_level_ref = from_union([from_bool, from_none], obj.get("allowOutOfLevelRef"))
        array_max_length = from_union([from_none, from_int], obj.get("arrayMaxLength"))
        array_min_length = from_union([from_none, from_int], obj.get("arrayMinLength"))
        auto_chain_ref = from_union([from_bool, from_none], obj.get("autoChainRef"))
        can_be_null = from_union([from_bool, from_none], obj.get("canBeNull"))
        default_override = obj.get("defaultOverride")
        editor_always_show = from_union([from_bool, from_none], obj.get("editorAlwaysShow"))
        editor_cut_long_values = from_union([from_bool, from_none], obj.get("editorCutLongValues"))
        editor_display_mode = from_union([EditorDisplayMode, from_none], obj.get("editorDisplayMode"))
        editor_display_pos = from_union([EditorDisplayPos, from_none], obj.get("editorDisplayPos"))
        editor_text_prefix = from_union([from_none, from_str], obj.get("editorTextPrefix"))
        editor_text_suffix = from_union([from_none, from_str], obj.get("editorTextSuffix"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        is_array = from_union([from_bool, from_none], obj.get("isArray"))
        max = from_union([from_float, from_none], obj.get("max"))
        min = from_union([from_float, from_none], obj.get("min"))
        regex = from_union([from_none, from_str], obj.get("regex"))
        symmetrical_ref = from_union([from_bool, from_none], obj.get("symmetricalRef"))
        text_language_mode = from_union([from_none, TextLanguageMode], obj.get("textLanguageMode"))
        tileset_uid = from_union([from_none, from_int], obj.get("tilesetUid"))
        field_definition_type = from_union([from_str, from_none], obj.get("type"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        use_for_smart_color = from_union([from_bool, from_none], obj.get("useForSmartColor"))
        return FieldDefinition(type, accept_file_types, allowed_refs, allowed_ref_tags, allow_out_of_level_ref, array_max_length, array_min_length, auto_chain_ref, can_be_null, default_override, editor_always_show, editor_cut_long_values, editor_display_mode, editor_display_pos, editor_text_prefix, editor_text_suffix, identifier, is_array, max, min, regex, symmetrical_ref, text_language_mode, tileset_uid, field_definition_type, uid, use_for_smart_color)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__type"] = from_union([from_str, from_none], self.type)
        result["acceptFileTypes"] = from_union([from_none, lambda x: from_list(from_str, x)], self.accept_file_types)
        result["allowedRefs"] = from_union([lambda x: to_enum(AllowedRefs, x), from_none], self.allowed_refs)
        result["allowedRefTags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.allowed_ref_tags)
        result["allowOutOfLevelRef"] = from_union([from_bool, from_none], self.allow_out_of_level_ref)
        result["arrayMaxLength"] = from_union([from_none, from_int], self.array_max_length)
        result["arrayMinLength"] = from_union([from_none, from_int], self.array_min_length)
        result["autoChainRef"] = from_union([from_bool, from_none], self.auto_chain_ref)
        result["canBeNull"] = from_union([from_bool, from_none], self.can_be_null)
        result["defaultOverride"] = self.default_override
        result["editorAlwaysShow"] = from_union([from_bool, from_none], self.editor_always_show)
        result["editorCutLongValues"] = from_union([from_bool, from_none], self.editor_cut_long_values)
        result["editorDisplayMode"] = from_union([lambda x: to_enum(EditorDisplayMode, x), from_none], self.editor_display_mode)
        result["editorDisplayPos"] = from_union([lambda x: to_enum(EditorDisplayPos, x), from_none], self.editor_display_pos)
        result["editorTextPrefix"] = from_union([from_none, from_str], self.editor_text_prefix)
        result["editorTextSuffix"] = from_union([from_none, from_str], self.editor_text_suffix)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["isArray"] = from_union([from_bool, from_none], self.is_array)
        result["max"] = from_union([to_float, from_none], self.max)
        result["min"] = from_union([to_float, from_none], self.min)
        result["regex"] = from_union([from_none, from_str], self.regex)
        result["symmetricalRef"] = from_union([from_bool, from_none], self.symmetrical_ref)
        result["textLanguageMode"] = from_union([from_none, lambda x: to_enum(TextLanguageMode, x)], self.text_language_mode)
        result["tilesetUid"] = from_union([from_none, from_int], self.tileset_uid)
        result["type"] = from_union([from_str, from_none], self.field_definition_type)
        result["uid"] = from_union([from_none, from_int], self.uid)
        result["useForSmartColor"] = from_union([from_bool, from_none], self.use_for_smart_color)
        return result


class LimitBehavior(Enum):
    """Possible values: `DiscardOldOnes`, `PreventAdding`, `MoveLastOne`"""
    DISCARD_OLD_ONES = "DiscardOldOnes"
    MOVE_LAST_ONE = "MoveLastOne"
    PREVENT_ADDING = "PreventAdding"


class LimitScope(Enum):
    """If TRUE, the maxCount is a "per world" limit, if FALSE, it's a "per level". Possible
    values: `PerLayer`, `PerLevel`, `PerWorld`
    """
    PER_LAYER = "PerLayer"
    PER_LEVEL = "PerLevel"
    PER_WORLD = "PerWorld"


class RenderMode(Enum):
    """Possible values: `Rectangle`, `Ellipse`, `Tile`, `Cross`"""
    CROSS = "Cross"
    ELLIPSE = "Ellipse"
    RECTANGLE = "Rectangle"
    TILE = "Tile"


class TilesetRectangle:
    """This object represents a custom sub rectangle in a Tileset image."""
    """Height in pixels"""
    h: Optional[int]
    """UID of the tileset"""
    tileset_uid: Optional[int]
    """Width in pixels"""
    w: Optional[int]
    """X pixels coordinate of the top-left corner in the Tileset image"""
    x: Optional[int]
    """Y pixels coordinate of the top-left corner in the Tileset image"""
    y: Optional[int]

    def __init__(self, h: Optional[int], tileset_uid: Optional[int], w: Optional[int], x: Optional[int], y: Optional[int]) -> None:
        self.h = h
        self.tileset_uid = tileset_uid
        self.w = w
        self.x = x
        self.y = y

    @staticmethod
    def from_dict(obj: Any) -> 'TilesetRectangle':
        assert isinstance(obj, dict)
        h = from_union([from_none, from_int], obj.get("h"))
        tileset_uid = from_union([from_none, from_int], obj.get("tilesetUid"))
        w = from_union([from_none, from_int], obj.get("w"))
        x = from_union([from_none, from_int], obj.get("x"))
        y = from_union([from_none, from_int], obj.get("y"))
        return TilesetRectangle(h, tileset_uid, w, x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["h"] = from_union([from_none, from_int], self.h)
        result["tilesetUid"] = from_union([from_none, from_int], self.tileset_uid)
        result["w"] = from_union([from_none, from_int], self.w)
        result["x"] = from_union([from_none, from_int], self.x)
        result["y"] = from_union([from_none, from_int], self.y)
        return result


class TileRenderMode(Enum):
    """An enum describing how the the Entity tile is rendered inside the Entity bounds. Possible
    values: `Cover`, `FitInside`, `Repeat`, `Stretch`, `FullSizeCropped`,
    `FullSizeUncropped`, `NineSlice`
    """
    COVER = "Cover"
    FIT_INSIDE = "FitInside"
    FULL_SIZE_CROPPED = "FullSizeCropped"
    FULL_SIZE_UNCROPPED = "FullSizeUncropped"
    NINE_SLICE = "NineSlice"
    REPEAT = "Repeat"
    STRETCH = "Stretch"


class EntityDefinition:
    """Base entity color"""
    color: Optional[str]
    """Array of field definitions"""
    field_defs: Optional[List[FieldDefinition]]
    fill_opacity: Optional[float]
    """Pixel height"""
    height: Optional[int]
    hollow: Optional[bool]
    """User defined unique identifier"""
    identifier: Optional[str]
    """Only applies to entities resizable on both X/Y. If TRUE, the entity instance width/height
    will keep the same aspect ratio as the definition.
    """
    keep_aspect_ratio: Optional[bool]
    """Possible values: `DiscardOldOnes`, `PreventAdding`, `MoveLastOne`"""
    limit_behavior: Optional[LimitBehavior]
    """If TRUE, the maxCount is a "per world" limit, if FALSE, it's a "per level". Possible
    values: `PerLayer`, `PerLevel`, `PerWorld`
    """
    limit_scope: Optional[LimitScope]
    line_opacity: Optional[float]
    """Max instances count"""
    max_count: Optional[int]
    """An array of 4 dimensions for the up/right/down/left borders (in this order) when using
    9-slice mode for `tileRenderMode`.<br/>  If the tileRenderMode is not NineSlice, then
    this array is empty.<br/>  See: https://en.wikipedia.org/wiki/9-slice_scaling
    """
    nine_slice_borders: Optional[List[int]]
    """Pivot X coordinate (from 0 to 1.0)"""
    pivot_x: Optional[float]
    """Pivot Y coordinate (from 0 to 1.0)"""
    pivot_y: Optional[float]
    """Possible values: `Rectangle`, `Ellipse`, `Tile`, `Cross`"""
    render_mode: Optional[RenderMode]
    """If TRUE, the entity instances will be resizable horizontally"""
    resizable_x: Optional[bool]
    """If TRUE, the entity instances will be resizable vertically"""
    resizable_y: Optional[bool]
    """Display entity name in editor"""
    show_name: Optional[bool]
    """An array of strings that classifies this entity"""
    tags: Optional[List[str]]
    """**WARNING**: this deprecated value will be *removed* completely on version 1.2.0+
    Replaced by: `tileRect`
    """
    tile_id: Optional[int]
    tile_opacity: Optional[float]
    """An object representing a rectangle from an existing Tileset"""
    tile_rect: Optional[TilesetRectangle]
    """An enum describing how the the Entity tile is rendered inside the Entity bounds. Possible
    values: `Cover`, `FitInside`, `Repeat`, `Stretch`, `FullSizeCropped`,
    `FullSizeUncropped`, `NineSlice`
    """
    tile_render_mode: Optional[TileRenderMode]
    """Tileset ID used for optional tile display"""
    tileset_id: Optional[int]
    """Unique Int identifier"""
    uid: Optional[int]
    """Pixel width"""
    width: Optional[int]

    def __init__(self, color: Optional[str], field_defs: Optional[List[FieldDefinition]], fill_opacity: Optional[float], height: Optional[int], hollow: Optional[bool], identifier: Optional[str], keep_aspect_ratio: Optional[bool], limit_behavior: Optional[LimitBehavior], limit_scope: Optional[LimitScope], line_opacity: Optional[float], max_count: Optional[int], nine_slice_borders: Optional[List[int]], pivot_x: Optional[float], pivot_y: Optional[float], render_mode: Optional[RenderMode], resizable_x: Optional[bool], resizable_y: Optional[bool], show_name: Optional[bool], tags: Optional[List[str]], tile_id: Optional[int], tile_opacity: Optional[float], tile_rect: Optional[TilesetRectangle], tile_render_mode: Optional[TileRenderMode], tileset_id: Optional[int], uid: Optional[int], width: Optional[int]) -> None:
        self.color = color
        self.field_defs = field_defs
        self.fill_opacity = fill_opacity
        self.height = height
        self.hollow = hollow
        self.identifier = identifier
        self.keep_aspect_ratio = keep_aspect_ratio
        self.limit_behavior = limit_behavior
        self.limit_scope = limit_scope
        self.line_opacity = line_opacity
        self.max_count = max_count
        self.nine_slice_borders = nine_slice_borders
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.render_mode = render_mode
        self.resizable_x = resizable_x
        self.resizable_y = resizable_y
        self.show_name = show_name
        self.tags = tags
        self.tile_id = tile_id
        self.tile_opacity = tile_opacity
        self.tile_rect = tile_rect
        self.tile_render_mode = tile_render_mode
        self.tileset_id = tileset_id
        self.uid = uid
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> 'EntityDefinition':
        assert isinstance(obj, dict)
        color = from_union([from_str, from_none], obj.get("color"))
        field_defs = from_union([lambda x: from_list(FieldDefinition.from_dict, x), from_none], obj.get("fieldDefs"))
        fill_opacity = from_union([from_float, from_none], obj.get("fillOpacity"))
        height = from_union([from_none, from_int], obj.get("height"))
        hollow = from_union([from_bool, from_none], obj.get("hollow"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        keep_aspect_ratio = from_union([from_bool, from_none], obj.get("keepAspectRatio"))
        limit_behavior = from_union([LimitBehavior, from_none], obj.get("limitBehavior"))
        limit_scope = from_union([LimitScope, from_none], obj.get("limitScope"))
        line_opacity = from_union([from_float, from_none], obj.get("lineOpacity"))
        max_count = from_union([from_none, from_int], obj.get("maxCount"))
        nine_slice_borders = from_union([lambda x: from_list(from_int, x), from_none], obj.get("nineSliceBorders"))
        pivot_x = from_union([from_float, from_none], obj.get("pivotX"))
        pivot_y = from_union([from_float, from_none], obj.get("pivotY"))
        render_mode = from_union([RenderMode, from_none], obj.get("renderMode"))
        resizable_x = from_union([from_bool, from_none], obj.get("resizableX"))
        resizable_y = from_union([from_bool, from_none], obj.get("resizableY"))
        show_name = from_union([from_bool, from_none], obj.get("showName"))
        tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("tags"))
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        tile_opacity = from_union([from_float, from_none], obj.get("tileOpacity"))
        tile_rect = from_union([from_none, TilesetRectangle.from_dict], obj.get("tileRect"))
        tile_render_mode = from_union([TileRenderMode, from_none], obj.get("tileRenderMode"))
        tileset_id = from_union([from_none, from_int], obj.get("tilesetId"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        width = from_union([from_none, from_int], obj.get("width"))
        return EntityDefinition(color, field_defs, fill_opacity, height, hollow, identifier, keep_aspect_ratio, limit_behavior, limit_scope, line_opacity, max_count, nine_slice_borders, pivot_x, pivot_y, render_mode, resizable_x, resizable_y, show_name, tags, tile_id, tile_opacity, tile_rect, tile_render_mode, tileset_id, uid, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_union([from_str, from_none], self.color)
        result["fieldDefs"] = from_union([lambda x: from_list(lambda x: to_class(FieldDefinition, x), x), from_none], self.field_defs)
        result["fillOpacity"] = from_union([to_float, from_none], self.fill_opacity)
        result["height"] = from_union([from_none, from_int], self.height)
        result["hollow"] = from_union([from_bool, from_none], self.hollow)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["keepAspectRatio"] = from_union([from_bool, from_none], self.keep_aspect_ratio)
        result["limitBehavior"] = from_union([lambda x: to_enum(LimitBehavior, x), from_none], self.limit_behavior)
        result["limitScope"] = from_union([lambda x: to_enum(LimitScope, x), from_none], self.limit_scope)
        result["lineOpacity"] = from_union([to_float, from_none], self.line_opacity)
        result["maxCount"] = from_union([from_none, from_int], self.max_count)
        result["nineSliceBorders"] = from_union([lambda x: from_list(from_int, x), from_none], self.nine_slice_borders)
        result["pivotX"] = from_union([to_float, from_none], self.pivot_x)
        result["pivotY"] = from_union([to_float, from_none], self.pivot_y)
        result["renderMode"] = from_union([lambda x: to_enum(RenderMode, x), from_none], self.render_mode)
        result["resizableX"] = from_union([from_bool, from_none], self.resizable_x)
        result["resizableY"] = from_union([from_bool, from_none], self.resizable_y)
        result["showName"] = from_union([from_bool, from_none], self.show_name)
        result["tags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.tags)
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        result["tileOpacity"] = from_union([to_float, from_none], self.tile_opacity)
        result["tileRect"] = from_union([from_none, lambda x: to_class(TilesetRectangle, x)], self.tile_rect)
        result["tileRenderMode"] = from_union([lambda x: to_enum(TileRenderMode, x), from_none], self.tile_render_mode)
        result["tilesetId"] = from_union([from_none, from_int], self.tileset_id)
        result["uid"] = from_union([from_none, from_int], self.uid)
        result["width"] = from_union([from_none, from_int], self.width)
        return result


class EnumValueDefinition:
    """An array of 4 Int values that refers to the tile in the tileset image: `[ x, y, width,
    height ]`
    """
    tile_src_rect: Optional[List[int]]
    """Optional color"""
    color: Optional[int]
    """Enum value"""
    id: Optional[str]
    """The optional ID of the tile"""
    tile_id: Optional[int]

    def __init__(self, tile_src_rect: Optional[List[int]], color: Optional[int], id: Optional[str], tile_id: Optional[int]) -> None:
        self.tile_src_rect = tile_src_rect
        self.color = color
        self.id = id
        self.tile_id = tile_id

    @staticmethod
    def from_dict(obj: Any) -> 'EnumValueDefinition':
        assert isinstance(obj, dict)
        tile_src_rect = from_union([lambda x: from_list(from_int, x), from_none], obj.get("__tileSrcRect"))
        color = from_union([from_none, from_int], obj.get("color"))
        id = from_union([from_str, from_none], obj.get("id"))
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        return EnumValueDefinition(tile_src_rect, color, id, tile_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__tileSrcRect"] = from_union([lambda x: from_list(from_int, x), from_none], self.tile_src_rect)
        result["color"] = from_union([from_none, from_int], self.color)
        result["id"] = from_union([from_str, from_none], self.id)
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        return result


class EnumDefinition:
    external_file_checksum: Optional[str]
    """Relative path to the external file providing this Enum"""
    external_rel_path: Optional[str]
    """Tileset UID if provided"""
    icon_tileset_uid: Optional[int]
    """User defined unique identifier"""
    identifier: Optional[str]
    """An array of user-defined tags to organize the Enums"""
    tags: Optional[List[str]]
    """Unique Int identifier"""
    uid: Optional[int]
    """All possible enum values, with their optional Tile infos."""
    values: Optional[List[EnumValueDefinition]]

    def __init__(self, external_file_checksum: Optional[str], external_rel_path: Optional[str], icon_tileset_uid: Optional[int], identifier: Optional[str], tags: Optional[List[str]], uid: Optional[int], values: Optional[List[EnumValueDefinition]]) -> None:
        self.external_file_checksum = external_file_checksum
        self.external_rel_path = external_rel_path
        self.icon_tileset_uid = icon_tileset_uid
        self.identifier = identifier
        self.tags = tags
        self.uid = uid
        self.values = values

    @staticmethod
    def from_dict(obj: Any) -> 'EnumDefinition':
        assert isinstance(obj, dict)
        external_file_checksum = from_union([from_none, from_str], obj.get("externalFileChecksum"))
        external_rel_path = from_union([from_none, from_str], obj.get("externalRelPath"))
        icon_tileset_uid = from_union([from_none, from_int], obj.get("iconTilesetUid"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("tags"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        values = from_union([lambda x: from_list(EnumValueDefinition.from_dict, x), from_none], obj.get("values"))
        return EnumDefinition(external_file_checksum, external_rel_path, icon_tileset_uid, identifier, tags, uid, values)

    def to_dict(self) -> dict:
        result: dict = {}
        result["externalFileChecksum"] = from_union([from_none, from_str], self.external_file_checksum)
        result["externalRelPath"] = from_union([from_none, from_str], self.external_rel_path)
        result["iconTilesetUid"] = from_union([from_none, from_int], self.icon_tileset_uid)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["tags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.tags)
        result["uid"] = from_union([from_none, from_int], self.uid)
        result["values"] = from_union([lambda x: from_list(lambda x: to_class(EnumValueDefinition, x), x), from_none], self.values)
        return result


class Checker(Enum):
    """Checker mode Possible values: `None`, `Horizontal`, `Vertical`"""
    HORIZONTAL = "Horizontal"
    NONE = "None"
    VERTICAL = "Vertical"


class TileMode(Enum):
    """Defines how tileIds array is used Possible values: `Single`, `Stamp`"""
    SINGLE = "Single"
    STAMP = "Stamp"


class AutoLayerRuleDefinition:
    """This complex section isn't meant to be used by game devs at all, as these rules are
    completely resolved internally by the editor before any saving. You should just ignore
    this part.
    """
    """If FALSE, the rule effect isn't applied, and no tiles are generated."""
    active: Optional[bool]
    """When TRUE, the rule will prevent other rules to be applied in the same cell if it matches
    (TRUE by default).
    """
    break_on_match: Optional[bool]
    """Chances for this rule to be applied (0 to 1)"""
    chance: Optional[float]
    """Checker mode Possible values: `None`, `Horizontal`, `Vertical`"""
    checker: Optional[Checker]
    """If TRUE, allow rule to be matched by flipping its pattern horizontally"""
    flip_x: Optional[bool]
    """If TRUE, allow rule to be matched by flipping its pattern vertically"""
    flip_y: Optional[bool]
    """Default IntGrid value when checking cells outside of level bounds"""
    out_of_bounds_value: Optional[int]
    """Rule pattern (size x size)"""
    pattern: Optional[List[int]]
    """If TRUE, enable Perlin filtering to only apply rule on specific random area"""
    perlin_active: Optional[bool]
    perlin_octaves: Optional[float]
    perlin_scale: Optional[float]
    perlin_seed: Optional[float]
    """X pivot of a tile stamp (0-1)"""
    pivot_x: Optional[float]
    """Y pivot of a tile stamp (0-1)"""
    pivot_y: Optional[float]
    """Pattern width & height. Should only be 1,3,5 or 7."""
    size: Optional[int]
    """Array of all the tile IDs. They are used randomly or as stamps, based on `tileMode` value."""
    tile_ids: Optional[List[int]]
    """Defines how tileIds array is used Possible values: `Single`, `Stamp`"""
    tile_mode: Optional[TileMode]
    """Unique Int identifier"""
    uid: Optional[int]
    """X cell coord modulo"""
    x_modulo: Optional[int]
    """X cell start offset"""
    x_offset: Optional[int]
    """Y cell coord modulo"""
    y_modulo: Optional[int]
    """Y cell start offset"""
    y_offset: Optional[int]

    def __init__(self, active: Optional[bool], break_on_match: Optional[bool], chance: Optional[float], checker: Optional[Checker], flip_x: Optional[bool], flip_y: Optional[bool], out_of_bounds_value: Optional[int], pattern: Optional[List[int]], perlin_active: Optional[bool], perlin_octaves: Optional[float], perlin_scale: Optional[float], perlin_seed: Optional[float], pivot_x: Optional[float], pivot_y: Optional[float], size: Optional[int], tile_ids: Optional[List[int]], tile_mode: Optional[TileMode], uid: Optional[int], x_modulo: Optional[int], x_offset: Optional[int], y_modulo: Optional[int], y_offset: Optional[int]) -> None:
        self.active = active
        self.break_on_match = break_on_match
        self.chance = chance
        self.checker = checker
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.out_of_bounds_value = out_of_bounds_value
        self.pattern = pattern
        self.perlin_active = perlin_active
        self.perlin_octaves = perlin_octaves
        self.perlin_scale = perlin_scale
        self.perlin_seed = perlin_seed
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.size = size
        self.tile_ids = tile_ids
        self.tile_mode = tile_mode
        self.uid = uid
        self.x_modulo = x_modulo
        self.x_offset = x_offset
        self.y_modulo = y_modulo
        self.y_offset = y_offset

    @staticmethod
    def from_dict(obj: Any) -> 'AutoLayerRuleDefinition':
        assert isinstance(obj, dict)
        active = from_union([from_bool, from_none], obj.get("active"))
        break_on_match = from_union([from_bool, from_none], obj.get("breakOnMatch"))
        chance = from_union([from_float, from_none], obj.get("chance"))
        checker = from_union([Checker, from_none], obj.get("checker"))
        flip_x = from_union([from_bool, from_none], obj.get("flipX"))
        flip_y = from_union([from_bool, from_none], obj.get("flipY"))
        out_of_bounds_value = from_union([from_none, from_int], obj.get("outOfBoundsValue"))
        pattern = from_union([lambda x: from_list(from_int, x), from_none], obj.get("pattern"))
        perlin_active = from_union([from_bool, from_none], obj.get("perlinActive"))
        perlin_octaves = from_union([from_float, from_none], obj.get("perlinOctaves"))
        perlin_scale = from_union([from_float, from_none], obj.get("perlinScale"))
        perlin_seed = from_union([from_float, from_none], obj.get("perlinSeed"))
        pivot_x = from_union([from_float, from_none], obj.get("pivotX"))
        pivot_y = from_union([from_float, from_none], obj.get("pivotY"))
        size = from_union([from_none, from_int], obj.get("size"))
        tile_ids = from_union([lambda x: from_list(from_int, x), from_none], obj.get("tileIds"))
        tile_mode = from_union([TileMode, from_none], obj.get("tileMode"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        x_modulo = from_union([from_none, from_int], obj.get("xModulo"))
        x_offset = from_union([from_none, from_int], obj.get("xOffset"))
        y_modulo = from_union([from_none, from_int], obj.get("yModulo"))
        y_offset = from_union([from_none, from_int], obj.get("yOffset"))
        return AutoLayerRuleDefinition(active, break_on_match, chance, checker, flip_x, flip_y, out_of_bounds_value, pattern, perlin_active, perlin_octaves, perlin_scale, perlin_seed, pivot_x, pivot_y, size, tile_ids, tile_mode, uid, x_modulo, x_offset, y_modulo, y_offset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_union([from_bool, from_none], self.active)
        result["breakOnMatch"] = from_union([from_bool, from_none], self.break_on_match)
        result["chance"] = from_union([to_float, from_none], self.chance)
        result["checker"] = from_union([lambda x: to_enum(Checker, x), from_none], self.checker)
        result["flipX"] = from_union([from_bool, from_none], self.flip_x)
        result["flipY"] = from_union([from_bool, from_none], self.flip_y)
        result["outOfBoundsValue"] = from_union([from_none, from_int], self.out_of_bounds_value)
        result["pattern"] = from_union([lambda x: from_list(from_int, x), from_none], self.pattern)
        result["perlinActive"] = from_union([from_bool, from_none], self.perlin_active)
        result["perlinOctaves"] = from_union([to_float, from_none], self.perlin_octaves)
        result["perlinScale"] = from_union([to_float, from_none], self.perlin_scale)
        result["perlinSeed"] = from_union([to_float, from_none], self.perlin_seed)
        result["pivotX"] = from_union([to_float, from_none], self.pivot_x)
        result["pivotY"] = from_union([to_float, from_none], self.pivot_y)
        result["size"] = from_union([from_none, from_int], self.size)
        result["tileIds"] = from_union([lambda x: from_list(from_int, x), from_none], self.tile_ids)
        result["tileMode"] = from_union([lambda x: to_enum(TileMode, x), from_none], self.tile_mode)
        result["uid"] = from_union([from_none, from_int], self.uid)
        result["xModulo"] = from_union([from_none, from_int], self.x_modulo)
        result["xOffset"] = from_union([from_none, from_int], self.x_offset)
        result["yModulo"] = from_union([from_none, from_int], self.y_modulo)
        result["yOffset"] = from_union([from_none, from_int], self.y_offset)
        return result


class AutoLayerRuleGroup:
    active: Optional[bool]
    """*This field was removed in 1.0.0 and should no longer be used.*"""
    collapsed: Optional[bool]
    is_optional: Optional[bool]
    name: Optional[str]
    rules: Optional[List[AutoLayerRuleDefinition]]
    uid: Optional[int]

    def __init__(self, active: Optional[bool], collapsed: Optional[bool], is_optional: Optional[bool], name: Optional[str], rules: Optional[List[AutoLayerRuleDefinition]], uid: Optional[int]) -> None:
        self.active = active
        self.collapsed = collapsed
        self.is_optional = is_optional
        self.name = name
        self.rules = rules
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'AutoLayerRuleGroup':
        assert isinstance(obj, dict)
        active = from_union([from_bool, from_none], obj.get("active"))
        collapsed = from_union([from_bool, from_none], obj.get("collapsed"))
        is_optional = from_union([from_bool, from_none], obj.get("isOptional"))
        name = from_union([from_str, from_none], obj.get("name"))
        rules = from_union([lambda x: from_list(AutoLayerRuleDefinition.from_dict, x), from_none], obj.get("rules"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        return AutoLayerRuleGroup(active, collapsed, is_optional, name, rules, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_union([from_bool, from_none], self.active)
        result["collapsed"] = from_union([from_bool, from_none], self.collapsed)
        result["isOptional"] = from_union([from_bool, from_none], self.is_optional)
        result["name"] = from_union([from_str, from_none], self.name)
        result["rules"] = from_union([lambda x: from_list(lambda x: to_class(AutoLayerRuleDefinition, x), x), from_none], self.rules)
        result["uid"] = from_union([from_none, from_int], self.uid)
        return result


class IntGridValueDefinition:
    """IntGrid value definition"""
    color: Optional[str]
    """User defined unique identifier"""
    identifier: Optional[str]
    """The IntGrid value itself"""
    value: Optional[int]

    def __init__(self, color: Optional[str], identifier: Optional[str], value: Optional[int]) -> None:
        self.color = color
        self.identifier = identifier
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'IntGridValueDefinition':
        assert isinstance(obj, dict)
        color = from_union([from_str, from_none], obj.get("color"))
        identifier = from_union([from_none, from_str], obj.get("identifier"))
        value = from_union([from_none, from_int], obj.get("value"))
        return IntGridValueDefinition(color, identifier, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_union([from_str, from_none], self.color)
        result["identifier"] = from_union([from_none, from_str], self.identifier)
        result["value"] = from_union([from_none, from_int], self.value)
        return result


class TypeEnum(Enum):
    """Type of the layer as Haxe Enum Possible values: `IntGrid`, `Entities`, `Tiles`,
    `AutoLayer`
    """
    AUTO_LAYER = "AutoLayer"
    ENTITIES = "Entities"
    INT_GRID = "IntGrid"
    TILES = "Tiles"


class LayerDefinition:
    """Type of the layer (*IntGrid, Entities, Tiles or AutoLayer*)"""
    type: Optional[str]
    """Contains all the auto-layer rule definitions."""
    auto_rule_groups: Optional[List[AutoLayerRuleGroup]]
    auto_source_layer_def_uid: Optional[int]
    """**WARNING**: this deprecated value will be *removed* completely on version 1.2.0+
    Replaced by: `tilesetDefUid`
    """
    auto_tileset_def_uid: Optional[int]
    """Opacity of the layer (0 to 1.0)"""
    display_opacity: Optional[float]
    """An array of tags to forbid some Entities in this layer"""
    excluded_tags: Optional[List[str]]
    """Width and height of the grid in pixels"""
    grid_size: Optional[int]
    """Height of the optional "guide" grid in pixels"""
    guide_grid_hei: Optional[int]
    """Width of the optional "guide" grid in pixels"""
    guide_grid_wid: Optional[int]
    hide_fields_when_inactive: Optional[bool]
    """Hide the layer from the list on the side of the editor view."""
    hide_in_list: Optional[bool]
    """User defined unique identifier"""
    identifier: Optional[str]
    """Alpha of this layer when it is not the active one."""
    inactive_opacity: Optional[float]
    """An array that defines extra optional info for each IntGrid value.<br/>  WARNING: the
    array order is not related to actual IntGrid values! As user can re-order IntGrid values
    freely, you may value "2" before value "1" in this array.
    """
    int_grid_values: Optional[List[IntGridValueDefinition]]
    """Parallax horizontal factor (from -1 to 1, defaults to 0) which affects the scrolling
    speed of this layer, creating a fake 3D (parallax) effect.
    """
    parallax_factor_x: Optional[float]
    """Parallax vertical factor (from -1 to 1, defaults to 0) which affects the scrolling speed
    of this layer, creating a fake 3D (parallax) effect.
    """
    parallax_factor_y: Optional[float]
    """If true (default), a layer with a parallax factor will also be scaled up/down accordingly."""
    parallax_scaling: Optional[bool]
    """X offset of the layer, in pixels (IMPORTANT: this should be added to the `LayerInstance`
    optional offset)
    """
    px_offset_x: Optional[int]
    """Y offset of the layer, in pixels (IMPORTANT: this should be added to the `LayerInstance`
    optional offset)
    """
    px_offset_y: Optional[int]
    """An array of tags to filter Entities that can be added to this layer"""
    required_tags: Optional[List[str]]
    """If the tiles are smaller or larger than the layer grid, the pivot value will be used to
    position the tile relatively its grid cell.
    """
    tile_pivot_x: Optional[float]
    """If the tiles are smaller or larger than the layer grid, the pivot value will be used to
    position the tile relatively its grid cell.
    """
    tile_pivot_y: Optional[float]
    """Reference to the default Tileset UID being used by this layer definition.<br/>
    **WARNING**: some layer *instances* might use a different tileset. So most of the time,
    you should probably use the `__tilesetDefUid` value found in layer instances.<br/>  Note:
    since version 1.0.0, the old `autoTilesetDefUid` was removed and merged into this value.
    """
    tileset_def_uid: Optional[int]
    """Type of the layer as Haxe Enum Possible values: `IntGrid`, `Entities`, `Tiles`,
    `AutoLayer`
    """
    layer_definition_type: Optional[TypeEnum]
    """Unique Int identifier"""
    uid: Optional[int]

    def __init__(self, type: Optional[str], auto_rule_groups: Optional[List[AutoLayerRuleGroup]], auto_source_layer_def_uid: Optional[int], auto_tileset_def_uid: Optional[int], display_opacity: Optional[float], excluded_tags: Optional[List[str]], grid_size: Optional[int], guide_grid_hei: Optional[int], guide_grid_wid: Optional[int], hide_fields_when_inactive: Optional[bool], hide_in_list: Optional[bool], identifier: Optional[str], inactive_opacity: Optional[float], int_grid_values: Optional[List[IntGridValueDefinition]], parallax_factor_x: Optional[float], parallax_factor_y: Optional[float], parallax_scaling: Optional[bool], px_offset_x: Optional[int], px_offset_y: Optional[int], required_tags: Optional[List[str]], tile_pivot_x: Optional[float], tile_pivot_y: Optional[float], tileset_def_uid: Optional[int], layer_definition_type: Optional[TypeEnum], uid: Optional[int]) -> None:
        self.type = type
        self.auto_rule_groups = auto_rule_groups
        self.auto_source_layer_def_uid = auto_source_layer_def_uid
        self.auto_tileset_def_uid = auto_tileset_def_uid
        self.display_opacity = display_opacity
        self.excluded_tags = excluded_tags
        self.grid_size = grid_size
        self.guide_grid_hei = guide_grid_hei
        self.guide_grid_wid = guide_grid_wid
        self.hide_fields_when_inactive = hide_fields_when_inactive
        self.hide_in_list = hide_in_list
        self.identifier = identifier
        self.inactive_opacity = inactive_opacity
        self.int_grid_values = int_grid_values
        self.parallax_factor_x = parallax_factor_x
        self.parallax_factor_y = parallax_factor_y
        self.parallax_scaling = parallax_scaling
        self.px_offset_x = px_offset_x
        self.px_offset_y = px_offset_y
        self.required_tags = required_tags
        self.tile_pivot_x = tile_pivot_x
        self.tile_pivot_y = tile_pivot_y
        self.tileset_def_uid = tileset_def_uid
        self.layer_definition_type = layer_definition_type
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'LayerDefinition':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("__type"))
        auto_rule_groups = from_union([lambda x: from_list(AutoLayerRuleGroup.from_dict, x), from_none], obj.get("autoRuleGroups"))
        auto_source_layer_def_uid = from_union([from_none, from_int], obj.get("autoSourceLayerDefUid"))
        auto_tileset_def_uid = from_union([from_none, from_int], obj.get("autoTilesetDefUid"))
        display_opacity = from_union([from_float, from_none], obj.get("displayOpacity"))
        excluded_tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("excludedTags"))
        grid_size = from_union([from_none, from_int], obj.get("gridSize"))
        guide_grid_hei = from_union([from_none, from_int], obj.get("guideGridHei"))
        guide_grid_wid = from_union([from_none, from_int], obj.get("guideGridWid"))
        hide_fields_when_inactive = from_union([from_bool, from_none], obj.get("hideFieldsWhenInactive"))
        hide_in_list = from_union([from_bool, from_none], obj.get("hideInList"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        inactive_opacity = from_union([from_float, from_none], obj.get("inactiveOpacity"))
        int_grid_values = from_union([lambda x: from_list(IntGridValueDefinition.from_dict, x), from_none], obj.get("intGridValues"))
        parallax_factor_x = from_union([from_float, from_none], obj.get("parallaxFactorX"))
        parallax_factor_y = from_union([from_float, from_none], obj.get("parallaxFactorY"))
        parallax_scaling = from_union([from_bool, from_none], obj.get("parallaxScaling"))
        px_offset_x = from_union([from_none, from_int], obj.get("pxOffsetX"))
        px_offset_y = from_union([from_none, from_int], obj.get("pxOffsetY"))
        required_tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("requiredTags"))
        tile_pivot_x = from_union([from_float, from_none], obj.get("tilePivotX"))
        tile_pivot_y = from_union([from_float, from_none], obj.get("tilePivotY"))
        tileset_def_uid = from_union([from_none, from_int], obj.get("tilesetDefUid"))
        layer_definition_type = from_union([TypeEnum, from_none], obj.get("type"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        return LayerDefinition(type, auto_rule_groups, auto_source_layer_def_uid, auto_tileset_def_uid, display_opacity, excluded_tags, grid_size, guide_grid_hei, guide_grid_wid, hide_fields_when_inactive, hide_in_list, identifier, inactive_opacity, int_grid_values, parallax_factor_x, parallax_factor_y, parallax_scaling, px_offset_x, px_offset_y, required_tags, tile_pivot_x, tile_pivot_y, tileset_def_uid, layer_definition_type, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__type"] = from_union([from_str, from_none], self.type)
        result["autoRuleGroups"] = from_union([lambda x: from_list(lambda x: to_class(AutoLayerRuleGroup, x), x), from_none], self.auto_rule_groups)
        result["autoSourceLayerDefUid"] = from_union([from_none, from_int], self.auto_source_layer_def_uid)
        result["autoTilesetDefUid"] = from_union([from_none, from_int], self.auto_tileset_def_uid)
        result["displayOpacity"] = from_union([to_float, from_none], self.display_opacity)
        result["excludedTags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.excluded_tags)
        result["gridSize"] = from_union([from_none, from_int], self.grid_size)
        result["guideGridHei"] = from_union([from_none, from_int], self.guide_grid_hei)
        result["guideGridWid"] = from_union([from_none, from_int], self.guide_grid_wid)
        result["hideFieldsWhenInactive"] = from_union([from_bool, from_none], self.hide_fields_when_inactive)
        result["hideInList"] = from_union([from_bool, from_none], self.hide_in_list)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["inactiveOpacity"] = from_union([to_float, from_none], self.inactive_opacity)
        result["intGridValues"] = from_union([lambda x: from_list(lambda x: to_class(IntGridValueDefinition, x), x), from_none], self.int_grid_values)
        result["parallaxFactorX"] = from_union([to_float, from_none], self.parallax_factor_x)
        result["parallaxFactorY"] = from_union([to_float, from_none], self.parallax_factor_y)
        result["parallaxScaling"] = from_union([from_bool, from_none], self.parallax_scaling)
        result["pxOffsetX"] = from_union([from_none, from_int], self.px_offset_x)
        result["pxOffsetY"] = from_union([from_none, from_int], self.px_offset_y)
        result["requiredTags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.required_tags)
        result["tilePivotX"] = from_union([to_float, from_none], self.tile_pivot_x)
        result["tilePivotY"] = from_union([to_float, from_none], self.tile_pivot_y)
        result["tilesetDefUid"] = from_union([from_none, from_int], self.tileset_def_uid)
        result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.layer_definition_type)
        result["uid"] = from_union([from_none, from_int], self.uid)
        return result


class TileCustomMetadata:
    """In a tileset definition, user defined meta-data of a tile."""
    data: Optional[str]
    tile_id: Optional[int]

    def __init__(self, data: Optional[str], tile_id: Optional[int]) -> None:
        self.data = data
        self.tile_id = tile_id

    @staticmethod
    def from_dict(obj: Any) -> 'TileCustomMetadata':
        assert isinstance(obj, dict)
        data = from_union([from_str, from_none], obj.get("data"))
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        return TileCustomMetadata(data, tile_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([from_str, from_none], self.data)
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        return result


class EmbedAtlas(Enum):
    LDTK_ICONS = "LdtkIcons"


class EnumTagValue:
    """In a tileset definition, enum based tag infos"""
    enum_value_id: Optional[str]
    tile_ids: Optional[List[int]]

    def __init__(self, enum_value_id: Optional[str], tile_ids: Optional[List[int]]) -> None:
        self.enum_value_id = enum_value_id
        self.tile_ids = tile_ids

    @staticmethod
    def from_dict(obj: Any) -> 'EnumTagValue':
        assert isinstance(obj, dict)
        enum_value_id = from_union([from_str, from_none], obj.get("enumValueId"))
        tile_ids = from_union([lambda x: from_list(from_int, x), from_none], obj.get("tileIds"))
        return EnumTagValue(enum_value_id, tile_ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["enumValueId"] = from_union([from_str, from_none], self.enum_value_id)
        result["tileIds"] = from_union([lambda x: from_list(from_int, x), from_none], self.tile_ids)
        return result


class TilesetDefinition:
    """The `Tileset` definition is the most important part among project definitions. It
    contains some extra informations about each integrated tileset. If you only had to parse
    one definition section, that would be the one.
    """
    """Grid-based height"""
    c_hei: Optional[int]
    """Grid-based width"""
    c_wid: Optional[int]
    """The following data is used internally for various optimizations. It's always synced with
    source image changes.
    """
    cached_pixel_data: Optional[Dict[str, Any]]
    """An array of custom tile metadata"""
    custom_data: Optional[List[TileCustomMetadata]]
    """If this value is set, then it means that this atlas uses an internal LDtk atlas image
    instead of a loaded one. Possible values: &lt;`null`&gt;, `LdtkIcons`
    """
    embed_atlas: Optional[EmbedAtlas]
    """Tileset tags using Enum values specified by `tagsSourceEnumId`. This array contains 1
    element per Enum value, which contains an array of all Tile IDs that are tagged with it.
    """
    enum_tags: Optional[List[EnumTagValue]]
    """User defined unique identifier"""
    identifier: Optional[str]
    """Distance in pixels from image borders"""
    padding: Optional[int]
    """Image height in pixels"""
    px_hei: Optional[int]
    """Image width in pixels"""
    px_wid: Optional[int]
    """Path to the source file, relative to the current project JSON file<br/>  It can be null
    if no image was provided, or when using an embed atlas.
    """
    rel_path: Optional[str]
    """Array of group of tiles selections, only meant to be used in the editor"""
    saved_selections: Optional[List[Dict[str, Any]]]
    """Space in pixels between all tiles"""
    spacing: Optional[int]
    """An array of user-defined tags to organize the Tilesets"""
    tags: Optional[List[str]]
    """Optional Enum definition UID used for this tileset meta-data"""
    tags_source_enum_uid: Optional[int]
    tile_grid_size: Optional[int]
    """Unique Intidentifier"""
    uid: Optional[int]

    def __init__(self, c_hei: Optional[int], c_wid: Optional[int], cached_pixel_data: Optional[Dict[str, Any]], custom_data: Optional[List[TileCustomMetadata]], embed_atlas: Optional[EmbedAtlas], enum_tags: Optional[List[EnumTagValue]], identifier: Optional[str], padding: Optional[int], px_hei: Optional[int], px_wid: Optional[int], rel_path: Optional[str], saved_selections: Optional[List[Dict[str, Any]]], spacing: Optional[int], tags: Optional[List[str]], tags_source_enum_uid: Optional[int], tile_grid_size: Optional[int], uid: Optional[int]) -> None:
        self.c_hei = c_hei
        self.c_wid = c_wid
        self.cached_pixel_data = cached_pixel_data
        self.custom_data = custom_data
        self.embed_atlas = embed_atlas
        self.enum_tags = enum_tags
        self.identifier = identifier
        self.padding = padding
        self.px_hei = px_hei
        self.px_wid = px_wid
        self.rel_path = rel_path
        self.saved_selections = saved_selections
        self.spacing = spacing
        self.tags = tags
        self.tags_source_enum_uid = tags_source_enum_uid
        self.tile_grid_size = tile_grid_size
        self.uid = uid

    @staticmethod
    def from_dict(obj: Any) -> 'TilesetDefinition':
        assert isinstance(obj, dict)
        c_hei = from_union([from_none, from_int], obj.get("__cHei"))
        c_wid = from_union([from_none, from_int], obj.get("__cWid"))
        cached_pixel_data = from_union([from_none, lambda x: from_dict(lambda x: x, x)], obj.get("cachedPixelData"))
        custom_data = from_union([lambda x: from_list(TileCustomMetadata.from_dict, x), from_none], obj.get("customData"))
        embed_atlas = from_union([from_none, EmbedAtlas], obj.get("embedAtlas"))
        enum_tags = from_union([lambda x: from_list(EnumTagValue.from_dict, x), from_none], obj.get("enumTags"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        padding = from_union([from_none, from_int], obj.get("padding"))
        px_hei = from_union([from_none, from_int], obj.get("pxHei"))
        px_wid = from_union([from_none, from_int], obj.get("pxWid"))
        rel_path = from_union([from_none, from_str], obj.get("relPath"))
        saved_selections = from_union([lambda x: from_list(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("savedSelections"))
        spacing = from_union([from_none, from_int], obj.get("spacing"))
        tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("tags"))
        tags_source_enum_uid = from_union([from_none, from_int], obj.get("tagsSourceEnumUid"))
        tile_grid_size = from_union([from_none, from_int], obj.get("tileGridSize"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        return TilesetDefinition(c_hei, c_wid, cached_pixel_data, custom_data, embed_atlas, enum_tags, identifier, padding, px_hei, px_wid, rel_path, saved_selections, spacing, tags, tags_source_enum_uid, tile_grid_size, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__cHei"] = from_union([from_none, from_int], self.c_hei)
        result["__cWid"] = from_union([from_none, from_int], self.c_wid)
        result["cachedPixelData"] = from_union([from_none, lambda x: from_dict(lambda x: x, x)], self.cached_pixel_data)
        result["customData"] = from_union([lambda x: from_list(lambda x: to_class(TileCustomMetadata, x), x), from_none], self.custom_data)
        result["embedAtlas"] = from_union([from_none, lambda x: to_enum(EmbedAtlas, x)], self.embed_atlas)
        result["enumTags"] = from_union([lambda x: from_list(lambda x: to_class(EnumTagValue, x), x), from_none], self.enum_tags)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["padding"] = from_union([from_none, from_int], self.padding)
        result["pxHei"] = from_union([from_none, from_int], self.px_hei)
        result["pxWid"] = from_union([from_none, from_int], self.px_wid)
        result["relPath"] = from_union([from_none, from_str], self.rel_path)
        result["savedSelections"] = from_union([lambda x: from_list(lambda x: from_dict(lambda x: x, x), x), from_none], self.saved_selections)
        result["spacing"] = from_union([from_none, from_int], self.spacing)
        result["tags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.tags)
        result["tagsSourceEnumUid"] = from_union([from_none, from_int], self.tags_source_enum_uid)
        result["tileGridSize"] = from_union([from_none, from_int], self.tile_grid_size)
        result["uid"] = from_union([from_none, from_int], self.uid)
        return result


class Definitions:
    """If you're writing your own LDtk importer, you should probably just ignore *most* stuff in
    the `defs` section, as it contains data that are mostly important to the editor. To keep
    you away from the `defs` section and avoid some unnecessary JSON parsing, important data
    from definitions is often duplicated in fields prefixed with a double underscore (eg.
    `__identifier` or `__type`).  The 2 only definition types you might need here are
    **Tilesets** and **Enums**.
    
    A structure containing all the definitions of this project
    """
    """All entities definitions, including their custom fields"""
    entities: Optional[List[EntityDefinition]]
    """All internal enums"""
    enums: Optional[List[EnumDefinition]]
    """Note: external enums are exactly the same as `enums`, except they have a `relPath` to
    point to an external source file.
    """
    external_enums: Optional[List[EnumDefinition]]
    """All layer definitions"""
    layers: Optional[List[LayerDefinition]]
    """All custom fields available to all levels."""
    level_fields: Optional[List[FieldDefinition]]
    """All tilesets"""
    tilesets: Optional[List[TilesetDefinition]]

    def __init__(self, entities: Optional[List[EntityDefinition]], enums: Optional[List[EnumDefinition]], external_enums: Optional[List[EnumDefinition]], layers: Optional[List[LayerDefinition]], level_fields: Optional[List[FieldDefinition]], tilesets: Optional[List[TilesetDefinition]]) -> None:
        self.entities = entities
        self.enums = enums
        self.external_enums = external_enums
        self.layers = layers
        self.level_fields = level_fields
        self.tilesets = tilesets

    @staticmethod
    def from_dict(obj: Any) -> 'Definitions':
        assert isinstance(obj, dict)
        entities = from_union([lambda x: from_list(EntityDefinition.from_dict, x), from_none], obj.get("entities"))
        enums = from_union([lambda x: from_list(EnumDefinition.from_dict, x), from_none], obj.get("enums"))
        external_enums = from_union([lambda x: from_list(EnumDefinition.from_dict, x), from_none], obj.get("externalEnums"))
        layers = from_union([lambda x: from_list(LayerDefinition.from_dict, x), from_none], obj.get("layers"))
        level_fields = from_union([lambda x: from_list(FieldDefinition.from_dict, x), from_none], obj.get("levelFields"))
        tilesets = from_union([lambda x: from_list(TilesetDefinition.from_dict, x), from_none], obj.get("tilesets"))
        return Definitions(entities, enums, external_enums, layers, level_fields, tilesets)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_union([lambda x: from_list(lambda x: to_class(EntityDefinition, x), x), from_none], self.entities)
        result["enums"] = from_union([lambda x: from_list(lambda x: to_class(EnumDefinition, x), x), from_none], self.enums)
        result["externalEnums"] = from_union([lambda x: from_list(lambda x: to_class(EnumDefinition, x), x), from_none], self.external_enums)
        result["layers"] = from_union([lambda x: from_list(lambda x: to_class(LayerDefinition, x), x), from_none], self.layers)
        result["levelFields"] = from_union([lambda x: from_list(lambda x: to_class(FieldDefinition, x), x), from_none], self.level_fields)
        result["tilesets"] = from_union([lambda x: from_list(lambda x: to_class(TilesetDefinition, x), x), from_none], self.tilesets)
        return result


class Flag(Enum):
    DISCARD_PRE_CSV_INT_GRID = "DiscardPreCsvIntGrid"
    EXPORT_PRE_CSV_INT_GRID_FORMAT = "ExportPreCsvIntGridFormat"
    IGNORE_BACKUP_SUGGEST = "IgnoreBackupSuggest"
    MULTI_WORLDS = "MultiWorlds"
    PREPEND_INDEX_TO_LEVEL_FILE_NAMES = "PrependIndexToLevelFileNames"
    USE_MULTILINES_TYPE = "UseMultilinesType"


class FieldInstance:
    """Field definition identifier"""
    identifier: Optional[str]
    """Optional TilesetRect used to display this field (this can be the field own Tile, or some
    other Tile guessed from the value, like an Enum).
    """
    tile: Optional[TilesetRectangle]
    """Type of the field, such as `Int`, `Float`, `String`, `Enum(my_enum_name)`, `Bool`,
    etc.<br/>  NOTE: if you enable the advanced option **Use Multilines type**, you will have
    "*Multilines*" instead of "*String*" when relevant.
    """
    type: Optional[str]
    """Actual value of the field instance. The value type varies, depending on `__type`:<br/>
    - For **classic types** (ie. Integer, Float, Boolean, String, Text and FilePath), you
    just get the actual value with the expected type.<br/>   - For **Color**, the value is an
    hexadecimal string using "#rrggbb" format.<br/>   - For **Enum**, the value is a String
    representing the selected enum value.<br/>   - For **Point**, the value is a
    [GridPoint](#ldtk-GridPoint) object.<br/>   - For **Tile**, the value is a
    [TilesetRect](#ldtk-TilesetRect) object.<br/>   - For **EntityRef**, the value is an
    [EntityReferenceInfos](#ldtk-EntityReferenceInfos) object.<br/><br/>  If the field is an
    array, then this `__value` will also be a JSON array.
    """
    value: Any
    """Reference of the **Field definition** UID"""
    def_uid: Optional[int]
    """Editor internal raw values"""
    real_editor_values: Optional[List[Any]]

    def __init__(self, identifier: Optional[str], tile: Optional[TilesetRectangle], type: Optional[str], value: Any, def_uid: Optional[int], real_editor_values: Optional[List[Any]]) -> None:
        self.identifier = identifier
        self.tile = tile
        self.type = type
        self.value = value
        self.def_uid = def_uid
        self.real_editor_values = real_editor_values

    @staticmethod
    def from_dict(obj: Any) -> 'FieldInstance':
        assert isinstance(obj, dict)
        identifier = from_union([from_str, from_none], obj.get("__identifier"))
        tile = from_union([from_none, TilesetRectangle.from_dict], obj.get("__tile"))
        type = from_union([from_str, from_none], obj.get("__type"))
        value = obj.get("__value")
        def_uid = from_union([from_none, from_int], obj.get("defUid"))
        real_editor_values = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("realEditorValues"))
        return FieldInstance(identifier, tile, type, value, def_uid, real_editor_values)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__identifier"] = from_union([from_str, from_none], self.identifier)
        result["__tile"] = from_union([from_none, lambda x: to_class(TilesetRectangle, x)], self.tile)
        result["__type"] = from_union([from_str, from_none], self.type)
        result["__value"] = self.value
        result["defUid"] = from_union([from_none, from_int], self.def_uid)
        result["realEditorValues"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.real_editor_values)
        return result


class EntityInstance:
    """Grid-based coordinates (`[x,y]` format)"""
    grid: Optional[List[int]]
    """Entity definition identifier"""
    identifier: Optional[str]
    """Pivot coordinates  (`[x,y]` format, values are from 0 to 1) of the Entity"""
    pivot: Optional[List[float]]
    """The entity "smart" color, guessed from either Entity definition, or one its field
    instances.
    """
    smart_color: Optional[str]
    """Array of tags defined in this Entity definition"""
    tags: Optional[List[str]]
    """Optional TilesetRect used to display this entity (it could either be the default Entity
    tile, or some tile provided by a field value, like an Enum).
    """
    tile: Optional[TilesetRectangle]
    """Reference of the **Entity definition** UID"""
    def_uid: Optional[int]
    """An array of all custom fields and their values."""
    field_instances: Optional[List[FieldInstance]]
    """Entity height in pixels. For non-resizable entities, it will be the same as Entity
    definition.
    """
    height: Optional[int]
    """Unique instance identifier"""
    iid: Optional[str]
    """Pixel coordinates (`[x,y]` format) in current level coordinate space. Don't forget
    optional layer offsets, if they exist!
    """
    px: Optional[List[int]]
    """Entity width in pixels. For non-resizable entities, it will be the same as Entity
    definition.
    """
    width: Optional[int]

    def __init__(self, grid: Optional[List[int]], identifier: Optional[str], pivot: Optional[List[float]], smart_color: Optional[str], tags: Optional[List[str]], tile: Optional[TilesetRectangle], def_uid: Optional[int], field_instances: Optional[List[FieldInstance]], height: Optional[int], iid: Optional[str], px: Optional[List[int]], width: Optional[int]) -> None:
        self.grid = grid
        self.identifier = identifier
        self.pivot = pivot
        self.smart_color = smart_color
        self.tags = tags
        self.tile = tile
        self.def_uid = def_uid
        self.field_instances = field_instances
        self.height = height
        self.iid = iid
        self.px = px
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> 'EntityInstance':
        assert isinstance(obj, dict)
        grid = from_union([lambda x: from_list(from_int, x), from_none], obj.get("__grid"))
        identifier = from_union([from_str, from_none], obj.get("__identifier"))
        pivot = from_union([lambda x: from_list(from_float, x), from_none], obj.get("__pivot"))
        smart_color = from_union([from_str, from_none], obj.get("__smartColor"))
        tags = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("__tags"))
        tile = from_union([from_none, TilesetRectangle.from_dict], obj.get("__tile"))
        def_uid = from_union([from_none, from_int], obj.get("defUid"))
        field_instances = from_union([lambda x: from_list(FieldInstance.from_dict, x), from_none], obj.get("fieldInstances"))
        height = from_union([from_none, from_int], obj.get("height"))
        iid = from_union([from_str, from_none], obj.get("iid"))
        px = from_union([lambda x: from_list(from_int, x), from_none], obj.get("px"))
        width = from_union([from_none, from_int], obj.get("width"))
        return EntityInstance(grid, identifier, pivot, smart_color, tags, tile, def_uid, field_instances, height, iid, px, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__grid"] = from_union([lambda x: from_list(from_int, x), from_none], self.grid)
        result["__identifier"] = from_union([from_str, from_none], self.identifier)
        result["__pivot"] = from_union([lambda x: from_list(to_float, x), from_none], self.pivot)
        result["__smartColor"] = from_union([from_str, from_none], self.smart_color)
        result["__tags"] = from_union([from_none, lambda x: from_list(from_str, x)], self.tags)
        result["__tile"] = from_union([from_none, lambda x: to_class(TilesetRectangle, x)], self.tile)
        result["defUid"] = from_union([from_none, from_int], self.def_uid)
        result["fieldInstances"] = from_union([lambda x: from_list(lambda x: to_class(FieldInstance, x), x), from_none], self.field_instances)
        result["height"] = from_union([from_none, from_int], self.height)
        result["iid"] = from_union([from_str, from_none], self.iid)
        result["px"] = from_union([lambda x: from_list(from_int, x), from_none], self.px)
        result["width"] = from_union([from_none, from_int], self.width)
        return result


class FieldInstanceEntityReference:
    """This object is used in Field Instances to describe an EntityRef value."""
    """IID of the refered EntityInstance"""
    entity_iid: Optional[str]
    """IID of the LayerInstance containing the refered EntityInstance"""
    layer_iid: Optional[str]
    """IID of the Level containing the refered EntityInstance"""
    level_iid: Optional[str]
    """IID of the World containing the refered EntityInstance"""
    world_iid: Optional[str]

    def __init__(self, entity_iid: Optional[str], layer_iid: Optional[str], level_iid: Optional[str], world_iid: Optional[str]) -> None:
        self.entity_iid = entity_iid
        self.layer_iid = layer_iid
        self.level_iid = level_iid
        self.world_iid = world_iid

    @staticmethod
    def from_dict(obj: Any) -> 'FieldInstanceEntityReference':
        assert isinstance(obj, dict)
        entity_iid = from_union([from_str, from_none], obj.get("entityIid"))
        layer_iid = from_union([from_str, from_none], obj.get("layerIid"))
        level_iid = from_union([from_str, from_none], obj.get("levelIid"))
        world_iid = from_union([from_str, from_none], obj.get("worldIid"))
        return FieldInstanceEntityReference(entity_iid, layer_iid, level_iid, world_iid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entityIid"] = from_union([from_str, from_none], self.entity_iid)
        result["layerIid"] = from_union([from_str, from_none], self.layer_iid)
        result["levelIid"] = from_union([from_str, from_none], self.level_iid)
        result["worldIid"] = from_union([from_str, from_none], self.world_iid)
        return result


class FieldInstanceGridPoint:
    """This object is just a grid-based coordinate used in Field values."""
    """X grid-based coordinate"""
    cx: Optional[int]
    """Y grid-based coordinate"""
    cy: Optional[int]

    def __init__(self, cx: Optional[int], cy: Optional[int]) -> None:
        self.cx = cx
        self.cy = cy

    @staticmethod
    def from_dict(obj: Any) -> 'FieldInstanceGridPoint':
        assert isinstance(obj, dict)
        cx = from_union([from_none, from_int], obj.get("cx"))
        cy = from_union([from_none, from_int], obj.get("cy"))
        return FieldInstanceGridPoint(cx, cy)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cx"] = from_union([from_none, from_int], self.cx)
        result["cy"] = from_union([from_none, from_int], self.cy)
        return result


class IntGridValueInstance:
    """IntGrid value instance"""
    """Coordinate ID in the layer grid"""
    coord_id: Optional[int]
    """IntGrid value"""
    v: Optional[int]

    def __init__(self, coord_id: Optional[int], v: Optional[int]) -> None:
        self.coord_id = coord_id
        self.v = v

    @staticmethod
    def from_dict(obj: Any) -> 'IntGridValueInstance':
        assert isinstance(obj, dict)
        coord_id = from_union([from_none, from_int], obj.get("coordId"))
        v = from_union([from_none, from_int], obj.get("v"))
        return IntGridValueInstance(coord_id, v)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordId"] = from_union([from_none, from_int], self.coord_id)
        result["v"] = from_union([from_none, from_int], self.v)
        return result


class TileInstance:
    """This structure represents a single tile from a given Tileset."""
    """Internal data used by the editor.<br/>  For auto-layer tiles: `[ruleId, coordId]`.<br/>
    For tile-layer tiles: `[coordId]`.
    """
    d: Optional[List[int]]
    """"Flip bits", a 2-bits integer to represent the mirror transformations of the tile.<br/>
    - Bit 0 = X flip<br/>   - Bit 1 = Y flip<br/>   Examples: f=0 (no flip), f=1 (X flip
    only), f=2 (Y flip only), f=3 (both flips)
    """
    f: Optional[int]
    """Pixel coordinates of the tile in the **layer** (`[x,y]` format). Don't forget optional
    layer offsets, if they exist!
    """
    px: Optional[List[int]]
    """Pixel coordinates of the tile in the **tileset** (`[x,y]` format)"""
    src: Optional[List[int]]
    """The *Tile ID* in the corresponding tileset."""
    t: Optional[int]

    def __init__(self, d: Optional[List[int]], f: Optional[int], px: Optional[List[int]], src: Optional[List[int]], t: Optional[int]) -> None:
        self.d = d
        self.f = f
        self.px = px
        self.src = src
        self.t = t

    @staticmethod
    def from_dict(obj: Any) -> 'TileInstance':
        assert isinstance(obj, dict)
        d = from_union([lambda x: from_list(from_int, x), from_none], obj.get("d"))
        f = from_union([from_none, from_int], obj.get("f"))
        px = from_union([lambda x: from_list(from_int, x), from_none], obj.get("px"))
        src = from_union([lambda x: from_list(from_int, x), from_none], obj.get("src"))
        t = from_union([from_none, from_int], obj.get("t"))
        return TileInstance(d, f, px, src, t)

    def to_dict(self) -> dict:
        result: dict = {}
        result["d"] = from_union([lambda x: from_list(from_int, x), from_none], self.d)
        result["f"] = from_union([from_none, from_int], self.f)
        result["px"] = from_union([lambda x: from_list(from_int, x), from_none], self.px)
        result["src"] = from_union([lambda x: from_list(from_int, x), from_none], self.src)
        result["t"] = from_union([from_none, from_int], self.t)
        return result


class LayerInstance:
    """Grid-based height"""
    c_hei: Optional[int]
    """Grid-based width"""
    c_wid: Optional[int]
    """Grid size"""
    grid_size: Optional[int]
    """Layer definition identifier"""
    identifier: Optional[str]
    """Layer opacity as Float [0-1]"""
    opacity: Optional[float]
    """Total layer X pixel offset, including both instance and definition offsets."""
    px_total_offset_x: Optional[int]
    """Total layer Y pixel offset, including both instance and definition offsets."""
    px_total_offset_y: Optional[int]
    """The definition UID of corresponding Tileset, if any."""
    tileset_def_uid: Optional[int]
    """The relative path to corresponding Tileset, if any."""
    tileset_rel_path: Optional[str]
    """Layer type (possible values: IntGrid, Entities, Tiles or AutoLayer)"""
    type: Optional[str]
    """An array containing all tiles generated by Auto-layer rules. The array is already sorted
    in display order (ie. 1st tile is beneath 2nd, which is beneath 3rd etc.).<br/><br/>
    Note: if multiple tiles are stacked in the same cell as the result of different rules,
    all tiles behind opaque ones will be discarded.
    """
    auto_layer_tiles: Optional[List[TileInstance]]
    entity_instances: Optional[List[EntityInstance]]
    grid_tiles: Optional[List[TileInstance]]
    """Unique layer instance identifier"""
    iid: Optional[str]
    """**WARNING**: this deprecated value is no longer exported since version 1.0.0  Replaced
    by: `intGridCsv`
    """
    int_grid: Optional[List[IntGridValueInstance]]
    """A list of all values in the IntGrid layer, stored in CSV format (Comma Separated
    Values).<br/>  Order is from left to right, and top to bottom (ie. first row from left to
    right, followed by second row, etc).<br/>  `0` means "empty cell" and IntGrid values
    start at 1.<br/>  The array size is `__cWid` x `__cHei` cells.
    """
    int_grid_csv: Optional[List[int]]
    """Reference the Layer definition UID"""
    layer_def_uid: Optional[int]
    """Reference to the UID of the level containing this layer instance"""
    level_id: Optional[int]
    """An Array containing the UIDs of optional rules that were enabled in this specific layer
    instance.
    """
    optional_rules: Optional[List[int]]
    """This layer can use another tileset by overriding the tileset UID here."""
    override_tileset_uid: Optional[int]
    """X offset in pixels to render this layer, usually 0 (IMPORTANT: this should be added to
    the `LayerDef` optional offset, see `__pxTotalOffsetX`)
    """
    px_offset_x: Optional[int]
    """Y offset in pixels to render this layer, usually 0 (IMPORTANT: this should be added to
    the `LayerDef` optional offset, see `__pxTotalOffsetY`)
    """
    px_offset_y: Optional[int]
    """Random seed used for Auto-Layers rendering"""
    seed: Optional[int]
    """Layer instance visibility"""
    visible: Optional[bool]

    def __init__(self, c_hei: Optional[int], c_wid: Optional[int], grid_size: Optional[int], identifier: Optional[str], opacity: Optional[float], px_total_offset_x: Optional[int], px_total_offset_y: Optional[int], tileset_def_uid: Optional[int], tileset_rel_path: Optional[str], type: Optional[str], auto_layer_tiles: Optional[List[TileInstance]], entity_instances: Optional[List[EntityInstance]], grid_tiles: Optional[List[TileInstance]], iid: Optional[str], int_grid: Optional[List[IntGridValueInstance]], int_grid_csv: Optional[List[int]], layer_def_uid: Optional[int], level_id: Optional[int], optional_rules: Optional[List[int]], override_tileset_uid: Optional[int], px_offset_x: Optional[int], px_offset_y: Optional[int], seed: Optional[int], visible: Optional[bool]) -> None:
        self.c_hei = c_hei
        self.c_wid = c_wid
        self.grid_size = grid_size
        self.identifier = identifier
        self.opacity = opacity
        self.px_total_offset_x = px_total_offset_x
        self.px_total_offset_y = px_total_offset_y
        self.tileset_def_uid = tileset_def_uid
        self.tileset_rel_path = tileset_rel_path
        self.type = type
        self.auto_layer_tiles = auto_layer_tiles
        self.entity_instances = entity_instances
        self.grid_tiles = grid_tiles
        self.iid = iid
        self.int_grid = int_grid
        self.int_grid_csv = int_grid_csv
        self.layer_def_uid = layer_def_uid
        self.level_id = level_id
        self.optional_rules = optional_rules
        self.override_tileset_uid = override_tileset_uid
        self.px_offset_x = px_offset_x
        self.px_offset_y = px_offset_y
        self.seed = seed
        self.visible = visible

    @staticmethod
    def from_dict(obj: Any) -> 'LayerInstance':
        assert isinstance(obj, dict)
        c_hei = from_union([from_none, from_int], obj.get("__cHei"))
        c_wid = from_union([from_none, from_int], obj.get("__cWid"))
        grid_size = from_union([from_none, from_int], obj.get("__gridSize"))
        identifier = from_union([from_str, from_none], obj.get("__identifier"))
        opacity = from_union([from_float, from_none], obj.get("__opacity"))
        px_total_offset_x = from_union([from_none, from_int], obj.get("__pxTotalOffsetX"))
        px_total_offset_y = from_union([from_none, from_int], obj.get("__pxTotalOffsetY"))
        tileset_def_uid = from_union([from_none, from_int], obj.get("__tilesetDefUid"))
        tileset_rel_path = from_union([from_none, from_str], obj.get("__tilesetRelPath"))
        type = from_union([from_str, from_none], obj.get("__type"))
        auto_layer_tiles = from_union([lambda x: from_list(TileInstance.from_dict, x), from_none], obj.get("autoLayerTiles"))
        entity_instances = from_union([lambda x: from_list(EntityInstance.from_dict, x), from_none], obj.get("entityInstances"))
        grid_tiles = from_union([lambda x: from_list(TileInstance.from_dict, x), from_none], obj.get("gridTiles"))
        iid = from_union([from_str, from_none], obj.get("iid"))
        int_grid = from_union([from_none, lambda x: from_list(IntGridValueInstance.from_dict, x)], obj.get("intGrid"))
        int_grid_csv = from_union([lambda x: from_list(from_int, x), from_none], obj.get("intGridCsv"))
        layer_def_uid = from_union([from_none, from_int], obj.get("layerDefUid"))
        level_id = from_union([from_none, from_int], obj.get("levelId"))
        optional_rules = from_union([lambda x: from_list(from_int, x), from_none], obj.get("optionalRules"))
        override_tileset_uid = from_union([from_none, from_int], obj.get("overrideTilesetUid"))
        px_offset_x = from_union([from_none, from_int], obj.get("pxOffsetX"))
        px_offset_y = from_union([from_none, from_int], obj.get("pxOffsetY"))
        seed = from_union([from_none, from_int], obj.get("seed"))
        visible = from_union([from_bool, from_none], obj.get("visible"))
        return LayerInstance(c_hei, c_wid, grid_size, identifier, opacity, px_total_offset_x, px_total_offset_y, tileset_def_uid, tileset_rel_path, type, auto_layer_tiles, entity_instances, grid_tiles, iid, int_grid, int_grid_csv, layer_def_uid, level_id, optional_rules, override_tileset_uid, px_offset_x, px_offset_y, seed, visible)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__cHei"] = from_union([from_none, from_int], self.c_hei)
        result["__cWid"] = from_union([from_none, from_int], self.c_wid)
        result["__gridSize"] = from_union([from_none, from_int], self.grid_size)
        result["__identifier"] = from_union([from_str, from_none], self.identifier)
        result["__opacity"] = from_union([to_float, from_none], self.opacity)
        result["__pxTotalOffsetX"] = from_union([from_none, from_int], self.px_total_offset_x)
        result["__pxTotalOffsetY"] = from_union([from_none, from_int], self.px_total_offset_y)
        result["__tilesetDefUid"] = from_union([from_none, from_int], self.tileset_def_uid)
        result["__tilesetRelPath"] = from_union([from_none, from_str], self.tileset_rel_path)
        result["__type"] = from_union([from_str, from_none], self.type)
        result["autoLayerTiles"] = from_union([lambda x: from_list(lambda x: to_class(TileInstance, x), x), from_none], self.auto_layer_tiles)
        result["entityInstances"] = from_union([lambda x: from_list(lambda x: to_class(EntityInstance, x), x), from_none], self.entity_instances)
        result["gridTiles"] = from_union([lambda x: from_list(lambda x: to_class(TileInstance, x), x), from_none], self.grid_tiles)
        result["iid"] = from_union([from_str, from_none], self.iid)
        result["intGrid"] = from_union([from_none, lambda x: from_list(lambda x: to_class(IntGridValueInstance, x), x)], self.int_grid)
        result["intGridCsv"] = from_union([lambda x: from_list(from_int, x), from_none], self.int_grid_csv)
        result["layerDefUid"] = from_union([from_none, from_int], self.layer_def_uid)
        result["levelId"] = from_union([from_none, from_int], self.level_id)
        result["optionalRules"] = from_union([lambda x: from_list(from_int, x), from_none], self.optional_rules)
        result["overrideTilesetUid"] = from_union([from_none, from_int], self.override_tileset_uid)
        result["pxOffsetX"] = from_union([from_none, from_int], self.px_offset_x)
        result["pxOffsetY"] = from_union([from_none, from_int], self.px_offset_y)
        result["seed"] = from_union([from_none, from_int], self.seed)
        result["visible"] = from_union([from_bool, from_none], self.visible)
        return result


class LevelBackgroundPosition:
    """Level background image position info"""
    """An array of 4 float values describing the cropped sub-rectangle of the displayed
    background image. This cropping happens when original is larger than the level bounds.
    Array format: `[ cropX, cropY, cropWidth, cropHeight ]`
    """
    crop_rect: Optional[List[float]]
    """An array containing the `[scaleX,scaleY]` values of the **cropped** background image,
    depending on `bgPos` option.
    """
    scale: Optional[List[float]]
    """An array containing the `[x,y]` pixel coordinates of the top-left corner of the
    **cropped** background image, depending on `bgPos` option.
    """
    top_left_px: Optional[List[int]]

    def __init__(self, crop_rect: Optional[List[float]], scale: Optional[List[float]], top_left_px: Optional[List[int]]) -> None:
        self.crop_rect = crop_rect
        self.scale = scale
        self.top_left_px = top_left_px

    @staticmethod
    def from_dict(obj: Any) -> 'LevelBackgroundPosition':
        assert isinstance(obj, dict)
        crop_rect = from_union([lambda x: from_list(from_float, x), from_none], obj.get("cropRect"))
        scale = from_union([lambda x: from_list(from_float, x), from_none], obj.get("scale"))
        top_left_px = from_union([lambda x: from_list(from_int, x), from_none], obj.get("topLeftPx"))
        return LevelBackgroundPosition(crop_rect, scale, top_left_px)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cropRect"] = from_union([lambda x: from_list(to_float, x), from_none], self.crop_rect)
        result["scale"] = from_union([lambda x: from_list(to_float, x), from_none], self.scale)
        result["topLeftPx"] = from_union([lambda x: from_list(from_int, x), from_none], self.top_left_px)
        return result


class BgPos(Enum):
    CONTAIN = "Contain"
    COVER = "Cover"
    COVER_DIRTY = "CoverDirty"
    UNSCALED = "Unscaled"


class NeighbourLevel:
    """Nearby level info"""
    """A single lowercase character tipping on the level location (`n`orth, `s`outh, `w`est,
    `e`ast).
    """
    dir: Optional[str]
    """Neighbour Instance Identifier"""
    level_iid: Optional[str]
    """**WARNING**: this deprecated value will be *removed* completely on version 1.2.0+
    Replaced by: `levelIid`
    """
    level_uid: Optional[int]

    def __init__(self, dir: Optional[str], level_iid: Optional[str], level_uid: Optional[int]) -> None:
        self.dir = dir
        self.level_iid = level_iid
        self.level_uid = level_uid

    @staticmethod
    def from_dict(obj: Any) -> 'NeighbourLevel':
        assert isinstance(obj, dict)
        dir = from_union([from_str, from_none], obj.get("dir"))
        level_iid = from_union([from_str, from_none], obj.get("levelIid"))
        level_uid = from_union([from_none, from_int], obj.get("levelUid"))
        return NeighbourLevel(dir, level_iid, level_uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dir"] = from_union([from_str, from_none], self.dir)
        result["levelIid"] = from_union([from_str, from_none], self.level_iid)
        result["levelUid"] = from_union([from_none, from_int], self.level_uid)
        return result


class Level:
    """This section contains all the level data. It can be found in 2 distinct forms, depending
    on Project current settings:  - If "*Separate level files*" is **disabled** (default):
    full level data is *embedded* inside the main Project JSON file, - If "*Separate level
    files*" is **enabled**: level data is stored in *separate* standalone `.ldtkl` files (one
    per level). In this case, the main Project JSON file will still contain most level data,
    except heavy sections, like the `layerInstances` array (which will be null). The
    `externalRelPath` string points to the `ldtkl` file.  A `ldtkl` file is just a JSON file
    containing exactly what is described below.
    """
    """Background color of the level (same as `bgColor`, except the default value is
    automatically used here if its value is `null`)
    """
    bg_color: Optional[str]
    """Position informations of the background image, if there is one."""
    bg_pos: Optional[LevelBackgroundPosition]
    """An array listing all other levels touching this one on the world map.<br/>  Only relevant
    for world layouts where level spatial positioning is manual (ie. GridVania, Free). For
    Horizontal and Vertical layouts, this array is always empty.
    """
    neighbours: Optional[List[NeighbourLevel]]
    """The "guessed" color for this level in the editor, decided using either the background
    color or an existing custom field.
    """
    smart_color: Optional[str]
    """Background color of the level. If `null`, the project `defaultLevelBgColor` should be
    used.
    """
    level_bg_color: Optional[str]
    """Background image X pivot (0-1)"""
    bg_pivot_x: Optional[float]
    """Background image Y pivot (0-1)"""
    bg_pivot_y: Optional[float]
    """An enum defining the way the background image (if any) is positioned on the level. See
    `__bgPos` for resulting position info. Possible values: &lt;`null`&gt;, `Unscaled`,
    `Contain`, `Cover`, `CoverDirty`
    """
    level_bg_pos: Optional[BgPos]
    """The *optional* relative path to the level background image."""
    bg_rel_path: Optional[str]
    """This value is not null if the project option "*Save levels separately*" is enabled. In
    this case, this **relative** path points to the level Json file.
    """
    external_rel_path: Optional[str]
    """An array containing this level custom field values."""
    field_instances: Optional[List[FieldInstance]]
    """User defined unique identifier"""
    identifier: Optional[str]
    """Unique instance identifier"""
    iid: Optional[str]
    """An array containing all Layer instances. **IMPORTANT**: if the project option "*Save
    levels separately*" is enabled, this field will be `null`.<br/>  This array is **sorted
    in display order**: the 1st layer is the top-most and the last is behind.
    """
    layer_instances: Optional[List[LayerInstance]]
    """Height of the level in pixels"""
    px_hei: Optional[int]
    """Width of the level in pixels"""
    px_wid: Optional[int]
    """Unique Int identifier"""
    uid: Optional[int]
    """If TRUE, the level identifier will always automatically use the naming pattern as defined
    in `Project.levelNamePattern`. Becomes FALSE if the identifier is manually modified by
    user.
    """
    use_auto_identifier: Optional[bool]
    """Index that represents the "depth" of the level in the world. Default is 0, greater means
    "above", lower means "below".<br/>  This value is mostly used for display only and is
    intended to make stacking of levels easier to manage.
    """
    world_depth: Optional[int]
    """World X coordinate in pixels.<br/>  Only relevant for world layouts where level spatial
    positioning is manual (ie. GridVania, Free). For Horizontal and Vertical layouts, the
    value is always -1 here.
    """
    world_x: Optional[int]
    """World Y coordinate in pixels.<br/>  Only relevant for world layouts where level spatial
    positioning is manual (ie. GridVania, Free). For Horizontal and Vertical layouts, the
    value is always -1 here.
    """
    world_y: Optional[int]

    def __init__(self, bg_color: Optional[str], bg_pos: Optional[LevelBackgroundPosition], neighbours: Optional[List[NeighbourLevel]], smart_color: Optional[str], level_bg_color: Optional[str], bg_pivot_x: Optional[float], bg_pivot_y: Optional[float], level_bg_pos: Optional[BgPos], bg_rel_path: Optional[str], external_rel_path: Optional[str], field_instances: Optional[List[FieldInstance]], identifier: Optional[str], iid: Optional[str], layer_instances: Optional[List[LayerInstance]], px_hei: Optional[int], px_wid: Optional[int], uid: Optional[int], use_auto_identifier: Optional[bool], world_depth: Optional[int], world_x: Optional[int], world_y: Optional[int]) -> None:
        self.bg_color = bg_color
        self.bg_pos = bg_pos
        self.neighbours = neighbours
        self.smart_color = smart_color
        self.level_bg_color = level_bg_color
        self.bg_pivot_x = bg_pivot_x
        self.bg_pivot_y = bg_pivot_y
        self.level_bg_pos = level_bg_pos
        self.bg_rel_path = bg_rel_path
        self.external_rel_path = external_rel_path
        self.field_instances = field_instances
        self.identifier = identifier
        self.iid = iid
        self.layer_instances = layer_instances
        self.px_hei = px_hei
        self.px_wid = px_wid
        self.uid = uid
        self.use_auto_identifier = use_auto_identifier
        self.world_depth = world_depth
        self.world_x = world_x
        self.world_y = world_y

    @staticmethod
    def from_dict(obj: Any) -> 'Level':
        assert isinstance(obj, dict)
        bg_color = from_union([from_str, from_none], obj.get("__bgColor"))
        bg_pos = from_union([from_none, LevelBackgroundPosition.from_dict], obj.get("__bgPos"))
        neighbours = from_union([lambda x: from_list(NeighbourLevel.from_dict, x), from_none], obj.get("__neighbours"))
        smart_color = from_union([from_str, from_none], obj.get("__smartColor"))
        level_bg_color = from_union([from_none, from_str], obj.get("bgColor"))
        bg_pivot_x = from_union([from_float, from_none], obj.get("bgPivotX"))
        bg_pivot_y = from_union([from_float, from_none], obj.get("bgPivotY"))
        level_bg_pos = from_union([from_none, BgPos], obj.get("bgPos"))
        bg_rel_path = from_union([from_none, from_str], obj.get("bgRelPath"))
        external_rel_path = from_union([from_none, from_str], obj.get("externalRelPath"))
        field_instances = from_union([lambda x: from_list(FieldInstance.from_dict, x), from_none], obj.get("fieldInstances"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        iid = from_union([from_str, from_none], obj.get("iid"))
        layer_instances = from_union([from_none, lambda x: from_list(LayerInstance.from_dict, x)], obj.get("layerInstances"))
        px_hei = from_union([from_none, from_int], obj.get("pxHei"))
        px_wid = from_union([from_none, from_int], obj.get("pxWid"))
        uid = from_union([from_none, from_int], obj.get("uid"))
        use_auto_identifier = from_union([from_bool, from_none], obj.get("useAutoIdentifier"))
        world_depth = from_union([from_none, from_int], obj.get("worldDepth"))
        world_x = from_union([from_none, from_int], obj.get("worldX"))
        world_y = from_union([from_none, from_int], obj.get("worldY"))
        return Level(bg_color, bg_pos, neighbours, smart_color, level_bg_color, bg_pivot_x, bg_pivot_y, level_bg_pos, bg_rel_path, external_rel_path, field_instances, identifier, iid, layer_instances, px_hei, px_wid, uid, use_auto_identifier, world_depth, world_x, world_y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__bgColor"] = from_union([from_str, from_none], self.bg_color)
        result["__bgPos"] = from_union([from_none, lambda x: to_class(LevelBackgroundPosition, x)], self.bg_pos)
        result["__neighbours"] = from_union([lambda x: from_list(lambda x: to_class(NeighbourLevel, x), x), from_none], self.neighbours)
        result["__smartColor"] = from_union([from_str, from_none], self.smart_color)
        result["bgColor"] = from_union([from_none, from_str], self.level_bg_color)
        result["bgPivotX"] = from_union([to_float, from_none], self.bg_pivot_x)
        result["bgPivotY"] = from_union([to_float, from_none], self.bg_pivot_y)
        result["bgPos"] = from_union([from_none, lambda x: to_enum(BgPos, x)], self.level_bg_pos)
        result["bgRelPath"] = from_union([from_none, from_str], self.bg_rel_path)
        result["externalRelPath"] = from_union([from_none, from_str], self.external_rel_path)
        result["fieldInstances"] = from_union([lambda x: from_list(lambda x: to_class(FieldInstance, x), x), from_none], self.field_instances)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["iid"] = from_union([from_str, from_none], self.iid)
        result["layerInstances"] = from_union([from_none, lambda x: from_list(lambda x: to_class(LayerInstance, x), x)], self.layer_instances)
        result["pxHei"] = from_union([from_none, from_int], self.px_hei)
        result["pxWid"] = from_union([from_none, from_int], self.px_wid)
        result["uid"] = from_union([from_none, from_int], self.uid)
        result["useAutoIdentifier"] = from_union([from_bool, from_none], self.use_auto_identifier)
        result["worldDepth"] = from_union([from_none, from_int], self.world_depth)
        result["worldX"] = from_union([from_none, from_int], self.world_x)
        result["worldY"] = from_union([from_none, from_int], self.world_y)
        return result


class WorldLayout(Enum):
    FREE = "Free"
    GRID_VANIA = "GridVania"
    LINEAR_HORIZONTAL = "LinearHorizontal"
    LINEAR_VERTICAL = "LinearVertical"


class World:
    """**IMPORTANT**: this type is not used *yet* in current LDtk version. It's only presented
    here as a preview of a planned feature.  A World contains multiple levels, and it has its
    own layout settings.
    """
    """Default new level height"""
    default_level_height: Optional[int]
    """Default new level width"""
    default_level_width: Optional[int]
    """User defined unique identifier"""
    identifier: Optional[str]
    """Unique instance identifer"""
    iid: Optional[str]
    """All levels from this world. The order of this array is only relevant in
    `LinearHorizontal` and `linearVertical` world layouts (see `worldLayout` value).
    Otherwise, you should refer to the `worldX`,`worldY` coordinates of each Level.
    """
    levels: Optional[List[Level]]
    """Height of the world grid in pixels."""
    world_grid_height: Optional[int]
    """Width of the world grid in pixels."""
    world_grid_width: Optional[int]
    """An enum that describes how levels are organized in this project (ie. linearly or in a 2D
    space). Possible values: `Free`, `GridVania`, `LinearHorizontal`, `LinearVertical`, `null`
    """
    world_layout: Optional[WorldLayout]

    def __init__(self, default_level_height: Optional[int], default_level_width: Optional[int], identifier: Optional[str], iid: Optional[str], levels: Optional[List[Level]], world_grid_height: Optional[int], world_grid_width: Optional[int], world_layout: Optional[WorldLayout]) -> None:
        self.default_level_height = default_level_height
        self.default_level_width = default_level_width
        self.identifier = identifier
        self.iid = iid
        self.levels = levels
        self.world_grid_height = world_grid_height
        self.world_grid_width = world_grid_width
        self.world_layout = world_layout

    @staticmethod
    def from_dict(obj: Any) -> 'World':
        assert isinstance(obj, dict)
        default_level_height = from_union([from_none, from_int], obj.get("defaultLevelHeight"))
        default_level_width = from_union([from_none, from_int], obj.get("defaultLevelWidth"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        iid = from_union([from_str, from_none], obj.get("iid"))
        levels = from_union([lambda x: from_list(Level.from_dict, x), from_none], obj.get("levels"))
        world_grid_height = from_union([from_none, from_int], obj.get("worldGridHeight"))
        world_grid_width = from_union([from_none, from_int], obj.get("worldGridWidth"))
        world_layout = from_union([from_none, WorldLayout], obj.get("worldLayout"))
        return World(default_level_height, default_level_width, identifier, iid, levels, world_grid_height, world_grid_width, world_layout)

    def to_dict(self) -> dict:
        result: dict = {}
        result["defaultLevelHeight"] = from_union([from_none, from_int], self.default_level_height)
        result["defaultLevelWidth"] = from_union([from_none, from_int], self.default_level_width)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        result["iid"] = from_union([from_str, from_none], self.iid)
        result["levels"] = from_union([lambda x: from_list(lambda x: to_class(Level, x), x), from_none], self.levels)
        result["worldGridHeight"] = from_union([from_none, from_int], self.world_grid_height)
        result["worldGridWidth"] = from_union([from_none, from_int], self.world_grid_width)
        result["worldLayout"] = from_union([from_none, lambda x: to_enum(WorldLayout, x)], self.world_layout)
        return result


class ForcedRefs:
    """This object is not actually used by LDtk. It ONLY exists to force explicit references to
    all types, to make sure QuickType finds them and integrate all of them. Otherwise,
    Quicktype will drop types that are not explicitely used.
    """
    auto_layer_rule_group: Optional[AutoLayerRuleGroup]
    auto_rule_def: Optional[AutoLayerRuleDefinition]
    definitions: Optional[Definitions]
    entity_def: Optional[EntityDefinition]
    entity_instance: Optional[EntityInstance]
    entity_reference_infos: Optional[FieldInstanceEntityReference]
    enum_def: Optional[EnumDefinition]
    enum_def_values: Optional[EnumValueDefinition]
    enum_tag_value: Optional[EnumTagValue]
    field_def: Optional[FieldDefinition]
    field_instance: Optional[FieldInstance]
    grid_point: Optional[FieldInstanceGridPoint]
    int_grid_value_def: Optional[IntGridValueDefinition]
    int_grid_value_instance: Optional[IntGridValueInstance]
    layer_def: Optional[LayerDefinition]
    layer_instance: Optional[LayerInstance]
    level: Optional[Level]
    level_bg_pos_infos: Optional[LevelBackgroundPosition]
    neighbour_level: Optional[NeighbourLevel]
    tile: Optional[TileInstance]
    tile_custom_metadata: Optional[TileCustomMetadata]
    tileset_def: Optional[TilesetDefinition]
    tileset_rect: Optional[TilesetRectangle]
    world: Optional[World]

    def __init__(self, auto_layer_rule_group: Optional[AutoLayerRuleGroup], auto_rule_def: Optional[AutoLayerRuleDefinition], definitions: Optional[Definitions], entity_def: Optional[EntityDefinition], entity_instance: Optional[EntityInstance], entity_reference_infos: Optional[FieldInstanceEntityReference], enum_def: Optional[EnumDefinition], enum_def_values: Optional[EnumValueDefinition], enum_tag_value: Optional[EnumTagValue], field_def: Optional[FieldDefinition], field_instance: Optional[FieldInstance], grid_point: Optional[FieldInstanceGridPoint], int_grid_value_def: Optional[IntGridValueDefinition], int_grid_value_instance: Optional[IntGridValueInstance], layer_def: Optional[LayerDefinition], layer_instance: Optional[LayerInstance], level: Optional[Level], level_bg_pos_infos: Optional[LevelBackgroundPosition], neighbour_level: Optional[NeighbourLevel], tile: Optional[TileInstance], tile_custom_metadata: Optional[TileCustomMetadata], tileset_def: Optional[TilesetDefinition], tileset_rect: Optional[TilesetRectangle], world: Optional[World]) -> None:
        self.auto_layer_rule_group = auto_layer_rule_group
        self.auto_rule_def = auto_rule_def
        self.definitions = definitions
        self.entity_def = entity_def
        self.entity_instance = entity_instance
        self.entity_reference_infos = entity_reference_infos
        self.enum_def = enum_def
        self.enum_def_values = enum_def_values
        self.enum_tag_value = enum_tag_value
        self.field_def = field_def
        self.field_instance = field_instance
        self.grid_point = grid_point
        self.int_grid_value_def = int_grid_value_def
        self.int_grid_value_instance = int_grid_value_instance
        self.layer_def = layer_def
        self.layer_instance = layer_instance
        self.level = level
        self.level_bg_pos_infos = level_bg_pos_infos
        self.neighbour_level = neighbour_level
        self.tile = tile
        self.tile_custom_metadata = tile_custom_metadata
        self.tileset_def = tileset_def
        self.tileset_rect = tileset_rect
        self.world = world

    @staticmethod
    def from_dict(obj: Any) -> 'ForcedRefs':
        assert isinstance(obj, dict)
        auto_layer_rule_group = from_union([AutoLayerRuleGroup.from_dict, from_none], obj.get("AutoLayerRuleGroup"))
        auto_rule_def = from_union([AutoLayerRuleDefinition.from_dict, from_none], obj.get("AutoRuleDef"))
        definitions = from_union([Definitions.from_dict, from_none], obj.get("Definitions"))
        entity_def = from_union([EntityDefinition.from_dict, from_none], obj.get("EntityDef"))
        entity_instance = from_union([EntityInstance.from_dict, from_none], obj.get("EntityInstance"))
        entity_reference_infos = from_union([FieldInstanceEntityReference.from_dict, from_none], obj.get("EntityReferenceInfos"))
        enum_def = from_union([EnumDefinition.from_dict, from_none], obj.get("EnumDef"))
        enum_def_values = from_union([EnumValueDefinition.from_dict, from_none], obj.get("EnumDefValues"))
        enum_tag_value = from_union([EnumTagValue.from_dict, from_none], obj.get("EnumTagValue"))
        field_def = from_union([FieldDefinition.from_dict, from_none], obj.get("FieldDef"))
        field_instance = from_union([FieldInstance.from_dict, from_none], obj.get("FieldInstance"))
        grid_point = from_union([FieldInstanceGridPoint.from_dict, from_none], obj.get("GridPoint"))
        int_grid_value_def = from_union([IntGridValueDefinition.from_dict, from_none], obj.get("IntGridValueDef"))
        int_grid_value_instance = from_union([IntGridValueInstance.from_dict, from_none], obj.get("IntGridValueInstance"))
        layer_def = from_union([LayerDefinition.from_dict, from_none], obj.get("LayerDef"))
        layer_instance = from_union([LayerInstance.from_dict, from_none], obj.get("LayerInstance"))
        level = from_union([Level.from_dict, from_none], obj.get("Level"))
        level_bg_pos_infos = from_union([from_none, LevelBackgroundPosition.from_dict], obj.get("LevelBgPosInfos"))
        neighbour_level = from_union([NeighbourLevel.from_dict, from_none], obj.get("NeighbourLevel"))
        tile = from_union([TileInstance.from_dict, from_none], obj.get("Tile"))
        tile_custom_metadata = from_union([TileCustomMetadata.from_dict, from_none], obj.get("TileCustomMetadata"))
        tileset_def = from_union([TilesetDefinition.from_dict, from_none], obj.get("TilesetDef"))
        tileset_rect = from_union([from_none, TilesetRectangle.from_dict], obj.get("TilesetRect"))
        world = from_union([World.from_dict, from_none], obj.get("World"))
        return ForcedRefs(auto_layer_rule_group, auto_rule_def, definitions, entity_def, entity_instance, entity_reference_infos, enum_def, enum_def_values, enum_tag_value, field_def, field_instance, grid_point, int_grid_value_def, int_grid_value_instance, layer_def, layer_instance, level, level_bg_pos_infos, neighbour_level, tile, tile_custom_metadata, tileset_def, tileset_rect, world)

    def to_dict(self) -> dict:
        result: dict = {}
        result["AutoLayerRuleGroup"] = from_union([lambda x: to_class(AutoLayerRuleGroup, x), from_none], self.auto_layer_rule_group)
        result["AutoRuleDef"] = from_union([lambda x: to_class(AutoLayerRuleDefinition, x), from_none], self.auto_rule_def)
        result["Definitions"] = from_union([lambda x: to_class(Definitions, x), from_none], self.definitions)
        result["EntityDef"] = from_union([lambda x: to_class(EntityDefinition, x), from_none], self.entity_def)
        result["EntityInstance"] = from_union([lambda x: to_class(EntityInstance, x), from_none], self.entity_instance)
        result["EntityReferenceInfos"] = from_union([lambda x: to_class(FieldInstanceEntityReference, x), from_none], self.entity_reference_infos)
        result["EnumDef"] = from_union([lambda x: to_class(EnumDefinition, x), from_none], self.enum_def)
        result["EnumDefValues"] = from_union([lambda x: to_class(EnumValueDefinition, x), from_none], self.enum_def_values)
        result["EnumTagValue"] = from_union([lambda x: to_class(EnumTagValue, x), from_none], self.enum_tag_value)
        result["FieldDef"] = from_union([lambda x: to_class(FieldDefinition, x), from_none], self.field_def)
        result["FieldInstance"] = from_union([lambda x: to_class(FieldInstance, x), from_none], self.field_instance)
        result["GridPoint"] = from_union([lambda x: to_class(FieldInstanceGridPoint, x), from_none], self.grid_point)
        result["IntGridValueDef"] = from_union([lambda x: to_class(IntGridValueDefinition, x), from_none], self.int_grid_value_def)
        result["IntGridValueInstance"] = from_union([lambda x: to_class(IntGridValueInstance, x), from_none], self.int_grid_value_instance)
        result["LayerDef"] = from_union([lambda x: to_class(LayerDefinition, x), from_none], self.layer_def)
        result["LayerInstance"] = from_union([lambda x: to_class(LayerInstance, x), from_none], self.layer_instance)
        result["Level"] = from_union([lambda x: to_class(Level, x), from_none], self.level)
        result["LevelBgPosInfos"] = from_union([from_none, lambda x: to_class(LevelBackgroundPosition, x)], self.level_bg_pos_infos)
        result["NeighbourLevel"] = from_union([lambda x: to_class(NeighbourLevel, x), from_none], self.neighbour_level)
        result["Tile"] = from_union([lambda x: to_class(TileInstance, x), from_none], self.tile)
        result["TileCustomMetadata"] = from_union([lambda x: to_class(TileCustomMetadata, x), from_none], self.tile_custom_metadata)
        result["TilesetDef"] = from_union([lambda x: to_class(TilesetDefinition, x), from_none], self.tileset_def)
        result["TilesetRect"] = from_union([from_none, lambda x: to_class(TilesetRectangle, x)], self.tileset_rect)
        result["World"] = from_union([lambda x: to_class(World, x), from_none], self.world)
        return result


class IdentifierStyle(Enum):
    """Naming convention for Identifiers (first-letter uppercase, full uppercase etc.) Possible
    values: `Capitalize`, `Uppercase`, `Lowercase`, `Free`
    """
    CAPITALIZE = "Capitalize"
    FREE = "Free"
    LOWERCASE = "Lowercase"
    UPPERCASE = "Uppercase"


class ImageExportMode(Enum):
    """"Image export" option when saving project. Possible values: `None`, `OneImagePerLayer`,
    `OneImagePerLevel`, `LayersAndLevels`
    """
    LAYERS_AND_LEVELS = "LayersAndLevels"
    NONE = "None"
    ONE_IMAGE_PER_LAYER = "OneImagePerLayer"
    ONE_IMAGE_PER_LEVEL = "OneImagePerLevel"


class Ldtk:
    """This file is a JSON schema of files created by LDtk level editor (https://ldtk.io).
    
    This is the root of any Project JSON file. It contains:  - the project settings, - an
    array of levels, - a group of definitions (that can probably be safely ignored for most
    users).
    """
    """This object is not actually used by LDtk. It ONLY exists to force explicit references to
    all types, to make sure QuickType finds them and integrate all of them. Otherwise,
    Quicktype will drop types that are not explicitely used.
    """
    forced_refs: Optional[ForcedRefs]
    """LDtk application build identifier.<br/>  This is only used to identify the LDtk version
    that generated this particular project file, which can be useful for specific bug fixing.
    Note that the build identifier is just the date of the release, so it's not unique to
    each user (one single global ID per LDtk public release), and as a result, completely
    anonymous.
    """
    app_build_id: Optional[float]
    """Number of backup files to keep, if the `backupOnSave` is TRUE"""
    backup_limit: Optional[int]
    """If TRUE, an extra copy of the project will be created in a sub folder, when saving."""
    backup_on_save: Optional[bool]
    """Project background color"""
    bg_color: Optional[str]
    """Default grid size for new layers"""
    default_grid_size: Optional[int]
    """Default background color of levels"""
    default_level_bg_color: Optional[str]
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Default new level height
    """
    default_level_height: Optional[int]
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Default new level width
    """
    default_level_width: Optional[int]
    """Default X pivot (0 to 1) for new entities"""
    default_pivot_x: Optional[float]
    """Default Y pivot (0 to 1) for new entities"""
    default_pivot_y: Optional[float]
    """A structure containing all the definitions of this project"""
    defs: Optional[Definitions]
    """**WARNING**: this deprecated value is no longer exported since version 0.9.3  Replaced
    by: `imageExportMode`
    """
    export_png: Optional[bool]
    """If TRUE, a Tiled compatible file will also be generated along with the LDtk JSON file
    (default is FALSE)
    """
    export_tiled: Optional[bool]
    """If TRUE, one file will be saved for the project (incl. all its definitions) and one file
    in a sub-folder for each level.
    """
    external_levels: Optional[bool]
    """An array containing various advanced flags (ie. options or other states). Possible
    values: `DiscardPreCsvIntGrid`, `ExportPreCsvIntGridFormat`, `IgnoreBackupSuggest`,
    `PrependIndexToLevelFileNames`, `MultiWorlds`, `UseMultilinesType`
    """
    flags: Optional[List[Flag]]
    """Naming convention for Identifiers (first-letter uppercase, full uppercase etc.) Possible
    values: `Capitalize`, `Uppercase`, `Lowercase`, `Free`
    """
    identifier_style: Optional[IdentifierStyle]
    """"Image export" option when saving project. Possible values: `None`, `OneImagePerLayer`,
    `OneImagePerLevel`, `LayersAndLevels`
    """
    image_export_mode: Optional[ImageExportMode]
    """File format version"""
    json_version: Optional[str]
    """The default naming convention for level identifiers."""
    level_name_pattern: Optional[str]
    """All levels. The order of this array is only relevant in `LinearHorizontal` and
    `linearVertical` world layouts (see `worldLayout` value).<br/>  Otherwise, you should
    refer to the `worldX`,`worldY` coordinates of each Level.
    """
    levels: Optional[List[Level]]
    """If TRUE, the Json is partially minified (no indentation, nor line breaks, default is
    FALSE)
    """
    minify_json: Optional[bool]
    """Next Unique integer ID available"""
    next_uid: Optional[int]
    """File naming pattern for exported PNGs"""
    png_file_pattern: Optional[str]
    """If TRUE, a very simplified will be generated on saving, for quicker & easier engine
    integration.
    """
    simplified_export: Optional[bool]
    """This optional description is used by LDtk Samples to show up some informations and
    instructions.
    """
    tutorial_desc: Optional[str]
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Height of the world grid in pixels.
    """
    world_grid_height: Optional[int]
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Width of the world grid in pixels.
    """
    world_grid_width: Optional[int]
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  An enum that describes how levels are organized in
    this project (ie. linearly or in a 2D space). Possible values: &lt;`null`&gt;, `Free`,
    `GridVania`, `LinearHorizontal`, `LinearVertical`
    """
    world_layout: Optional[WorldLayout]
    """This array is not used yet in current LDtk version (so, for now, it's always
    empty).<br/><br/>In a later update, it will be possible to have multiple Worlds in a
    single project, each containing multiple Levels.<br/><br/>What will change when "Multiple
    worlds" support will be added to LDtk:<br/><br/> - in current version, a LDtk project
    file can only contain a single world with multiple levels in it. In this case, levels and
    world layout related settings are stored in the root of the JSON.<br/> - after the
    "Multiple worlds" update, there will be a `worlds` array in root, each world containing
    levels and layout settings. Basically, it's pretty much only about moving the `levels`
    array to the `worlds` array, along with world layout related values (eg. `worldGridWidth`
    etc).<br/><br/>If you want to start supporting this future update easily, please refer to
    this documentation: https://github.com/deepnight/ldtk/issues/231
    """
    worlds: Optional[List[World]]

    def __init__(self, forced_refs: Optional[ForcedRefs], app_build_id: Optional[float], backup_limit: Optional[int], backup_on_save: Optional[bool], bg_color: Optional[str], default_grid_size: Optional[int], default_level_bg_color: Optional[str], default_level_height: Optional[int], default_level_width: Optional[int], default_pivot_x: Optional[float], default_pivot_y: Optional[float], defs: Optional[Definitions], export_png: Optional[bool], export_tiled: Optional[bool], external_levels: Optional[bool], flags: Optional[List[Flag]], identifier_style: Optional[IdentifierStyle], image_export_mode: Optional[ImageExportMode], json_version: Optional[str], level_name_pattern: Optional[str], levels: Optional[List[Level]], minify_json: Optional[bool], next_uid: Optional[int], png_file_pattern: Optional[str], simplified_export: Optional[bool], tutorial_desc: Optional[str], world_grid_height: Optional[int], world_grid_width: Optional[int], world_layout: Optional[WorldLayout], worlds: Optional[List[World]]) -> None:
        self.forced_refs = forced_refs
        self.app_build_id = app_build_id
        self.backup_limit = backup_limit
        self.backup_on_save = backup_on_save
        self.bg_color = bg_color
        self.default_grid_size = default_grid_size
        self.default_level_bg_color = default_level_bg_color
        self.default_level_height = default_level_height
        self.default_level_width = default_level_width
        self.default_pivot_x = default_pivot_x
        self.default_pivot_y = default_pivot_y
        self.defs = defs
        self.export_png = export_png
        self.export_tiled = export_tiled
        self.external_levels = external_levels
        self.flags = flags
        self.identifier_style = identifier_style
        self.image_export_mode = image_export_mode
        self.json_version = json_version
        self.level_name_pattern = level_name_pattern
        self.levels = levels
        self.minify_json = minify_json
        self.next_uid = next_uid
        self.png_file_pattern = png_file_pattern
        self.simplified_export = simplified_export
        self.tutorial_desc = tutorial_desc
        self.world_grid_height = world_grid_height
        self.world_grid_width = world_grid_width
        self.world_layout = world_layout
        self.worlds = worlds

    @staticmethod
    def from_dict(obj: Any) -> 'Ldtk':
        assert isinstance(obj, dict)
        forced_refs = from_union([ForcedRefs.from_dict, from_none], obj.get("__FORCED_REFS"))
        app_build_id = from_union([from_float, from_none], obj.get("appBuildId"))
        backup_limit = from_union([from_none, from_int], obj.get("backupLimit"))
        backup_on_save = from_union([from_bool, from_none], obj.get("backupOnSave"))
        bg_color = from_union([from_str, from_none], obj.get("bgColor"))
        default_grid_size = from_union([from_none, from_int], obj.get("defaultGridSize"))
        default_level_bg_color = from_union([from_str, from_none], obj.get("defaultLevelBgColor"))
        default_level_height = from_union([from_none, from_int], obj.get("defaultLevelHeight"))
        default_level_width = from_union([from_none, from_int], obj.get("defaultLevelWidth"))
        default_pivot_x = from_union([from_float, from_none], obj.get("defaultPivotX"))
        default_pivot_y = from_union([from_float, from_none], obj.get("defaultPivotY"))
        defs = from_union([Definitions.from_dict, from_none], obj.get("defs"))
        export_png = from_union([from_bool, from_none], obj.get("exportPng"))
        export_tiled = from_union([from_bool, from_none], obj.get("exportTiled"))
        external_levels = from_union([from_bool, from_none], obj.get("externalLevels"))
        flags = from_union([lambda x: from_list(Flag, x), from_none], obj.get("flags"))
        identifier_style = from_union([IdentifierStyle, from_none], obj.get("identifierStyle"))
        image_export_mode = from_union([ImageExportMode, from_none], obj.get("imageExportMode"))
        json_version = from_union([from_str, from_none], obj.get("jsonVersion"))
        level_name_pattern = from_union([from_str, from_none], obj.get("levelNamePattern"))
        levels = from_union([lambda x: from_list(Level.from_dict, x), from_none], obj.get("levels"))
        minify_json = from_union([from_bool, from_none], obj.get("minifyJson"))
        next_uid = from_union([from_none, from_int], obj.get("nextUid"))
        png_file_pattern = from_union([from_none, from_str], obj.get("pngFilePattern"))
        simplified_export = from_union([from_bool, from_none], obj.get("simplifiedExport"))
        tutorial_desc = from_union([from_none, from_str], obj.get("tutorialDesc"))
        world_grid_height = from_union([from_none, from_int], obj.get("worldGridHeight"))
        world_grid_width = from_union([from_none, from_int], obj.get("worldGridWidth"))
        world_layout = from_union([from_none, WorldLayout], obj.get("worldLayout"))
        worlds = from_union([lambda x: from_list(World.from_dict, x), from_none], obj.get("worlds"))
        return Ldtk(forced_refs, app_build_id, backup_limit, backup_on_save, bg_color, default_grid_size, default_level_bg_color, default_level_height, default_level_width, default_pivot_x, default_pivot_y, defs, export_png, export_tiled, external_levels, flags, identifier_style, image_export_mode, json_version, level_name_pattern, levels, minify_json, next_uid, png_file_pattern, simplified_export, tutorial_desc, world_grid_height, world_grid_width, world_layout, worlds)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__FORCED_REFS"] = from_union([lambda x: to_class(ForcedRefs, x), from_none], self.forced_refs)
        result["appBuildId"] = from_union([to_float, from_none], self.app_build_id)
        result["backupLimit"] = from_union([from_none, from_int], self.backup_limit)
        result["backupOnSave"] = from_union([from_bool, from_none], self.backup_on_save)
        result["bgColor"] = from_union([from_str, from_none], self.bg_color)
        result["defaultGridSize"] = from_union([from_none, from_int], self.default_grid_size)
        result["defaultLevelBgColor"] = from_union([from_str, from_none], self.default_level_bg_color)
        result["defaultLevelHeight"] = from_union([from_none, from_int], self.default_level_height)
        result["defaultLevelWidth"] = from_union([from_none, from_int], self.default_level_width)
        result["defaultPivotX"] = from_union([to_float, from_none], self.default_pivot_x)
        result["defaultPivotY"] = from_union([to_float, from_none], self.default_pivot_y)
        result["defs"] = from_union([lambda x: to_class(Definitions, x), from_none], self.defs)
        result["exportPng"] = from_union([from_bool, from_none], self.export_png)
        result["exportTiled"] = from_union([from_bool, from_none], self.export_tiled)
        result["externalLevels"] = from_union([from_bool, from_none], self.external_levels)
        result["flags"] = from_union([lambda x: from_list(lambda x: to_enum(Flag, x), x), from_none], self.flags)
        result["identifierStyle"] = from_union([lambda x: to_enum(IdentifierStyle, x), from_none], self.identifier_style)
        result["imageExportMode"] = from_union([lambda x: to_enum(ImageExportMode, x), from_none], self.image_export_mode)
        result["jsonVersion"] = from_union([from_str, from_none], self.json_version)
        result["levelNamePattern"] = from_union([from_str, from_none], self.level_name_pattern)
        result["levels"] = from_union([lambda x: from_list(lambda x: to_class(Level, x), x), from_none], self.levels)
        result["minifyJson"] = from_union([from_bool, from_none], self.minify_json)
        result["nextUid"] = from_union([from_none, from_int], self.next_uid)
        result["pngFilePattern"] = from_union([from_none, from_str], self.png_file_pattern)
        result["simplifiedExport"] = from_union([from_bool, from_none], self.simplified_export)
        result["tutorialDesc"] = from_union([from_none, from_str], self.tutorial_desc)
        result["worldGridHeight"] = from_union([from_none, from_int], self.world_grid_height)
        result["worldGridWidth"] = from_union([from_none, from_int], self.world_grid_width)
        result["worldLayout"] = from_union([from_none, lambda x: to_enum(WorldLayout, x)], self.world_layout)
        result["worlds"] = from_union([lambda x: from_list(lambda x: to_class(World, x), x), from_none], self.worlds)
        return result


def ldtk_from_dict(s: Any) -> Ldtk:
    return Ldtk.from_dict(s)


def ldtk_to_dict(x: Ldtk) -> Any:
    return to_class(Ldtk, x)
