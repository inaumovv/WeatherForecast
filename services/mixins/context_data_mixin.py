class ContextDataMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context: dict | None = None, **kwargs):
        if not context:
            context: dict = {}
            context.update(kwargs)
        else:
            context.update(kwargs)

        return context
