from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# from django.views.decorators.cache import cache_page
import markdown

from core.views import paginate_queryset
from core.models import User
from .models import Idea, Opinion, Team, TeamUser, TeamCandidates, TeamCandidatesUser
from .forms import IdeaForm, OpinionForm


def index(request):
    ideas_list = Idea.objects.all()
    page_obj = paginate_queryset(ideas_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'ideas/index.html', context)

def idea_detail(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    tags = idea.tags.all()
    team = idea.team
    form = OpinionForm()
    if team:
        team_members = team.members.all()
    else:
        team_members = None
    opinions = idea.opinions.all()
    is_editable = False
    if request.user == idea.author:
        is_editable = True
    context = {
        'is_editable': is_editable,
        'idea': idea,
        'tags': tags,
        'opinions': opinions,
        'team_members': team_members,
        'form': form
    }
    return render(request, 'ideas/idea_detail.html', context)

@login_required
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            f = form.save(commit=False)
            f.author_id = request.user.id
            form.save()
            team = Team.objects.create(idea=f, owner=request.user)
            TeamCandidates.objects.create(team=team)
            team.members.add(request.user)
            return redirect(f'/ideas/idea/{f.id}/')
        return render(request, 'ideas/create_idea.html', {'form': form})
    form = IdeaForm()
    return render(request, 'ideas/create_idea.html', {'form': form})


@login_required
def idea_edit(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    if idea.author.id != request.user.id:
        return redirect(f'/ideas/idea/{idea.id}/')
    if request.method == 'POST':
        form = IdeaForm(
            request.POST,
            files=request.FILES or None,
            instance=idea
        )
        if form.is_valid():
            f = form.save(commit=False)
            f.author_id = request.user.id
            form.save()
            return redirect(f'/ideas/idea/{idea.id}/')

    form = IdeaForm(instance=idea)
    context = {
        'is_edit': True,
        "form": form
    }
    return render(request, 'ideas/create_idea.html', context)


@login_required
def team_profile(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    team = idea.team
    team_members = team.members.all() or None
    team_candidates = team.candidates.users.all() or None
    is_editable = False
    if request.user == team.owner:
        is_editable = True

    in_team = False
    if request.user in team_members:
        in_team = True

    is_candidate = False
    if team_candidates:
        if request.user in team_candidates:
            is_candidate = True

    context = {
        'idea': idea,
        'team_members': team_members,
        'team_candidates': team_candidates,
        'is_editable': is_editable,
        'in_team': in_team,
        'is_candidate': is_candidate
    }
    return render(request, 'ideas/team_profile.html', context)


@login_required
def participate(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    team = idea.team
    team.candidates.users.add(request.user)
    return redirect(f'/ideas/idea/{idea_id}/team/')


@login_required
def leave(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    team = idea.team
    TeamUser.objects.get(team=team, user=request.user).delete()
    return redirect(f'/ideas/idea/{idea_id}/team/')


@login_required
def accept_member(request, idea_id, user_id, team_id):
    if request.user == Idea.objects.get(pk=idea_id).author:
        team = Team.objects.get(pk=team_id) or None
        candidate = User.objects.get(pk=user_id) or None
        if team and candidate:
            team.members.add(candidate)
            team_candidate = TeamCandidates.objects.get(team=team)
            candidate_delete = TeamCandidatesUser.objects.get(
                user=candidate,
                teamcandidates=team_candidate
            )
            candidate_delete.delete()
        return redirect(f'/ideas/idea/{idea_id}/team/')
    return redirect(f'/ideas/idea/{idea_id}/team/')

@login_required
def decline_member(request, idea_id, user_id, team_id):
    if request.user == Idea.objects.get(pk=idea_id).author:
        team = Team.objects.get(pk=team_id) or None
        candidate = User.objects.get(pk=user_id) or None
        if team and candidate:
            team_candidate = TeamCandidates.objects.get(team=team)
            candidate_delete = TeamCandidatesUser.objects.get(
                user=candidate,
                teamcandidates=team_candidate
            )
            candidate_delete.delete()
    return redirect(f'/ideas/idea/{idea_id}/team/')

@login_required
def add_opinion(request, idea_id):
    idea = Idea.objects.get(pk=idea_id)
    form = OpinionForm(request.POST or None)
    if form.is_valid():
        opinion = form.save(commit=False)
        opinion.author = request.user
        opinion.idea = idea
        opinion.save()
    return redirect('ideas:idea_detail', idea_id=idea_id)


@login_required
def delete_member(request, idea_id, user_id, team_id):
    team = Team.objects.get(pk=team_id) or None
    if request.user == team.owner:
        TeamUser.objects.get(team=team, user=User.objects.get(pk=user_id)).delete()
    return redirect(f'/ideas/idea/{idea_id}/team/')



