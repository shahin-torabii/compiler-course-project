import os
import re

from antlr4 import *

from src.logic.FinalEncryptor import FinalEncryptor
from src.logic.InitialReader import InitialReader
from src.logic.JavaLexer import JavaLexer
from src.logic.JavaParser import JavaParser
from Listener import *
from Identifier import *
from IdentiferList import *
from Renamer import *
import time

class Extractor:
    def __init__(self, files, projectName):
        self.__projectName = projectName
        self.fileNames, self.filePaths = files
        self.extractor = None
        self.renamer = None
        self.initialReader = None
        self.tokenStreamDict = {}
        self.methodCountDict = {}
        self.localVarCountDict = {}
        self.identifierList = IdentifierList()
        self.symbol_table = {}
        self.fileCopies = []
        self.modified_tokens = {}
        self.finalEncryptor = None
        self.mini_should_ignore_classes = [
            "toCharArray",
            "codePointAt",
            "toUnsignedLong",
            "floatToIntBits",
            "trim",
            "isJavaIdentifierPart",
            "join",
            "codePointBefore",
            "equalsIgnoreCase",
            "compareToIgnoreCase",
            "signum",
            "charValue",
            "isUnicodeIdentifierPart",
            "divideUnsigned",
            "isSpaceChar",
            "logicalAnd",
            "concat",
            "doubleValue",
            "doubleToLongBits",
            "matches",
            "toUnsignedInt",
            "highSurrogate",
            "contains",
            "compareUnsigned",
            "toBinaryString",
            "getType",
            "endsWith",
            "logicalOr",
            "stripLeading",
            "wait",
            "compare",
            "isLowerCase",
            "getNumericValue",
            "formatted",
            "rotateLeft",
            "intBitsToFloat",
            "replaceFirst",
            "sum",
            "notify",
            "longValue",
            "isFinite",
            "min",
            "remainderUnsigned",
            "isInfinite",
            "lowSurrogate",
            "getBoolean",
            "isJavaLetterOrDigit",
            "copyValueOf",
            "isUnicodeIdentifierStart",
            "getDirectionality",
            "intern",
            "toHexString",
            "max",
            "isJavaIdentifierStart",
            "getChars",
            "isUpperCase",
            "reverse",
            "doubleToRawLongBits",
            "getLong",
            "isIdeographic",
            "isTitleCase",
            "equals",
            "isBmpCodePoint",
            "toString",
            "bitCount",
            "toUnsignedString",
            "isLowSurrogate",
            "chars",
            "stripTrailing",
            "byteValue",
            "toCodePoint",
            "getClass",
            "stripIndent",
            "replace",
            "getInteger",
            "compareTo",
            "resolveConstantDesc",
            "longBitsToDouble",
            "isNaN",
            "describeConstable",
            "isJavaLetter",
            "isSpace",
            "getBytes",
            "floatToRawIntBits",
            "split",
            "strip",
            "toUpperCase",
            "shortValue",
            "isIdentifierIgnorable",
            "indexOf",
            "codePoints",
            "digit",
            "isSupplementaryCodePoint",
            "toLowerCase",
            "format",
            "floatValue",
            "isWhitespace",
            "numberOfLeadingZeros",
            "isLetterOrDigit",
            "isDigit",
            "booleanValue",
            "logicalXor",
            "isValidCodePoint",
            "reverseBytes",
            "toChars",
            "charCount",
            "indent",
            "isISOControl",
            "notifyAll",
            "isSurrogatePair",
            "regionMatches",
            "isBlank",
            "replaceAll",
            "substring",
            "toOctalString",
            "isLetter",
            "transform",
            "isAlphabetic",
            "hashCode",
            "repeat",
            "lines",
            "lowestOneBit",
            "codePointCount",
            "translateEscapes",
            "isMirrored",
            "rotateRight",
            "valueOf",
            "intValue",
            "contentEquals",
            "forDigit",
            "length",
            "isEmpty",
            "isHighSurrogate",
            "codePointOf",
            "subSequence",
            "lastIndexOf",
            "isSurrogate",
            "isDefined",
            "toTitleCase",
            "highestOneBit",
            "charAt",
            "offsetByCodePoints",
            "numberOfTrailingZeros",
            "startsWith",
        ]
        self.should_ignore_classes = [
            "nextFloat",
            "renameTo",
            "toUnsignedLong",
            "findAll",
            "bind",
            "trim",
            "isDaemon",
            "isJavaIdentifierPart",
            "mkdir",
            "canExecute",
            "printStackTrace",
            "isUnicodeIdentifierPart",
            "subMap",
            "divideUnsigned",
            "logicalAnd",
            "useDelimiter",
            "concat",
            "shutdownInput",
            "contains",
            "size",
            "stop",
            "toBinaryString",
            "mkdirs",
            "endsWith",
            "listIterator",
            "lowerKey",
            "pollFirst",
            "headMap",
            "compare",
            "isLowerCase",
            "roll",
            "nextAfter",
            "startVirtualThread",
            "lineSeparator",
            "sleep",
            "toLocalizedPattern",
            "nanoTime",
            "readAllBytes",
            "after",
            "close",
            "skipNBytes",
            "connect",
            "resume",
            "set",
            "toHexString",
            "isFile",
            "drawArc",
            "copyArea",
            "doubleToRawLongBits",
            "parseObject",
            "isIdeographic",
            "abs",
            "isClosed",
            "floorDiv",
            "isBmpCodePoint",
            "toString",
            "bitCount",
            "toUnsignedString",
            "fma",
            "hasNextBigDecimal",
            "stripTrailing",
            "byteValue",
            "retainAll",
            "stripIndent",
            "navigableKeySet",
            "resolveConstantDesc",
            "higherEntry",
            "longBitsToDouble",
            "describeConstable",
            "compute",
            "addSuppressed",
            "decrementExact",
            "digit",
            "applyPattern",
            "add",
            "isSupplementaryCodePoint",
            "openConnection",
            "createTempFile",
            "list",
            "ioException",
            "nextExponential",
            "isDigit",
            "ulp",
            "isDirectory",
            "reverseBytes",
            "fillInStackTrace",
            "charCount",
            "fillArc",
            "notifyAll",
            "regionMatches",
            "isBlank",
            "locale",
            "replaceAll",
            "remove",
            "drawString",
            "tanh",
            "random",
            "load",
            "hashCode",
            "subSet",
            "sin",
            "enumerate",
            "isOutputShutdown",
            "lines",
            "gc",
            "useRadix",
            "codePointCount",
            "hasNextBoolean",
            "isMirrored",
            "ceilMod",
            "fillRoundRect",
            "floorEntry",
            "toIntExact",
            "length",
            "isEmpty",
            "subSequence",
            "parse",
            "nextLong",
            "parseByte",
            "hasNextShort",
            "nextGaussian",
            "addRequestProperty",
            "isHidden",
            "computeIfPresent",
            "isBound",
            "isDefined",
            "clone",
            "countStackFrames",
            "asin",
            "fillOval",
            "charAt",
            "numberOfTrailingZeros",
            "hasNextLong",
            "append",
            "drawOval",
            "codePointAt",
            "headSet",
            "containsValue",
            "parseUnsignedLong",
            "identityHashCode",
            "sqrt",
            "higherKey",
            "toArray",
            "parallelStream",
            "join",
            "findInLine",
            "absExact",
            "codePointBefore",
            "write",
            "compareToIgnoreCase",
            "atan2",
            "toPattern",
            "spliterator",
            "floorDivExact",
            "lower",
            "hasNext",
            "toDegrees",
            "ceil",
            "doubleToLongBits",
            "ceilingKey",
            "highSurrogate",
            "toGMTString",
            "exit",
            "compareUnsigned",
            "mapLibraryName",
            "nullWriter",
            "hasNextDouble",
            "stripLeading",
            "tailMap",
            "wait",
            "ceilingEntry",
            "canRead",
            "intBitsToFloat",
            "skip",
            "notify",
            "ofVirtual",
            "stream",
            "drawGlyphVector",
            "parseShort",
            "yield",
            "copyValueOf",
            "trimToSize",
            "max",
            "nextLine",
            "isInterrupted",
            "draw",
            "IEEEremainder",
            "comparator",
            "toPath",
            "parseLong",
            "isTitleCase",
            "equals",
            "currentTimeMillis",
            "createNewFile",
            "toCodePoint",
            "rotate",
            "UTC",
            "cos",
            "expm1",
            "compareTo",
            "decode",
            "floatToRawIntBits",
            "nextUp",
            "split",
            "strip",
            "indexOf",
            "suspend",
            "read",
            "entrySet",
            "toLowerCase",
            "sort",
            "acos",
            "interrupted",
            "fill",
            "removeIf",
            "expand",
            "isLetterOrDigit",
            "multiplyHigh",
            "nullReader",
            "dispose",
            "addRenderingHints",
            "isValidCodePoint",
            "guessContentTypeFromName",
            "indent",
            "isISOControl",
            "isSurrogatePair",
            "delete",
            "substring",
            "parseDouble",
            "transform",
            "repeat",
            "putAll",
            "tokens",
            "withInitial",
            "nextBoolean",
            "floor",
            "keySet",
            "listFiles",
            "ofPlatform",
            "translateEscapes",
            "console",
            "forEach",
            "contentEquals",
            "isHighSurrogate",
            "nullInputStream",
            "canWrite",
            "nextInt",
            "toRadians",
            "drawLine",
            "clearRect",
            "drawImage",
            "lastEntry",
            "toCharArray",
            "rint",
            "ceilDiv",
            "iterator",
            "removeAll",
            "sameFile",
            "merge",
            "equalsIgnoreCase",
            "exp",
            "floorKey",
            "tailSet",
            "nextBigDecimal",
            "currentThread",
            "isSpaceChar",
            "initCause",
            "toUnsignedInt",
            "addExact",
            "lowerEntry",
            "drawRenderedImage",
            "nextByte",
            "log10",
            "descendingIterator",
            "replaceFirst",
            "sum",
            "pollLast",
            "isFinite",
            "parseUnsignedInt",
            "min",
            "isInfinite",
            "ints",
            "arraycopy",
            "hypot",
            "lowSurrogate",
            "pow",
            "unsignedMultiplyHigh",
            "deleteOnExit",
            "isUnicodeIdentifierStart",
            "activeCount",
            "subList",
            "toURL",
            "isDeprecated",
            "intern",
            "shear",
            "dumpStack",
            "toURI",
            "nextDouble",
            "radix",
            "holdsLock",
            "addAll",
            "hasNextLine",
            "incrementExact",
            "isLowSurrogate",
            "drawPolygon",
            "chars",
            "multiplyFull",
            "isInputShutdown",
            "log1p",
            "markSupported",
            "available",
            "onSpinWait",
            "run",
            "drawRenderableImage",
            "isNaN",
            "isSpace",
            "fillRect",
            "fillPolygon",
            "nextShort",
            "toUpperCase",
            "shortValue",
            "forEachRemaining",
            "codePoints",
            "last",
            "sinh",
            "newHashMap",
            "floatValue",
            "isWhitespace",
            "openStream",
            "numberOfLeadingZeros",
            "divideExact",
            "checkAccess",
            "drawBytes",
            "pollLastEntry",
            "hitClip",
            "firstKey",
            "logicalXor",
            "ensureCapacity",
            "higher",
            "toLocaleString",
            "next",
            "formatToCharacterIterator",
            "computeIfPresent",
            "descendingSet",
            "multiplyExact",
            "transferTo",
            "toOctalString",
            "cbrt",
            "guessContentTypeFromStream",
            "isAlphabetic",
            "negateExact",
            "flush",
            "lastKey",
            "valueOf",
            "applyLocalizedPattern",
            "start",
            "codePointOf",
            "nextDown",
            "shutdownOutput",
            "parseInt",
            "lastIndexOf",
            "isSurrogate",
            "isWeekDateSupported",
            "toTitleCase",
            "putIfAbsent",
            "mark",
            "useLocale",
            "copySign",
            "put",
            "threadId",
            "floatToIntBits",
            "supportedOptions",
            "delimiter",
            "drawPolyline",
            "nextBigInteger",
            "signum",
            "hasNextBigInteger",
            "charValue",
            "compress",
            "isSet",
            "doubleValue",
            "matches",
            "matcher",
            "toExternalForm",
            "doubles",
            "hasNextInt",
            "reset",
            "readNBytes",
            "logicalOr",
            "runFinalization",
            "parseFloat",
            "log",
            "formatted",
            "rotateLeft",
            "parseBoolean",
            "isConnected",
            "longValue",
            "longs",
            "remainderUnsigned",
            "draw3DRect",
            "get",
            "fill3DRect",
            "firstEntry",
            "isJavaLetterOrDigit",
            "isJavaIdentifierStart",
            "hasNextByte",
            "containsAll",
            "isUpperCase",
            "reverse",
            "toInstant",
            "isAbsolute",
            "exists",
            "finalize",
            "first",
            "clip",
            "descendingKeySet",
            "listRoots",
            "before",
            "replace",
            "isJavaLetter",
            "atan",
            "translate",
            "clearProperty",
            "hit",
            "drawRoundRect",
            "interrupt",
            "inheritedChannel",
            "ceilDivExact",
            "create",
            "isIdentifierIgnorable",
            "from",
            "tan",
            "loadLibrary",
            "containsKey",
            "format",
            "isAlive",
            "newHashSet",
            "sendUrgentData",
            "booleanValue",
            "lastModified",
            "isVirtual",
            "toChars",
            "hasNextFloat",
            "scalb",
            "floorMod",
            "descendingMap",
            "isLenient",
            "values",
            "scale",
            "findWithinHorizon",
            "isLetter",
            "nextBytes",
            "pollFirstEntry",
            "ready",
            "drawChars",
            "nullOutputStream",
            "lowestOneBit",
            "subtractExact",
            "ceiling",
            "rotateRight",
            "intValue",
            "forDigit",
            "clipRect",
            "clear",
            "match",
            "cosh",
            "round",
            "highestOneBit",
            "drawRect",
            "offsetByCodePoints",
            "startsWith",
        ]

    def readJavaFile(self, filepath: str):
        context = None
        readingJavaFile = filepath
        try:
            context = open(readingJavaFile, "r")
        except IOError:
            print("Something went wronged reading the file")
        return context.read()

    def executeFiles(self):
        applicationStartTime = time.time()
        print("Making Identifier list...")
        startingTime = time.time()
        self.makeTable()
        endingTime = time.time()
        print(f"Table completed in {endingTime - startingTime}\n")
        print("Renaming...")
        startingTime = time.time()
        self.renameClasses()
        endingTime = time.time()
        print(f"Renaming completed in {endingTime - startingTime}\n")
        print("encrypting...")
        startingTime = time.time()
        self.encryptClasses()
        endingTime = time.time()
        setJavaDecoderFilePath()
        makeJavaDecoder()
        print(f"encrypting completed in {endingTime - startingTime}")
        applicationEndTime = time.time()
        print(f"\ncompleted in {applicationEndTime-applicationStartTime}")

    def findMethods(self):
        for i in range(len(self.filePaths)):
            input_text = self.readJavaFile(
                os.path.join(self.filePaths[i], self.fileNames[i])
            )
            input_stream = InputStream(input_text)
            lexer = JavaLexer(input_stream)
            stream = CommonTokenStream(lexer)
            stream.fill()
            parser = JavaParser(stream)
            tree = parser.compilationUnit()  # Parse the entire compilation unit
            self.initialReader = InitialReader(self.fileNames[i], self, stream)
            walker = ParseTreeWalker()
            walker.walk(self.initialReader, tree)

    def makeTable(self):
        for i in range(len(self.filePaths)):
            input_text = self.readJavaFile(
                os.path.join(self.filePaths[i], self.fileNames[i])
            )
            input_stream = InputStream(input_text)
            lexer = JavaLexer(input_stream)
            stream = CommonTokenStream(lexer)
            stream.fill()
            stream.fill()
            parser = JavaParser(stream)
            tree = parser.compilationUnit()  # Parse the entire compilation unit
            self.extractor = Listener(self.fileNames[i], self, stream)
            walker = ParseTreeWalker()
            walker.walk(self.extractor, tree)

    def editTable(self):
        for iden in self.identifierList.findByType(20):
            parentIden = None
            for id in self.identifierList.findByType(7):
                if iden.fileName.replace(".java", "") == id.name and id.implementList:
                    parentIden = id
            if parentIden:
                for impl in parentIden.implementList:
                    for iden2 in self.identifierList.findByFileName(impl + ".java"):
                        if (
                            (iden2.name == iden.name)
                            and (iden.type == 20 or iden.type == 35)
                            and (iden2.type == 20 or iden2.type == 35)
                        ):
                            iden.editedName = iden2.editedName

    def renameClasses(self):
        for i in range(len(self.filePaths)):
            stream = None
            if self.fileNames[i] in self.tokenStreamDict:
                stream = self.tokenStreamDict[self.fileNames[i]]
            stream.fill()
            parser = JavaParser(stream)
            tree = parser.compilationUnit()  # Parse the entire compilation unit
            self.renamer = Renamer(self.fileNames[i], self, parser, stream)
            walker = ParseTreeWalker()
            walker.walk(self.renamer, tree)

            # if  self.fileNames[i] in self.renamedTokenStreamDict:
            # self.renamedTokenStreamDict[self.fileNames[i]] = stream
            # fileCopy = ''.join(self.renamer.rewriter.getDefaultText())
            # self.renamedTokenStreamDict[self.fileNames[i]]=self.renamer.rewriter.getDefaultText()
            # self.fileCopies.append(fileCopy)
            # self.makeOutput(i, fileCopy)

    def encryptClasses(self):
        for i in range(len(self.filePaths)):
            # if self.fileNames[i] != "Question2.java":
            # continue

            stream = None
            if self.fileNames[i] in self.tokenStreamDict:
                stream = self.tokenStreamDict[self.fileNames[i]]
            stream.fill()
            parser = JavaParser(stream)
            tree = parser.compilationUnit()  # Parse the entire compilation unit
            self.finalEncryptor = FinalEncryptor(
                self.fileNames[i], self, parser, stream
            )
            walker = ParseTreeWalker()
            walker.walk(self.finalEncryptor, tree)
            fileCopy = "".join(self.tokenStreamDict[self.fileNames[i]].getText())
            self.fileCopies.append(fileCopy)
            self.makeOutput(i, fileCopy)

    def makeOutput(self, i, final_output_with_replaced_classes):
        javaFileName = f"New_{self.fileNames[i]}"
        writePath = self.filePaths[i].replace(self.__projectName, "output")
        if not os.path.exists(writePath):
            os.makedirs(writePath)
        with open(os.path.join(writePath, javaFileName), "w") as java_file:
            java_file.write(final_output_with_replaced_classes)

    def addToList(self, identifier):
        self.identifierList.append(identifier)
