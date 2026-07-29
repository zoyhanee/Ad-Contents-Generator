from dataclasses import dataclass, field


@dataclass
class EditPlan:
    targets: list[str]
    keep: list[str]
    prompt: str
    metadata: dict = field(default_factory=dict)


class EditPlanner:

    def create_plan(
        self,
        instruction: str,
    ) -> EditPlan:

        targets = self._extract_targets(instruction)

        keep = self._build_keep_list(targets)

        prompt = self._build_prompt(
            keep=keep,
            instruction=instruction,
        )

        return EditPlan(
            targets=targets,
            keep=keep,
            prompt=prompt,
        )

    def _extract_targets(
        self,
        instruction: str,
    ) -> list[str]:

        targets = []

        if "배경" in instruction:
            targets.append("background")

        if "텍스트" in instruction:
            targets.append("text")

        if "제품" in instruction:
            targets.append("product")

        if not targets:
            targets.append("overall")

        return targets

    def _build_keep_list(
        self,
        targets: list[str],
    ) -> list[str]:

        keep = []

        if "background" not in targets:
            keep.append("background")

        if "text" not in targets:
            keep.append("text")

        if "product" not in targets:
            keep.append("product")

        return keep

    def _build_prompt(
        self,
        keep: list[str],
        instruction: str,
    ) -> str:

        lines = []

        if "product" in keep:
            lines.append("Keep the product exactly the same.")

        if "text" in keep:
            lines.append("Keep all existing text unchanged.")

        if "background" in keep:
            lines.append("Keep the background unchanged.")

        lines.append(instruction)

        return "\n".join(lines)