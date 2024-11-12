# Programa para calcular los conjuntos FIRST y FOLLOW de una gramática
from collections import defaultdict

class Grammar:
    def __init__(self, productions, start_symbol):
        """
        Inicializa la gramática.

        :param productions: Lista de producciones. Cada producción es una tupla (LHS, RHS),
                            donde LHS es un no terminal y RHS es una lista de símbolos.
        :param start_symbol: Símbolo no terminal que es el inicio de la gramática.
        """
        self.productions = productions
        self.start_symbol = start_symbol
        self.non_terminals = set()
        self.terminals = set()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self._identify_symbols()

    def _identify_symbols(self):
        """
        Identifica los símbolos terminales y no terminales en la gramática.
        """
        for lhs, rhs in self.productions:
            self.non_terminals.add(lhs)
            for symbol in rhs:
                if symbol == 'ε':
                    continue
                if not symbol.isupper() and symbol not in self.terminals:
                    self.terminals.add(symbol)
                elif symbol.isupper():
                    self.non_terminals.add(symbol)
        # Añade el símbolo de fin de entrada a los FOLLOW del símbolo inicial
        self.follow[self.start_symbol].add('$')

    def compute_first(self):
        """
        Calcula los conjuntos FIRST para todos los símbolos no terminales.
        """
        # Inicializa FIRST de los terminales
        for terminal in self.terminals:
            self.first[terminal].add(terminal)

        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.productions:
                # Guardar el tamaño actual del conjunto FIRST
                before = len(self.first[lhs])
                
                if rhs == ['ε']:
                    self.first[lhs].add('ε')
                else:
                    for symbol in rhs:
                        self.first[lhs].update(self.first[symbol] - {'ε'})
                        if 'ε' not in self.first[symbol]:
                            break
                    else:
                        self.first[lhs].add('ε')
                
                # Verificar si se realizaron cambios
                after = len(self.first[lhs])
                if after > before:
                    changed = True

    def compute_follow(self):
        """
        Calcula los conjuntos FOLLOW para todos los símbolos no terminales.
        """
        # Se asume que compute_first ya ha sido llamado
        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.productions:
                trailer = self.follow[lhs].copy()
                for symbol in reversed(rhs):
                    if symbol in self.non_terminals:
                        before = len(self.follow[symbol])
                        self.follow[symbol].update(trailer)
                        after = len(self.follow[symbol])
                        if after > before:
                            changed = True
                        if 'ε' in self.first[symbol]:
                            trailer.update(self.first[symbol] - {'ε'})
                        else:
                            trailer = self.first[symbol]
                    else:
                        trailer = self.first[symbol]

    def display_first(self):
        """
        Muestra los conjuntos FIRST.
        """
        print("Conjuntos FIRST:")
        for non_terminal in sorted(self.non_terminals):
            if self.first[non_terminal]:
                first_set = ', '.join(sorted(self.first[non_terminal]))
                print(f"FIRST({non_terminal}) = {{ {first_set} }}")

    def display_follow(self):
        """
        Muestra los conjuntos FOLLOW.
        """
        print("\nConjuntos FOLLOW:")
        for non_terminal in sorted(self.non_terminals):
            if self.follow[non_terminal]:
                follow_set = ', '.join(sorted(self.follow[non_terminal]))
                print(f"FOLLOW({non_terminal}) = {{ {follow_set} }}")

def main():
    # Gramática
    # E  → T E'
    # E' → + T E' | ε
    # T  → F T'
    # T' → * F T' | ε
    # F  → ( E ) | id | num

    productions = [
        ('E', ['T', "E'"]),
        ("E'", ['+', 'T', "E'"]),
        ("E'", ['ε']),
        ('T', ['F', "T'"]),
        ("T'", ['*', 'F', "T'"]),
        ("T'", ['ε']),
        ('F', ['(', 'E', ')']),
        ('F', ['id']),
        ('F', ['num'])  
    ]

    start_symbol = 'E'

    grammar = Grammar(productions, start_symbol)
    grammar.compute_first()
    grammar.compute_follow()
    grammar.display_first()
    grammar.display_follow()

if __name__ == "__main__":
    main()
