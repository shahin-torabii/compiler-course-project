from src.logic.JavaLexer import JavaLexer
from src.logic.JavaParserListener import JavaParserListener
from JavaParser import *
from antlr4.TokenStreamRewriter import *

from src.logic.JavaParser import JavaParser


class InitialReader(JavaParserListener):
    def __init__(self, currentFile, executer, common_token_stream):
        self.currentFile = currentFile
        self.executer = executer
        self.common_token_stream = common_token_stream
        self.methodCount = 0
        self.localVarCount = 0
        if common_token_stream is not None:
            self.rewriter = TokenStreamRewriter(
                self.common_token_stream)

    # def exitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
    #     self.executer.methodCountDict[self.currentFile] = self.executer.methodCountDict[self.currentFile] + 1
    #     # print(self.currentFile, self.methodCount)
    # def exitClassBody(self, ctx:JavaParser.ClassBodyContext):
    #     self.executer.methodCountDict[self.currentFile] = self.methodCount

    # def exitClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
    #     print("mm")
    #     self.executer.methodCountDict[self.currentFile] = self.methodCount
    def enterMethodBody(self, ctx: JavaParser.MethodBodyContext):
        self.methodCount += 1

    def enterLocalVariableDeclaration(self, ctx: JavaParser.LocalVariableDeclarationContext):
        # print("line ", ctx.start.line, ctx.getText())
        self.localVarCount += 1

    def exitCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        self.executer.methodCountDict[self.currentFile] = self.methodCount
        self.executer.localVarCountDict[self.currentFile] = self.localVarCount
        self.changeRewriterTokenStream(self.rewriter.getDefaultText())

    def changeRewriterTokenStream(self, text):
        # Create an ANTLR input stream from the modified text
        input_stream = InputStream(text)

        # Create an instance of your lexer using the input stream
        lexer = JavaLexer(input_stream)  # Replace with your lexer class

        # Generate tokens using the lexer
        token_stream = CommonTokenStream(lexer)

        # Update self.token_stream_writer's token stream
        self.executer.tokenStreamDict[self.currentFile] = token_stream
