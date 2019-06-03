class EvaluationException(Exception):
    """
    Exception associated with evaluation of AST
    """
    def __init__(self, msg):
        super().__init__(msg)