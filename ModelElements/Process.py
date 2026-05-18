from math import ceil

from GameElements.Building import Building
from GameElements.Recipe import Recipe
from ModelElements.ResourceFlow import ResourceFlow


class Process:
    # Abstract
    recipe: Recipe
    target: ResourceFlow
    target_is_output: bool

    # Actualization
    processor: Building

    def __init__(self, recipe: Recipe, target: ResourceFlow, processor : Building, target_is_output: bool = True):
        self.recipe = recipe
        self.target = target
        self.processor = processor
        self.target_is_output = target_is_output

    def _target_amount_per_cycle(self):
        amount_per_cycle: int
        if self.target_is_output:
            amount_per_cycle = self.recipe.outputs[self.target.resource.name]
            amount_per_cycle *= 1 + self.processor.productivity()
        else:
            amount_per_cycle = self.recipe.inputs[self.target.resource.name]
            print("WARNING: Productivity on input-based processes has not be fully implemented!")
            amount_per_cycle *= 1 - self.processor.productivity()

        return amount_per_cycle

    def _scaling_factor(self) -> float:
        scaling_factor = self.target.rate / self._target_amount_per_cycle()
        return scaling_factor

    def inputs(self) -> list[ResourceFlow]:
        a = self._scaling_factor()
        inputs = []
        for resource in self.recipe.inputs:
            input_rate = a * self.recipe.inputs[resource]
            inputs.append(ResourceFlow(resource, input_rate))
        return inputs

    def outputs(self) -> list[ResourceFlow]:
        a = self._scaling_factor()
        outputs = []
        for resource in self.recipe.outputs:
            output_rate = a * self.recipe.outputs[resource]
            outputs.append(ResourceFlow(resource, output_rate))
        return outputs

    def building_count(self) -> int:
        single_processor_rate = self._target_amount_per_cycle() * self.processor.crafting_speed() / self.recipe.duration
        n = ceil(self.target.rate / single_processor_rate)
        return n