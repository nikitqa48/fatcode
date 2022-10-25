from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from src.team.models import Team, TeamMember, Invitation


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Только для создателя или просмотр'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class CommentOwnerTeam(permissions.BasePermission):
    '''Только для автора изменение/удаление ссылки'''
    def has_object_permission(self, request, view, obj):
        print(obj)
        return obj.post.user == request.user


class SocialOwnerTeam(permissions.BasePermission):
    '''Только для автора изменение/удаление ссылки'''
    def has_object_permission(self, request, view, obj):
        print(obj.team)
        return obj.team.user == request.user


class PostOwnerTeam(permissions.BasePermission):
    '''Только для участников команды просмотр обьекта и'''
    def has_object_permission(self, request, view, obj):
        team = TeamMember.objects.get(team=obj.team, user=request.user)
        return team.user == request.user


class MemberTeam(permissions.BasePermission):
    '''Только участников команды'''
    def has_object_permission(self, request, view, obj):
        team = TeamMember.objects.get(team=obj, user=request.user)
        return team.user == request.user


class MemberTeam(permissions.BasePermission):
    '''Только участников команды'''
    def has_object_permission(self, request, view, obj):
        print(obj)
        team = TeamMember.objects.get(team=obj, user=request.user)
        return team.user == request.user


class OwnerTeam(permissions.BasePermission):
    '''Только для автора'''
    def has_object_permission(self, request, view, obj):
        print(obj)
        return obj.user == request.user


class AuthorOrMember(BasePermission):
    """ Для автора или члена команды """
    def has_permission(self, request, view):
        print('r', request)
        user = TeamMember.objects.filter(Q(user=request.user) | Q(team__user=request.user))
        print(user)
        return user == request.user

# class OwnerTeam(permissions.BasePermission):
#     '''Только для автора'''
#     def has_permission(self, request, view):
#         return bool(request.user)
# class OwnerTeam(BasePermission):
#     def has_permission(self, request, view):
#         if view.request.data.get('team'):
#             return Team.objects.filter(
#                 id=view.request.data.get('team'),
#                 user=request.user
#             ).exists()
#
#     def has_object_permission(self, request, view, obj):
#         return bool(obj.team.user == request.user)


# class IsAuthorOfTeam(BasePermission):
#     """ Is Author of team """
#
#     def has_permission(self, request, view):
#         if view.request.data.get('team'):
#             return Team.objects.filter(
#                 id=view.request.data.get('team'),
#                 user=request.user
#             ).exists()


def is_author_of_team_for_project(request):
    """ Is Author of team for creating a project """
    return Team.objects.filter(id=request.data['teams'], user=request.user)


# class IsAuthorOfTeamForDetail(BasePermission):
#     """ Is Author of team for team detail view """
#
#     def has_object_permission(self, request, view, obj):
#         return Team.objects.filter(
#             id=view.kwargs['team'],
#             user=request.user,
#             #members__id=view.kwargs['pk']
#         ).exists() and not obj.user == request.user


# class IsNotAuthorOfTeamForSelfDelete(BasePermission):
#     """ Is NOT Author of team for self delete from team """
#
#     def has_object_permission(self, request, view, obj):
#         return not Team.objects.filter(
#             id=view.kwargs['team'],
#             user=request.user,
#         ).exists() and obj.user == request.user

class AuthorOrMember(BasePermission):
    """ Для автора или члена команды """
    def has_permission(self, request, view):
        user = TeamMember.objects.filter(Q(user=request.user) | Q(team__user=request.user))
        return user

class IsAuthorOfTeamForInvitation(BasePermission):
    """ Is Author of team for team invitation """

    def has_object_permission(self, request, view, obj):
        return Team.objects.filter(
            id=obj.team.id,
            user=request.user,
        ).exists() and not obj.user == request.user


class PostAuthorOrMember(permissions.BasePermission):
    '''Посты только для автора или для просмотра члена команды'''
    def has_object_permission(self, request, view, obj):
        print(request)
        print(obj)

        return obj.user == request.user


class IsMemberOfTeam(BasePermission):
    """ Если член команды """

    def has_permission(self, request, view):
        print(view.request.data)
        print(view.request.data.get('team'))
        if view.request.data.get('team'):
            return TeamMember.objects.filter(
                team_id=view.request.data.get('team'),
                user=request.user
            ).exists()
        else:
            return TeamMember.objects.filter(user=request.user)



class IsMemberOfTeamForPost(BasePermission):
    """ Is member of team for team post """

    def has_object_permission(self, request, view, obj):
        return TeamMember.objects.filter(
            team_id=obj.team.id,
            user=request.user
        ).exists()


class IsMemberOfTeamForComment(BasePermission):
    """ Is member of team for team comment """

    def has_permission(self, request, view):
        if view.request.data.get('post'):
            return TeamMember.objects.filter(
                team__articles=view.request.data.get('post'),
                user=request.user
            ).exists()


class IsInvitationToRequestUser(BasePermission):
    """ Is Invitation to request user """

    def has_object_permission(self, request, view, obj):
        return Invitation.objects.filter(
            id=obj.id,
            user=request.user,
            asking=False
        ).exists()


class IsInvitationUser(IsAuthenticated):
    """ Is Invitation to request user """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsInvitationAskingToAuthorOfTeam(BasePermission):
    """ Is request to team member to request user """

    def has_object_permission(self, request, view, obj):
        return Invitation.objects.filter(
            id=obj.id,
            asking=True
        ).exists()


class PostPermission(BasePermission):
    """ Is request to team member to request user """

    def has_object_permission(self, request, view, obj):
        return Invitation.objects.filter(
            id=obj.id,
            asking=True
        ).exists()
