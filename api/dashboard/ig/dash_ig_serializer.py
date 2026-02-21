from rest_framework import serializers
import json

from django.db.models import Sum
from db.task import InterestGroup, UserIgLink


class InterestGroupSerializer(serializers.ModelSerializer):

    updated_by = serializers.CharField(source="updated_by.full_name")
    created_by = serializers.CharField(source="created_by.full_name")
    members = serializers.SerializerMethodField()
    category = serializers.ChoiceField(
        choices=["maker", "coder", "creative", "manager", "others"]
    )
    status = serializers.ChoiceField(
        choices=["active", "requested", "cancelled", "rejected"]
    )

    class Meta:
        model = InterestGroup
        fields = [
            "id",
            "name",
            "resource",
            "about",
            "prerequisites",
            "career_opportunities",
            "top_blogs",
            "people_to_follow",
            "leads",
            "mentors",
            "thinktank",
            "office_hours",
            "icon",
            "code",
            "category",
            "status",
            "members",
            "updated_by",
            "updated_at",
            "created_by",
            "created_at",
        ]

    def get_members(self, obj):
        return obj.user_ig_link_ig.all().count()

    def to_representation(self, instance):
        """Convert JSON-serialized text fields back to Python objects for API output."""
        data = super().to_representation(instance)
        json_fields = [
            "prerequisites",
            "career_opportunities",
            "top_blogs",
            "people_to_follow",
            "mentors",
            "leads",
        ]

        for field in json_fields:
            val = data.get(field)
            if isinstance(val, str) and val:
                try:
                    parsed = json.loads(val)
                    data[field] = parsed
                except Exception:
                    # leave as-is (plain string)
                    pass

        return data


class InterestGroupCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterestGroup
        fields = [
            "name",
            "code",
            "category",
            "status",
            "icon",
            "about",
            "prerequisites",
            "career_opportunities",
            "resource",
            "top_blogs",
            "people_to_follow",
            "leads",
            "mentors",
            "thinktank",
            "office_hours",
            "created_by",
            "updated_by",
        ]


class InterestGroupRequestSerializer(serializers.ModelSerializer):
    """Serializer for user-submitted IG creation requests."""
    
    class Meta:
        model = InterestGroup
        fields = [
            "name",
            "code",
            "category",
            "icon",
            "about",
            "prerequisites",
            "career_opportunities",
            "resource",
            "top_blogs",
            "people_to_follow",
            "leads",
            "mentors",
            "thinktank",
            "office_hours",
        ]
        extra_kwargs = {
            "name": {"required": True},
            "code": {"required": True},
            "category": {"required": True},
            "icon": {"required": True},
        }

class InterestGroupMemberSerializer(serializers.ModelSerializer):
    """Serializer for IG members, used in the IG members API."""
    
    id = serializers.UUIDField(source="user.id")    
    full_name = serializers.CharField(source="user.full_name")
    muid = serializers.CharField(source="user.muid")
    
    profile_pic = serializers.SerializerMethodField()
    ig_level = serializers.SerializerMethodField()
    level = serializers.CharField(
        source="user.user_lvl_link_user.level.name",
        default=None
        )
    # interest_groups = serializers.SerializerMethodField()
    # organizations = serializers.SerializerMethodField()

    ig_karma = serializers.IntegerField()
    joined_at = serializers.DateTimeField(source="created_at")

    class Meta:
        model = UserIgLink
        fields = [
            "id",
            "full_name",
            "muid",
            "profile_pic",
            "level",    
            "ig_level",
            "ig_karma",
            # "interest_groups",
            # "organizations",
            "joined_at",
        ]

    def get_profile_pic(self, obj):
        request = self.context.get("request")

        if not request:
            return None

        return request.build_absolute_uri(
            f"/muback-media/user/profile/{obj.user.id}.png"
        )

    def get_ig_level(self, obj):
        lvl = obj.user.user_ig_lvl_link_user.filter(
            ig_id=obj.ig_id
        ).select_related("level").first()

        if lvl:
            return lvl.level.level_order
        return None

    # def get_interest_groups(self, obj):
    #     ig_links = obj.user.user_ig_link_user.select_related("ig").all()

    #     return [
    #         {
    #             "id": link.ig.id,
    #             "name": link.ig.name,
    #         }
    #         for link in ig_links
    #     ]

    # def get_organizations(self, obj):
    #     org_links = obj.user.user_organization_link_user.select_related("org").all()

    #     return [
    #         {
    #             "id": link.org.id,
    #             "title": link.org.title,
    #             "code": link.org.code,
    #             "org_type": link.org.org_type,
    #         }
    #         for link in org_links
    #     ]