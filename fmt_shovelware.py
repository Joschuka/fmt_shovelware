# Version 0.1
from inc_noesis import *
from ctypes import c_uint32

decompDump = False

def registerNoesisTypes():
    handle = noesis.register("Shovelware bundle",".bundle")
    noesis.setHandlerTypeCheck(handle, CheckTextureType)
    noesis.setHandlerLoadRGBA(handle, LoadRGBA)
    handle = noesis.register("Shovelware swizzle",".swizzle")
    noesis.setHandlerTypeCheck(handle, CheckSwTextureType)
    noesis.setHandlerWriteRGBA(handle, WriteRGBA)
    return 1
    
def Align(bs, n):
    value = bs.tell() % n
    if (value):
        bs.seek(n - value, 1)

def CheckTextureType(data):
    bs = NoeBitStream(data, 1)
    if bs.readUInt64() != 6155973689633821440:
        return 0
    return 1
    
def WriteRGBA(data, width, height, bs):
    # if not ASTCEncode:
        # blockWidth = blockHeight = 4
        # blockSize = 16
        # widthInBlocks = (width + (blockWidth - 1)) // blockWidth
        # heightInBlocks = (height + (blockHeight - 1)) // blockHeight
        # maxBlockHeight = 8 if width <= 512 or height <= 256 else 16
        # maxBlockHeight = 4 if width <= 256 or height <= 128 else maxBlockHeight
        # maxBlockHeight = 2 if width <= 64 or height <= 64 else maxBlockHeight    
        # texData = rapi.imageEncodeDXT(data, 4, width, height, noesis.FOURCC_BC7)
        # texData = rapi.callExtensionMethod("tile_blocklineargob", texData, widthInBlocks, heightInBlocks, blockSize, maxBlockHeight)
    # else:
    blockWidth,	blockHeight = 8,8
    widthInBlocks = (width + (blockWidth - 1)) // blockWidth
    heightInBlocks = (height + (blockHeight - 1)) // blockHeight			
    blockSize = 16
    maxBlockHeight = 8 if width <= 512 or height <= 256 else 16
    maxBlockHeight = 4 if width <= 256 or height <= 128 else maxBlockHeight
    maxBlockHeight = 2 if width <= 128 or height <= 64 else maxBlockHeight
    maxBlockHeight = 1 if width <= 64 or height <= 32 else maxBlockHeight        	
    texData = rapi.imageEncodeASTC(data, blockWidth, blockHeight, 1, width, height, 1,2)
    texData = rapi.callExtensionMethod("tile_blocklineargob", texData, widthInBlocks, heightInBlocks, blockSize, maxBlockHeight)
    texData = rapi.callExtensionMethod("astc_decoderaw32", texData, blockWidth, blockHeight, 1, width, height, 1)
    format = noesis.NOESISTEX_RGBA32
    texData = rapi.imageFlipRGBA32(texData, width, height, 0,1)
    tex = NoeTexture("t", width, height, texData, format)
    noesis.saveImageRGBA(rapi.getExtensionlessName(rapi.getInputName()) + "_swizzled" + ".png",tex)
    return 1
    
def CheckSwTextureType(data):
    return 1
    
supportedClassIDs = {
    28: "Texture2D",
}

commonStr = {
    0: "AABB",
    5: "AnimationClip",
    19: "AnimationCurve",
    34: "AnimationState",
    49: "Array",
    55: "Base",
    60: "BitField",
    69: "bitset",
    76: "bool",
    81: "char",
    86: "ColorRGBA",
    96: "Component",
    106: "data",
    111: "deque",
    117: "double",
    124: "dynamic_array",
    138: "FastPropertyName",
    155: "first",
    161: "float",
    167: "Font",
    172: "GameObject",
    183: "Generic Mono",
    196: "GradientNEW",
    208: "GUID",
    213: "GUIStyle",
    222: "int",
    226: "list",
    231: "long long",
    241: "map",
    245: "Matrix4x4f",
    256: "MdFour",
    263: "MonoBehaviour",
    277: "MonoScript",
    288: "m_ByteSize",
    299: "m_Curve",
    307: "m_EditorClassIdentifier",
    331: "m_EditorHideFlags",
    349: "m_Enabled",
    359: "m_ExtensionPtr",
    374: "m_GameObject",
    387: "m_Index",
    395: "m_IsArray",
    405: "m_IsStatic",
    416: "m_MetaFlag",
    427: "m_Name",
    434: "m_ObjectHideFlags",
    452: "m_PrefabInternal",
    469: "m_PrefabParentObject",
    490: "m_Script",
    499: "m_StaticEditorFlags",
    519: "m_Type",
    526: "m_Version",
    536: "Object",
    543: "pair",
    548: "PPtr<Component>",
    564: "PPtr<GameObject>",
    581: "PPtr<Material>",
    596: "PPtr<MonoBehaviour>",
    616: "PPtr<MonoScript>",
    633: "PPtr<Object>",
    646: "PPtr<Prefab>",
    659: "PPtr<Sprite>",
    672: "PPtr<TextAsset>",
    688: "PPtr<Texture>",
    702: "PPtr<Texture2D>",
    718: "PPtr<Transform>",
    734: "Prefab",
    741: "Quaternionf",
    753: "Rectf",
    759: "RectInt",
    767: "RectOffset",
    778: "second",
    785: "set",
    789: "short",
    795: "size",
    800: "SInt16",
    807: "SInt32",
    814: "SInt64",
    821: "SInt8",
    827: "staticvector",
    840: "string",
    847: "TextAsset",
    857: "TextMesh",
    866: "Texture",
    874: "Texture2D",
    884: "Transform",
    894: "TypelessData",
    907: "UInt16",
    914: "UInt32",
    921: "UInt64",
    928: "UInt8",
    934: "unsigned int",
    947: "unsigned long long",
    966: "unsigned short",
    981: "vector",
    988: "Vector2f",
    997: "Vector3f",
    1006: "Vector4f",
    1015: "m_ScriptingClassIdentifier",
    1042: "Gradient",
    1051: "Type*",
    1057: "int2_storage",
    1070: "int3_storage",
    1083: "BoundsInt",
    1093: "m_CorrespondingSourceObject",
    1121: "m_PrefabInstance",
    1138: "m_PrefabAsset",
    1152: "FileSize",
    1161: "Hash128",
}
   
def Align(bs, n):
    value = bs.tell() % n
    if (value):
        bs.seek(n - value, 1)
        
def readStrSpecial(v,bs, strBufOffs):
    if v & 0x80000000:
        if v&0x7fffffff not in commonStr:
            assert(0)
        return commonStr[v&0x7fffffff]
    else:
        check = bs.tell()
        bs.seek(strBufOffs + v)
        o = bs.readString()
        bs.seek(check)
        return o

# https://github.com/K0lb3/UnityPy/blob/ba572869925b516ee5e332699d938b9b237ba84c/UnityPy/helpers/TypeTreeHelper.py#L112
def getNodes(nodes, index):
    level = nodes[index].level
    for k, node in enumerate(nodes[index + 1 :], index + 1):
        if node.level <= level:
            return nodes[index:k]
    return nodes[index:]

# https://github.com/K0lb3/UnityPy/blob/ba572869925b516ee5e332699d938b9b237ba84c/UnityPy/helpers/TypeTreeHelper.py#L172  
def readTree(nodes, bs, i):
    node = nodes[i.value]
    typ = node.typeStr
    c_uint32(0)
    align = node.metaFlag & 0x4000
    if node.typeStr == "SInt8":
        value = bs.readByte()
    elif node.typeStr in ["UInt8", "char"]:
        value = bs.readUByte()
    elif node.typeStr in ["short", "SInt16"]:
        value = bs.readShort()
    elif node.typeStr in ["UInt16", "unsigned short"]:
        value = bs.readUShort()
    elif node.typeStr in ["int", "SInt32"]:
        value = bs.readInt()
    elif node.typeStr in ["UInt32", "unsigned int", "Type*"]:
        value = bs.readUInt()
    elif node.typeStr in ["long long", "SInt64"]:
        value = bs.readInt64()
    elif node.typeStr in ["UInt64", "unsigned long long", "FileSize"]:
        value = bs.readUInt64()
    elif node.typeStr == "float":
        value = bs.readFloat()
    elif node.typeStr == "double":
        value = bs.readDouble()
    elif node.typeStr == "bool":
        value = True if bs.readByte() else False
    elif node.typeStr == "string":
        l = bs.readUInt()
        value = bs.readBytes(l).decode("utf8", "surrogateescape")
        Align(bs,4)
        i.value += 3  # Array, Size, Data(typ)
    elif node.typeStr == "map":  # map == MultiDict
        if nodes[i.value + 1].metaFlag & 0x4000:
            align = True
        map_ = getNodes(nodes, i.value)
        i.value += len(map_) - 1
        first = getNodes(map_, 4)
        second = getNodes(map_, 4 + len(first))
        size = bs.readInt()
        value = [None] * size
        for j in range(size):
            key = readTree(first, bs, c_uint32(0))
            value[j] = (key, readTree(second, bs, c_uint32(0)))
    elif node.typeStr == "TypelessData":
        size = bs.readInt()
        value = bs.readBytes(size)
        i.value += 2  # Size == int, Data(typ) == char/uint8
    else:
        # Vector
        if i.value < len(nodes) - 1 and nodes[i.value + 1].typeStr == "Array":
            if nodes[i.value + 1].metaFlag & 0x4000:
                align = True
            vector = getNodes(nodes, i.value)
            i.value += len(vector) - 1
            size = bs.readInt()
            value = [readTree(vector, bs, c_uint32(3)) for _ in range(size)]
        else:  # Class
            clz = getNodes(nodes, i.value)
            i.value += len(clz) - 1
            value = {}
            j = c_uint32(1)
            while j.value < len(clz):
                clz_node = clz[j.value]
                value[clz_node.nameStr] = readTree(clz, bs, j)
                j.value += 1
    if align:
        Align(bs,4)
    return value
    
class TypeTreeNode:
    def __init__(self, bs, strBufOffs):
        self.nodeVersion = bs.readShort()
        self.level = bs.readByte()
        self.typeFlags = bs.readByte()
        self.typeStr = readStrSpecial(bs.readUInt(),bs, strBufOffs)
        self.nameStr = readStrSpecial(bs.readUInt(),bs, strBufOffs)
        self.byteSize = bs.readInt()
        self.index = bs.readInt()
        self.metaFlag = bs.readUInt()
        self.refTypeHash = bs.readUInt64()

class TypeTree:
    def __init__(self, bs):
        self.nodeCount = bs.readUInt()
        self.stringBufSize = bs.readUInt()
        strBuffOffs = bs.tell() + 0x20 * self.nodeCount
        self.nodes = [TypeTreeNode(bs,strBuffOffs) for _ in range(self.nodeCount)]
        bs.readBytes(self.stringBufSize)

class Type:
    def __init__(self, bs, bEnableTypeTree, bIsRefType):
        self.classID = bs.readUInt()
        self.bIsStripped = bs.readByte()
        self.scriptTypeIndex = bs.readShort()
        if(bIsRefType and scriptTypeIndex >= 0):
            self.scriptID = bs.readBytes(0x10)
        elif self.classID == 114:
            self.scriptID = bs.readBytes(0x10)
        self.oldTypeHash = bs.readBytes(0x10)
        if bEnableTypeTree:
            self.typeTree = TypeTree(bs)
            if bIsRefType:
                self.className = bs.readString()
                self.nameSpace = bs.readString()
                self.asmName = bs.readString()
            else:
                typeDepSize = bs.readInt()
                self.typeDependencies = [bs.readInt() for _ in range(typeDepSize)]    

class Object:
    def __init__(self, bs):
        Align(bs, 4)
        self.pathID = bs.readUInt64()
        self.offset = bs.readUInt64()
        self.size = bs.readUInt()
        self.typeID = bs.readInt()

class TexInfo:
    def __init__(self):
        self.w = None
        self.h = None
        self.offs = None
        self.size = None
        self.format = None
        self.resName = None

def LoadRGBA(data, texList):
    ctx = rapi.rpgCreateContext()
    lz4Flags = [2,3]
    
    bs = NoeBitStream(data, 1)	
    magic = bs.readString()
    version = bs.readUInt()
    v1, v2 = bs.readString(), bs.readString()
    size = bs.readUInt64()
    
    compSize = bs.readUInt()
    decompSize = bs.readUInt()
    flags = bs.readUInt()
    Align(bs, 16)    
    
    if flags & 0x3F not in lz4Flags:
        print("Need to implement other compression schemes")
        return 0
    
    blocksInfoBytes = rapi.decompLZ4(bs.readBytes(compSize), decompSize)
    bs2 = NoeBitStream(blocksInfoBytes, 1)
    bs2.readBytes(16)
    blocksInfoCount = bs2.readInt()    
    blocksInfo = [[bs2.readUInt(), bs2.readUInt(), bs2.readUShort()] for i in range(blocksInfoCount)]
    concatBlockBytes = b"".join(rapi.decompLZ4(bs.readBytes(blockInfo[1]), blockInfo[0]) for blockInfo in blocksInfo)
    entryCount = bs2.readInt()
    entryInfos = [[bs2.readUInt64(), bs2.readUInt64(),bs2.readUInt(), bs2.readString() ] for i in range(entryCount)]
    nameToOffset = {}
    for e in entryInfos:
        nameToOffset[e[3]] = e[0]    
    
    if decompDump:
        with open(rapi.getInputName().split("\\")[-1], "wb") as f:
            f.write(concatBlockBytes)
    
    # Header
    bs = NoeBitStream(concatBlockBytes,1)
    bs.seek(0x10)
    bIsBE = bs.readByte()
    bs.readBytes(3)    
    metadataSize, fileSize, dataOffs, junk = [bs.readUInt(), bs.readUInt64(),bs.readUInt64(),bs.readUInt64()]
    if not bIsBE:
        bs.setEndian(NOE_LITTLEENDIAN)
    unityV = bs.readString()
    platform = bs.readUInt()
    bEnableTypeTree = bs.readByte()
    
    # Relevant stuff
    typeCount = bs.readUInt()
    types = [Type(bs, bEnableTypeTree, False) for _ in range(typeCount)]
    objectCount = bs.readUInt()
    objects = [Object(bs) for _ in range(objectCount)]
    
    # Process
    for object in objects:
        typ = types[object.typeID]
        if typ.classID not in supportedClassIDs:
            continue
        
        bs.seek(dataOffs + object.offset)
        nodeDic = readTree(typ.typeTree.nodes, bs, c_uint32(0))
        
        if supportedClassIDs[typ.classID] == "Texture2D":
            args1 = ["m_Width", "m_Height", "m_TextureFormat", "m_CompleteImageSize"]
            args2 = ["offset", "path"]
            width, height, format, size = [nodeDic[a] for a in args1]
            offs, resName = [nodeDic["m_StreamData"][a] for a in args2]
            
            bs.seek(nameToOffset[resName.split("/")[-1]] + offs)
            textureData = bs.readBytes(size)
            if format == 0xA:
               format= noesis.NOESISTEX_DXT1
            elif format == 0x19:
                format = noesis.FOURCC_BC7
            elif format == 0x33:
                format = "ASTC_8_8"
            else:
                print("unknown format " + str(format), width, height)  
            # print(format)   
            bRaw = type(format) == str
            if bRaw and format.startswith("ASTC"):
                blockWidth,	blockHeight = list(map(lambda x: int(x), format.split('_')[1:]))
                widthInBlocks = (width + (blockWidth - 1)) // blockWidth
                heightInBlocks = (height + (blockHeight - 1)) // blockHeight			
                blockSize = 16
                maxBlockHeight = 8 if width <= 512 or height <= 256 else 16
                maxBlockHeight = 4 if width <= 256 or height <= 128 else maxBlockHeight
                maxBlockHeight = 2 if width <= 128 or height <= 64 else maxBlockHeight
                maxBlockHeight = 1 if width <= 64 or height <= 32 else maxBlockHeight
                textureData = rapi.callExtensionMethod("untile_blocklineargob", textureData, widthInBlocks, heightInBlocks, blockSize, maxBlockHeight)		
                textureData = rapi.callExtensionMethod("astc_decoderaw32", textureData, blockWidth, blockHeight, 1, width, height, 1)
                format = noesis.NOESISTEX_RGBA32
            else:
                blockWidth = blockHeight = 4
                blockSize = 8 if format == noesis.NOESISTEX_DXT1 else 16
                widthInBlocks = (width + (blockWidth - 1)) // blockWidth
                heightInBlocks = (height + (blockHeight - 1)) // blockHeight
                maxBlockHeight = 8 if width <= 512 or height <= 256 else 16
                maxBlockHeight = 4 if width <= 256 or height <= 128 else maxBlockHeight
                maxBlockHeight = 2 if width <= 64 or height <= 64 else maxBlockHeight
                textureData = rapi.callExtensionMethod("untile_blocklineargob", textureData, widthInBlocks, heightInBlocks, blockSize, maxBlockHeight)
                textureData = rapi.imageDecodeDXT(textureData, width, height, format)
                format = noesis.NOESISTEX_RGBA32
            tex = NoeTexture(str(len(texList)), width, height, textureData, format)
            texList.append(tex)
    return 1

