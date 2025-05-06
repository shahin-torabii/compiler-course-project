import random
import string

from src.logic.Encoding.Cipher import *
from src.logic.JavaLexer import JavaLexer
from src.logic.JavaParserListener import JavaParserListener
from JavaParser import *
from Identifier import *
from antlr4.TokenStreamRewriter import *

from src.logic.JavaParser import JavaParser


class Listener(JavaParserListener):
    def __init__(self, currentFile, executer, common_token_stream):
        self.out = []
        self.identifiers = []
        self.currentFile = currentFile
        self.executer = executer
        self.currentId = None
        self.types = [
            "int",
            "boolean",
            "long",
            "short",
            "float",
            "double",
            "char",
            "final",
        ]
        self.common_token_stream = common_token_stream
        if common_token_stream is not None:
            self.rewriter = TokenStreamRewriter(self.common_token_stream)

    def exitCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        self.changeRewriterTokenStream(self.rewriter.getDefaultText())

    def enterIdentifier(self, ctx: JavaParser.IdentifierContext):
        name = ctx.getText()
        self.identifiers.append(name)
        exactType = ctx.parentCtx.parentCtx.getRuleIndex()
        tempType = ctx.parentCtx.getRuleIndex()

        value = None
        parent_ctx = ctx.parentCtx
        fileName = self.currentFile
        typesList = [11, 7, 38, 20, 13, 15, 31, 35]

        if tempType == 20 and name in self.executer.should_ignore_classes:
            return
        elif tempType in typesList:
            if parent_ctx.getRuleIndex() == 38:
                initializer = parent_ctx.parentCtx.getChild(2)
                if initializer:
                    variable_type = parent_ctx.parentCtx.parentCtx.parentCtx.getChild(
                        0
                    ).getText()
                    varType = variable_type
                    if (
                        variable_type == "String"
                        or variable_type == "int"
                        or variable_type == "double"
                        or variable_type == "float"
                        or variable_type == "long"
                        or variable_type == "short"
                        or variable_type == "char"
                        or variable_type == "boolean"
                    ):
                        value = initializer.getText()
            # TODO

            newIdentifier = Identifier(
                name, tempType, exactType, ctx.start.line, fileName, value
            )
            # if name == "length" :
            #     newIdentifier.setEditedName("length")
            # elif name == "add":
            #     newIdentifier.setEditedName("add")
            # elif name == "matcher":
            #     newIdentifier.setEditedName("matcher")
            # else:
            if tempType == 7:
                newIdentifier.varOrReturnType = newIdentifier.fileName.replace(
                    ".java", ""
                )
                if ctx.parentCtx.IMPLEMENTS():
                    tempList = []
                    for elem in ctx.parentCtx.typeList():
                        tempList.append(elem.getText())
                    newIdentifier.implementList = tempList
                if ctx.parentCtx.EXTENDS():
                    newIdentifier.extend = ctx.parentCtx.typeType().getText()
            newIdentifier.setEditedName(self.makeNewName(newIdentifier))
            newIdentifier.setEditedValue(makeNewValue(newIdentifier))
            self.currentId = newIdentifier
            self.executer.identifierList.addToList(newIdentifier)

    def enterPrimary(self, ctx: JavaParser.PrimaryContext):
        tempCtx = ctx.parentCtx
        while tempCtx.parentCtx is not None:
            tempCtx = tempCtx.parentCtx
            if (
                hasattr(tempCtx, "bop")
                and tempCtx.bop
                and tempCtx.bop.text
                in (
                    "=",
                    "+=",
                    "-=",
                    "/=",
                    "*=",
                    "&=",
                    "|=",
                    "^=",
                    ">>=",
                    "<<<=",
                    "<<=",
                    "%=",
                )
            ):
                left_exp = tempCtx.getChild(0)
                op = tempCtx.getChild(1)
                right_exp = tempCtx.getChild(2)
                bopDict = {
                    "+=": f"{left_exp.getText()}+{right_exp.getText()}",
                    "-=": f"{left_exp.getText()}-{right_exp.getText()}",
                    "*=": f"{left_exp.getText()}*{right_exp.getText()}",
                    "/=": f"{left_exp.getText()}/{right_exp.getText()}",
                    "%=": f"{left_exp.getText()}%{right_exp.getText()}",
                    "&=": f"{left_exp.getText()}&{right_exp.getText()}",
                    "|=": f"{left_exp.getText()}|{right_exp.getText()}",
                    "^=": f"{left_exp.getText()}^{right_exp.getText()}",
                    ">>=": f"{left_exp.getText()}>>{right_exp.getText()}",
                    "<<=": f"{left_exp.getText()}<<{right_exp.getText()}",
                    "<<<=": f"{left_exp.getText()}<<<{right_exp.getText()}",
                }

                if op.getText() != "=":
                    modified_text = bopDict[op.getText()]
                    tempCtx.bop.text = "="

                    self.rewriter.replaceRange(
                        right_exp.start.tokenIndex,
                        right_exp.stop.tokenIndex,
                        modified_text,
                    )

                    self.changeRewriterTokenStream(self.rewriter.getDefaultText())
                    break
            elif hasattr(tempCtx, "postfix") and tempCtx.postfix is not None:
                if tempCtx.postfix.text == "++":
                    modified_text = f"{tempCtx.getChild(0).getText()} = {tempCtx.getChild(0).getText()} + 1"
                    self.rewriter.replaceRange(
                        tempCtx.start.tokenIndex, tempCtx.stop.tokenIndex, modified_text
                    )
                    self.changeRewriterTokenStream(self.rewriter.getDefaultText())
                elif tempCtx.postfix.text == "--":
                    modified_text = f"{tempCtx.getChild(0).getText()} = {tempCtx.getChild(0).getText()} - 1"
                    self.rewriter.replaceRange(
                        tempCtx.start.tokenIndex, tempCtx.stop.tokenIndex, modified_text
                    )
                    self.changeRewriterTokenStream(self.rewriter.getDefaultText())
            elif hasattr(tempCtx, "prefix") and tempCtx.prefix is not None:
                if tempCtx.prefix.text == "++":
                    modified_text = f"{tempCtx.getChild(0).getText()} = {tempCtx.getChild(0).getText()} + 1"
                    self.rewriter.replaceRange(
                        tempCtx.start.tokenIndex, tempCtx.stop.tokenIndex, modified_text
                    )
                    self.changeRewriterTokenStream(self.rewriter.getDefaultText())
                elif tempCtx.prefix.text == "--":
                    modified_text = f"{tempCtx.getChild(0).getText()} = {tempCtx.getChild(0).getText()} - 1"
                    self.rewriter.replaceRange(
                        tempCtx.start.tokenIndex, tempCtx.stop.tokenIndex, modified_text
                    )
                    self.changeRewriterTokenStream(self.rewriter.getDefaultText())

    def exitVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        varType = ctx.parentCtx.parentCtx.getChild(0).getText()
        if f"{self.currentId.name}[]" == ctx.variableDeclaratorId().getText():
            varType = varType + "[]"
        if (
            self.currentId is not None
            and self.currentId.name == ctx.variableDeclaratorId().identifier().getText()
            and self.currentId.type == 38
        ):
            self.currentId.varOrReturnType = varType

        varType = ctx.parentCtx.parentCtx.getChild(0)
        typeText = varType.getText()
        if f"{self.currentId.name}[]" == ctx.variableDeclaratorId().getText():
            typeText = typeText + "[]"
            self.rewriter.replaceRangeTokens(
                ctx.variableDeclaratorId().start,
                ctx.variableDeclaratorId().stop,
                self.currentId.name,
            )
            self.rewriter.replaceRangeTokens(
                varType.start, varType.stop, f"{varType.getText()}[]"
            )
            self.changeRewriterTokenStream(self.rewriter.getDefaultText())

        if typeText not in self.types:
            return
        if typeText in ["final", "public", "private", "static", "protected"]:
            varType = ctx.parentCtx.parentCtx.getChild(1)
        token = varType.start
        # Use the token's line and column as a unique identifier
        self.currentId.isStringified = True
        self.rewriter.replaceRangeTokens(varType.start, varType.stop, "String")

    def exitFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        varType = ctx.typeType().getText()
        if (
            self.currentId is not None
            and self.currentId.name == ctx.variableDeclaratorId().identifier().getText()
            and self.currentId.type == 38
        ):
            self.currentId.varOrReturnType = varType

    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_returnType = ctx.typeTypeOrVoid().getText()
        if (
            self.currentId is not None
            and self.currentId.name == ctx.identifier().getText()
            and self.currentId.type == 20
        ):
            self.currentId.varOrReturnType = method_returnType

    def exitEnhancedForControl(self, ctx: JavaParser.EnhancedForControlContext):
        varType = ctx.typeType().getText()
        if (
            self.currentId is not None
            and self.currentId.name == ctx.variableDeclaratorId().identifier().getText()
            and self.currentId.exactType == 95
        ):
            self.currentId.varOrReturnType = varType

    def changeRewriterTokenStream(self, text):
        # Create an ANTLR input stream from the modified text
        input_stream = InputStream(text)

        # Create an instance of your lexer using the input stream
        lexer = JavaLexer(input_stream)  # Replace with your lexer class

        # Generate tokens using the lexer
        token_stream = CommonTokenStream(lexer)

        # Update self.token_stream_writer's token stream
        self.executer.tokenStreamDict[self.currentFile] = token_stream

    def makeNewString(self, value, token):
        line = token.line
        encoder = encodeString(value, line, self.currentFile)
        return encoder.cipherHex

    def makeNewName(self, id):
        # length = 10
        # random_string = random.choice(string.ascii_uppercase) + "".join(
        #     random.choice(string.ascii_letters + string.digits) for _ in range(length)
        # )
        # # newName = f'New_{name}'
        # newName = random_string
        # if id.type in (7, 11, 13, 15):
        #     newName = "New_" + id.name
        newName = "New_" + id.name
        return newName


def makeNewValue(id):
    if id.value is not None:
        encoder = encodeIdentifier(id)
        id.isEncrypted = True
        return encoder.cipherHex
