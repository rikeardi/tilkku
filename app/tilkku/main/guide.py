from django.contrib.auth.models import User
from user_guide.models import Guide, GuideInfo


Guide.objects.create(
    guide_name="Map import",
    guide_tag="map-import",
    guide_importance=1,
    html_file="map-import.html",
)

users = User.objects.all()
for user in users:
    GuideInfo.objects.create(
        user=user,
        guide=Guide.objects.get(guide_tag="map-import"),
        guide_status=1,
    )
