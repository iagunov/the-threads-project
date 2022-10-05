from .models import Member, User
from posts.models import Group, Post, Difficulty, Comment, Follow
from ideas.models import Idea, Opinion, Team, TeamCandidates
import random

# НИЖЕ ЛЕЖАТ КОНСТАНТЫ И ФУНКЦИИ ДЛЯ ГЕНЕРАЦИЮ КОНТЕНТА
# СГЕНЕРИРУЕТСЯ ВОСЕМЬ ПОЛЬЗОВАТЕЛЕЙ И СТОЛЬКО ЖЕ ИДЕЙ
# к ним так же сгенерируется случайное кол-во комментариев


USER_TO_CREATE = [
    'berkowitz',
    'kemper',
    'bittaker',
    'norris',
    'brady',
    'hindley',
    'bianchi',
    'buono'
]

GROUPS_TO_CREATE = [
    'eatshitscript',
    'javascript',
    'frontend_dog',
    'backend_god',
    'praktikum',
]

DIFF_TO_CREATE = [
    'easy',
    'medium',
    'hard',
]

TITLE_TO_POST = [
    'Давайте повторим?',
    'Эмансипация',
    'Осуждение общества',
    'В отпуск!',
    'Tortuga',
    'A long time ago',
    'Кто не спрятался...',
    'Я томат',
]

TEXT_TO_POST = [
    'i killed 6 people and injured 7',
    'i was 15 when i killed six women',
    'в 1981 меня объвили маньяком',
    'меня приговорили к 45 годам тюремного заключения',
    'i tortured people in my wagon',
    'в 1963-1965 годах я убивал детей',
    'местонахождение одной их моих жертв до сих пор неизвестно',
    'а я вообще душитель'
]

COMMENTS_TO_CREATE = [
    'моя ты красота',
    'отлично',
    'тебе не стыдно?',
    'stupid fucking cockroach',
    'its absurd!',
    'чивоооо блеаааать',
    'готов стать админом вашей хуйни',
]


def make_user():
    for record in USER_TO_CREATE:
        if not User.objects.filter(username=record).exists():
            new = User.objects.create_user(username=record)
            Member.objects.create(
                user=new,
                about=new.username,
                contact_telegram='@KrivosheevNikita',
                contact_slack='fukoff',
                contact_github='https://github.com/jingleMyBells'
            )

def make_groups():
    for i in range(0, len(GROUPS_TO_CREATE)-1):
        descr = 'группа про ' + GROUPS_TO_CREATE[i]
        Group.objects.create(
            title=GROUPS_TO_CREATE[i],
            slug=GROUPS_TO_CREATE[i],
            description=descr
        )

def make_difficulty():
    for i in range(0, len(DIFF_TO_CREATE)-1):
        Difficulty.objects.create(
            title=DIFF_TO_CREATE[i],
            slug=DIFF_TO_CREATE[i],
        )

def make_posts():
    for i in range(0, len(TITLE_TO_POST)):
        group = Group.objects.order_by('?').first()
        difficulty = Difficulty.objects.order_by('?').first()
        user = User.objects.order_by('?').first()
        Post.objects.create(
            title=TITLE_TO_POST[i],
            text=TEXT_TO_POST[i],
            author=user,
            group=group,
            difficulty=difficulty
        )

def make_comments():
    posts = Post.objects.all()
    for post in posts:
        comment_index = random.randint(0, len(COMMENTS_TO_CREATE) - 1)
        Comment.objects.create(
            post=post,
            title='название коммента',
            text=COMMENTS_TO_CREATE[comment_index],
            author=User.objects.order_by('?').first()
        )


def make_follows():
    for i in range(0, 4):
        user1 = User.objects.order_by('?').first()
        user2 = User.objects.order_by('?').last()
        if len(Follow.objects.filter(user=user1, author=user2)) != 0:
            Follow.objects.create(user=user1, author=user2)




def make_ideas():
    for i in range(0, len(TITLE_TO_POST)):
        Idea.objects.create(
            title=TITLE_TO_POST[i],
            text=TEXT_TO_POST[i],
            author=User.objects.get(username=USER_TO_CREATE[i]),
            github_link='https://github.com/jingleMyBells/the-threads-project',
            tags='памагити;python;js;css;html'
        )


def make_opinions():
    ideas = Idea.objects.all()
    for idea in ideas:
        comment_index = random.randint(0, len(COMMENTS_TO_CREATE) - 1)
        Opinion.objects.create(
            idea=idea,
            title='название коммента',
            text=COMMENTS_TO_CREATE[comment_index],
            author=User.objects.order_by('?').first()
        )

def make_teams():
    ideas = Idea.objects.all()
    for idea in ideas:
        team = Team.objects.create(idea=idea, owner=idea.author)
        TeamCandidates.objects.create(team=team)
        user1 = User.objects.order_by('?').first()
        user2 = User.objects.order_by('?').last()
        team.members.add(user1)
        team.members.add(user2)


def make_all():
    make_user()
    make_groups()
    make_difficulty()
    make_posts()
    make_comments()
    make_follows()
    make_ideas()
    make_opinions()
    make_teams()

if __name__ == '__main__':
    pass