from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product, Category


@registry.register_document
class ProductDocument(Document):
    category = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    class Index:
        # Name of the Elasticsearch index
        name = 'products'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

        fields = [
            'name',
            'description'
        ]
        related_models = [Category]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(ProductDocument, self).get_queryset().select_related(
            'category'
        )
