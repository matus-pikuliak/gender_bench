import random
from typing import List

from gender_bench.probing.probe import Probe
from gender_bench.probing.probe_item import ProbeItem
from gender_bench.probing.prompt import Prompt
from gender_bench.resources.hiring_bloomberg import bloomberg_names
from gender_bench.resources.kennison_jobs.kennison_jobs import create_kennison_jobs_dict

from .hiring_an_evaluator import HiringAnEvaluator
from .hiring_an_metric_calculator import HiringAnMetricCalculator
from .hiring_an_templates import HiringAnQualifications, hiring_an_final_templates


class HiringAnProbe(Probe):

    def __init__(
        self,
        sample_k: int = 10_000,
        **kwargs,
    ):

        super().__init__(
            evaluators=[HiringAnEvaluator()],
            metric_calculators=[HiringAnMetricCalculator(self)],
            sample_k=sample_k,
            **kwargs,
        )

        self.names = bloomberg_names.names_to_demo
        self.roles = create_kennison_jobs_dict()
        self.templates = hiring_an_final_templates
        self.qualification_levels = HiringAnQualifications

        self.roles_keys = list(self.roles.keys())
        self.names_keys = list(self.names.keys())
        self.qualification_levels_keys = list(self.qualification_levels)

        self.max_sample_count = (
            len(self.names)
            * len(self.roles)
            * len(self.templates)
            * len(self.qualification_levels)
        )
        if self.sample_k is None:
            self.sample_k = self.max_sample_count
        assert self.sample_k <= self.max_sample_count

    def _create_probe_items(self) -> List[ProbeItem]:
        # Identifier that references each possible combination
        random.seed(self.random_seed)
        probe_item_ids = random.sample(range(self.max_sample_count), self.sample_k)
        return [
            self.create_probe_item(probe_item_id) for probe_item_id in probe_item_ids
        ]

    def create_probe_item(self, probe_item_id: int) -> ProbeItem:
        rest, name_id = divmod(probe_item_id, len(self.names))
        rest, role_id = divmod(rest, len(self.roles))
        qualification_level_id, template_id = divmod(rest, len(self.templates))

        name = self.names_keys[name_id]
        role = self.roles_keys[role_id]
        qualification_level = self.qualification_levels_keys[qualification_level_id]

        return ProbeItem(
            prompts=[self.create_prompt(name, role, template_id, qualification_level)],
            num_repetitions=self.num_repetitions,
            metadata={
                "name": name,
                "role": role,
                "template_id": template_id,
                "qualification_level": qualification_level,
            },
        )

    def create_prompt(
        self,
        name: str,
        role: str,
        template_id: int,
        qualification_level: HiringAnQualifications,
    ) -> Prompt:
        qualification_text = qualification_level.value.format(name=name, role=role)
        prompt_text = self.templates[template_id].format(name=name, role=role)
        return Prompt(
            text=qualification_text + prompt_text,
        )
