from antlr4.Token import *
import re

from JavaParser import *
from src.logic.Encoding.Cipher import *
from src.logic.Identifier import *
from src.logic.JavaLexer import JavaLexer
from src.logic.JavaParserListener import *

from antlr4 import *
from antlr4.TokenStreamRewriter import *

from src.logic.JavaParser import JavaParser


class FinalEncryptor(JavaParserListener):
    def __init__(self, currentFile, executer, parser, common_token_stream):
        self.executer = executer
        self.currentFile = currentFile
        self.parser = parser
        self.out = []
        self.acceptedTypes = [
            "int",
            "boolean",
            "long",
            "short",
            "float",
            "double",
            "char",
            "final",
            "String",
        ]
        self.varType_dict = {
            "Integer": "int",
            "Float": "float",
            "String": "MyCipher",
            "Boolean": "boolean",
            "Double": "double",
            "Char": "char",
        }
        self.type_to_transform = {

            "String": "MyCipher.getInstance().decode({})",
            "int": "Integer.parseInt(MyCipher.getInstance().decode({}))",
            "float": "Float.parseFloat(MyCipher.getInstance().decode({}))",
            "double": "Double.parseDouble(MyCipher.getInstance().decode({}))",
            "char": "MyCipher.getInstance().decode({}).charAt(0)",
            "boolean": "Boolean.parseBoolean(MyCipher.getInstance().decode({}))",
        }
        self.commonTokenStream = common_token_stream
        if common_token_stream is not None:
            self.rewriter = TokenStreamRewriter(common_token_stream)

    def exitCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        """
        TODO
        This method is called when the parser exits the compilation unit context, which
        represents the entire Java source file being parsed.

        Purpose:
        - The main purpose of this method is to finalize the transformations made to the
          Java source code and update the token stream with the modified text.

        Functionality:
        1. It retrieves the modified text from the TokenStreamRewriter.
           - `self.rewriter.getDefaultText()` gets the entire text of the Java source file
             with all the modifications applied during the parse tree traversal.

        2. It calls the `changeRewriterTokenStream` method to update the token stream with
           this modified text.
           - This ensures that any subsequent processing or output generation uses the
             transformed version of the source code.

        Parameters:
        - ctx (JavaParser.CompilationUnitContext): The context object representing the
          compilation unit (i.e., the entire Java source file).

        Usage:
        - This method is automatically invoked by the ANTLR parse tree walker after all
          the child nodes of the compilation unit have been visited and processed.
        """
        # START YOUR CODE HERE
        self.changeRewriterTokenStream(self.rewriter.getDefaultText())
        # END YOUR CODE HERE

    # DO NOT CHANGE THIS CODE
    def enterStatement(self, ctx: JavaParser.StatementContext):
        """
        This method is called when entering a statement in the parse tree.

        It processes switch statements to identify and potentially transform expressions
        using the custom MyCipher class. The method handles various conditions to ensure
        that encrypted or stringified expressions are appropriately transformed.

        Args:
            ctx (JavaParser.StatementContext): The context object representing the statement node in the parse tree.

        Functionality:
        - Checks if the statement is a switch statement with a parenthesized expression.
        - Skips transformation if the expression already contains MyCipher.decode.
        - Retrieves the variable type of the expression based on the identifier list.
        - Skips transformation if the exact type of the identifier is 47.
        - Applies the appropriate transformation based on the variable type using MyCipher.
        - Replaces the original expression with the transformed text in the token stream.
        """

        if ctx.SWITCH() and ctx.parExpression():
            exp = ctx.parExpression().expression()
            if "MyCipher" and "decode" in exp.getText():
                return
            token_type = None
            for id in self.executer.identifierList.findByFileName(self.currentFile):
                if id.editedName == exp.getText() and id.line <= ctx.start.line:
                    token_type = id.varOrReturnType
                    if id.exactType == 47:
                        token_type = None
            for token_type, transform_format in self.type_to_transform.items():
                if token_type == token_type and token_type:
                    self.rewriter.replaceRangeTokens(
                        exp.start, exp.stop, transform_format.format(exp.getText())
                    )
                    return

    def exitExpression(self, ctx: JavaParser.ExpressionContext):
        """
        This method is called when exiting an expression in the parse tree.

        It processes expressions to identify and potentially transform them using the custom MyCipher class.
        The method handles various conditions to ensure that encrypted or stringified expressions are appropriately transformed.

        Args:
            ctx (JavaParser.ExpressionContext): The context object representing the expression node in the parse tree.

        Functionality:
        - Checks if the expression is part of a specific rule index (105).
        - Determines the variable type of the expression based on the identifier list or member access.
        - Applies the appropriate transformation based on the variable type using MyCipher.
        - Handles different types of binary operations (e.g., assignment, equality, inequality).
        - For equality checks, ensures both sides of the expression are appropriately encoded/decoded.
        - Replaces the original expression with the transformed text in the token stream.
        - Updates the rewriter's token stream with the modified text.

        """
        try:
            if ctx.parentCtx.parentCtx.parentCtx.getRuleIndex() == 105:
                tCtx = ctx.parentCtx
                tVarType = None
                if tCtx.bop and tCtx.bop.text == "." and tCtx.getChildCount() > 1:
                    tVarType = self.extractList(tCtx.getText().split("."))
                else:
                    for id in self.executer.identifierList.findByFileName(
                            self.currentFile
                    ):
                        if (
                                id.editedName == tCtx.getText()
                                and id.line <= tCtx.start.line
                        ):
                            tVarType = id.varOrReturnType
                        if id.exactType == 47:
                            tVarType = None
                for token_type, transform_format in self.type_to_transform.items():
                    if token_type == tVarType and tVarType:
                        self.rewriter.replaceRangeTokens(
                            tCtx.start,
                            tCtx.stop,
                            transform_format.format(tCtx.getText()),
                        )
                        return

            if ctx.bop and (
                    ctx.bop.text == "=" or ctx.bop.text == "==" or ctx.bop.text == "!="
            ):
                left_exp = ctx.getChild(0)
                op = ctx.getChild(1)
                right_exp = ctx.getChild(2)
                literalPivot = right_exp.getChild(0).getChild(0)

                if isinstance(literalPivot, JavaParser.LiteralContext):
                    if literalPivot.NULL_LITERAL():
                        return
                tempList = None
                left_variable_type = ""
                if (
                        left_exp.bop
                        and left_exp.bop.text == "."
                        and left_exp.getChildCount() > 1
                ):
                    left_parts = left_exp.getText().split(".")
                    left_variable_type = self.extractList(left_parts)
                else:
                    tempList = self.executer.identifierList.identifiers.copy()
                    tempList.reverse()
                    for id in tempList:
                        if (
                                id.editedName == left_exp.getText()
                                and id.fileName == self.currentFile
                        ):
                            if id.isStringified:
                                left_variable_type = "String"
                            else:
                                left_variable_type = id.varOrReturnType
                            break
                # if the return type or varType is not accepted it returns
                if left_variable_type not in self.acceptedTypes:
                    return
                # TODO complete the right side transitions
                # find right side var type

                right_variable_type = None
                if right_exp.bop and right_exp.bop.text == ".":
                    right_parts = right_exp.getText().split(".")
                    right_variable_type = self.extractList(right_parts)
                if right_exp.getChildCount() > 1:
                    tempList = self.executer.identifierList.identifiers.copy()
                    tempList.reverse()
                    if right_variable_type is None:
                        for id in tempList:
                            if (
                                    id.editedName == right_exp.getChild(0).getText()
                                    and id.fileName == self.currentFile
                            ):
                                if id.isStringified:
                                    right_variable_type = "String"
                                else:
                                    right_variable_type = id.varOrReturnType
                                break
                        if (
                                right_variable_type is None
                                and right_exp.getChild(0).getText() in self.varType_dict
                        ):
                            right_variable_type = self.varType_dict[
                                right_exp.getChild(0).getText()
                            ]
                else:
                    if right_variable_type is None:
                        tempList = self.executer.identifierList.identifiers.copy()
                        tempList.reverse()
                        for id in tempList:
                            if (
                                    id.editedName == right_exp.getText()
                                    and id.fileName == self.currentFile
                            ):
                                if id.isStringified:
                                    right_variable_type = "String"
                                else:
                                    right_variable_type = id.varOrReturnType
                                break
                ttCtx = ctx.parentCtx
                while ttCtx.parentCtx:
                    if isinstance(ttCtx, JavaParser.ConstructorDeclarationContext):
                        modified_text = (
                            f"MyCipher.getInstance().encode({right_exp.getText()})"
                        )
                        # if self.currentFile == "Course.java":
                        #     print("b", right_exp.getText(), modified_text)
                        self.rewriter.replaceRangeTokens(
                            right_exp.start, right_exp.stop, modified_text
                        )
                        return
                    ttCtx = ttCtx.parentCtx
                if right_variable_type == left_variable_type:
                    return

                modified_text = f"MyCipher.getInstance().encode({right_exp.getText()})"
                if ctx.bop.text == "==":
                    modified_text = f"MyCipher.getInstance().decode(MyCipher.getInstance().encode({right_exp.getText()}))"
                    modified_left_text = (
                        f"MyCipher.getInstance().decode({left_exp.getText()})"
                    )
                    varType = None
                    tempParts = left_exp.getText().split(".")
                    tempParts2 = []
                    for part in tempParts:
                        tempParts2.append(part.split("(")[0])
                    index = len(tempParts2) - 1
                    tempParts2[:index]
                    if index == 1:
                        tempList = self.executer.identifierList.identifiers.copy()
                        tempList.reverse()
                        for id in tempList:
                            if (
                                    id.editedName == tempParts2[0]
                                    and id.fileName == self.currentFile
                            ):
                                varType = id.varOrReturnType
                    else:
                        varType = self.extractList(tempParts2[:index])
                    for id in self.executer.identifierList.findByType(7):
                        if id.name == varType:
                            modified_left_text = f"MyCipher.getInstance().decode(MyCipher.getInstance().encode({left_exp.getText()}))"
                    self.rewriter.replaceRange(
                        left_exp.start.tokenIndex,
                        left_exp.stop.tokenIndex,
                        modified_left_text,
                    )
                self.rewriter.replaceRangeTokens(
                    right_exp.start, right_exp.stop, modified_text
                )
                return
            return
        except:
            pass
        # END YOUR CODE HERE

    def enterExpression(self, ctx: JavaParser.ExpressionContext):
        """
        This method is called when the parser enters an expression context. It processes
        expressions to determine if any transformations are needed, specifically focusing
        on method calls and member accesses.

        Purpose:
        - To identify and handle specific expressions involving method calls and member
          accesses, ensuring that transformations are applied appropriately.

        Functionality:
        1. Check if the expression contains a member access or method call.
           - `ctx.bop` and `ctx.bop.text == "."` ensures the expression involves a dot
             operator (member access or method call).

        2. Skip transformations for expressions starting with certain predefined types or
           methods.
           - Iterate through a list of predefined types and method calls (e.g.,
             "Integer", "Float", "Double", "MyCipher.getInstance().decode", etc.).
           - If the expression starts with any of these, it returns without making any
             changes.
        3. Handle specific class method calls that should be ignored.
           - Iterates through a list of class names (`self.executer.mini_should_ignore_classes`).
           - If the expression contains a method call from one of these classes, it
             processes the expression further.
        4. Extract and split the expression parts.
           - Splits the expression into parts based on the dot operator.
           - Identifies the index of the relevant class name within the parts.

        5. Resolve transformations before the specific method call.
           - Retrieves the child context at the relevant index.
           - Ensures the child context rule index matches the expected value (98).
           - Calls `self.resolveBeforTheShould(ctx, name)` to handle any necessary
             transformations before the method call.

        Exception Handling:
        - The method is wrapped in a try-except block to gracefully handle any unexpected
          errors without interrupting the parsing process.

        Parameters:
        - ctx (JavaParser.ExpressionContext): The context object representing the
          expression.

        Usage:
        - This method is automatically invoked by the ANTLR parse tree walker when it
          encounters an expression node in the parse tree.
        """
        try:
            if ctx.bop and ctx.bop.text == ".":
                for start in (
                        "Integer",
                        "Float",
                        "Double",
                        "MyCipher.getInstance().decode",
                        "Boolean",
                        "String",
                        "System",
                        "Math",
                        "Char",
                        "Short",
                        "Long",
                        "Byte",
                ):
                    if ctx.getText().startswith(start):
                        return
                for name in self.executer.mini_should_ignore_classes:
                    if name + "(" in ctx.getText():
                        tempParts = ctx.getText().split(".")
                        tempParts2 = []
                        for part in tempParts:
                            tempParts2.append(part.split("(")[0])
                        index = tempParts2.index(name)

                        temppCtx = ctx.getChild(2 * index)
                        if temppCtx.getRuleIndex() != 98:
                            return
                        self.resolveBeforeTheShould(ctx, name)
                        return
        except:
            pass

    # DO NOT CHANGE THIS METHOD
    def resolveBeforeTheShould(self, ctx, functionName):
        """
        This method resolves and transforms expressions before specific method calls,
        ensuring that necessary transformations are applied to variable references
        and method calls in the context.

        Purpose:
        - To identify and apply necessary transformations to parts of an expression
          before a specific method call, particularly for method calls that should be
          handled in a special way.

        Functionality:
        1. Extract and split the expression into parts.
           - Splits the expression text into parts based on the dot operator.
           - Further splits each part to handle method calls separately.

        2. Identify the relevant index of the function name within the parts.
           - Finds the index of the specified `functionName` in the split parts.

        3. Reverse the identifier list for easier backward search.
           - Reverses the list of identifiers to facilitate searching from the
             current context backward.

        4. Search for the first part of the expression in the identifier list.
           - Iterates through the reversed identifier list to find a match for the
             first part of the expression.
           - Checks if the file name matches and if the identifier's line number is
             less than or equal to the current context's line number.

        5. Determine the variable type (`varType`).
           - If the index is 1, searches the identifier list for the variable type.
           - Otherwise, calls `self.extractList` to recursively determine the
             variable type from the parts.

        6. Apply transformations based on the variable type.
           - Iterates through the `type_to_transform` dictionary to find the
             appropriate transformation format for the variable type.
           - Constructs the transformed text and replaces the original text in the
             token stream using `self.rewriter.replaceRangeTokens`.

        Parameters:
        - ctx (JavaParser.ExpressionContext): The context object representing the
          expression.
        - functionName (str): The name of the function to handle specially.

        """
        varType = None
        tempParts = ctx.getText().split(".")
        tempParts2 = []
        for part in tempParts:
            tempParts2.append(part.split("(")[0])
        index = tempParts2.index(functionName)
        list = self.executer.identifierList.identifiers.copy()
        list.reverse()
        for id in list:
            if id.editedName == tempParts2[0] or id.name == tempParts2[0]:
                if self.currentFile == id.fileName:
                    if (
                            id.exactType == 44
                            or id.exactType == 47
                            and id.line <= ctx.start.line
                    ):
                        return
        if index == 1:
            for id in list:
                if tempParts[0] == id.editedName or tempParts[0] == id.name:
                    if self.currentFile == id.fileName or (
                            id.type in (7, 11, 13, 15) or id.exactType == 95
                    ):
                        varType = id.varOrReturnType
        else:
            varType = self.extractList(tempParts[:index])
        for (
                token_type,
                transform_format,
        ) in self.type_to_transform.items():
            if token_type == varType and varType:
                text = ".".join(tempParts[:index])
                text2 = transform_format.format(text)
                out = ctx.getText()
                out = out.replace(text, text2)
                self.rewriter.replaceRangeTokens(
                    ctx.start,
                    ctx.stop,
                    ctx.getText().replace(text, text2),
                )
                return

    # DO NOT CHANGE THIS CODE
    def extractList(self, parts, prev_iteration_file=""):
        left = parts[0]
        second_left_part = ""
        if len(parts) > 1:
            second_left_part = parts[1]

        if left == "this":
            left_name = self.currentFile.replace(".java", "")
        else:
            left_name = left
        left_isMethod = "(" in left_name

        for id in self.executer.identifierList.identifiers:
            if (
                    not left_isMethod
                    and (left_name == id.editedName or left_name == id.name)
            ) or (
                    left_isMethod
                    and id.type == 20
                    and (
                            id.name == left_name.split("(")[0]
                            or id.editedName == left_name.split("(")[0]
                    )
            ):
                if (
                        id.fileName == self.currentFile
                        or prev_iteration_file == id.fileName
                        or id.type in (7, 11, 13, 15)
                ):
                    varType = id.varOrReturnType
                    if varType is None:
                        return
                    second_left_filename = varType + ".java"
                    varTypeWithoutArr = None
                    if varType.startswith("ArrayList"):
                        varTypeWithoutArr = varType.split("ArrayList<")[1].replace(
                            ">", ""
                        )
                    for iden in self.executer.identifierList.identifiers:
                        if "get" in second_left_part and varTypeWithoutArr:
                            return varTypeWithoutArr
                        if "decode" in second_left_part or "encode" in second_left_part:
                            return id.varOrReturnType
                        elif iden.fileName == second_left_filename:
                            if (
                                    iden.name == second_left_part
                                    or iden.editedName == second_left_part
                            ) or (
                                    iden.type == 20
                                    and (
                                            iden.editedName == second_left_part.split("(")[0]
                                            or iden.name == second_left_part.split("(")[0]
                                    )
                            ):
                                del parts[0]
                                if len(parts) > 1:
                                    return self.extractList(
                                        parts, second_left_filename
                                    )  # Recursive call
                                else:
                                    # if iden.isStringified:
                                    # varType = "String"
                                    # else:
                                    varType = iden.varOrReturnType
                                    return varType

    def exitVariableInitializer(self, ctx: JavaParser.VariableInitializerContext):
        """
        TODO
        This method is called when the parser exits a variable initializer context. It
        processes variable initializations and applies transformations, specifically
        focusing on encoding string literals.

        Purpose:
        - To encode string literals during variable initialization using `MyCipher`.

        Functionality:
        1. Retrieve the text of the variable initializer.
           - `text = ctx.getText()` gets the full text of the variable initializer context.

        2. Determine the type of the variable being initialized.
           - `variable_type = ctx.parentCtx.parentCtx.parentCtx.getChild(0).getText()`
             navigates up the parse tree to get the type of the variable.

        3. Get the starting token of the context.
           - `token = ctx.start` retrieves the starting token for the variable initializer.

        4. Get the first child of the context (the value being assigned).
           - `pivot = ctx.getChild(0)` gets the first child of the variable initializer
             context, which represents the value being assigned.

        5. Check if the value being assigned is complex (has multiple parts).
           - `if pivot.getChildCount() > 1:` checks if the value has more than one part.

        6. Encode the string value if the variable type is `String`.
           - `if variable_type == "String":` checks if the variable type is `String`.
           - Constructs the encoded text using `MyCipher.getInstance().encode({ctx.getText()})`.
           - Replaces the original text with the encoded text in the token stream using
             `self.rewriter.replaceRange`.

        Parameters:
        - ctx (JavaParser.VariableInitializerContext): The context object representing
          the variable initializer.

        Usage:
        - This method is automatically invoked by the ANTLR parse tree walker when it
          exits a variable initializer node in the parse tree.
        """
        # START YOUR CODE HERE
        text = ctx.getText()
        variable_type = ctx.parentCtx.parentCtx.parentCtx.getChild(0).getText()
        token = ctx.start
        pivot = ctx.getChild(0)
        # print(pivot.getText())
        if pivot.getChildCount() > 1:
            if variable_type == "String":
                # String b = a - 3 -> String b = "asdasdasdasxasxaw"

                modified_text = f"MyCipher.getInstance().encode({ctx.getText()})"
                self.rewriter.replaceRange(
                    pivot.start.tokenIndex, pivot.stop.tokenIndex, modified_text
                )
                return

        otherType = ctx.getChild(0).getChild(0)
        if isinstance(otherType, JavaParser.PrimaryContext):
            if variable_type in ["final", "public", "private"]:
                variable_type = (
                    variable_type
                ) = ctx.parentCtx.parentCtx.parentCtx.getChild(1).getText()
            if variable_type in self.acceptedTypes:
                for en in getEncrypted():
                    try:
                        if not en.identifier.isEncrypted:
                            return

                        if not en.identifier.value == text:
                            # string a = 3 -> string a = "asdasdawsasASXASX"
                            if variable_type == "String":
                                token.text = f'"{self.makeNewValue(text, token)}"'
                                # print(token.text)
                    except:
                        # print("No identifier")
                        # print(ctx.start.line, self.currentFile, ctx.getText())
                        pass
        # END YOUR CODE HERE

    def changeRewriterTokenStream(self, text):
        # Create an ANTLR input stream from the modified text
        input_stream = InputStream(text)

        # Create an instance of your lexer using the input stream
        lexer = JavaLexer(input_stream)  # Replace with your lexer class

        # Generate tokens using the lexer
        token_stream = CommonTokenStream(lexer)

        # Update self.token_stream_writer's token stream
        self.executer.tokenStreamDict[self.currentFile] = token_stream

    # DO NOT CHANGE THIS CODE
    def getConstructorName(self, ctx):
        parent = ctx.parentCtx
        while parent:
            if parent.getRuleIndex() == JavaParser.RULE_constructorDeclaration:
                return parent.identifier().getText()
            parent = parent.parentCtx
        return None

    # DO NOT CHANGE THIS CODE
    def getIdentifier(self, ctx):
        name = ctx.getText()
        for id in self.executer.identifierList.identifiers:
            if id.editedName == name:
                return id

    def visitTerminal(self, node):
        token = node.symbol
        # print(self.modified_tokens)

        if token is not None:
            # Use the token's line and column as a unique identifier
            token_key = (token.line, token.column)

            # if token_key in self.executer.modified_tokens:
            # token.text = self.executer.modified_tokens[token_key]

            self.out.append(token.text)
            # print(token)

        return super().visitTerminal(node)

    def makeNewValue(self, value, token):
        line = token.line
        encoder = encodeString(value, line, self.currentFile)
        # print("----------------------------")
        # print(value, encoder.cipherHex, encoder.ivHex, encoder.keyHex)
        return encoder.cipherHex
