from GameElements.Building import Building
from GameElements.Recipe import Recipe
from ModelElements.ResourceFlow import ResourceFlow


class Process:
    # Abstract
    recipe: Recipe
    target: ResourceFlow
    target_is_output: bool

    # Actualization
    processor: Building | None

    def _scaling_factor(self) -> float:
        amount_per_cycle: int
        if self.target_is_output:
            amount_per_cycle = self.recipe.outputs[self.target.resource]
        else:
            amount_per_cycle = self.recipe.inputs[self.target.resource]

        scaling_factor = self.target.rate / amount_per_cycle
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