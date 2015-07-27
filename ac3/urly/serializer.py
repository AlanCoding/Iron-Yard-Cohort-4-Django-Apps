from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.reverse import reverse
from urly.models import *
from profiles.models import Profile

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.HyperlinkedIdentityField(view_name='bookmarker-detail')
    _links = SerializerMethodField()

    def get__links(self, obj):
        links = {
            "clicks": reverse('bookmark-click', kwargs=dict(bmk_id=obj.pk),
                              request=self.context.get('request')), }
        return links

    class Meta:
        model = Bookmark
        fields = ['URL', 'url', 'user', 'profile', 'posted_at', 'title',
                    'description', 'total_clicks', 'click_set', '_links']


class BookmarkerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField( read_only=True)
    _links = SerializerMethodField()

    def get__links(self, obj):
        links = {
            "bookmarks": reverse('bookmarker-bookmark', kwargs=dict(bmkr_id=obj.user.pk),
                              request=self.context.get('request')), }
        return links

    class Meta:
        model = Profile
        fields = ['age', 'gender', 'user', '_links','total_bookmarks', 'total_clicks']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'click_set']

class ClickSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    bookmark = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')
    class Meta:
        model = Click
        fields = ['clicked_at', 'bookmark', 'user']
