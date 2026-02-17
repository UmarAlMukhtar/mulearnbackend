from rest_framework import serializers
import json

from django.db.models import Sum
from db.task import InterestGroup, UserIgLvlLink


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
    
    user_id = serializers.UUIDField(source="user.id")    
    full_name = serializers.CharField(source="user.full_name")
    muid = serializers.CharField(source="user.muid")
    profile_pic = serializers.CharField(source="user.profile_pic")
    
    ig_level = serializers.IntegerField(source="level.level_order")   
    ig_karma = serializers.IntegerField()
    
    joined_at = serializers.DateTimeField(source="created_at")
    class Meta:
        model = UserIgLvlLink
        fields = [
            "user_id",
            "full_name",
            "muid",
            "profile_pic",
            "ig_level",
            "ig_karma",
            "joined_at",  
        ]