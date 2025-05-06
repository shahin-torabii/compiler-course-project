from antlr4.Token import *

from JavaParser import *
from src.logic.Encoding.Cipher import *
from src.logic.Identifier import *
from src.logic.JavaLexer import JavaLexer
from src.logic.JavaParserListener import *

from antlr4 import *
from antlr4.TokenStreamRewriter import *

from src.logic.JavaParser import JavaParser


class Renamer(JavaParserListener):
    def __init__(self, currentFile, executer, parser, common_token_stream):
        self.executer = executer
        self.currentFile = currentFile
        self.parser = parser
        self.out = []
        self.literals = []
        self.i = 1
        self.symbol_table = {}
        self.commonTokenStream = common_token_stream
        if common_token_stream is not None:
            self.rewriter = TokenStreamRewriter(common_token_stream)
        self.typesDic = {
            7: [7, 51, 104, 25, 111, 41, 82],
            11: [11, 104, 41, 82, 51],
            20: [20, 98, 41, 99, 104],
            38: [38, 104, 99],
            13: [13, 99, 104],
            15: [15, 51, 41, 82],
            35: [35, 98, 20],
            31: [31, 104],
        }

    # DO NOT CHANGE THIS METHOD
    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        for id in self.executer.identifierList.identifiers:
            for id2 in self.executer.identifierList.identifiers:
                if (
                        id.name == id2.name
                        and id.fileName == id2.fileName
                        and id.type == id2.type
                        and id.line != id2.line
                ):
                    id2.editedName = id.editedName
                    id.editedName = id2.editedName

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

    def enterTypeDeclaration(self, ctx: JavaParser.TypeDeclarationContext):
        """
        This method is called when entering a type declaration in the parse tree.

        It ensures that the import statement for the custom `MyCipher` class is added at the beginning
        of the type declaration. This is done to ensure that the necessary encryption/decryption functionality
        is available for use within the class. The import statement is only added once, regardless of the number
        of type declarations processed.

        Args:
            ctx (JavaParser.TypeDeclarationContext): The context object representing the type declaration node in the parse tree.

        TODO:
        - Verify that the import statement is not already present before adding it.
        - Ensure compatibility with different Java versions and coding styles.
        - Consider handling multiple type declarations in a single file.
        - Add error handling for cases where the token insertion might fail.
        """
        # START YOUR CODE HERE
        # Check if the import statement has already been added.
        while self.i == 1:
            # Insert the import statement for the custom MyCipher class.
            self.rewriter.insertBeforeToken(
                ctx.start, "import ir.ac.kntu.MyCipher;\n\n"
            )
            # Update the token stream with the modified text.
            self.changeRewriterTokenStream(self.rewriter.getDefaultText())
            self.i += 1
        # END YOUR CODE HERE

    def enterIdentifier(self, ctx: JavaParser.IdentifierContext):
        self.castIdent(ctx)

    # TODO: Implement logic to process literal nodes based on their context and conditions specified below
    # - Skip modification if the literal is part of a switch label context.
    # - Skip modification if the literal is an empty string or a single space.
    # - Traverse up the parent contexts to check if the literal is part of a variable declaration,
    # and skip modification if it is.
    # - If none of the above conditions are met, call the method to edit the literal.

    def enterLiteral(self, ctx: JavaParser.LiteralContext):
        # START YOUR CODE HERE
        last_parent = ctx.parentCtx.parentCtx.parentCtx
        if (
                isinstance(last_parent, JavaParser.SwitchLabelContext)
                or last_parent.parentCtx.getRuleIndex() == 106
        ):
            return
        if ctx.getText() == '""' or ctx.getText() == '" "':
            return
        # Walk up parent contexts until we find a common ancestor
        parent = ctx.parentCtx
        while parent:
            if isinstance(parent, JavaParser.VariableDeclaratorContext):
                # Literal is part of a variable declaration, don't modify
                return

            parent = parent.parentCtx
        self.editLiteral(ctx)
        # END YOUR CODE HERE

    # TODO: Implement logic to edit literal values based on their type and context specified below
    # - Define a dictionary mapping literal types to their transformation formats using MyCipher.
    # - Retrieve the token and text of the literal.
    # - For string and character literals, strip the surrounding quotes.
    # - Iterate over the dictionary to find the matching token type and apply the corresponding transformation.
    # - Skip transformation if the text starts with a Unicode escape sequence.
    # - Use the transformation format to encode the literal and update the token's text.
    def editLiteral(self, ctx):
        # START YOUR CODE HERE
        transformed = {
            ctx.STRING_LITERAL: 'MyCipher.getInstance().decode("{}")',
            ctx.integerLiteral: 'Integer.parseInt(MyCipher.getInstance().decode("{}"))',
            ctx.floatLiteral: 'Float.parseFloat(MyCipher.getInstance().decode("{}"))',
            ctx.CHAR_LITERAL: 'MyCipher.getInstance().decode("{}").charAt(0)',
            ctx.BOOL_LITERAL: 'Boolean.parseBoolean(MyCipher.getInstance().decode("{}"))',
        }
        token = ctx.start
        text = ctx.getText()
        if ctx.STRING_LITERAL() or ctx.CHAR_LITERAL():
            text = text[1:-1]

        for token_type, transform_format in transformed.items():
            if token_type():
                if text.startswith("\\u"):
                    return
                print(text)
                token.text = transform_format.format(self.makeNewValue(text, token))
                print(token.text)
                break  # Stop processing after the first match
        # END YOUR CODE HERE

    # TODO: Implement logic to handle variable initializers and recursively traverse them based on conditions specified below
    # - Retrieve the text and variable type of the initializer.
    # - Identify the starting token and the first child of the initializer.
    # - If the first child has more than one child, traverse the variable initializer to handle complex expressions.
    # - Implement a helper method to recursively traverse the initializer and edit literals as needed.

    def exitVariableInitializer(self, ctx: JavaParser.VariableInitializerContext):
        # START YOUR CODE HERE
        this_child = ctx.getChild(0)
        if this_child.getChildCount() > 1:
            self.traverse_variable_initializer(this_child, self.literals)

    def traverse_variable_initializer(self, ctx, literals):
        # Check if the current context is an instance of LiteralContext
        if isinstance(ctx, JavaParser.LiteralContext):
            self.editLiteral(ctx)
            literals.append(ctx.getText())

        # Iterate through the children of the current context
        try:
            for child in ctx.getChildren():
                # Recursively call the function on each child
                self.traverse_variable_initializer(child, literals)
        except:
            return

        # END YOUR CODE HERE

    def enterTypeIdentifier(self, ctx: JavaParser.TypeIdentifierContext):
        self.castIdent(ctx)

    # DO NOT CHANGE THIS CODE
    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_name = ctx.identifier().getText()
        for id in self.executer.identifierList.identifiers:
            if id.name == method_name:
                method_name = id.editedName
        params = []
        formal_params_ctx = ctx.formalParameters()

        if formal_params_ctx.formalParameterList():
            for p in formal_params_ctx.formalParameterList().formalParameter():
                # Get IDENTIFIER from variableDeclaratorId
                id_ctx = p.variableDeclaratorId()
                param_name = id_ctx.identifier().getText()
                params.append(param_name)

        self.executer.symbol_table[method_name] = params

    # DO NOT CHANGE THIS METHOD
    def enterConstructorDeclaration(
            self, ctx: JavaParser.ConstructorDeclarationContext
    ):
        constructor_name = ctx.identifier().getText()
        for id in self.executer.identifierList.identifiers:
            if id.name == constructor_name:
                constructor_name = id.editedName
        params = []
        formal_params_ctx = ctx.formalParameters()

        if formal_params_ctx.formalParameterList():
            for p in formal_params_ctx.formalParameterList().formalParameter():
                # Get IDENTIFIER from variableDeclaratorId
                id_ctx = p.variableDeclaratorId()
                param_name = id_ctx.identifier().getText()
                params.append(param_name)

        self.executer.symbol_table[constructor_name] = params

    def enterPrimary(self, ctx: JavaParser.PrimaryContext):
        """
        This method is called when entering a primary expression in the parse tree.

        It processes primary expressions to identify and potentially rename identifiers
        based on their context. The method handles various conditions to ensure that
        encrypted or stringified identifiers are appropriately transformed using the
        custom MyCipher class.

        Args:
            ctx (JavaParser.PrimaryContext): The context object representing the primary expression node in the parse tree.

        Functionality:
        - Retrieves the text of the primary expression.
        - Determines the method and constructor names if applicable.
        - Checks if the primary expression is part of a member access and validates the type of the left part.
        - Traverses up the parent contexts to identify the left-hand side of assignments.
        - Skips renaming for identifiers in certain contexts like enhanced for loops.
        - For encrypted or stringified identifiers, applies the appropriate decryption transformation based on the variable type.
        - Replaces the original identifier with the transformed text in the token stream.
        - Updates the rewriter's token stream with the modified text.

        """
        name = ctx.getText()

        method_name = self.getMethodName(ctx)
        constructor_name = self.getConstructorName(ctx)

        tempCtx = ctx.parentCtx.parentCtx
        if (
                hasattr(tempCtx, "bop")
                and tempCtx.bop
                and tempCtx.bop.text == "."
                and tempCtx.getChildCount() > 1
        ):
            left_parts = tempCtx.getText().split(".")
            left_varType = self.extractList(left_parts)
            if (left_varType is None) or (
                    left_varType
                    not in (
                            "int",
                            "boolean",
                            "long",
                            "short",
                            "float",
                            "double",
                            "char",
                            "final",
                            "String",
                    )
            ):
                return

        tempCtx = ctx.parentCtx
        left_exp = None
        while tempCtx.parentCtx is not None:
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
            tempCtx = tempCtx.parentCtx

        for id in self.executer.identifierList.identifiers:
            if id.name == name:
                if not id.isEncrypted:
                    if self.enhancedForCheck(ctx, id):
                        return
        for en in self.executer.identifierList.identifiers:
            try:
                if (
                        left_exp
                        and name == left_exp.getText()
                        and left_exp.start == ctx.start
                ):
                    return
                if method_name and name in self.executer.symbol_table[method_name]:
                    return
                if (
                        constructor_name
                        and name in self.executer.symbol_table[constructor_name]
                ):
                    return
                if (
                        en.name == name
                        and en.fileName == self.currentFile
                        and (en.isEncrypted or en.isStringified)
                ):

                    variable_type = en.varOrReturnType
                    varEditedName = en.editedName
                    if variable_type == "String":
                        text = f"MyCipher.getInstance().decode({varEditedName})"
                    elif variable_type == "int":
                        text = f"Integer.parseInt(MyCipher.getInstance().decode({varEditedName}))"
                    elif variable_type == "double":
                        text = f"Double.parseDouble(MyCipher.getInstance().decode({varEditedName}))"
                    elif variable_type == "float":
                        text = f"Float.parseFloat(MyCipher.getInstance().decode({varEditedName}))"
                    elif variable_type == "long":
                        text = f"Long.parseLong(MyCipher.getInstance().decode({varEditedName}))"
                    elif variable_type == "short":
                        text = f"Short.parseShort(MyCipher.getInstance().decode({varEditedName}))"
                    elif variable_type == "char":
                        text = (
                            f"MyCipher.getInstance().decode({varEditedName}).charAt(0)"
                        )
                    elif variable_type == "boolean":
                        text = f"Boolean.parseBoolean(MyCipher.getInstance().decode({varEditedName}))"
                    self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, text)
                    self.changeRewriterTokenStream(self.rewriter.getDefaultText())
                    return

            except:
                pass
        list = self.executer.identifierList.identifiers.copy()
        list.reverse()
        if (
                ctx.getChild(0)
                and hasattr(ctx.getChild(0), "getRuleIndex")
                and name == ctx.getChild(0).getText()
                and ctx.getRuleIndex() == 104
                and ctx.getChild(0).getRuleIndex() == 81
        ):
            # TODO: Implement logic to transform encrypted or stringified identifiers based on their variable type
            # - Retrieve the variable type and edited name from the identifier.
            # - Apply the appropriate decryption transformation based on the variable type using MyCipher.
            # - Replace the original identifier with the transformed text in the token stream.
            # - Update the rewriter's token stream with the modified text.

            # START YOUR CODE HERE
            for id in list:
                if (
                        (id.editedName == name or id.name == name)
                        and id.fileName == self.currentFile
                        and ctx.parentCtx.getRuleIndex() in self.typesDic[id.type]
                ):
                    v_type = id.varOrReturnType
                    text = None
                    if v_type == "String":
                        text = f"MyCipher.getInstance().decode({id.editedName})"
                    elif v_type == "int":
                        text = f"Integer.parseInt(MyCipher.getInstance().decode({id.editedName}))"
                    elif v_type == "double":
                        text = f"Double.parseDouble(MyCipher.getInstance().decode({id.editedName}))"
                    elif v_type == "float":
                        text = f"Float.parseFloat(MyCipher.getInstance().decode({id.editedName}))"
                    elif v_type == "long":
                        text = f"Long.parseLong(MyCipher.getInstance().decode({id.editedName}))"
                    elif v_type == "short":
                        text = f"Short.parseShort(MyCipher.getInstance().decode({id.editedName}))"
                    elif v_type == "char":
                        text = (
                            f"MyCipher.getInstance().decode({id.editedName}).charAt(0)"
                        )
                    elif v_type == "boolean":
                        text = f"Boolean.parseBoolean(MyCipher.getInstance().decode({id.editedName}))"
                    if text:
                        self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, text)
                        self.changeRewriterTokenStream(self.rewriter.getDefaultText())
                        return

            # END YOUR CODE HERE

    # TODO: Implement logic to handle primary expressions and rename identifiers based on their context and conditions specified below
    # - Retrieve the text of the primary expression.
    # - Traverse up the parent contexts to identify the left-hand side of assignments.
    # - Skip renaming for identifiers in certain contexts like enhanced for loops.
    # - If the primary expression is part of a member access, validate the type of the left part.
    # - Replace the original identifier with the transformed text in the token stream if it is encrypted or stringified.
    # - Update the rewriter's token stream with the modified text.

    def exitPrimary(self, ctx: JavaParser.PrimaryContext):
        name = ctx.getText()

        tempCtx = ctx.parentCtx
        left_exp = None
        while tempCtx.parentCtx is not None:
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
            tempCtx = tempCtx.parentCtx

        for id in self.executer.identifierList.identifiers:
            if id.name == name:
                if not id.isEncrypted:
                    if self.enhancedForCheck(ctx, id):
                        return
        if left_exp and name == left_exp.getText() and left_exp.start == ctx.start:
            return

        tempCtx = ctx.parentCtx.parentCtx
        if (
                hasattr(tempCtx, "bop")
                and tempCtx.bop
                and tempCtx.bop.text == "."
                and tempCtx.getChildCount() > 1
        ):
            if left_exp and tempCtx.getText() == left_exp.getText():
                return
            left_parts = tempCtx.getText().split(".")
            left_varType = self.extractList(left_parts)
            if (left_varType is None) or (
                    left_varType
                    not in (
                            "int",
                            "boolean",
                            "long",
                            "short",
                            "float",
                            "double",
                            "char",
                            "final",
                            "String",
                    )
            ):
                return
            tempName = tempCtx.getChild(tempCtx.getChildCount() - 1).getText()
            tempIds = tempCtx.getText()

            for part in left_parts:
                for en in self.executer.identifierList.identifiers:
                    if (
                            en.name == part
                            and en.fileName == self.currentFile
                            and part != "this"
                    ):
                        tempIds = tempIds.replace("." + part, "." + en.editedName)
            # START YOUR CODE HERE
            for en in self.executer.identifierList.identifiers:
                try:
                    if (
                            en.name == tempName
                            and en.fileName == self.currentFile
                            and (en.isEncrypted or en.isStringified)
                    ):
                        if left_varType == "String":
                            text = f"MyCipher.getInstance().decode({tempIds})"
                        elif left_varType == "int":
                            text = f"Integer.parseInt(MyCipher.getInstance().decode({tempIds}))"
                        elif left_varType == "double":
                            text = f"Double.parseDouble(MyCipher.getInstance().decode({tempIds}))"
                        elif left_varType == "float":
                            text = f"Float.parseFloat(MyCipher.getInstance().decode({tempIds}))"
                        elif left_varType == "long":
                            text = f"Long.parseLong(MyCipher.getInstance().decode({tempIds}))"
                        elif left_varType == "short":
                            text = f"Short.parseShort(MyCipher.getInstance().decode({tempIds}))"
                        elif left_varType == "char":
                            text = f"MyCipher.getInstance().decode({tempIds}).charAt(0)"
                        elif left_varType == "boolean":
                            text = f"Boolean.parseBoolean(MyCipher.getInstance().decode({tempIds}))"
                        self.rewriter.replaceRangeTokens(
                            tempCtx.start, tempCtx.stop, text
                        )
                        self.changeRewriterTokenStream(self.rewriter.getDefaultText())
                        break
                except:
                    pass
            # END YOUR CODE HERE

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

    # DO NOT CHANGE THIS METHOD
    def getMethodName(self, ctx):
        # Get the parent method name
        parent = ctx.parentCtx
        while parent:
            if parent.getRuleIndex() == JavaParser.RULE_methodDeclaration:
                return parent.identifier().getText()
            parent = parent.parentCtx
        return None

    # DO NOT CHANGE THIS METHOD
    def getConstructorName(self, ctx):
        parent = ctx.parentCtx
        while parent:
            if parent.getRuleIndex() == JavaParser.RULE_constructorDeclaration:
                return parent.identifier().getText()
            parent = parent.parentCtx
        return None

    # DO NOT CHANGE THIS METHOD
    def enhancedForCheck(self, ctx, id):
        tempCtx = ctx
        while tempCtx.parentCtx is not None:
            if isinstance(tempCtx, JavaParser.StatementContext):
                break
            tempCtx = tempCtx.parentCtx
        while tempCtx.parentCtx is not None:
            if (
                    hasattr(tempCtx, "FOR")
                    and tempCtx.FOR()
                    and tempCtx.forControl()
                    and tempCtx.forControl().enhancedForControl()
            ):
                if (
                        id.editedName
                        == tempCtx.forControl()
                        .enhancedForControl()
                        .variableDeclaratorId()
                        .identifier()
                        .getText()
                ):
                    return True
            tempCtx = tempCtx.parentCtx
        return False

    # DO NOT CHANGE THIS METHOD
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
    def castIdent(self, ctx):
        """
        This method processes and renames identifiers based on their context within the parse tree.

        It ensures that identifiers are correctly renamed according to their edited names stored in the
        executer's identifier list. The method also handles specific cases such as member accesses and
        ignoring certain classes.

        Args:
            ctx: The context object representing the identifier node in the parse tree.
        Pre-made functionalities:
            - Add more comprehensive documentation for each conditional block.
            - Optimize the logic for extracting and processing parts of the identifier.
            - Handle edge cases where identifiers might be part of complex expressions.
        """

        name = ctx.getText()
        type = ctx.parentCtx.getRuleIndex()
        temp = ctx.parentCtx.parentCtx

        # Check for member access and ignore system classes
        if (
                hasattr(temp, "bop")
                and temp.bop
                and temp.bop.text == "."
                and temp.getChildCount() > 1
        ):
            if temp.getChild(0).getChild(0).getText() in ["System"]:
                return
        list = self.executer.identifierList.identifiers.copy()
        list.reverse()

        temp = ctx.parentCtx.parentCtx
        if (
                hasattr(temp, "bop")
                and temp.bop
                and temp.bop.text == "."
                and temp.getChildCount() > 1
        ):
            tempParts = temp.getText().split(".")
            tempParts2 = []
            for part in tempParts:
                tempParts2.append(part.split("(")[0])
            index = tempParts2.index(name)
            varType = None
            if index == 1:
                if tempParts[0] == "this":
                    varType = self.currentFile.replace(".java", "")
                else:
                    for id in list:
                        if tempParts[0] == id.editedName or tempParts[0] == id.name:
                            if self.currentFile == id.fileName or (
                                    id.type in (7, 11, 13, 15) or id.exactType == 95
                            ):
                                varType = id.varOrReturnType
            else:
                varType = self.extractList(tempParts[:index])

            if varType is None or (varType + ".java" not in self.executer.fileNames):
                return

            extends = None
            for id in list:
                if (
                        id.fileName == varType + ".java"
                        and varType == id.name
                        and id.type == 7
                        and id.extend
                ):
                    extends = id.extend
            for id in list:
                if (
                        id.name == name
                        and type in self.typesDic[id.type]
                        and (
                        id.fileName == varType + ".java"
                        or (extends and id.fileName == extends + ".java")
                )
                ):
                    ctx.start.text = id.editedName
                    return
            return

        for id in list:
            if id.name == name:
                if name in self.executer.should_ignore_classes:
                    temp = ctx.parentCtx.parentCtx
                    if (
                            hasattr(temp, "bop")
                            and temp.bop
                            and temp.bop.text == "."
                            and temp.getChildCount() > 1
                    ):
                        if name in temp.getText():
                            return
                if self.currentFile == id.fileName and type in self.typesDic[id.type]:
                    if id.type == 38 and id.exactType in (37, 36):
                        if id.line - 2 <= ctx.start.line:
                            ctx.start.text = id.editedName
                            return
                    else:
                        ctx.start.text = id.editedName
                        return
        for id in list:
            if id.name == name:
                if type in self.typesDic[id.type]:
                    ctx.start.text = id.editedName
                    return

    def visitTerminal(self, node):
        token = node.symbol

        if token is not None:
            # Use the token's line and column as a unique identifier
            token_key = (token.line, token.column)

            # if token_key in self.executer.modified_tokens:
            # token.text = self.executer.modified_tokens[token_key]

            self.out.append(token.text)

        return super().visitTerminal(node)

    def makeNewValue(self, value, token):
        line = token.line
        encoder = encodeString(value, line, self.currentFile)
        return encoder.cipherHex
