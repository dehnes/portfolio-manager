from ...models.portfolio import Portfolio


def get_sidebar_context():
    return {"portfolios": Portfolio.objects.all()}
