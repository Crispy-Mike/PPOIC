"""
Модуль парсинга логических выражений.
Поддерживаемые операции: & (AND), | (OR), ! (NOT), -> (IMPLIES), ~ (XOR)
Переменные: a, b, c, d, e (до 5 переменных)
"""

from typing import List, Optional, Set
import re


class Token:
    """Токен для лексического анализа."""
    
    VARIABLE = 'VARIABLE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    IMPLIES = 'IMPLIES'
    XOR = 'XOR'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'
    
    def __init__(self, token_type: str, value: str):
        self.type = token_type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Lexer:
    """Лексический анализатор логических выражений."""
    
    VALID_VARIABLES: Set[str] = {'a', 'b', 'c', 'd', 'e'}
    
    def __init__(self, text: str):
        self.text = text.replace(' ', '').replace('\t', '').replace('\n', '')
        self.pos = 0
        self.current_char: Optional[str] = self.text[0] if self.text else None
    
    def advance(self) -> None:
        """Перемещение к следующему символу."""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Просмотр символа на позиции offset без перемещения."""
        peek_pos = self.pos + offset
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None
    
    def tokenize(self) -> List[Token]:
        """Разбиение входной строки на токены."""
        tokens = []
        
        while self.current_char is not None:
            if self.current_char in ' \t\n':
                self.advance()
                continue
            
            if self.current_char == '&':
                tokens.append(Token(Token.AND, '&'))
                self.advance()
            
            elif self.current_char == '|':
                tokens.append(Token(Token.OR, '|'))
                self.advance()
            
            elif self.current_char == '!':
                tokens.append(Token(Token.NOT, '!'))
                self.advance()
            
            elif self.current_char == '-' and self.peek() == '>':
                tokens.append(Token(Token.IMPLIES, '->'))
                self.advance()
                self.advance()
            
            elif self.current_char == '~':
                tokens.append(Token(Token.XOR, '~'))
                self.advance()
            
            elif self.current_char == '(':
                tokens.append(Token(Token.LPAREN, '('))
                self.advance()
            
            elif self.current_char == ')':
                tokens.append(Token(Token.RPAREN, ')'))
                self.advance()
            
            elif self.current_char.isalpha():
                var_name = self.current_char.lower()
                if var_name not in self.VALID_VARIABLES:
                    raise ValueError(f"Недопустимая переменная: {var_name}. "
                                   f"Разрешены: {self.VALID_VARIABLES}")
                tokens.append(Token(Token.VARIABLE, var_name))
                self.advance()
            
            else:
                raise ValueError(f"Недопустимый символ: {self.current_char}")
        
        tokens.append(Token(Token.EOF, ''))
        return tokens


class ASTNode:
    """Базовый класс для узлов абстрактного синтаксического дерева."""
    
    def evaluate(self, variables: dict) -> bool:
        """Вычисление значения узла при заданных переменных."""
        raise NotImplementedError
    
    def get_variables(self) -> Set[str]:
        """Получение множества переменных, используемых в узле."""
        raise NotImplementedError
    
    def __str__(self) -> str:
        """Строковое представление узла."""
        raise NotImplementedError


class VariableNode(ASTNode):
    """Узел переменной."""
    
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, variables: dict) -> bool:
        return bool(variables.get(self.name, False))
    
    def get_variables(self) -> Set[str]:
        return {self.name}
    
    def __str__(self) -> str:
        return self.name


class NotNode(ASTNode):
    """Узел операции NOT."""
    
    def __init__(self, operand: ASTNode):
        self.operand = operand
    
    def evaluate(self, variables: dict) -> bool:
        return not self.operand.evaluate(variables)
    
    def get_variables(self) -> Set[str]:
        return self.operand.get_variables()
    
    def __str__(self) -> str:
        return f"!({self.operand})"


class AndNode(ASTNode):
    """Узел операции AND."""
    
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def evaluate(self, variables: dict) -> bool:
        return self.left.evaluate(variables) and self.right.evaluate(variables)
    
    def get_variables(self) -> Set[str]:
        return self.left.get_variables() | self.right.get_variables()
    
    def __str__(self) -> str:
        return f"({self.left}&{self.right})"


class OrNode(ASTNode):
    """Узел операции OR."""
    
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def evaluate(self, variables: dict) -> bool:
        return self.left.evaluate(variables) or self.right.evaluate(variables)
    
    def get_variables(self) -> Set[str]:
        return self.left.get_variables() | self.right.get_variables()
    
    def __str__(self) -> str:
        return f"({self.left}|{self.right})"


class ImpliesNode(ASTNode):
    """Узел операции IMPLIES (->)."""
    
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def evaluate(self, variables: dict) -> bool:
        return (not self.left.evaluate(variables)) or self.right.evaluate(variables)
    
    def get_variables(self) -> Set[str]:
        return self.left.get_variables() | self.right.get_variables()
    
    def __str__(self) -> str:
        return f"({self.left}->{self.right})"


class XorNode(ASTNode):
    """Узел операции XOR (~)."""
    
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def evaluate(self, variables: dict) -> bool:
        return self.left.evaluate(variables) != self.right.evaluate(variables)
    
    def get_variables(self) -> Set[str]:
        return self.left.get_variables() | self.right.get_variables()
    
    def __str__(self) -> str:
        return f"({self.left}~{self.right})"


class Parser:
    """Синтаксический анализатор логических выражений."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else Token(Token.EOF, '')
    
    def advance(self) -> None:
        """Перемещение к следующему токену."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(Token.EOF, '')
    
    def parse(self) -> ASTNode:
        """Разбор выражения."""
        result = self.parse_or_expression()
        if self.current_token.type != Token.EOF:
            raise ValueError(f"Ожидался конец выражения, получено: {self.current_token}")
        return result
    
    def parse_or_expression(self) -> ASTNode:
        """Разбор OR выражения (низший приоритет)."""
        node = self.parse_xor_expression()
        
        while self.current_token.type == Token.OR:
            self.advance()
            node = OrNode(node, self.parse_xor_expression())
        
        return node
    
    def parse_xor_expression(self) -> ASTNode:
        """Разбор XOR выражения."""
        node = self.parse_and_expression()
        
        while self.current_token.type == Token.XOR:
            self.advance()
            node = XorNode(node, self.parse_and_expression())
        
        return node
    
    def parse_and_expression(self) -> ASTNode:
        """Разбор AND выражения."""
        node = self.parse_implies_expression()
        
        while self.current_token.type == Token.AND:
            self.advance()
            node = AndNode(node, self.parse_implies_expression())
        
        return node
    
    def parse_implies_expression(self) -> ASTNode:
        """Разбор IMPLIES выражения."""
        node = self.parse_primary()
        
        while self.current_token.type == Token.IMPLIES:
            self.advance()
            node = ImpliesNode(node, self.parse_primary())
        
        return node
    
    def parse_primary(self) -> ASTNode:
        """Разбор первичного выражения (переменная, NOT, скобки)."""
        token = self.current_token
        
        if token.type == Token.NOT:
            self.advance()
            return NotNode(self.parse_primary())
        
        if token.type == Token.VARIABLE:
            self.advance()
            return VariableNode(token.value)
        
        if token.type == Token.LPAREN:
            self.advance()
            node = self.parse_or_expression()
            if self.current_token.type != Token.RPAREN:
                raise ValueError("Ожидалась закрывающая скобка")
            self.advance()
            return node
        
        raise ValueError(f"Неожиданный токен: {token}")


def parse_expression(expression: str) -> ASTNode:
    """
    Парсинг логического выражения.
    
    Args:
        expression: Строка с логическим выражением
        
    Returns:
        ASTNode: Корень абстрактного синтаксического дерева
    """
    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def get_all_variables(expression: str) -> Set[str]:
    """
    Получение всех переменных из выражения.
    
    Args:
        expression: Строка с логическим выражением
        
    Returns:
        Set[str]: Множество переменных
    """
    ast = parse_expression(expression)
    return ast.get_variables()
