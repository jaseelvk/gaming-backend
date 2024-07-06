from rest_framework import serializers
from product.models import Product, Feature, PlatformImages, Wishlist
import logging

logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_image')

class ProductDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    platform_images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "product_image", "product_name", "product_description", "product_price", "product_logo", "created_by", "features", "platform_images")

    def get_created_by(self, instance):
        return instance.created_by.username

    def get_features(self, instance):
        features = Feature.objects.filter(product=instance)
        serializer = FeatureSerializer(features, many=True)
        return serializer.data

    def get_platform_images(self, instance):
        request = self.context.get("request")
        images = PlatformImages.objects.filter(product=instance)
        serializer = PlatformSerializer(images, many=True, context={"request": request})
        return serializer.data

class PlatformSerializer(serializers.ModelSerializer):
    short_images = serializers.FileField()

    class Meta:
        model = PlatformImages
        fields = ("short_images",)

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("product_features_count", "product_features_items")

class TaskSerializer(serializers.ModelSerializer):
    short_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    features = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = ("product_image", "product_name", "product_description", "product_price", "product_logo", "created_by", "features", "short_images")
        extra_kwargs = {'created_by': {'read_only': True}}

    def create(self, validated_data):
        logger.debug(f"Validated data received: {validated_data}")

        short_images_data = validated_data.pop('short_images', [])
        features_data = validated_data.pop('features', [])

        product = Product.objects.create(**validated_data)

        for image_data in short_images_data:
            try:
                logger.debug(f"Processing image data: {image_data.name}, Type: {image_data.content_type}")
                PlatformImages.objects.create(product=product, short_images=image_data)
            except Exception as e:
                logger.error(f"Invalid image data: {e}")
                raise serializers.ValidationError(f"Invalid image data: {e}")

        for feature_data in features_data:
            logger.debug(f"Creating feature with data: {feature_data}")
            Feature.objects.create(product=product, **feature_data)

        return product

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        features = Feature.objects.filter(product=instance)
        ret['features'] = FeatureSerializer(features, many=True).data
        return ret

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(self.flatten_errors(e.detail))

    def flatten_errors(self, errors):
        flat_errors = {}
        for field, error_list in errors.items():
            if isinstance(error_list, list):
                flat_errors[field] = [error for error in error_list]
            else:
                flat_errors[field] = error_list
        return flat_errors

class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  
    product = ProductSerializer()

    class Meta:
        model = Wishlist
        fields = ("user", "product")
