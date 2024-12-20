from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gender_bench.probing.attempt import Attempt


class Evaluator:
    """
    Evaluator evaluates answers generated by attempts. The results of the
    evaluation is used by metric calculators.

    The class is used as a key when the results of the evaluation are stored in
    an attempt.
    """

    UNDETECTED = "undetected"

    def evaluate(self, attempt: "Attempt") -> Any:
        raise NotImplementedError

    def __call__(self, attempt: "Attempt") -> Any:
        return self.evaluate(attempt)
