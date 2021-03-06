from rest_framework import serializers
from .models import Profile, CustomUser, Skillset

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = ('email',
              'password',
              )
    # write_only_fields = ('password',)


class SkillSerializer(serializers.ModelSerializer):

  class Meta:
    model = Skillset
    fields = ('skill',
              'exp',
              )

class ProfileSerializer(serializers.ModelSerializer):
  skill_details = SkillSerializer(source='skills', many=True)
  user = UserSerializer(read_only=True, required=False)

  class Meta:
    model = Profile
    fields = (
              'id',
              'name',
              'email',
              'time',
              'designation',
              'location',
              'current_ctc',
              'expected_ctc',
              'notice_period',
              'resume',
              'recording',
              'skill_details',
              'user',
                )
        # write_only_fields = ('user',)

  def create(self, validated_data):
    skill_data = validated_data.pop('skills')
    user = Profile.objects.create(**validated_data)
    for each in skill_data:
      skill = each['skill']
      exp = int(each['exp'])
      Skillset.objects.create(profile=user, skill=skill, exp=exp)
    return user

  def get_validation_exclusions(self, *args, **kwargs):
    exclusions = super(ProfileSerializer, self).get_validation_exclusions()

    return exclusions + ['user']

  def update(self, instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.email = validated_data.get('email', instance.email)
    instance.designation = validated_data.get('designation', instance.designation)
    instance.location = validated_data.get('location', instance.location)
    instance.current_ctc = validated_data.get('current_ctc', instance.current_ctc)
    instance.expected_ctc = validated_data.get('expected_ctc', instance.expected_ctc)
    instance.notice_period = validated_data.get('notice_period', instance.notice_period)
    instance.save()
    return instance
