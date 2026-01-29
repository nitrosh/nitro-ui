import inspect
from typing import Union, List, Any, Dict, Set

from nitro_ui.core.element import HTMLElement
from nitro_ui.core.slot import Slot


class Component(HTMLElement):
    """Base class for building reusable components with declarative templates.

    Components provide a cleaner way to create reusable HTML structures with:
    - Declarative class attributes for tag and default CSS classes
    - A template() method that defines the component structure
    - Named slots for flexible content insertion
    - Automatic separation of props, slots, and HTML attributes

    Example:
        class Card(Component):
            tag = "div"
            class_name = "card"

            def template(self, title: str):
                return [
                    H3(title, cls="card-title"),
                    Slot()  # children go here
                ]

        # Usage
        Card("My Title",
            Paragraph("content"),
            id="card-1",
            class_name="highlighted"
        )

        # Renders:
        # <div class="card highlighted" id="card-1">
        #     <h3 class="card-title">My Title</h3>
        #     <p>content</p>
        # </div>
    """

    tag: str = "div"
    class_name: str = None

    def __init__(self, *args, **kwargs):
        # Get template method signature to identify props
        template_params = self._get_template_params()

        # Separate props from positional args
        # HTMLElement args always go to default slot, non-HTMLElement args are props
        props = {}
        default_slot_children = []
        prop_index = 0

        for arg in args:
            if isinstance(arg, HTMLElement):
                # HTMLElement children go to default slot
                default_slot_children.append(arg)
            elif prop_index < len(template_params):
                # Non-HTMLElement args are props
                props[template_params[prop_index]] = arg
                prop_index += 1
            else:
                # Extra non-HTMLElement args (shouldn't happen normally)
                default_slot_children.append(arg)

        # Build complete props with defaults for template call
        template_sig = inspect.signature(self.template)
        final_props = {}
        for param_name, param in template_sig.parameters.items():
            if param_name in props:
                final_props[param_name] = props[param_name]
            elif param_name in kwargs:
                # Check if it's a prop passed via kwarg
                final_props[param_name] = kwargs[param_name]
            elif param.default is not inspect.Parameter.empty:
                final_props[param_name] = param.default
            else:
                raise TypeError(
                    f"{self.__class__.__name__} missing required prop: {param_name!r}"
                )

        # Call template to get structure and discover slots
        template_result = self.template(**final_props)
        slot_names = self._find_slot_names(template_result)

        # Separate kwargs into: slots, props (already handled), and HTML attributes
        slot_content: Dict[str, List[Any]] = {}
        html_attrs = {}

        for key, value in kwargs.items():
            if key in slot_names:
                # It's a named slot
                if isinstance(value, list):
                    slot_content[key] = value
                else:
                    slot_content[key] = [value]
            elif key in template_params:
                # It's a prop - already handled above
                pass
            else:
                # It's an HTML attribute
                html_attrs[key] = value

        # Handle class_name merging
        default_class = self.__class__.class_name
        user_class = html_attrs.get("class_name") or html_attrs.get("cls")

        if default_class and user_class:
            # Merge: default + user
            merged_class = f"{default_class} {user_class}"
            html_attrs["class_name"] = merged_class
            html_attrs.pop("cls", None)
        elif default_class:
            html_attrs["class_name"] = default_class

        # Initialize the base HTMLElement
        super().__init__(tag=self.__class__.tag, **html_attrs)

        # Process template result, replacing slots with content
        has_default_slot = self._has_default_slot(template_result)
        children = self._process_template(
            template_result,
            slot_content,
            default_slot_children,
        )

        # Append all children
        for child in children:
            if child is not None:
                self.append(child)

        # If no default slot was found, append remaining children at the end
        if not has_default_slot and default_slot_children:
            for child in default_slot_children:
                if child is not None:
                    self.append(child)

    def _get_template_params(self) -> List[str]:
        """Get the parameter names of the template method (excluding self)."""
        sig = inspect.signature(self.template)
        return [
            name for name, param in sig.parameters.items()
            if name != "self"
        ]

    def _find_slot_names(self, items: Any) -> Set[str]:
        """Recursively find all named slot names in the template structure."""
        names = set()

        if isinstance(items, Slot):
            if items.slot_name:
                names.add(items.slot_name)
        elif isinstance(items, (list, tuple)):
            for item in items:
                names.update(self._find_slot_names(item))
        elif isinstance(items, HTMLElement):
            for child in items.children:
                names.update(self._find_slot_names(child))

        return names

    def _has_default_slot(self, items: Any) -> bool:
        """Check if the template contains a default (unnamed) slot."""
        if isinstance(items, Slot):
            return items.slot_name is None
        elif isinstance(items, (list, tuple)):
            for item in items:
                if self._has_default_slot(item):
                    return True
        elif isinstance(items, HTMLElement):
            for child in items.children:
                if self._has_default_slot(child):
                    return True
        return False

    def _process_template(
        self,
        items: Any,
        slot_content: Dict[str, List[Any]],
        default_slot_children: List[Any],
    ) -> List[Any]:
        """Process template items, replacing Slot markers with content."""
        result = []

        if items is None:
            return result

        if not isinstance(items, (list, tuple)):
            items = [items]

        for item in items:
            if item is None:
                continue

            if isinstance(item, Slot):
                # Replace slot with content
                if item.slot_name:
                    # Named slot
                    content = slot_content.get(item.slot_name)
                    if content:
                        result.extend(content)
                    elif item.slot_default is not None:
                        # Use default content
                        if isinstance(item.slot_default, list):
                            result.extend(item.slot_default)
                        else:
                            result.append(item.slot_default)
                else:
                    # Default slot
                    if default_slot_children:
                        result.extend(default_slot_children)
                    elif item.slot_default is not None:
                        if isinstance(item.slot_default, list):
                            result.extend(item.slot_default)
                        else:
                            result.append(item.slot_default)

            elif isinstance(item, HTMLElement):
                # Recursively process children of this element
                processed_children = self._process_template(
                    item.children,
                    slot_content,
                    default_slot_children,
                )
                item._children = []
                for child in processed_children:
                    if child is not None:
                        item.append(child)
                result.append(item)

            else:
                # Regular item (string, etc.)
                result.append(item)

        return result

    def template(self) -> List[Any]:
        """Override to define the component structure.

        Returns:
            List of HTMLElement instances and/or Slot markers.
            Use Slot() for default slot, Slot("name") for named slots.
        """
        return [Slot()]
